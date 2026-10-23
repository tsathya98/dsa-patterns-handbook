# Large-Scale Recommendation Systems: Two-Tower Models, Approximate Nearest Neighbors, and Multi-Task Ranking

> **Difficulty:** Case Study  
> **Pattern:** Recommendation Systems and Deep Ranking  
> **Scope:** Multi-Stage Funnel, Two-Tower Networks, ANN Vector Search (HNSW), DLRM, Multi-Task Ranking (MMoE), and Real-Time Latency Budgets

Recommendation systems power the primary revenue engines of modern tech giants: YouTube recommendations, TikTok feed, Amazon product carousels, Instagram Explore, and Spotify Discover Weekly. The engineering challenge is immense: given an inventory of 1 billion items and a user request arriving with a strict 50 millisecond SLA, the system must select, rank, and personalize the top 20 items.

This guide provides the complete systems architecture for building internet-scale recommendation platforms.

---

## 1. The Multi-Stage Recommendation Funnel

Evaluating a complex deep learning model over 1 billion candidate items for every user query is computationally impossible within a 50 ms latency window.

All production recommendation systems solve this by decomposing the problem into a multi-stage funnel:

```
Total Inventory: 1,000,000,000 Items
               |
               v
 [Stage 1: Candidate Generation / Retrieval]  (Latency: 10 - 15 ms)
  * Two-Tower Deep Neural Networks
  * Approximate Nearest Neighbors (ANN: HNSW / ScaNN)
  * Graph Collaborative Filtering
  * Filters 1B items down to ~1,000 candidates
               |
               v
 [Stage 2: Scoring & Heavy Ranking]          (Latency: 20 - 25 ms)
  * Deep Learning Recommendation Models (DLRM / MMoE)
  * Multi-task prediction: P(Click), P(Like), P(Share), P(Watch Time)
  * Evaluates complex cross-features over 1,000 items -> Top 100
               |
               v
 [Stage 3: Re-ranking, Diversity & Business Logic] (Latency: 5 - 10 ms)
  * Deduplication & author fatigue filtering
  * Maximal Marginal Relevance (MMR) for diversity
  * Freshness boost & sponsored ad injection
  * Final selection: Top 20 items streamed to client
```

---

## 2. Stage 1: Two-Tower Deep Neural Networks

The foundational architecture for candidate retrieval is the **Two-Tower Model** (pioneered by Google and YouTube).

```
         User Features                               Item Features
 (User ID, Search History, Age,               (Video ID, Title, Tags,
  Device, Recent Interactions)                 Category, Duration, Age)
               |                                            |
               v                                            v
     [User Deep Tower MLP]                        [Item Deep Tower MLP]
               |                                            |
               v                                            v
     User Embedding u in R^d                      Item Embedding v in R^d
               \                                            /
                \                                          /
                 +-------> Dot Product <------------------+
                                 |
                                 v
                     Similarity Score = <u, v>
```

### Key Architectural Advantage: Asymmetric Computation
1. **Offline Item Tower:** Item embeddings $v_i \in \mathbb{R}^d$ are computed offline in batch jobs across the catalog and indexed into an Approximate Nearest Neighbor (ANN) vector database.
2. **Online User Tower:** When a user opens the app, only the lightweight **User Tower** runs in real-time ($< 5\text{ ms}$), producing query vector $u$.
3. **Retrieval via Vector Search:** The query vector $u$ queries the ANN index, retrieving the top 1,000 most similar items using inner product search in $< 10\text{ ms}$.

### Loss Formulation: Sampled Softmax with In-Batch Negatives
Training uses cross-entropy over batch items. For a user $u_i$ and their interacted positive item $v_i$, all other items in the mini-batch $v_j$ ($j \ne i$) serve as negative samples:

$$\mathcal{L} = -\sum_{i=1}^B \log \frac{\exp(u_i^T v_i / \tau)}{\sum_{j=1}^B \exp(u_i^T v_j / \tau)}$$

where $\tau$ is a temperature hyperparameter.

---

## 3. Approximate Nearest Neighbor (ANN) Indexing: HNSW vs ScaNN

Exact nearest neighbor search requires comparing the query vector against all 1 billion items ($O(N \cdot d)$ complexity), which takes seconds. Production systems use **Approximate Nearest Neighbors (ANN)** to trade $< 2\%$ recall accuracy for a 1,000x speedup.

| Algorithm | Mechanism | Memory Footprint | Query Latency | Best Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **HNSW (Hierarchical Navigable Small World)** | Multi-layer proximity graph with skip-list navigation | High (Stores graph edges in RAM) | Ultra-fast ($< 2\text{ ms}$) | High-throughput, low-latency in-memory vector search |
| **IVFPQ (Inverted File with Product Quantization)** | Partitions space into Voronoi cells + compresses vectors into byte codes | Extremely low (8x to 16x compression) | Fast ($5 - 10\text{ ms}$) | Massive catalogs (100M+ vectors) constrained by RAM |
| **Google ScaNN** | Anisotropic vector quantization penalized along parallel direction | Low to Moderate | Ultra-fast ($< 3\text{ ms}$) | Maximum cosine similarity and inner product recall |

---

## 4. Stage 2: Heavy Ranking Models (DLRM & MMoE)

While the Two-Tower model generates candidates using decoupled user and item vectors, the **Ranking Stage** processes rich cross-features between the user and specific items.

### Multi-Gate Mixture-of-Experts (MMoE) for Multi-Objective Ranking
In platforms like YouTube or Instagram, recommendations must optimize for multiple competing objectives:
* Objective 1: Click-Through Rate ($P(\text{Click})$)
* Objective 2: Engagement Duration ($E[\text{Watch Time}]$)
* Objective 3: Explicit Feedback ($P(\text{Like})$ or $P(\text{Share})$)

Training separate models for each objective wastes infrastructure. **MMoE** shares intermediate representation experts across multiple task-specific prediction heads.

```
                   Input Dense & Sparse Features
                                 |
         +-----------------------+-----------------------+
         |                       |                       |
         v                       v                       v
     [Expert 1]              [Expert 2]              [Expert 3]
         |                       |                       |
         +-----------+-----------+-----------+-----------+
                     |                       |
                     v                       v
               [Gate Task A]           [Gate Task B]
                     |                       |
                     v                       v
                 [Head A]                [Head B]
               P(Watch Time)              P(Share)
```

Each task $k$ has its own gating router $g^k(x) = \text{Softmax}(x W_g^k)$, allowing task heads to select which expert subnetworks to leverage dynamically.

### Final Scoring Formula:
The final ranking score combines the multi-task predictions into a unified business utility function:

$$\text{Final Score} = w_1 \cdot P(\text{Click}) + w_2 \cdot E[\text{Watch Time}] + w_3 \cdot P(\text{Share}) - w_4 \cdot P(\text{Dislike})$$

---

## 5. Stage 3: Re-ranking and Diversity (MMR)

If the ranking model simply returns the top 20 highest-scoring items, the user feed often becomes monotonous (e.g. 20 consecutive videos about the same topic).

### Maximal Marginal Relevance (MMR)
MMR iteratively selects items that balance high relevance to the user with high novelty relative to items already selected:

$$\text{MMR} = \arg\max_{D_i \in R \setminus S} \left[ \lambda \cdot \text{Sim}_1(D_i, Q) - (1 - \lambda) \max_{D_j \in S} \text{Sim}_2(D_i, D_j) \right]$$

Where:
* $R$: Candidate set from the ranking model.
* $S$: Set of already selected items in the user feed.
* $\lambda \in [0, 1]$: Diversity tradeoff parameter ($\lambda = 0.7$ gives high relevance with controlled diversity).
* $\text{Sim}_1(D_i, Q)$: Predicted relevance score for candidate item $D_i$.
* $\text{Sim}_2(D_i, D_j)$: Cosine similarity between candidate item $D_i$ and already selected item $D_j$.

---

## 6. Real-Time Latency Budget Breakdown (50 ms Target)

In a Staff Engineer system design interview, you must articulate the end-to-end latency budget breakdown:

| Step | Operation | SLA Budget | Technologies Used |
| :--- | :--- | :--- | :--- |
| **1. Gateway & Auth** | Terminate TLS, authenticate user session, route request | $3\text{ ms}$ | Envoy / API Gateway |
| **2. Feature Retrieval** | Fetch real-time user history & context from Online Store | $5\text{ ms}$ | Redis Cluster / DynamoDB |
| **3. Candidate Retrieval** | Run User Tower MLP + HNSW vector search over 1B items | $12\text{ ms}$ | Triton Inference Server + ScaNN |
| **4. Feature Joining** | Batch join item features for the 1,000 retrieved candidates | $5\text{ ms}$ | In-memory distributed cache |
| **5. Heavy Scoring** | Execute MMoE ranking model over 1,000 items on GPU | $15\text{ ms}$ | TensorRT / ONNX Runtime |
| **6. Re-ranking & Dedupe**| Run MMR diversity, ad injection, author fatigue rules | $5\text{ ms}$ | C++ / Go Microservice |
| **7. Serialization** | Serialize JSON response and stream over network to client | $5\text{ ms}$ | Protobuf / gRPC |
| **Total** | End-to-End Latency | **$50\text{ ms}$** | |

---

## Summary Checklist for Staff RecSys Interviews
* [x] Three-stage funnel (Retrieval -> Heavy Ranking -> Re-ranking) is mandatory for large-scale catalogs.
* [x] Two-Tower models decouple item embedding indexing (offline) from user query generation (online).
* [x] HNSW and ScaNN enable sub-10ms Approximate Nearest Neighbor search over billions of vectors.
* [x] MMoE handles multi-task optimization (clicks, watch time, shares) with shared expert representations.
* [x] Maximal Marginal Relevance (MMR) balances user relevance with feed diversity.
