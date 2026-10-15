# 🎯 The FAANG System Design 4-Step Interview Framework

> **Target:** 45-Minute Senior/Staff System Design Interview  
> **Philosophy:** System design is **not** a quiz; it is a collaborative technical design discussion. The interviewer wants to see how you handle ambiguity, drive architectural decisions, and evaluate trade-offs.

---

## ⏱️ The 45-Minute Time Allocation

```text
[ 0m - 5m ]   Step 1: Clarify Scope & Requirements (Functional & Non-Functional)
[ 5m - 10m ]  Step 2: Back-of-the-Envelope Math & Core API Design
[ 10m - 25m ] Step 3: High-Level Architecture Diagram (End-to-End Happy Path)
[ 25m - 40m ] Step 4: Deep Dives, Bottlenecks & Scale-Out Trade-offs
[ 40m - 45m ] Wrap-Up: Summary, Monitoring, Failure Scenarios
```

---

## 📋 Step 1: Scope & Clarify Requirements (5 Minutes)

Never start drawing boxes immediately. A candidate who jumps straight to drawing fails within 3 minutes because they solve the wrong problem.

### 1. Functional Requirements (2–3 Core Use Cases ONLY)
* Ask: *"What are the primary actions a user takes?"*
* Keep it to **2–3 critical features**. Out-of-scope features should be explicitly parked.
* *Example (TinyURL):*
  1. User inputs a long URL $\to$ receives a shortened URL.
  2. User visits shortened URL $\to$ redirected to original URL.
  3. (Out of scope for now: analytics, custom aliases).

### 2. Non-Functional Requirements (The "-ilities")
* **Scale:** How many Daily Active Users (DAU)? Read vs. Write heavy?
* **Latency:** Sub-100ms reads? Sub-500ms writes?
* **Availability vs. Consistency (CAP):** Highly Available (99.99% uptime, eventual consistency like Twitter) OR Strongly Consistent (financial transactions, seat reservations)?
* **Durability:** Can URLs expire? Data must never be lost.

---

## 🔢 Step 2: Back-of-the-Envelope Math & API Design (5 Minutes)

### 1. The Math Formula Template:
```text
Daily Active Users (DAU):           100 Million
Writes per user/day:                1 write  ──> 100M writes / day
Reads per user/day:                 10 reads ──> 1 Billion reads / day (10:1 Read-to-Write ratio)

Average Write QPS:                  100,000,000 / 86,400 ≈ 1,200 writes/sec
Peak Write QPS (2x - 3x):           ~3,000 writes/sec
Average Read QPS:                   1,000,000,000 / 86,400 ≈ 12,000 reads/sec
Peak Read QPS:                      ~30,000 reads/sec

Storage per Year:                   100M writes/day * 500 bytes * 365 ≈ 18.25 TB / year
Bandwidth (Inbound):                1,200 * 500 bytes ≈ 600 KB/s
Bandwidth (Outbound):               12,000 * 500 bytes ≈ 6 MB/s
```

### 2. Define 2 Core API Endpoints:
```http
POST /v1/urls
Request Body:  { "original_url": "https://example.com/very/long/path", "user_id": "u123" }
Response Body: { "short_url": "https://tiny.url/aB3x9", "expires_at": 1893456000 }

GET /{short_code}
Response:      HTTP 302 Found (or 301 Permanent Redirect)
Header:        Location: https://example.com/very/long/path
```
> [!TIP]
> **301 vs. 302 Redirect:**
> - `301 Moved Permanently`: Browser caches the redirect locally $\to$ zero server load, but analytics cannot track click counts.
> - `302 Found / 307 Temporary`: Browser always hits your server first $\to$ allows accurate click tracking, but increases server load.

---

## 🏛️ Step 3: High-Level Architecture (15 Minutes)

Draw the standard happy-path flow from left to right:

```text
[ Client ] ──> [ DNS ] ──> [ CDN ] ──> [ Load Balancer (L7) ]
                                                │
                                                ▼
                                     [ Stateless App Servers ]
                                         │              │
                           (Cache Hit)   │              │ (Cache Miss)
                                         ▼              ▼
                                   [ Redis Cache ]  [ Primary DB (SQL) ]
                                                        │
                                                        ▼ (Replication)
                                                 [ Read Replicas ]
```

1. **State your assumptions aloud:** *"I am making the application tier completely stateless so we can auto-scale horizontally based on CPU utilization."*
2. **Explain data flow:** Show how a request enters, checks cache, queries DB if needed, and writes asynchronously.

---

## 🔬 Step 4: Deep Dives & Bottlenecks (15 Minutes)

This is where candidates distinguish themselves between L4 (Mid-level) and L5/L6 (Senior/Staff).

Select **2–3 critical bottlenecks** to dive deep into:

### 1. Database Sharding & Partitioning
* When the database exceeds 1 TB or write throughput maxes out single-node IOPS:
* Partition by `hash(user_id)` or `hash(short_code)`.
* Explain **Consistent Hashing** with virtual nodes to prevent re-sharding hot spots.

### 2. Cache Invalidation & Stampede
* Cache-Aside strategy: Look in Redis $\to$ if miss, read DB $\to$ write to Redis with TTL.
* **Thundering Herd / Cache Stampede:** If a hot key expires, 10,000 concurrent requests hammer the DB simultaneously.
  * *Fix:* Mutex lock (single flight) or probabilistic early expiration (XFetch).

### 3. Single Points of Failure (SPOF)
* Redundant Load Balancers using Active-Passive VRRP floating IP.
* Multi-AZ database failover with automated leader election (Raft/Paxos).

---

## 🚨 5 Red Flags That Fail Candidates

1. ❌ **Silent Drawing:** Drawing boxes for 5 minutes without explaining your thought process.
2. ❌ **Over-Engineering Early:** Throwing Kafka, Cassandra, Kubernetes, and Spark at a system with 50 QPS.
3. ❌ **Ignoring Scale Constraints:** Designing a strongly-consistent multi-region relational database without addressing network latency or CAP theorem.
4. ❌ **Vague Tech Choices:** Saying "I will store this in NoSQL" without explaining *why* Document vs. Key-Value vs. Wide-Column.
5. ❌ **Defensive Reactions:** Fighting the interviewer when they introduce a constraint or failure scenario. Treat them as a peer brainstorming partner!
