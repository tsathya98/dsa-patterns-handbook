# Enterprise RAG and Agentic AI: Production System Design and Evaluation

> **Difficulty:** Case Study  
> **Pattern:** RAG, Agentic Systems, and GenAI Applications  
> **Scope:** Ingestion Pipelines, Hybrid Search, Reranking, Agent Loops, Semantic Caching, and Automated Evaluation

Retrieval-Augmented Generation (RAG) and Agentic Workflows have become the dominant architectural paradigms for applying Generative AI in enterprise settings. While a basic tutorial RAG application uses naive cosine similarity search over text chunks, a production-grade enterprise RAG system requires hybrid search, multi-stage reranking, query decomposition, semantic caching, guardrails, and quantitative evaluation.

This guide details the complete production architecture for building scalable, reliable, and grounded enterprise GenAI systems.

---

## 1. End-to-End Enterprise Architecture

A production RAG system is split into two asynchronous pipelines: the **Offline Ingestion Pipeline** and the **Online Query Execution Pipeline**.

```
+========================================================================================+
|                              OFFLINE INGESTION PIPELINE                                |
+========================================================================================+
[Raw Docs: PDF, Notion, SQL] 
    |
    v
[Document Parsers & OCR] (Unstructured / LlamaParse)
    |
    v
[Semantic Chunking Engine] (Header-aware, sliding window with 15% overlap)
    |
    v
[Metadata Enrichment] (Summaries, entity extraction, timestamps, ACL permissions)
    |
    +-------------------------------------+-------------------------------------+
    |                                     |                                     |
    v                                     v                                     v
[Dense Embeddings]              [Sparse Lexical Tokens]               [Metadata Store]
(e.g. OpenAI text-embed-3)      (BM25 / SPLADE)                       (PostgreSQL / Redis)
    |                                     |                                     |
    +-------------------------------------+-------------------------------------+
                                          |
                                          v
                              [Hybrid Vector Database]
                              (Milvus / Pinecone / Qdrant)

+========================================================================================+
|                              ONLINE QUERY PIPELINE                                     |
+========================================================================================+
User Query: "What was our Q3 cloud infrastructure spend variance?"
    |
    v
[Semantic Cache Check] (Redis / GPTCache: Return cached response if cosine sim > 0.96)
    | (Cache Miss)
    v
[Query Rewriting & HyDE] (Generate hypothetical answer, decompose multi-hop questions)
    |
    +-------------------------------------+-------------------------------------+
    |                                     |                                     |
    v (Dense Vector Search)               v (Sparse Lexical Search)             v (Metadata Filter)
[Top-50 Vector Chunks]                [Top-50 BM25 Chunks]                  [Tenant ID & ACLs]
    |                                     |                                     |
    +-------------------------------------+-------------------------------------+
                                          |
                                          v
                    [Reciprocal Rank Fusion (RRF)] (Merge into Top-40)
                                          |
                                          v
                    [Cross-Encoder Reranker] (Cohere / BGE-Reranker-Large -> Top-5)
                                          |
                                          v
                    [Context Compression & Prompt Assembly]
                                          |
                                          v
                    [LLM Generation: Claude 3.5 Sonnet / GPT-4o]
                                          |
                                          v
                    [Output Guardrails & Faithfulness Verification]
                                          |
                                          v
                            Streaming Answer to User
```

---

## 2. Ingestion Tier: Chunking Strategies and Metadata

Naive chunking (e.g. fixed 500 characters with no boundary awareness) is the single biggest cause of RAG hallucinations in production. It breaks sentences in half, separates tables from headers, and loses document context.

### Modern Chunking Strategies:
1. **Recursive Character Chunking:** Slices text iteratively using a priority hierarchy of separators: `["\n\n", "\n", ".", " ", ""]`. Keeps paragraphs and sentences intact.
2. **Semantic / Embedding Chunking:** Computes embedding distances between consecutive sentences. When cosine distance crosses a statistical threshold (e.g. 95th percentile of differences), a new chunk boundary is created.
3. **Document Layout Chunking:** Parses HTML/Markdown headers (`#`, `##`, `###`), table blocks, and bullet lists as distinct atomic units.
4. **Hierarchical / Parent-Document Chunking:**
   * Small chunks (e.g. 128 tokens) are indexed in the vector database for high-precision retrieval.
   * Each small chunk references a larger **Parent Document** (e.g. 1,024 tokens).
   * At retrieval time, matching the small chunk returns the full parent context to the LLM, preserving overarching narrative context.

---

## 3. Retrieval Tier: Hybrid Dense-Sparse Search

Pure vector search (dense embeddings) excels at semantic understanding and concept matching, but frequently fails on:
* Exact alphanumeric identifiers (e.g. error code `ERR_7301`, SKU `A89-Z2`).
* Acronyms and specialized internal domain jargon.
* Precise names and numbers.

Pure lexical search (BM25) excels at exact keyword matching, but fails on synonyms, paraphrase, and intent.

### The Production Solution: Reciprocal Rank Fusion (RRF)
Hybrid search executes both Dense Vector Search and BM25 Sparse Search in parallel, combining their rank lists using **Reciprocal Rank Fusion**:

$$RRF\_Score(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where:
* $M$: The set of retrieval models (Dense, BM25, SPLADE).
* $r_m(d)$: The rank position of document $d$ in system $m$ (1-indexed).
* $k$: Smoothing constant (typically $k = 60$).

```python
def reciprocal_rank_fusion(dense_ranks, sparse_ranks, k=60):
    rrf_scores = {}
    
    # Process dense search rankings
    for rank, doc_id in enumerate(dense_ranks, start=1):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))
        
    # Process sparse BM25 search rankings
    for rank, doc_id in enumerate(sparse_ranks, start=1):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))
        
    # Sort descending by fused score
    sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
    return [doc_id for doc_id, score in sorted_docs]
```

---

## 4. Late Interaction and Cross-Encoder Reranking

Embedding models are **Bi-Encoders**: they compress an entire document into a single fixed-length vector independently of the query.

While bi-encoders are fast ($O(1)$ vector dot product during retrieval), they cannot capture fine-grained token-level cross-interactions between the query and document.

### Multi-Stage Retrieval Pipeline:
1. **Stage 1 (High Recall):** Hybrid Search retrieves the top 50 to 100 candidate chunks in $< 15\text{ ms}$.
2. **Stage 2 (High Precision Reranking):** A **Cross-Encoder Reranker** (such as `bge-reranker-large` or Cohere Rerank) processes the query and each candidate chunk simultaneously through full cross-attention layers:

$$\text{Cross-Encoder Score} = \text{Model}(\text{Concat}(Q, \text{Chunk}))$$

* Cross-attention evaluates every query token against every chunk token.
* Filters out irrelevant matches, reducing 100 candidates down to the top 3 to 5 highest-relevance contexts.
* Adds approximately 20 to 40 ms of latency, but improves answer accuracy by **25% to 40%**.

---

## 5. Mitigating "Lost in the Middle"

Liu et al. (Stanford, 2023) demonstrated the **Lost in the Middle** phenomenon: LLMs are significantly better at extracting information located at the very beginning or the very end of their input prompt context window. Information placed in the middle of long prompts experiences attention degradation and is frequently ignored.

```
Model Attention Retrieval Accuracy vs Token Position:
Accuracy (%)
 100% | \                                          /
      |  \                                        /
      |   \                                      /
  50% |    \                                    /
      |     \________ Attention Dip ___________/
   0% +-------------------------------------------------->
     Beginning (Top Chunks)    Middle (Buried)     End (Recent Context)
```

### Production Mitigations:
1. **Context Compression:** Use extractive summarizers (e.g. LLMLingua) to remove low-information tokens before feeding context to the LLM.
2. **Position-Aware Reordering:** Place the highest-scoring reranked chunk at the very beginning, the second-highest at the very end, and lower-scored chunks in the middle.
3. **Prompt Structuring:** Clearly tag chunks with XML tags (`<context id="1">...</context>`) and instruct the model to explicitly cite chunk IDs in its reasoning.

---

## 6. Agentic AI Architecture: ReAct and Multi-Agent Workflows

While standard RAG is a static, single-turn retrieval pipeline, complex enterprise tasks require **Agentic AI**: models equipped with tool use, memory, and multi-step reasoning loops.

```
       User Goal: "Find all pending invoices over $50k and email the finance lead"
                                   |
                                   v
                         [Agent Planning State]
                                   |
      +----------------------------+----------------------------+
      |                                                         |
      v                                                         v
   [Thought]                                                 [Action]
   "I need to query the billing database                      "Call SQLTool with:
    for invoices > 50000 where status = 'pending'"            SELECT * FROM invoices..."
      ^                                                         |
      |                                                         v
      |                                                    [Observation]
      |                                                    "Found 3 matching invoices:
      |                                                     INV-101, INV-104, INV-109"
      +----------------------------+----------------------------+
                                   |
                                   v
                               [Thought]
                               "Now I must look up the finance lead email in Slack Directory"
                                   |
                                   v
                               [Action]
                               "Call DirectoryTool(role='finance_lead')" ...
```

### Core Agent Patterns:
1. **ReAct (Reasoning + Acting):** Interleaves thought generation with action execution, allowing the agent to observe tool outputs before deciding the next step.
2. **Plan-and-Solve:** The agent first generates an explicit step-by-step DAG plan, then executes each step sequentially, re-planning if an intermediate step fails.
3. **Multi-Agent Orchestration (LangGraph / AutoGen):**
   * **Supervisor Agent:** Decomposes user goals and delegates sub-tasks.
   * **Worker Agents:** Specialized agents with restricted toolsets (e.g. SQL Agent, Python Code Execution Agent, Web Search Agent).
   * **Deterministic State Graphs:** Enforces state transitions using formal state machines rather than open-ended LLM loops, preventing infinite tool loops.

---

## 7. Production Guardrails and Semantic Caching

```
User Input
    |
    v
[Input Guardrail: NeMo / Llama Guard] ---> (Blocked: Injection attack / PII detected)
    |
    v (Passed)
[Semantic Cache: Redis Vector Similarity]
    |
    +---> (Cosine similarity > 0.96) ----> Return Cached Response (Latency: 8 ms!)
    |
    v (Cache Miss)
[RAG Execution & LLM Generation]
    |
    v
[Output Guardrail: Hallucination Check & Faithfulness]
    |
    v
Sanitized Answer Delivered
```

1. **Semantic Caching (GPTCache / Redis):**
   * Stores past user query embeddings and answers in Redis.
   * If a new query has cosine similarity $\ge 0.96$ with a cached query, the system returns the cached answer instantly.
   * Reduces LLM token costs by **30% to 50%** and drops latency from 2 seconds to under 10 milliseconds for repetitive queries.
2. **Prompt Injection Guardrails:**
   * Uses dual-model architecture: a lightweight classifier (e.g. Llama Guard) screens incoming inputs for jailbreak attempts (`"Ignore all previous instructions"`).
3. **PII Masking:**
   * Runs local regex and spaCy NER to redact Social Security Numbers, credit cards, and email addresses before sending data to external API models.

---

## 8. Continuous Evaluation Framework: The RAG Triad

Traditional software uses unit tests. Enterprise GenAI systems rely on synthetic benchmark datasets and continuous evaluation using the **RAG Triad** (promoted by TruLens and Ragas):

```
                       [User Query]
                      /            \
                     /              \
         (Context Relevance)   (Answer Relevance)
                   /                  \
                  v                    v
          [Retrieved Context] ======> [Generated Answer]
                     \                  /
                      \                /
                       (Faithfulness)
```

1. **Context Relevance:**
   * Is the retrieved context actually relevant to the user query?
   * Low score indicates: Poor embedding model, suboptimal chunking, or noisy search index.
2. **Faithfulness (Groundedness):**
   * Can every claim in the generated answer be directly inferred from the retrieved context?
   * Low score indicates: The LLM is hallucinating from its pretraining weights rather than relying on enterprise documents.
3. **Answer Relevance:**
   * Does the generated answer directly address the user query without rambling or omitting key instructions?
   * Low score indicates: Suboptimal prompt engineering or model instruction-following failure.

### Evaluation Formula:
$$\text{RAG Triad Score} = \frac{\text{Context Relevance} + \text{Faithfulness} + \text{Answer Relevance}}{3}$$

In production CI/CD pipelines, any code change (chunk size change, embedding model upgrade, system prompt tweak) is automatically evaluated against a test set of 200 reference question-context-answer triples. If the Faithfulness score drops below 0.90, the deployment is blocked.

---

## Summary Checklist for Enterprise RAG & Agents
* [x] Hybrid Search (Dense Vector + BM25 Lexical) via Reciprocal Rank Fusion is mandatory for production recall.
* [x] Cross-Encoder Reranking reduces 100 candidate chunks to top-5 high-precision passages.
* [x] Semantic Caching with Redis cuts recurring query latency from 2,000 ms to 10 ms.
* [x] ReAct and state-machine graphs (LangGraph) prevent uncontrolled tool execution loops.
* [x] The RAG Triad (Context Relevance, Faithfulness, Answer Relevance) provides automated regression testing in CI/CD.
