# MASTER PROMPT: Big Tech AI/ML/CV/GenAI Interview Preparation Platform (Next.js)

You are tasked with building a production-grade, highly visual, dynamic Next.js web platform tailored specifically for cracking Staff and Senior (L5/L6) AI, Machine Learning, Computer Vision, and Generative AI interviews at Big Tech (Google, Meta, Apple, Amazon, Microsoft, Uber, OpenAI, Anthropic, Databricks).

The existing codebase contains heavy text-based markdown files. The user finds these excessively wordy and lacking visual intuition ("TOO WORDY LESS DIAGRAMS URGH").
Your mission is to build a modern, interactive Next.js application that flips this paradigm: **Every single topic MUST start with a research-paper grade architecture diagram first**, followed by crisp mathematical formulas, tensor shape transformations, and interview-critical trade-offs.

---

## 1. Core Operating Principles & Writing Style

1. **Activate the Humanizer and Gen Z Writer Skills:**
   * You MUST invoke and adhere to the `humanizer` and `genz-writer` skills on every piece of content you write.
   * **Absolute Zero AI Slop:** No "In today's fast-paced world", no "It's not just X, it's Y", no fake-profound one-line closers ("That is the real win", "Let that sink in"), no dramatic staging, no bullet padding.
   * Keep explanations raw, plain, technical, and direct. Write like a Principal Engineer coaching a Senior peer over a whiteboard.
2. **Absolute Zero Em-Dashes and En-Dashes:**
   * Never use em-dashes (Unicode U+2014) or en-dashes (Unicode U+2013) anywhere in code, markdown, comments, or UI text. Use hyphens `-`, colons `:`, or parentheses `()`.
3. **Diagram-First Rule (Research Paper Standard):**
   * Just like premier papers (Vaswani 2017, Dosovitskiy 2020 ViT, He 2015 ResNet, Kingma 2013 VAE), **every single concept MUST begin with a clear, self-explanatory architecture diagram** (ASCII diagram + interactive SVG/Mermaid block).
   * A candidate looking at the diagram for 10 seconds must immediately understand:
     - What tensors enter the block and their exact shapes: e.g. `(B, S, D)` or `(B, C, H, W)`.
     - What internal operations occur (e.g. Projections, Split Heads, MatMul, Softmax, Masking, Residual addition).
     - What tensors exit the block.
4. **Anti-Wordiness & High Information Density:**
   * Replace 5 paragraphs of prose with:
     - 1 clear Architecture Diagram.
     - 1 compact LaTeX Mathematical Formulation box.
     - 1 Tensor Flow Step-by-Step Trace Table.
     - 1 Bulleted "Big Tech Interview Traps & Edge Cases" list.

---

## 2. Comprehensive Curriculum Breakdown

The Next.js application must organize and present all 4 core tracks with zero gaps:

### Track 1: Deep Learning Foundations & Modern LLMs
1. **Transformer Architectures:**
   * Full comparative architecture diagrams: Encoder-Only (BERT bidirectional) vs Decoder-Only (GPT/Llama causal triangular mask) vs Encoder-Decoder (T5 cross-attention).
   * Exact Query, Key, Value linear projections, Scaled Dot-Product Attention derivation, and mathematical proof of why dividing by $\sqrt{d_k}$ prevents softmax gradient saturation.
   * Multi-Head Attention (MHA) vs Multi-Query Attention (MQA) vs Grouped-Query Attention (GQA) tensor layouts.
2. **KV Cache Mechanics & Memory Bottlenecks:**
   * Visual diagrams of the Prefill Phase (compute-bound GEMM) vs Decode Phase (memory bandwidth-bound GEMV).
   * Physical memory fragmentation in naive serving vs PagedAttention (vLLM logical-to-physical block tables).
   * Exact KV cache VRAM sizing formula: $2 \times B \times L \times n_{\text{layers}} \times n_{\text{kv\_heads}} \times d_{\text{head}} \times P$.
3. **Rotary Position Embeddings (RoPE):**
   * Visual diagram of 2D complex plane rotations: $\begin{pmatrix} \cos(m\theta) & -\sin(m\theta) \\ \sin(m\theta) & \cos(m\theta) \end{pmatrix}$.
   * Proof of relative distance invariance: $\langle R_m q, R_n k \rangle = q^T R_{n-m} k$.
   * Long-context scaling mechanics: YaRN, NTK-aware interpolation.
4. **Normalization Layers:**
   * Side-by-side visual 3D tensor axis diagram: Batch Normalization $(N, C, H, W)$ vs Layer Normalization $(C, H, W)$ vs Instance Normalization $(H, W)$ vs Group Normalization.
   * RMSNorm: Why eliminating the mean-centering step $\mu$ saves 7% compute per layer without degrading stability.
5. **Vision Transformer (ViT):**
   * Step-by-step pipeline diagram: Image $(H, W, C) \to$ Patch Extraction $P \times P \to$ Linear Projection of Flattened Patches $\to$ Concatenate `[CLS]` Token $\to$ Add 1D Positional Embeddings $\to$ Transformer Encoder $\to$ MLP Classification Head.
   * Inductive bias comparison: CNNs (translation equivariance, locality) vs ViTs (global receptive field, high data dependency).
6. **Multimodal LLMs (Vision, Audio, Video):**
   * Architectural connectors: Linear Projection (LLaVA), Cross-Attention Perceiver Resampler (Flamingo), Q-Former (BLIP-2).
   * How continuous representations from frozen encoders (CLIP ViT, Whisper) map into the LLM token embedding space.
7. **Recurrent Networks: LSTM & RNN:**
   * Vanishing gradient problem in vanilla RNNs due to repeated multiplication by $W_{hh}^T$.
   * Detailed LSTM Cell Architecture Diagram: Forget Gate ($f_t$), Input Gate ($i_t$), Candidate State ($\tilde{C}_t$), Output Gate ($o_t$), and the Cell State Highway ($C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$).
8. **Subword Tokenization Algorithms:**
   * Byte-Pair Encoding (BPE: frequency-based pair merging, GPT-4/Llama).
   * WordPiece (likelihood-based merging, BERT).
   * Unigram (probabilistic subword pruning, SentencePiece).
   * Byte-level fallback preventing out-of-vocabulary (`<UNK>`) tokens.
9. **Embedding Model Training:**
   * Bi-encoder architecture with Siamese networks.
   * Contrastive Learning and InfoNCE loss formulation.
   * Batch construction: In-batch negatives, hard negative mining (BM25 top negatives + cross-encoder false positive mining).

---

### Track 2: Generative AI, RAG & Agentic Systems
1. **RAG Architectures & Taxonomy:**
   * Visual pipeline: Naive RAG vs Advanced RAG (Pre-retrieval query expansion / HyDE, Post-retrieval cross-encoder reranking) vs Modular RAG.
   * Self-RAG (reflection tokens: retrieve, critique, generate) and Corrective RAG (CRAG: web-search fallback on low confidence).
2. **Knowledge Graphs & GraphRAG:**
   * Knowledge Graph primitives: Entities, Relations, Subject-Predicate-Object Triples $(S, P, O)$.
   * Hybrid Vector + Graph Search: Using graph traversal (Cypher / Neo4j) for global community summarization and multi-hop reasoning where vector cosine similarity fails.
3. **Agentic AI & Cognitive Architectures:**
   * ReAct (Reason + Act) loop diagram: User Goal $\to$ Thought $\to$ Action (Tool Call) $\to$ Environment Observation $\to$ Reflection.
   * Plan-and-Solve vs Multi-Agent DAG Orchestration (LangGraph / AutoGen supervisor-worker patterns).
   * Memory hierarchies: Short-term scratchpad, working memory, and long-term vector/episodic memory.
4. **Model Context Protocol (MCP):**
   * What MCP is: The open standard connecting AI models to external tools, datasources, and local environments securely.
   * Core architectural components diagram:
     - MCP Host (LLM client / IDE / Agent runtime).
     - MCP Client (maintains 1:1 connection with an MCP server).
     - MCP Server (exposes Tools, Resources, and Prompts).
     - Primitives: Resources (data/files), Prompts (pre-built prompt templates), Tools (executable functions with JSON schemas).
     - Transports: Local stdio (pipes) vs Remote SSE (Server-Sent Events over HTTP).
5. **AI & Agent Communication Protocols:**
   * JSON-RPC 2.0 message framing (requests, responses, notifications, error codes).
   * Server-Sent Events (SSE) for unidirectional streaming token responses.
   * WebSockets for full-duplex bi-directional multi-agent event streaming.
   * Agent-to-Agent (A2A) protocol designs and capability negotiation.

---

### Track 3: Computer Vision & Generative Models
1. **Classical Image Processing Fundamentals:**
   * 2D Discrete Convolution mechanics, stride, padding (valid vs same).
   * Kernel filters: Gaussian smoothing, Laplacian, Sobel gradient operator for edge detection, Canny edge detection pipeline (noise reduction, gradient calculation, non-maximum suppression, hysteresis thresholding).
2. **Object Detection:**
   * Two-Stage Detectors: Faster R-CNN (Backbone, Region Proposal Network - RPN, Anchor Boxes, RoIPooling / RoIAlign, Classification + Bounding Box Regression Heads).
   * Single-Stage Detectors: YOLO family (grid cell prediction, anchor-free YOLOv8/v10), SSD.
   * Transformer-based Detection: DETR (CNN backbone, Transformer Encoder-Decoder, Bipartite matching with Hungarian Loss).
3. **Semantic Segmentation:**
   * Fully Convolutional Networks (FCN).
   * U-Net Architecture Diagram: Contracting path (encoder), bottleneck, expansive path (decoder), and horizontal Skip Connections preserving spatial resolution.
   * DeepLabv3+: Atrous (Dilated) Convolutions and Atrous Spatial Pyramid Pooling (ASPP).
4. **Instance Segmentation:**
   * Mask R-CNN: Adding a third parallel branch for pixel-level binary mask prediction.
   * RoIAlign: Replacing RoIPooling with bilinear interpolation to solve spatial quantization misalignment.
5. **Human Pose Estimation:**
   * Top-down vs Bottom-up keypoint estimation.
   * Heatmap regression using Gaussian targets around joints.
   * HRNet (High-Resolution Network) maintaining multi-resolution representations throughout the network.
6. **Autoencoders & Variational Autoencoders (VAE):**
   * Standard Autoencoder bottleneck and why its latent space lacks smoothness.
   * VAE Architecture Diagram: Encoder outputs mean $\mu$ and log-variance $\log\sigma^2$.
   * The Reparameterization Trick: $z = \mu + \sigma \odot \epsilon$ where $\epsilon \sim \mathcal{N}(0, I)$, allowing backpropagation.
   * Evidence Lower Bound (ELBO) Loss: Reconstruction Loss + $\text{KL}(\mathcal{N}(\mu, \sigma^2) \parallel \mathcal{N}(0, I))$.
7. **Generative Adversarial Networks (GANs):**
   * Minimax objective: $\min_G \max_D V(D, G)$.
   * Mode collapse and vanishing gradients with standard cross-entropy.
   * Wasserstein GAN (WGAN) with Earth Mover's Distance and gradient penalty (WGAN-GP).
   * Architectural comparison: GANs vs Diffusion Models (forward noise addition vs reverse denoising score matching).

---

### Track 4: Classical Machine Learning & Applied Statistics
1. **Naive Bayes Classifiers:**
   * Bayes' Theorem derivation and the fundamental "naive" conditional independence assumption: $P(X \mid Y) = \prod_{i=1}^d P(x_i \mid Y)$.
   * Gaussian Naive Bayes (continuous features) vs Multinomial Naive Bayes (text token counts).
   * Laplace Smoothing ($+\alpha$) preventing zero probability annihilation.
2. **Preprocessing, Statistical Modeling & Hypothesis Testing:**
   * Correlation: Pearson (linear) vs Spearman rank (monotonic non-linear).
   * Feature scaling: Standardization ($z$-score) vs Min-Max Normalization vs Robust Scaler.
   * Hypothesis Testing: Null vs Alternative hypothesis, Type I ($\alpha$) vs Type II ($\beta$) errors, $p$-value interpretation.
   * Statistical tests: Student's $t$-test (two means), ANOVA (three or more means), Chi-Square $\chi^2$ test of independence (categorical data).
3. **Support Vector Machines (SVM):**
   * Optimal margin hyperplane and derivation of the margin width $\frac{2}{\|w\|}$.
   * Primal vs Dual Lagrangian formulation using KKT conditions.
   * The Kernel Trick: Mercer's Theorem, Linear, Polynomial, and Radial Basis Function (RBF) kernels: $K(x, x') = \exp(-\gamma \|x - x'\|^2)$.
4. **XGBoost & Gradient Boosted Decision Trees:**
   * Gradient Boosting as gradient descent in functional space.
   * XGBoost optimizations: Second-order Taylor series expansion of the objective function (using gradients $g_i$ and Hessians $h_i$).
   * Exact formula for optimal leaf weights and split gain: $\text{Gain} = \frac{1}{2}\left[\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda}\right] - \gamma$.
5. **Unsupervised Learning: K-Means & PCA:**
   * K-Means: Lloyd's algorithm (Assignment step $\to$ Update step), convergence proof, Elbow method, and Silhouette coefficient.
   * K-Means++ initialization preventing poor local minima.
   * Principal Component Analysis (PCA): Covariance matrix eigendecomposition vs Singular Value Decomposition (SVD), explained variance ratio.
6. **K-Nearest Neighbors (KNN):**
   * Distance metrics: Euclidean ($L_2$), Manhattan ($L_1$), Cosine distance.
   * Curse of dimensionality: Volume of hypercube vs hypersphere, distances collapsing to equal values in high dimensions.
   * Indexing for fast search: KD-Trees, Ball Trees, and inverted indexing.
7. **Decision Trees & Random Forest:**
   * Splitting criteria: Gini Impurity ($1 - \sum p_i^2$) vs Shannon Entropy ($-\sum p_i \log_2 p_i$).
   * Bias-Variance tradeoff: Single deep tree has low bias, high variance.
   * Random Forest: Bootstrap Aggregating (Bagging) + Random Feature Subsampling ($\sqrt{p}$ features per split), Out-Of-Bag (OOB) error estimation.

---

## 3. Standardized Topic Layout Template

To maintain consistency, **every single topic page in the Next.js app MUST follow this uniform 6-block template**:

```markdown
# [Topic Title]

> **Track:** [Deep Learning / GenAI / Computer Vision / Classical ML]  
> **Level:** [Senior (L5) / Staff (L6)]  
> **Big Tech Target:** [e.g. Google DeepMind, Meta FAIR/GenAI, Apple AIML, OpenAI]

---

## 1. Visual Architecture & Mental Model
[ASCII Architecture Diagram or Interactive SVG/Mermaid Component]
(Must show inputs, tensor shapes, internal operations, and outputs)

---

## 2. 10-Second High-Yield TL;DR
* **What it is:** (1-2 sentences maximum, zero fluff)
* **Why it exists:** (What prior limitation it solved)
* **Big Tech interview context:** (Exactly how interviewers test this concept)

---

## 3. Mathematical Formalism
* Governing equations with KaTeX LaTeX notation.
* Explicit tensor shapes at every transition: e.g. Input $X \in \mathbb{R}^{B \times S \times D}$.
* Loss functions and optimization dynamics.

---

## 4. Step-by-Step Execution Trace / Tensor Flow
| Step | Operation | Input Shape | Transformation | Output Shape | Memory / Hardware Implication |
| :--- | :--- | :--- | :--- | :--- | :--- |

---

## 5. Staff-Level Interview Traps & Failure Modes
* **Trap 1:** (e.g. Forgetting to divide by $\sqrt{d_k}$ causing vanishing gradients)
* **Trap 2:** (e.g. Data leakage in point-in-time joins)
* **Trap 3:** (e.g. Numerical instability during FP16 softmax or log-sum-exp)
* **Production Trade-off:** (Latency vs Memory vs Accuracy)

---

## 6. Minimal Production PyTorch / Python Implementation
[Clean, commented, runnable code block implementing the core mathematical equation]
```

---

## 4. Next.js Application Architecture

Build the web application using modern Next.js best practices:

1. **Framework:** Next.js 14 or 15 (App Router with Server Components for content delivery and Client Components for interactivity).
2. **Styling:** Tailwind CSS with dark mode as default (Tokyo Night / Linear dark palette) and high-contrast light mode toggle.
3. **Icons & UI:** Lucide React for modern, crisp icons.
4. **Math Rendering:** KaTeX integration via `rehype-katex` and `remark-math` for sub-millisecond mathematical typography.
5. **Interactive Architecture Components:**
   * `KVVisualizer.tsx`: Interactive widget demonstrating prompt prefill vs token decode and KV cache memory accumulation.
   * `RoPEVisualizer.tsx`: 2D rotation of query and key vectors showing angle subtraction $(m - n)$.
   * `UNetVisualizer.tsx`: Expandable skip-connection diagram showing spatial feature concatenation.
   * `NormVisualizer.tsx`: 3D tensor slicing showing the exact axes reduced by BatchNorm vs LayerNorm vs RMSNorm.
6. **Interview Mode Toggle (Grill-Me Mode):**
   * A global switch in the top navigation:
     - **Study Mode:** Displays the full guide with diagrams, formulas, and code.
     - **Interview Mode:** Collapses mathematical proofs, failure modes, and code behind click-to-reveal spoiler cards to test active recall before looking at the answers.
7. **Instant Search (Cmd+K):**
   * Global modal search indexing all topics, equations, diagrams, and failure modes using Fuse.js.

---

## 5. Execution Steps for the Implementation Agent

1. **Initialize the Next.js Workspace:**
   * Create the Next.js App Router structure in the designated frontend folder.
   * Configure Tailwind CSS, typography, KaTeX CSS, and Lucide icons.
2. **Build Reusable Layout & Nav:**
   * Top navigation bar with Track selector, Theme switcher, Interview Mode toggle, and Cmd+K search.
   * Collapsible sidebar grouping topics by Track and sub-specialty.
3. **Implement Visual Architecture Components:**
   * Build the reusable diagram and visual tensor components in `components/diagrams/`.
4. **Draft the Topic Content:**
   * For every topic across Track 1, 2, 3, and 4, author the content strictly using the 6-block template.
   * Run the `humanizer` and `genz-writer` checks on every page to ensure zero em-dashes, zero en-dashes, and zero AI filler.
5. **Build, Verify, and Test:**
   * Verify all KaTeX equations render cleanly without syntax errors.
   * Verify all responsive layouts look sharp on desktop and mobile.
   * Ensure build passes with zero TypeScript or lint errors.
