# 🚨 System Design Failure Modes & Fixes – Master Cheat Sheet

> **Quick Reference:** The 39 core distributed systems concepts grouped by the problem they solve—with real production examples and exact interview fixes.

---

## 🏆 The Top 11 Concepts Interviewers Ask About Most
1. **Thundering Herd & Jitter** (staggering synchronized spikes)
2. **Retries with Exponential Backoff** (preventing retry storms)
3. **Idempotency Keys** (safe retries without double-charging)
4. **Circuit Breakers** (failing fast when a dependency is down)
5. **Cache-Aside & Invalidation** (the default caching pattern)
6. **Hot Keys / Celebrity Problem** (key replication & write sharding)
7. **Sharding with Consistent Hashing** (scaling storage without reshuffling keys)
8. **CAP Theorem & Eventual Consistency** (CP for money, AP for feeds)
9. **Leader Election, Leases & Fencing Tokens** (preventing zombie double-writes)
10. **Transactional Outbox Pattern** (solving the DB + Queue dual-write trap)
11. **Rate Limiting** (Token Bucket / Leaky Bucket at the edge)

---

## 1. 🌊 Too Much Traffic at Once

| Concept | What Goes Wrong | Usual Fix | Real Production Example |
| :--- | :--- | :--- | :--- |
| **Thundering Herd** | Many clients/cron jobs wake up at the exact same moment and hit one service together. | Add **random jitter** (`+ rand(0, 300s)`) to schedules and retries. | 6-hour sync jobs for 500k users who all signed up during a 9 AM launch. |
| **Cache Stampede (Dogpile)** | A popular cache key expires and 10,000 requests rush to the DB simultaneously to rebuild it. | **Mutex lock / Singleflight** (one request rebuilds while others wait) or refresh before expiry. | Homepage leaderboard cache expires at midnight; 10k users hit SQL at `00:00:01`. |
| **Cache Avalanche** | Thousands of cache entries expire at the same second because they were set with identical TTLs. | **Stagger TTLs with random jitter** (`TTL = 3600s + rand(0, 300s)`). | Cache warm-up script loads 1M product keys at noon with a flat 2-hour TTL. |
| **Retry Storm** | A service slows down, every caller immediately retries, and the retries multiply the load until it dies. | **Exponential backoff + jitter + max retry cap** + circuit breaker. | Payment service slows down (`408`/`429`); blind client retries multiply traffic 4x. |
| **Hot Key / Hot Partition** | One key gets 90% of traffic ("celebrity problem"), melting the single shard holding it. | Replicate hot key across suffix keys (`key#1..10`) for reads; shard counters for writes, or local cache. | Justin Bieber posts a tweet; Shard #4 melts while other shards sit idle. |
| **Rate Limiting** | One runaway client or scraper uses up all server capacity. | **Token Bucket** or **Sliding Window** per user/IP at API Gateway. | Buggy customer script calls `/export` in an infinite `while(true)` loop. |
| **Backpressure** | Fast producer pumps data faster than slow consumer can handle, exhausting memory (`OOM`). | **Bounded queue** + consumer signals producer to slow down (`429` / block). | Log forwarders sending 50k/s into an indexer that can only write 10k/s. |
| **Load Shedding** | When overloaded, server tries to do everything and *all* requests time out. | **Drop excess work early** (`HTTP 429` / `503`) so in-flight work succeeds. | Rejecting new requests with `409 TURN_IN_FLIGHT` or `503` when CPU > 90%. |

---

## 2. 🔥 Failures Spreading (Fault Isolation)

| Concept | What Goes Wrong | Usual Fix | Real Production Example |
| :--- | :--- | :--- | :--- |
| **Cascading Failure** | One slow dependency makes its callers slow, then their callers, until the whole platform is down. | Combine **Timeouts + Circuit Breakers + Bulkheads**. | Stuck analytics DB hangs all web worker threads so even `/login` dies. |
| **Timeouts & Deadlines** | A call that never returns ties up threads and sockets forever. | Set timeouts on **every** call and pass remaining **deadline budget** downstream. | Postgres `statement_timeout` + passing a 75s run deadline across services. |
| **Circuit Breaker** | You keep calling a service that is already dead, wasting resources. | After $N$ failures, **trip Open** (fail instantly for 30s), then test 1 request (**Half-Open**). | Tripping open on a dead third-party enrichment API instead of waiting 10s per call. |
| **Bulkhead** | One slow dependency uses up all shared threads/connections. | Give each dependency its **own isolated thread/connection pool**. | Isolating slow PDF export threads so they can't starve fast API endpoints. |
| **Graceful Degradation** | One minor component fails and the entire page returns a 500 error. | Serve **stale cached data** or hide the failed widget. | Showing the last known good Dashboard snapshot when live refresh fails. |
| **Single Point of Failure (SPOF)** | One machine dies and the whole system stops working. | **Redundancy:** run multiple replicas across Availability Zones. | Running multiple orchestrator replicas behind Active-Passive load balancers. |

---

## 3. 🎯 Doing Things Exactly Once

| Concept | What Goes Wrong | Usual Fix | Real Production Example |
| :--- | :--- | :--- | :--- |
| **Idempotency** | A retried request gets applied twice (double charge, duplicate database row). | Client sends an **Idempotency Key** (`UUID`); server stores and replays the first result. | Replaying the saved result when a client retries after a network blip. |
| **Delivery Guarantees** | At-most-once loses messages; at-least-once duplicates them; true exactly-once is hard. | **At-least-once delivery + Idempotent consumer**. | Kafka consumer retrying a batch safely using `UPSERT` by message ID. |
| **Dual Write** | You save to the DB, then crash before publishing to Kafka—now DB and queue disagree. | **Transactional Outbox:** write event to an `outbox` table in the *same* DB transaction, then relay to queue. | Writing to `reports` and `report_outbox` in one SQL `COMMIT`. |
| **Saga Pattern** | One business action spans multiple services with no shared SQL transaction. | Chain of local transactions, each with a **compensating ("undo") step** on failure. | Publishing across Report and Dashboard services; rolling back Report if Dashboard fails. |
| **Two-Phase Commit (2PC)** | Coordinator locks all participants until everyone votes "ready" then commits. | Rarely used at scale—slow and **blocks everyone** if coordinator crashes. | Legacy cross-bank wire transfer coordinators. |
| **Poison Message** | One malformed message crashes the consumer on every single retry loop. | Track retry count; after $N$ tries, move to a **Dead-Letter Queue (DLQ)**. | Corrupted JSON payload moved to DLQ after 3 consumer crashes. |

---

## 4. 🤝 Coordinating Several Machines

| Concept | What Goes Wrong | Usual Fix | Real Production Example |
| :--- | :--- | :--- | :--- |
| **Leader Election** | Several replicas all try to run the same singleton background job at once. | Elect one leader via **Raft / ZooKeeper / etcd** or DB advisory lock. | Only 1 of 3 cron pods runs the midnight billing sweep. |
| **Lease** | A machine grabs a lock and then crashes—holding the lock forever. | **Time-bounded lock (TTL)** that expires unless renewed via heartbeats. | Curation run lease that expires after 60s if the worker pod dies. |
| **Fencing Token** | A paused machine (GC pause) wakes up after its lease expired and overwrites newer work. | Hand out a **monotonically increasing number** (`fence_generation_num`) with each lease; storage rejects older tokens. | Rejecting writes from a zombie worker carrying `token=4` after `token=5` was issued. |
| **Split Brain** | Network split leaves two sides that both think they are the sole leader. | Require a **Quorum (majority: $\lfloor N/2 \rfloor + 1$)** before acting. | 5-node cluster splits 3 vs 2; only the 3-node side can accept writes. |
| **Consensus** | Distributed machines need to agree on one value even when some crash. | **Raft** or **Paxos** consensus protocols. | `etcd` storing Kubernetes cluster state across 3 control-plane nodes. |
| **Clock Skew** | Server wall-clocks drift out of sync, so "Latest Timestamp Wins" picks the wrong write. | Use **monotonic version numbers** or **logical clocks**, never raw wall-clock time. | Two servers with 150ms NTP drift editing the same record. |

---

## 5. 🔒 Data Consistency & Concurrency

| Concept | What It Means | Usual Fix or Choice | Real Production Example |
| :--- | :--- | :--- | :--- |
| **CAP Theorem** | During a network partition, choose between **Consistency (CP)** and **Availability (AP)**. | Pick per feature: **CP** for payments/inventory, **AP** for feeds/likes. | Rejecting ATM withdrawals if bank ledger partition is unreachable (CP). |
| **Eventual Consistency** | Replicas agree after a short delay, so reads may be temporarily stale. | Great for high-read feeds, view counters, and timelines. | YouTube video view count updating a few seconds later across regions. |
| **Replication Lag / Read-Your-Writes** | You save an edit, refresh the page, and your edit appears gone because your read hit a lagging replica. | Route **that user's reads to the Primary** for a few seconds after they write. | Pinning user to Primary DB for 5s after updating their profile settings. |
| **Lost Update** | Two users edit the same record at once; the second save silently wipes out the first. | **Optimistic Concurrency Control (OCC):** send `version` / `ETag`; reject save with `412 Precondition Failed` if version changed. | Checking `WHERE id = 1 AND version = 4` before saving dashboard edits. |
| **Pessimistic Locking** | Lock the row before editing (`SELECT ... FOR UPDATE`) so nobody else can touch it. | Safe for high contention, but slower and risks **deadlocks**. | Locking an owner row while mutating exclusive state. |
| **Sharding** | One database server cannot hold all data or write throughput. | Partition data horizontally across shards by a **shard key** (e.g., `user_id`). | Splitting 50 TB of user messages across 32 Postgres shards. |
| **Consistent Hashing** | Adding/removing a server in `hash(key) % N` reshuffles 99% of keys. | Map nodes and keys onto a **hash ring** so only $1/N$ of keys move. | Adding a new Redis cache node without invalidating the entire cluster. |

---

## 6. ⚡ Caching Quick Reference

| Concept | What It Means & How to Use It |
| :--- | :--- |
| **Cache-Aside** | App checks cache first; on miss, reads DB and populates cache. *(Default pattern for 90% of read workloads).* |
| **Write-Through / Write-Back** | **Write-Through:** Write to cache and DB synchronously (consistent, slower). **Write-Back:** Write to cache first, flush to DB asynchronously in batches (blazing fast, risks data loss on crash). |
| **Cache Invalidation** | Deleting or updating cached entries when the underlying DB row changes (hardest edge cases in race conditions). |
| **Cache Penetration** | Queries for non-existent IDs (`id = -999`) always miss cache and hit DB. **Fix:** Cache `null` with a short TTL or check a **Bloom Filter** first. |
| **Eviction (LRU)** | When cache RAM is full, evict the **Least Recently Used** entry to make room for new hot data. |

---

## 7. 🏎️ Speed & Latency

| Concept | What Goes Wrong | Usual Fix |
| :--- | :--- | :--- |
| **Tail Latency ($p99$)** | Average latency looks fast (`30ms`), but the slowest 1% (`6s`) ruins user experience. | Measure and optimize **$p95$ / $p99$**, never the average. |
| **Fan-Out Amplification** | One request calls 100 backends in parallel; the single slowest server sets total response time. | **Hedged Requests:** if a server is slow past $p95$, fire a duplicate request to a replica and take whichever finishes first. |
| **N+1 Queries** | Fetching a list of $N$ items (1 query), then running 1 query per item in a loop ($N$ queries). | **Batch lookup (`WHERE id IN (...)`)** or SQL `JOIN`. |
| **Head-of-Line Blocking** | One slow item at the front of a queue holds up 500 fast items behind it. | Split into **parallel queues** (fast lane vs heavy lane) or use `HTTP/2` / `HTTP/3` multiplexing. |
| **Connection Pooling** | Opening a new TCP + TLS + DB connection per request takes ~30ms and exhausts DB RAM. | Reuse a warm pool of connections (e.g., **PgBouncer / RDS Proxy**, 10 connections per pod). |
| **Noisy Neighbor** | One tenant's heavy query hogs shared CPU/Disk and slows down every other customer on that host. | **Per-tenant rate quotas**, fair queuing, and resource isolation. |

---

## 8. 🛡️ Security in Design Rounds

| Concept | What It Means | Real Production Example |
| :--- | :--- | :--- |
| **Confused Deputy** | A trusted service gets tricked into using its own admin permissions on behalf of an unauthorized caller. | Orchestrator accidentally falling back to its internal `service_token` when called by an anonymous user. |
| **Least Privilege** | Give every service token or IAM role **only** the minimum permissions required to do its job. | Giving a reporting service a read-only (`SELECT`) token instead of full read/write DB access. |
| **Defense in Depth** | Enforce security at multiple independent layers so one misconfiguration isn't fatal. | API Gateway validates the JWT, and the downstream microservice/tool verifies permissions again. |
