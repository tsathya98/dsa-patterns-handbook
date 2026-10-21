# LLM Inference Serving: PagedAttention, Continuous Batching, and Speculative Decoding

> **Difficulty:** Concept  
> **Pattern:** LLM Serving and Inference Systems  
> **Scope:** High-Throughput Serving Architecture, vLLM, Distributed Parallelism, and Low-Latency Optimization

Deploying Large Language Models in production requires solving completely different engineering challenges than traditional microservices. While traditional REST APIs scale horizontally with CPU workers, LLM inference is constrained by GPU High Bandwidth Memory (HBM) capacity, memory bus saturation during autoregressive decoding, and non-deterministic request execution lengths.

This guide details the systems architecture behind production LLM serving engines like vLLM, TensorRT-LLM, and TGI.

---

## 1. The Production Serving Latency Metrics

When evaluating LLM serving performance, standard endpoint response time is insufficient. Systems are benchmarked on three decoupled latency metrics:

```
User Request Arrives
      |
      |<-------- Time To First Token (TTFT) -------->|
      |   (Prefill Phase: Process prompt tokens)     |
      |                                              |
      v                                              v
   [Prompt Processing] ------------------------> [Token 1]
                                                    |
                                                    |<-- Inter-Token Latency (ITL) -->|
                                                    |    (Decode Phase per token)     |
                                                    v                                 v
                                                 [Token 2] -----------------------> [Token 3] ...
|<------------------------- Total Generation Time (E2E Latency) ---------------------------->|
```

1. **Time to First Token (TTFT):**
   * The latency from the moment the user request hits the server until the first generated token streams back.
   * Dominated by the **Prefill Phase** (parallel processing of all input prompt tokens).
   * Metric target for interactive chat: $< 200\text{ ms}$.
2. **Inter-Token Latency (ITL) or Time Per Output Token (TPOT):**
   * The latency to generate each subsequent token during the **Decode Phase**.
   * Human reading speed is approximately 5 to 8 tokens per second (125 to 200 ms per token).
   * Metric target for smooth streaming: $< 30\text{ to } 50\text{ ms per token}$ ($20\text{ to } 33\text{ tokens/sec}$).
3. **Total Generation Latency (E2E):**
   $$\text{E2E Latency} = \text{TTFT} + (\text{Generated Tokens} - 1) \times \text{ITL}$$
4. **Normalized Serving Throughput:**
   * Measured in **Tokens Per Second per GPU** ($\text{tokens/s/GPU}$).
   * Maximizing this metric minimizes operational infrastructure cost.

---

## 2. KV Cache Memory Fragmentation and PagedAttention

In naive LLM serving engines, GPU memory for the KV cache was allocated as a static, contiguous tensor based on the model's maximum possible context length (e.g. 4,096 or 8,192 tokens).

### The Three Sources of Memory Waste:
1. **Reserved Memory:** Memory allocated for future tokens that have not yet been generated.
2. **Internal Fragmentation:** Memory allocated up to the maximum context window when a request only generates 50 tokens.
3. **External Fragmentation:** Gaps between allocations that cannot satisfy incoming requests.

In practice, naive systems wasted **60% to 80% of GPU VRAM**, artificially capping concurrent batch sizes to 2 to 4 requests per GPU.

```
Naive Serving (Contiguous Virtual Memory):
Request 1 (Reserved for 4k): [Real Tokens: 50][-------------- Wasted Space: 3950 tokens -------------]
Request 2 (Reserved for 4k): [Real Tokens: 300][----------- Wasted Space: 3700 tokens -----------]
Result: GPU runs out of VRAM despite memory being 75% empty!
```

### The Solution: PagedAttention (vLLM)
Kwon et al. (UC Berkeley, 2023) introduced **PagedAttention**, inspired by the virtual memory and paging architecture of modern operating systems.

```
Logical Blocks (Per Request):
Logical Token Sequence:  [0..15] -> [16..31] -> [32..47] -> [48..63]
                            |          |           |           |
Block Table (Mapping):      |          |           |           |
Logical Block 0 ---------> Physical Block 7  (on GPU HBM)      |
Logical Block 1 ---------> Physical Block 2                    |
Logical Block 2 ---------> Physical Block 11                   |
Logical Block 3 ---------> Physical Block 4 <------------------+
```

1. **Non-Contiguous Allocation:** The KV cache for each request is partitioned into small, fixed-size **Physical Blocks** (typically 16 or 32 tokens).
2. **Page Table (Block Table):** The server maintains a lookup table mapping logical token indices to physical block addresses in GPU HBM.
3. **Near-Zero Waste:** Memory waste is confined strictly to the final block of a sequence ($< 4\%$ internal fragmentation).
4. **Memory Sharing (Copy-on-Write):** PagedAttention enables zero-copy prompt sharing:
   * **System Prompts:** Multiple requests sharing the exact same 1,000-token system prompt map their logical blocks to the same physical blocks.
   * **Parallel Sampling (Beam Search):** Forking paths share historical physical blocks until a token diverges, triggering copy-on-write allocation.

**Impact:** PagedAttention increases serving throughput by **2x to 4x** on identical GPU hardware without altering model weights or accuracy.

---

## 3. Continuous Batching (Iteration-Level Batching)

Traditional machine learning inference uses **Static Batching**: the engine waits for $B$ requests, batches them together, pads shorter prompts with pad tokens, and runs until all requests in the batch finish generating.

```
Static Batching Problem:
Request A (Len 5):   [t1][t2][t3][t4][t5] | [PAD][PAD][PAD][PAD][PAD] -> Idle GPU compute!
Request B (Len 10):  [t1][t2][t3][t4][t5][t6][t7][t8][t9][t10] (Finished)
Request C (Len 2):   [t1][t2] | [PAD][PAD][PAD][PAD][PAD][PAD][PAD][PAD] -> Idle GPU compute!
```

Because generation length varies wildly (e.g. 5 tokens vs 500 tokens), static batching leaves GPU cores idle waiting for the single longest sequence to complete.

### Continuous Batching (Orca / vLLM)
Continuous batching operates at the **iteration level** (per-token step) rather than the request level:

```
Iteration Step 1:  [Req A (Step 1)] [Req B (Step 1)] [Req C (Step 1)]
Iteration Step 2:  [Req A (Step 2)] [Req B (Step 2)] [Req C (Step 2: DONE!)]
Iteration Step 3:  [Req A (Step 3)] [Req B (Step 3)] [Req D (Prefill Step 1: ENTERS IMMEDIATELY!)]
```

* **Dynamic Insertion:** As soon as a request finishes (outputs `<|endoftext|>`), its KV blocks are freed, and a newly arrived request enters the batch at the very next iteration.
* **Elimination of Padding:** No padding tokens are ever processed.
* **GPU Saturation:** Keeps GPU tensor cores continuously utilized at near 100% duty cycle, multiplying system throughput by another 2x to 3x.

---

## 4. Chunked Prefill and Prefill-Decode Disaggregation

While Continuous Batching saturates GPUs, mixing prefill requests with decode requests introduces a major latency issue: **Prefill Bubbles**.

* A user submits a 4,000-token document. Processing the prompt (prefill) requires a massive matrix multiplication that monopolizes the GPU for 300 ms.
* Meanwhile, 10 other active requests waiting for their next decode token experience a 300 ms stall (**Inter-Token Latency spike**).

### Technique 1: Chunked Prefill (Sarathi-Serve / vLLM)
Instead of processing an entire 4,000-token prompt in a single monolithic pass, the engine slices large prompts into fixed-size chunks (e.g. 512 tokens):

```
Iteration 1: [Req A: Chunk 1 (512 tok)] + [Req B: Decode 1 tok] + [Req C: Decode 1 tok]
Iteration 2: [Req A: Chunk 2 (512 tok)] + [Req B: Decode 1 tok] + [Req C: Decode 1 tok]
```

* Smooths the execution time per iteration to an predictable budget (e.g. 35 ms).
* Prevents ITL degradation while maintaining high overall throughput.

### Technique 2: Prefill-Decode Disaggregation (SplitWise / DistServe)
Advanced multi-node setups separate GPUs into specialized pools:
* **Prefill Nodes:** Heavyweight GPUs (e.g. H100 with high FP8 Tensor Core throughput) dedicated exclusively to prompt processing.
* **Decode Nodes:** Memory-optimized GPUs (e.g. high HBM bandwidth) dedicated strictly to low-latency token generation.
* **High-Speed Transfer:** Once prefill completes, the computed KV cache blocks are transferred over NVLink or RDMA InfiniBand to the decode node.

---

## 5. Speculative Decoding

Autoregressive decoding generates exactly one token per model forward pass. Because forward passes are memory-bandwidth bound, generating 100 tokens requires 100 sequential passes through all 70 billion parameters.

**Speculative Decoding** breaks this sequential dependency by combining a small, fast **Draft Model** with a large **Target Model**.

```
1. Draft Model (e.g. Llama-3 8B, Fast):
   Generates K candidate tokens sequentially in low latency:
   Draft: ["Artificial", "intelligence", "transforms", "every", "industry"]

2. Target Model (e.g. Llama-3 70B, High Quality):
   Evaluates all K candidate tokens in a SINGLE forward pass using a causal tree mask:
   Scores:  Token 1: Accepted (p=0.98)
            Token 2: Accepted (p=0.95)
            Token 3: Accepted (p=0.91)
            Token 4: Rejected (Draft suggested "every", Target predicts "modern")
            Token 5: Discarded

3. Result:
   Generated 4 verified tokens in the time of a SINGLE 70B forward pass!
   Speedup: 2.5x to 3.5x with MATHEMATICALLY IDENTICAL probability distribution.
```

### Mathematical Guarantee (Lossless Verification)
Speculative decoding uses **rejection sampling** to ensure that the output probability distribution matches the target model exactly:
* Draft model generates token $x$ with probability $q(x)$.
* Target model assigns probability $p(x)$.
* If $p(x) \ge q(x)$: Accept token $x$ unconditionally.
* If $p(x) < q(x)$: Accept with probability $\frac{p(x)}{q(x)}$. If rejected, sample replacement token from $\max(0, p(x) - q(x))$ and terminate speculative window.
* **Result:** Zero loss in quality or perplexity compared to vanilla target model sampling.

---

## 6. Distributed Serving: Parallelism Strategies

When a model exceeds the memory of a single GPU (e.g. a 70B model in FP16 requires 140 GB just for weights, exceeding an 80 GB H100), we partition the model across multiple GPUs.

```
       Parallelism Strategies:
 +-----------------------------------------------------------+
 | 1. Tensor Parallelism (TP): Within a single node (NVLink) |
 |    Slices individual weight matrices across GPUs.         |
 +-----------------------------------------------------------+
 | 2. Pipeline Parallelism (PP): Across nodes (InfiniBand)   |
 |    Assigns layer 1..20 to Node 1, layer 21..40 to Node 2. |
 +-----------------------------------------------------------+
 | 3. Expert Parallelism (EP): For MoE Models                |
 |    Dispatches different expert FFNs to different GPUs.    |
 +-----------------------------------------------------------+
```

### Tensor Parallelism (TP) Internals (Megatron-LM Style)
Tensor Parallelism splits matrix multiplications across GPUs within the same server via high-speed NVLink (900 GB/s bidirectional bandwidth):
1. **Column Parallel Linear (First Linear Layer):**
   * Weight matrix $W$ is split column-wise: $W = [W_1 \mid W_2]$.
   * GPU 1 computes $Y_1 = X W_1$, GPU 2 computes $Y_2 = X W_2$.
   * No inter-GPU communication required yet.
2. **Row Parallel Linear (Second Linear Layer):**
   * Weight matrix $V$ is split row-wise: $V = \begin{pmatrix} V_1 \\ V_2 \end{pmatrix}$.
   * GPU 1 computes $Z_1 = Y_1 V_1$, GPU 2 computes $Z_2 = Y_2 V_2$.
   * Total output is $Z = Z_1 + Z_2$.
   * An **`All-Reduce` (Sum)** collective operation synchronizes the result across GPUs.
3. **Communication Cost:** Exactly two `All-Reduce` operations per Transformer layer (one for Attention, one for FFN). Because NVLink latency is sub-microsecond, TP is viable up to 8 GPUs within a single chassis.

---

## 7. Model Quantization: AWQ, GPTQ, and FP8

Quantization reduces the precision of model weights and activations from FP16 (16-bit) to 8-bit or 4-bit numbers, shrinking memory footprint and accelerating memory-bound decoding.

| Technique | Precision | Target | Key Innovation | Speedup / Memory |
| :--- | :--- | :--- | :--- | :--- |
| **GPTQ** | INT4 Weights, FP16 Activations | Weights only | Second-order Taylor series error compensation (Hessian matrix inversion) | 3.5x VRAM reduction, 2x to 3x decode speedup |
| **AWQ (Activation-aware Weight Quantization)** | INT4 Weights, FP16 Activations | Weights only | Protects the top 1% salient weights based on activation magnitudes | Superior accuracy preservation compared to GPTQ on instruction tasks |
| **FP8 (Hopper Native)** | FP8 (E4M3 / E5M2) | Weights AND Activations | Native hardware execution on NVIDIA H100 Tensor Cores | 2x speedup on both prefill (compute) and decode (memory), zero latency conversion overhead |

---

## 8. Enterprise Capacity Planning: Math & Sizing Walkthrough

### Interview Problem Scenario:
* Model: Llama 3 70B (Instruct)
* Concurrency: 500 active users streaming tokens simultaneously
* Average prompt length: 1,500 tokens
* Average response length: 500 tokens
* Target Inter-Token Latency (ITL): $< 35\text{ ms per token}$ ($> 28\text{ tokens/s}$)
* Target TTFT: $< 400\text{ ms}$

### Step 1: Memory Footprint per Node
Using 8x NVIDIA H100 (80GB HBM3 each) = 640 GB total VRAM.
Using Tensor Parallelism = 8 (`TP=8`).

1. **Model Weights in FP16:**
   $$\text{Weight Memory} = 70 \times 10^9 \times 2 \text{ bytes} = 140 \text{ GB}$$
2. **Available Memory for KV Cache:**
   $$\text{Total HBM} = 640 \text{ GB}$$
   $$\text{KV Cache Budget} = 640 \text{ GB} - 140 \text{ GB (Weights)} - 40 \text{ GB (CUDA context + scratch)} = 460 \text{ GB}$$
3. **KV Cache per Single Request (Length = 2,000 tokens):**
   * $n_{\text{layers}} = 80$
   * $n_{\text{kv\_heads}} = 8$ (GQA)
   * $d_{\text{head}} = 128$
   * Precision = FP16 ($2$ bytes)
   $$\text{KV Cache / Request} = 2 \times 2000 \times 80 \times 8 \times 128 \times 2 = 65,536,000 \text{ bytes} \approx 65.5 \text{ MB}$$
4. **Maximum Concurrent Requests per 8x H100 Node:**
   $$\text{Max Concurrent Streams} = \frac{460{,}000 \text{ MB}}{65.5 \text{ MB}} \approx 7{,}022 \text{ requests}$$
   * The node has ample VRAM for 500 concurrent requests! The bottleneck is **compute and memory bandwidth**, not VRAM capacity.

### Step 2: Compute and Bandwidth Verification
* 8x H100 total HBM bandwidth: $8 \times 3.35 \text{ TB/s} = 26.8 \text{ TB/s}$.
* Memory transfer required per decode token for 70B FP16 weights: $140 \text{ GB}$.
* Theoretical maximum decode iterations per second:
  $$\text{Max Iterations/sec} = \frac{26{,}800 \text{ GB/s}}{140 \text{ GB}} \approx 191 \text{ batch iterations/sec}$$
* At batch size $B=500$, generating 1 token for each of the 500 requests requires queuing them across multiple iterations or scaling horizontally across 4 nodes ($4 \times 8\text{-GPU}$ clusters) to achieve the target $< 35\text{ ms}$ per-token latency.

---

## Summary Checklist for Staff Serving Architecture
* [x] TTFT is dominated by compute-bound prompt prefill; ITL is dominated by memory-bandwidth-bound token decode.
* [x] PagedAttention eliminates internal and external memory fragmentation, increasing serving concurrency by 3x.
* [x] Continuous batching operates at iteration granularity, eliminating pad tokens and idle GPU time.
* [x] Chunked prefill prevents large prompt arrivals from creating latency spikes for active decode streams.
* [x] Speculative decoding accelerates inference by 2.5x to 3.5x without changing output probability distributions.
* [x] Tensor Parallelism uses intra-node NVLink to split linear layers with minimal communication overhead.
