# 🎨 Excalidraw Dry-Run #1: Production Architecture Foundations

> **Time Target:** 20–25 Minutes  
> **Tool:** Open [Excalidraw](https://excalidraw.com) or Miro on your second monitor or tablet.  
> **Rule:** No peeking at the cheat sheet during the first 15 minutes! Speak your decisions out loud.

---

## 🎯 The Prompt

> **"Design the core scalable web infrastructure for a modern photo-sharing application handling 50,000 active requests per second with 99.99% availability."**

---

## 📋 The 5 Stages to Draw on Your Canvas

### 1. The Edge Layer (Minutes 0–5)
- [ ] Draw **Client Devices** (Mobile iOS/Android + Web).
- [ ] Add **DNS (Anycast / Route 53)** resolving client traffic.
- [ ] Add **CDN (Cloudflare / CloudFront)** for caching static assets and image downloads.
- [ ] Add an **Edge Reverse Proxy / API Gateway** for SSL Termination, CORS checks, and Rate Limiting.

### 2. Traffic Distribution & Compute Layer (Minutes 5–10)
- [ ] Place an **Active-Passive Layer 7 Load Balancer** with health check probes (`/healthz`).
- [ ] Draw a fleet of **Stateless Application Servers** (e.g., Node.js / Go microservices) in an Auto-Scaling Group.
- [ ] Show how path-based routing separates traffic (e.g. `/api/auth` vs `/api/feed`).

### 3. Data & Storage Tier (Minutes 10–15)
- [ ] Add an **In-Memory Cache (Redis cluster)** for sub-millisecond session tokens and hot user profiles.
- [ ] Add a **Relational Primary Database (PostgreSQL)** for user accounts, credentials, and payment history (ACID).
- [ ] Add **2x Read Replicas** receiving asynchronous replication from the Primary.
- [ ] Add **Blob Storage (AWS S3)** for storing the raw original uploaded photos and thumbnails.

### 4. Asynchronous Processing Tier (Minutes 15–20)
- [ ] When a photo is uploaded, we must generate 3 thumbnail sizes without blocking the client.
- [ ] Add a **Message Queue (RabbitMQ / Apache Kafka)** to buffer photo processing tasks.
- [ ] Add **Background Worker Nodes** pulling jobs from the queue to resize images and upload to S3.

---

## 🧪 Self-Critique Grilling Questions (Ask Yourself Out Loud)

1. **What happens if Server #2 suddenly catches fire or crashes?**
   * *Answer:* LB health check fails $\to$ traffic immediately shifts to healthy servers $\to$ zero users notice because servers are stateless.
2. **What happens if the Primary Database goes down?**
   * *Answer:* Read replicas can still serve 90% of traffic (reads). A replica is elected as the new Primary within 15–30 seconds.
3. **Why didn't we store user sessions in server RAM?**
   * *Answer:* If Server #1 crashes, all logged-in users on that node would be forcibly logged out. Using a distributed Redis cluster decouples session state from compute.
4. **Why S3 for photos instead of saving binary blobs directly into PostgreSQL?**
   * *Answer:* Databases are optimized for structured indexing, not multi-megabyte binary blobs. Storing images in DB balloons disk size and ruins backup/cache efficiency. S3 offers 11 9s (99.999999999%) of durability.
