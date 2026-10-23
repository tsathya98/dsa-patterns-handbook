# Transformers and Generative AI: From Attention Mathematics to Modern LLM Architecture

> **Difficulty:** Concept  
> **Pattern:** Transformers and Modern GenAI  
> **Scope:** Architecture, Mathematics, Memory Roofline, and Production Systems

Modern Generative AI is built on the Transformer architecture introduced by Vaswani et al. in 2017 ("Attention is All You Need"). While the original paper targeted machine translation using an encoder-decoder structure, modern Large Language Models (LLMs) such as GPT-4, Claude 3, Llama 3, and Mistral have evolved into decoder-only models optimized for autoregressive token generation.

This guide provides an end-to-end breakdown of the mathematics, architectural components, hardware constraints, and production optimizations powering modern Generative AI.

---

## 1. High-Level Taxonomy: Encoders, Decoders, and Encoder-Decoder

The original Transformer was split into two halves: an Encoder and a Decoder. Modern GenAI models choose one of three distinct architectural paradigms depending on their downstream objective:

| Paradigm | Exemplar Models | Attention Masking | Best For | Typical Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **Encoder-Only** | BERT, RoBERTa, DeBERTa | Bidirectional (all tokens attend to all tokens) | Understanding, classification, feature extraction | Text classification, NER, embedding generation, reranking |
| **Decoder-Only** | GPT-4, Llama 3, Mistral, Claude | Causal / Autoregressive (tokens only attend to past tokens) | Open-ended generation, reasoning, instruction following | Chatbots, code generation, creative writing, agents |
| **Encoder-Decoder** | T5, BART, Whisper (Audio) | Bidirectional encoder + Causal cross-attention decoder | Transduction (mapping sequence A to sequence B) | Machine translation, abstractive summarization, audio-to-text |

### Why Decoder-Only Won the LLM Race
1. **Unified Objective:** Decoder-only models predict the next token given all prior tokens ($P(x_t \mid x_{<t})$). This unifies pretraining, few-shot in-context learning, and instruction tuning into a single generative framework.
2. **Compute Efficiency:** Pretraining a decoder-only model maximizes the number of tokens supervised per FLOP. Every token in a sequence of length $N$ provides training loss, whereas encoder-decoder models only compute loss on the target sequence.
3. **In-Context Generalization:** Autoregressive training forces the model to encode both past context and forward predictive reasoning within the same latent representations.

```
1. Encoder-Only (BERT):
   [x1] <---> [x2] <---> [x3] <---> [x4]  (Fully connected bidirectional attention)

2. Decoder-Only (GPT / Llama):
   [x1] ----> [x2] ----> [x3] ----> [x4]  (Causal triangular mask: no looking forward)
     |          |          |          |
   predict    predict    predict    predict
    token2     token3     token4     token5

3. Encoder-Decoder (T5):
   [Encoder: Bidirectional]  == Cross-Attention ==>  [Decoder: Causal Autoregressive]
```

---

## 2. Scaled Dot-Product Attention: Math and Mechanics

The fundamental operation of a Transformer is **Scaled Dot-Product Attention**.

Given an input sequence representation $X \in \mathbb{R}^{N \times d_{\text{model}}}$, we project it into three distinct matrices using learned weights $W_Q, W_K, W_V \in \mathbb{R}^{d_{\text{model}} \times d_k}$:

$$Q = X W_Q \quad (\text{Queries: what am I looking for?})$$
$$K = X W_K \quad (\text{Keys: what do I contain?})$$
$$V = X W_V \quad (\text{Values: what information do I communicate?})$$

The attention score between all tokens is calculated as:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

### Why Divide by $\sqrt{d_k}$?
* If components of $q$ and $k$ are independent random variables with zero mean and variance 1, their dot product $q \cdot k = \sum_{i=1}^{d_k} q_i k_i$ has mean 0 and variance $d_k$.
* For large head dimensions (e.g. $d_k = 128$), the variance of dot products is 128, leading to extreme values (magnitude $> 30$).
* When extreme values pass into $\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$, the softmax distribution saturates. The largest value receives a probability near 1.0, and all other tokens receive near 0.0.
* In saturated regions, the derivative of softmax is virtually zero ($\frac{\partial s_i}{\partial z_j} \approx 0$). This causes **vanishing gradients**, halting backpropagation.
* Scaling by $\frac{1}{\sqrt{d_k}}$ normalizes the dot product variance back to 1.0, preserving healthy gradients throughout deep networks.

---

## 3. Multi-Head, Multi-Query, and Grouped-Query Attention

In standard **Multi-Head Attention (MHA)**, queries, keys, and values are split across $h$ heads, each with dimension $d_k = d_{\text{model}} / h$:

$$\text{MHA}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W_O$$
$$\text{where} \quad \text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)$$

Splitting into multiple heads allows the model to attend to different types of relationships at the same time: syntactic dependencies, semantic coreference, and distant factual associations.

### The Memory Bottleneck: Moving to MQA and GQA
During autoregressive generation (the decode phase), the GPU must load past Key and Value vectors from High Bandwidth Memory (HBM) into SRAM for every single generated token. With large batch sizes and long contexts, memory bandwidth, not compute, becomes the primary bottleneck.

To solve this, modern LLMs use:
1. **Multi-Head Attention (MHA):** $h$ query heads, $h$ key heads, $h$ value heads. (High memory footprint).
2. **Multi-Query Attention (MQA):** $h$ query heads, but only 1 shared key head and 1 shared value head. (Cuts KV cache memory by $h\times$, but may degrade reasoning quality).
3. **Grouped-Query Attention (GQA):** $h$ query heads partitioned into $g$ groups (typically 4 or 8), where each group shares 1 key head and 1 value head.
   * Llama 2 (70B), Llama 3 (8B and 70B), and Mistral-7B use GQA.
   * Delivers an 8x reduction in KV cache memory footprint with virtually zero degradation in perplexity or task accuracy.

```
1. Multi-Head Attention (MHA):
   Q: [Q1] [Q2] [Q3] [Q4] [Q5] [Q6] [Q7] [Q8]
   K: [K1] [K2] [K3] [K4] [K5] [K6] [K7] [K8]  (1 Key head per Query head)
   V: [V1] [V2] [V3] [V4] [V5] [V6] [V7] [V8]

2. Multi-Query Attention (MQA):
   Q: [Q1] [Q2] [Q3] [Q4] [Q5] [Q6] [Q7] [Q8]
   K: [------------ K (Single Shared) ------------]
   V: [------------ V (Single Shared) ------------]

3. Grouped-Query Attention (GQA):
   Q: [Q1  Q2]  [Q3  Q4]  [Q5  Q6]  [Q7  Q8]
   K:   [K1]      [K2]      [K3]      [K4]     (Each Key/Value shared across 2 queries)
   V:   [V1]      [V2]      [V3]      [V4]
```

---

## 4. Positional Encodings: From Sinusoids to RoPE

Because self-attention is permutation-invariant ($\text{Attention}(P Q, P K, P V) = P \cdot \text{Attention}(Q, K, V)$), a Transformer has no inherent sense of word order unless positional information is explicitly injected.

### Evolution of Position Representations:
1. **Absolute Sinusoidal (Vaswani et al., 2017):**
   $$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right), \quad PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)$$
   Directly added to the input token embeddings. Fixed and non-trainable, but poor extrapolation beyond training context length.
2. **Learned Absolute Embeddings (BERT, GPT-2):**
   A lookup matrix $W_{pos} \in \mathbb{R}^{L_{\max} \times d}$. Easy to train, but completely fails if input length exceeds $L_{\max}$.
3. **ALiBi (Attention with Linear Biases, Press et al., 2021):**
   Injects a static penalty proportional to token distance directly into the attention logits:
   $$\text{Attention} = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}} - m \cdot |i - j|\right)$$
   Allows strong length extrapolation without positional embeddings, used in Falcon and MPT.
4. **RoPE (Rotary Position Embeddings, Su et al., 2021):**
   The industry standard used by Llama 3, Mistral, Gemma, and DeepSeek.
   * Instead of adding position vectors to embeddings, RoPE rotates the Query and Key vectors in the 2D complex plane by an angle proportional to their position index $m$:
     $$R_{\Theta, m}^d = \text{diag}\left(R_{\theta_1, m}, R_{\theta_2, m}, \dots, R_{\theta_{d/2}, m}\right)$$
     $$\text{where} \quad R_{\theta_i, m} = \begin{pmatrix} \cos(m\theta_i) & -\sin(m\theta_i) \\ \sin(m\theta_i) & \cos(m\theta_i) \end{pmatrix}, \quad \theta_i = 10000^{-2(i-1)/d}$$
   * **Crucial Mathematical Property:** The inner product between rotated query $q_m$ and rotated key $k_n$ depends **only on their relative distance $(m - n)$**:
     $$\langle R_{\Theta, m} q, R_{\Theta, n} k \rangle = q^T R_{\Theta, n - m} k$$
   * **Context Window Scaling:** Because RoPE operates on angles, context windows can be scaled (e.g. from 8k to 128k tokens) by adjusting base frequencies (NTK-aware scaling, YaRN, or RoPE interpolation) without retraining the model from scratch.

---

## 5. Modern Transformer Block Internals

A standard Transformer block consists of two sub-layers: Attention and a Feed-Forward Network (FFN), wrapped in residual connections and normalization layers.

```
       Input x
          |
     +----+----+
     |         |
     |      RMSNorm
     |         |
     |     Causal MHA / GQA (RoPE)
     |         |
     +--->(+)<-+  Residual Connection 1
          |
     +----+----+
     |         |
     |      RMSNorm
     |         |
     |       SwiGLU FFN
     |         |
     +--->(+)<-+  Residual Connection 2
          |
       Output
```

### Pre-LN vs Post-LN
* **Post-LN (Original 2017 Transformer):** $x_{l+1} = \text{LN}(x_l + \text{SubLayer}(x_l))$. Normalization occurs on the main residual highway. As depth increases, gradients passing through the normalization layer diminish or explode, requiring warmup schedules and careful tuning.
* **Pre-LN (Modern Standard):** $x_{l+1} = x_l + \text{SubLayer}(\text{LN}(x_l))$. The residual highway ($x_l + \dots$) remains completely untouched by normalization. Gradients flow unimpeded directly from the final layer to the initial layer, enabling stable training of 100B+ parameter models.

### RMSNorm: Faster Normalization
Standard LayerNorm calculates both mean and variance:
$$\text{LN}(x) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \odot \gamma + \beta$$

Zhang and Sennrich (2019) demonstrated that the mean-centering step ($\mu$) contributes negligible value to training stability. **RMSNorm** (Root Mean Square Normalization) scales strictly by the root mean square:

$$\text{RMSNorm}(x) = \frac{x}{\text{RMS}(x)} \odot \gamma, \quad \text{where} \quad \text{RMS}(x) = \sqrt{\frac{1}{d} \sum_{i=1}^d x_i^2 + \epsilon}$$

* Saves approximately 7% compute time per layer by avoiding two reduction passes over memory.
* Used across Llama, Gemma, and Mistral.

### SwiGLU: Higher Non-Linear Capacity
In original Transformers, the FFN used ReLU or GELU:
$$\text{FFN}(x) = \text{GELU}(x W_1 + b_1) W_2 + b_2$$

Shazeer (2020) introduced Gated Linear Units (GLU). **SwiGLU** applies the Swish activation function $\text{Swish}(x) = x \cdot \sigma(\beta x)$ as a multiplicative gate:

$$\text{SwiGLU}(x) = \left(\text{Swish}(x W_{\text{gate}}) \otimes (x W_{\text{up}})\right) W_{\text{down}}$$

* While standard FFN uses two weight matrices ($d_{\text{model}} \to 4 d_{\text{model}} \to d_{\text{model}}$), SwiGLU uses three matrices ($W_{\text{gate}}, W_{\text{up}}, W_{\text{down}}$).
* To maintain identical parameter counts, the intermediate hidden dimension is set to approximately $\frac{8}{3} d_{\text{model}}$ rather than $4 d_{\text{model}}$.
* Consistently achieves lower validation perplexity across all benchmark scales.

---

## 6. The KV Cache Bottleneck: Prefill vs Decode Phases

During LLM inference, token generation happens in two distinct phases:

### Phase 1: Prefill (Prompt Processing)
* The entire input prompt of $N$ tokens is processed in parallel.
* This is **compute-bound**. The GPU tensor cores operate at maximum arithmetic intensity performing matrix multiplications (GEMM).
* High FLOPs utilization, low memory latency bottleneck.

### Phase 2: Decode (Token Generation)
* The model generates tokens autoregressively, one token at a time.
* Generating token $t+1$ requires attention over all previous tokens $1 \dots t$.
* If we recomputed $K$ and $V$ vectors for all prior tokens at every step, decoding a sequence of length $N$ would require $O(N^2)$ redundant compute.
* **The Solution:** We cache the computed Key and Value matrices in GPU VRAM (the **KV Cache**). At step $t+1$, we compute only $q_{t+1}, k_{t+1}, v_{t+1}$, append $k_{t+1}$ and $v_{t+1}$ to the cache, and compute attention:

```
Step 1: Prompt "The quick brown" -> Prefill -> KV Cache stored
Step 2: Generate "fox" -> Compute q_fox, append k_fox, v_fox to KV Cache -> Attention(q_fox, KV_cache)
Step 3: Generate "jumps" -> Compute q_jumps, append k_jumps, v_jumps -> Attention(q_jumps, KV_cache)
```

### The Memory Bandwidth Bottleneck
During decode, we perform vector-matrix multiplication (GEMV): a single query vector of size $1 \times d_{\text{model}}$ is multiplied against the entire cached history of keys.
* Arithmetic intensity is extremely low: we transfer gigabytes of weights and KV states across the memory bus just to compute a few hundred thousand FLOPs.
* The GPU cores sit idle waiting for weights and cache data to transfer from High-Bandwidth Memory (HBM) to on-chip SRAM.
* **Inference throughput during decode is strictly memory bandwidth-bound.**

### KV Cache Memory Sizing Formula
To size GPU memory for production serving, use the exact KV cache formula:

$$\text{Memory}_{\text{KV}} = 2 \times B \times L \times n_{\text{layers}} \times n_{\text{kv\_heads}} \times d_{\text{head}} \times P$$

Where:
* $2$: Storing both Keys and Values.
* $B$: Batch size (concurrent requests).
* $L$: Sequence length (prompt tokens + generated tokens).
* $n_{\text{layers}}$: Total transformer layers.
* $n_{\text{kv\_heads}}$: Number of key-value heads ($h$ in MHA, $g$ in GQA).
* $d_{\text{head}}$: Dimension per attention head ($d_{\text{model}} / n_{\text{q\_heads}}$).
* $P$: Bytes per parameter ($2$ bytes for FP16/BF16, $1$ byte for FP8).

#### Practical Calculation: Llama 3 70B
* $n_{\text{layers}} = 80$
* $n_{\text{kv\_heads}} = 8$ (GQA with 64 query heads)
* $d_{\text{head}} = 128$
* Precision = FP16 ($2$ bytes)
* Batch size $B = 16$, Context length $L = 4096$

$$\text{Memory}_{\text{KV}} = 2 \times 16 \times 4096 \times 80 \times 8 \times 128 \times 2 = 21,474,836,480 \text{ bytes} \approx 21.48 \text{ GB}$$

* Notice: If Llama 3 70B used standard MHA (64 heads instead of 8), the KV cache alone would consume **171.8 GB**, requiring multiple additional 80GB H100 GPUs just to store the cache.

---

## 7. FlashAttention (v1, v2, and v3)

Standard GPU attention implementations write intermediate matrices to High Bandwidth Memory (HBM):
1. Compute $S = Q K^T \in \mathbb{R}^{N \times N}$ and write to HBM.
2. Read $S$ from HBM, compute $P = \text{softmax}(S)$, and write $P$ to HBM.
3. Read $P$ and $V$ from HBM, compute $O = P V$, and write $O$ to HBM.

For a context length of $N = 32{,}768$, storing $S$ requires $32768 \times 32768 \times 2 \text{ bytes} \approx 2.14 \text{ GB}$ per attention head. With 32 heads, that is 68 GB for a single layer, causing catastrophic out-of-memory errors and memory bus saturation.

```
Standard Attention (Memory IO Bound):
   GPU SRAM (Fast, small ~200KB/SM) <==== Massive HBM Read/Write ====> GPU HBM (Slow, 80GB)
   Writes intermediate N x N attention matrix back and forth to HBM!

FlashAttention (Compute Bound Tiling):
   GPU SRAM (Fast) <---- Tile Q_i, K_j, V_j blocks (e.g. 128x128) ---- GPU HBM
   Computes online softmax incrementally inside SRAM.
   Zero N x N matrix ever written to HBM!
```

### The FlashAttention Breakthrough (Dao et al.)
FlashAttention reformulates the attention computation to eliminate all HBM reads/writes for intermediate matrices:
1. **Tiling:** Divides the $Q, K, V$ matrices into small blocks that fit entirely inside fast on-chip SRAM (100 to 228 KB per Streaming Multiprocessor).
2. **Online Softmax:** Uses Milakov and Gimelshteyn's online softmax technique to compute the softmax normalization factor incrementally across blocks without needing the full row of $Q K^T$:
   $$m_{\text{new}} = \max(m_{\text{prev}}, x), \quad d_{\text{new}} = d_{\text{prev}} e^{m_{\text{prev}} - m_{\text{new}}} + e^{x - m_{\text{new}}}$$
3. **Recomputation in Backward Pass:** During training, FlashAttention does not store the $N \times N$ attention matrix for backpropagation. Instead, it recomputes it on-the-fly in SRAM from $Q, K, V$ during the backward pass, which is significantly faster than reading memory from HBM.

### FlashAttention Generations:
* **FlashAttention-1 (2022):** Cut memory from $O(N^2)$ to $O(N)$ and accelerated training by 2x to 4x.
* **FlashAttention-2 (2023):** Tweaked the outer/inner loop order to minimize non-matmul FLOPs and optimized parallelization across warp threads, reaching 73% theoretical peak FLOPs on A100.
* **FlashAttention-3 (2024):** Optimized specifically for NVIDIA Hopper (H100) architecture:
  * Uses Tensor Memory Accelerator (TMA) for asynchronous memory copies.
  * Overlaps Tensor Core matrix multiplication with data movement using Hopper warp-group instructions.
  * Native FP8 precision attention with hardware-level outlier suppression, achieving up to 1.2 PFLOPs/s on H100.

---

## 8. Mixture of Experts (MoE)

As dense models scale beyond 70B parameters, training and inference costs grow linearly with parameter count. **Mixture of Experts (MoE)** replaces the dense Feed-Forward Network in each Transformer block with multiple independent "experts", routing each token to only a sparse subset.

```
       Input Token x
             |
      +------+------+
      |             |
   [Router]     [Experts 1..8]
      |             |
  Top-2 Gating   Expert 1 (Dense FFN)
  Weights:       Expert 2 (Dense FFN)
  [0.7, 0.3]     ...
      |          Expert 8 (Dense FFN)
      +------+------+
             |
    y = 0.7 * E1(x) + 0.3 * E3(x)
```

### Routing Formulation
Given $E$ experts, a learned router produces logits $H(x) = x W_g$. The gating weights are calculated using Top-$K$ softmax:

$$g(x) = \text{Softmax}(\text{TopK}(H(x), K))$$
$$y = \sum_{i \in \text{TopK}} g(x)_i E_i(x)$$

### Notable Production Implementations:
* **Mixtral 8x7B:** 8 experts, Top-2 routing ($K=2$). Total parameters: 46.7B. Active parameters per token: **12.9B**. Operates at the latency and compute cost of a 13B model while matching or exceeding Llama 2 70B on benchmarks.
* **DeepSeek-V2 / V3:** Uses Fine-Grained Expert Segmentation (dividing experts into smaller slices) and isolates **Shared Experts** (always active for common language priors) alongside routed specialized experts, achieving state-of-the-art FLOP efficiency.

### MoE Trade-Offs in Production
1. **Memory vs Compute Asymmetry:** An MoE model requires VRAM to hold **all** expert weights simultaneously (e.g. 46.7B parameters in memory), but only consumes compute for the active weights (12.9B parameters).
2. **Routing Collapse & Load Imbalance:** Left unconstrained, the router may send all tokens to the same 1 or 2 popular experts, leaving other experts untrained. Models incorporate an auxiliary **load balancing loss**:
   $$\mathcal{L}_{\text{balance}} = \alpha \cdot E \sum_{i=1}^E f_i P_i$$
   where $f_i$ is the fraction of tokens dispatched to expert $i$, and $P_i$ is the average routing probability.
3. **All-to-All Communication Overhead:** In distributed training and serving across multiple GPUs (Expert Parallelism), routing tokens to experts situated on different physical GPUs requires heavy `All-to-All` network collective calls over NVLink or InfiniBand.

---

## 9. Model Architecture Comparison

| Feature | BERT | GPT-4 / Llama 3 | T5 | Mixtral 8x7B |
| :--- | :--- | :--- | :--- | :--- |
| **Type** | Encoder-Only | Decoder-Only | Encoder-Decoder | Sparse MoE Decoder |
| **Attention** | Bidirectional | Causal (Masked) | Bidirectional + Causal | Causal + GQA |
| **Positional Encoding** | Learned Absolute | RoPE (Rotary) | Relative Bias | RoPE |
| **Normalization** | Post-LN LayerNorm | Pre-LN RMSNorm | Pre-LN RMSNorm | Pre-LN RMSNorm |
| **Activation** | GELU | SwiGLU | Gated ReLU | SwiGLU |
| **KV Cache Needed?** | No (Single-pass) | Yes (Crucial for decode) | Yes (Decoder side) | Yes (For active experts) |
| **Inference Bottleneck**| Compute (Batch GEMM) | Memory Bandwidth (Decode)| Mixed | VRAM Capacity + Bandwidth|

---

## 10. System Design Interview Cheat Sheet: The Roofline Model

In an AI or GenAI System Design interview (e.g. for Senior or Staff Engineer roles at Google, Meta, Uber, or AI startups), you will frequently be asked to analyze hardware bottlenecks using the **Roofline Model**:

```
Attainable Performance (FLOP/s) = min(Peak Compute FLOP/s, Memory Bandwidth * Operational Intensity)
```

$$\text{Operational Intensity} = \frac{\text{Floating Point Operations (FLOPs)}}{\text{Memory Transferred (Bytes)}}$$

```
Compute / FLOPs
      ^
 Peak |======================= (Compute-Bound: Prefill, Matrix Multiply GEMM)
 FLOPs|                      /
      |                     /
      |                    /
      |                   /  (Memory-Bound: Autoregressive Decode GEMV)
      |                  /
      +-----------------+----------------------------------> Operational Intensity
                      Ridge Point
```

### Interview Diagnostic Checklist:
1. **Prefill Stage is Compute-Bound:**
   * High operational intensity ($\gg 100$ FLOPs/byte).
   * Bottleneck: GPU Tensor Cores.
   * Optimization: Chunked prefill, FlashAttention, Tensor Parallelism.
2. **Decode Stage is Memory Bandwidth-Bound:**
   * Low operational intensity ($\approx 1$ to $2$ FLOPs/byte for batch size 1).
   * Bottleneck: HBM to SRAM memory transfer bus.
   * Optimization: Grouped-Query Attention (GQA), PagedAttention, INT4/FP8 Quantization, Speculative Decoding.
3. **VRAM Sizing Rule of Thumb:**
   * Model Weights: $2 \text{ bytes per parameter}$ in FP16, $1 \text{ byte}$ in FP8, $0.5 \text{ bytes}$ in INT4.
   * KV Cache: $2 \times B \times L \times n_{\text{layers}} \times n_{\text{kv\_heads}} \times d_{\text{head}} \times P$.
   * Activation Overhead: $10\%$ to $20\%$ buffer for intermediate tensor buffers.

---

## Summary Checklist for Staff AI Interviews
* [x] Scaled dot-product attention divides by $\sqrt{d_k}$ to prevent softmax saturation and vanishing gradients.
* [x] RoPE rotates query and key vectors in the complex plane, preserving relative distance invariance $(m - n)$ and enabling context extension.
* [x] Modern LLMs standardize on Pre-LN, RMSNorm, and SwiGLU for deep gradient propagation stability.
* [x] GQA bridges MHA and MQA, cutting KV cache VRAM by 8x with zero quality loss.
* [x] FlashAttention tiles attention into SRAM blocks using online softmax, avoiding $O(N^2)$ HBM memory read/write cycles.
* [x] Inference alternates between compute-bound Prefill and memory-bandwidth-bound Decode.
