# System Design Failure Modes & Fixes Cheat Sheet

Quick reference for the 39 distributed systems failure modes that show up in system design interviews, grouped by what breaks and how to fix it.

## Top 11 High-Frequency Interview Concepts
1. **Thundering Herd & Jitter** (staggering synchronized spikes)
2. **Retries with Exponential Backoff** (preventing retry storms)
3. **Idempotency Keys** (safe retries without double-charging)
4. **Circuit Breakers** (failing fast when a dependency is down)
5. **Cache-Aside & Invalidation** (the default read caching pattern)
6. **Hot Keys / Celebrity Problem** (key replication & write sharding)
7. **Sharding with Consistent Hashing** (scaling storage without reshuffling all keys)
8. **CAP Theorem & Eventual Consistency** (CP for money/inventory, AP for feeds)
9. **Leader Election, Leases & Fencing Tokens** (preventing zombie double-writes)
10. **Transactional Outbox Pattern** (solving the DB + Queue dual-write bug)
11. **Rate Limiting** (Token Bucket / Sliding Window at the API Gateway)

### Decision rules:
* **1. Traffic spikes and retry storms:** Apply randomized jitter with exponential backoff and throttle abusive senders using Token Bucket rate limiting.
* **2. Cascading downstream degradation:** Protect callers from slow or unresponsive services by setting aggressive timeouts, tripping circuit breakers, and isolating thread pools with bulkheads.
* **3. Dual-writes and inconsistent transactions:** Enforce client-side idempotency keys for API operations and use the Transactional Outbox pattern with Change Data Capture (CDC) to publish database events reliably.
* **4. Hot partitions and split-brain zombies:** Replicate hot keys across salted suffixes, route traffic via consistent hashing, and issue monotonically increasing fencing tokens on leases to reject stale leader writes.


---

## 1. Traffic Spikes & Overload

| Concept | What Goes Wrong | Fix | Production Example |
| :--- | :--- | :--- | :--- |
| **Thundering Herd** | Thousands of clients or cron jobs wake up at the exact same second and hammer one service. | Add **random jitter** (`+ rand(0, 300s)`) to schedules and retry timers. | 500k users' 6-hour sync jobs all firing at 3:00:00 PM. |
| **Cache Stampede (Dogpile)** | A popular cache key expires and 10,000 requests rush to the database at once to recompute it. | **Singleflight / mutex lock** (one request rebuilds while others wait) or refresh before expiry. | Leaderboard cache key expires at midnight; 10k requests hit Postgres at `00:00:01`. |
| **Cache Avalanche** | Thousands of keys expire at the same second because they were loaded with the same TTL. | Add **random jitter to TTLs** (`TTL = 3600 + rand(0, 300)`). | Batch warmup script loads 1M product keys with a flat 1-hour TTL. |
| **Retry Storm** | A slow service triggers immediate retries from all callers, multiplying load until it crashes. | **Exponential backoff + jitter + max retry cap** + circuit breaker. | Payment service slows down; blind retries multiply traffic 4x. |
| **Hot Key / Hot Partition** | One key gets 90% of traffic ("celebrity problem"), overloading the single shard holding it. | Replicate key across salted suffixes (`key#1..10`) for reads; shard counters for writes. | Celebrity posts a link; Shard #4 melts while other shards sit idle. |
| **Rate Limiting** | One runaway client or scraper exhausts server capacity. | **Token Bucket** or **Sliding Window** per user/IP at the API Gateway. | Buggy customer script hits `/export` in an infinite `while True` loop. |
| **Backpressure** | Fast producer pushes data faster than slow consumer can process, causing `OOM`. | **Bounded queue** + block or return `429` to slow the producer down. | Log shippers sending 50k/s into an indexer that writes 10k/s. |
| **Load Shedding** | Overloaded server tries to run everything and times out on 100% of requests. | **Reject excess requests early** (`HTTP 429` / `503`) so in-flight work finishes. | Dropping low-priority requests when CPU exceeds 85%. |

---

## 2. Fault Isolation (Stopping Cascading Failures)

| Concept | What Goes Wrong | Fix | Production Example |
| :--- | :--- | :--- | :--- |
| **Cascading Failure** | One slow dependency stalls its callers, which stalls upstream services until everything is down. | Combine **Timeouts + Circuit Breakers + Bulkheads**. | Hung analytics DB ties up all web worker threads so `/login` dies too. |
| **Timeouts & Deadlines** | A hung network call holds threads and sockets forever. | Put a timeout on every RPC and propagate remaining **deadline budget** downstream. | Postgres `statement_timeout` + passing a 5s deadline across microservices. |
| **Circuit Breaker** | Calling a dead service repeatedly wastes threads waiting for timeouts. | After $N$ failures, trip **Open** (fail fast for 30s), then test 1 request (**Half-Open**). | Tripping open on a down enrichment API instead of waiting 10s per request. |
| **Bulkhead** | One slow endpoint consumes all shared worker threads. | Isolate each dependency into its **own thread/connection pool**. | Giving slow PDF export jobs a separate worker pool from fast API routes. |
| **Graceful Degradation** | One non-critical widget fails and causes the whole page to return `500`. | Return **stale cached data** or hide the optional widget. | Returning cached recommendations when the ML service is down. |
| **Single Point of Failure (SPOF)** | One machine crashes and takes down the whole system. | Run redundant replicas across multiple Availability Zones with automatic failover. | Active-passive Postgres primary + standby across AZs. |

---

## 3. Exactly-Once & Multi-Service Writes

| Concept | What Goes Wrong | Fix | Production Example |
| :--- | :--- | :--- | :--- |
| **Idempotency** | Client retries after a network timeout and gets charged twice. | Client sends an `Idempotency-Key` (`UUID`); server stores and replays the first response. | Stripe checking `idempotency_key` before charging a card. |
| **Delivery Guarantees** | At-most-once drops messages; at-least-once delivers duplicates. | Use **At-least-once delivery + Idempotent consumer**. | Kafka consumer deduplicating or `UPSERT`ing by `event_id`. |
| **Dual Write** | App writes to Postgres, then crashes before publishing to Kafka, leaving DB and queue out of sync. | **Transactional Outbox:** write row and `outbox` event in the same SQL transaction; a worker relays the outbox to Kafka. | Committing `orders` and `order_outbox` in one DB transaction. |
| **Saga Pattern** | A workflow spans multiple services that don't share a database. | Sequence of local transactions where each step has a **compensating undo action**. | Refunding payment if inventory reservation fails. |
| **Two-Phase Commit (2PC)** | Coordinator locks all participants until everyone votes ready. | Avoid across microservices; holds locks and blocks if the coordinator crashes. | Legacy cross-shard banking transfers. |
| **Poison Message** | One malformed queue message crashes the consumer forever in a retry loop. | Cap retries (e.g., 3 attempts) and move failed messages to a **Dead-Letter Queue (DLQ)**. | Bad JSON payload routed to DLQ for manual inspection. |

---

## 4. Distributed Coordination

| Concept | What Goes Wrong | Fix | Production Example |
| :--- | :--- | :--- | :--- |
| **Leader Election** | Multiple worker pods run the same singleton cron job at the same time. | Elect one leader via **etcd / ZooKeeper** or a database advisory lock. | Ensuring only 1 pod runs the nightly billing sweep. |
| **Lease** | A worker grabs a lock and crashes, holding the lock forever. | Use a **time-bounded lock (TTL)** that expires unless renewed by heartbeats. | 60-second worker lease renewed every 15 seconds. |
| **Fencing Token** | A worker freezes (GC pause), its lease expires, a new worker takes over, and the old worker wakes up and corrupts storage. | Issue a monotonically increasing **fencing token** (`4, 5, 6...`) with each lease; storage rejects writes with an older token. | Storage rejecting a delayed write carrying `token=4` after seeing `token=5`. |
| **Split Brain** | Network partition splits a cluster in two, and both sides act as primary. | Require a **Quorum (majority: $\lfloor N/2 \rfloor + 1$)** to accept writes. | In a 5-node cluster split 3 vs 2, only the 3-node side can commit writes. |
| **Clock Skew** | Wall clocks (`time.now()`) drift across servers, so "last write wins" drops newer data. | Use **monotonic version numbers** or logical clocks instead of wall-clock timestamps. | Two servers with 100ms NTP drift updating the same row. |

---

## 5. Consistency, Locking & Sharding

| Concept | What Goes Wrong | Fix |
| :--- | :--- | :--- |
| **CAP Theorem** | During a network partition, you cannot have both 100% Consistency and 100% Availability. | Pick **CP** for money/inventory/seat booking; pick **AP** (eventual consistency) for feeds/likes/views. |
| **Read-Your-Writes Lag** | User saves profile, refreshes page, and hits a lagging read replica that still shows old data. | Route **that user's reads to the Primary DB** for a few seconds after they write. |
| **Lost Update** | Two users edit the same row concurrently; the second save overwrites the first. | **Optimistic Concurrency Control (OCC):** `UPDATE ... WHERE id = 1 AND version = 4`; fail with `409/412` if 0 rows updated. |
| **Pessimistic Locking** | High contention makes optimistic retries fail constantly. | Lock the row upfront with `SELECT ... FOR UPDATE` inside a short transaction. |
| **Consistent Hashing** | `hash(key) % N` remaps 99% of keys when a cache/shard node is added or removed. | Place nodes and keys on a **hash ring** with virtual nodes so only $1/N$ of keys move. |

---

## 6. Caching & Latency

| Concept | Rule |
| :--- | :--- |
| **Cache-Aside** | App checks Redis; on miss, reads DB, writes to Redis with TTL, and returns. (Default for read-heavy systems). |
| **Write-Through vs. Write-Back** | Write-Through updates cache + DB synchronously. Write-Back updates cache in RAM and flushes batches to DB asynchronously (used for high-volume view/like counters). |
| **Cache Penetration** | Requests for non-existent IDs (`id = -999`) bypass cache and hit DB. Fix: cache `null` with a short TTL or put a **Bloom Filter** in front. |
| **Tail Latency ($p99$)** | Optimize $p95$ and $p99$, not the average. In fan-out calls to 50 backends, the slowest backend sets the user's wait time. |
| **N+1 Queries** | Fetching 50 posts (1 query) then running 1 query per post for author info (50 queries). Fix: batch fetch with `WHERE id IN (...)`. |
| **Connection Pooling** | Opening a new DB connection per request takes ~30ms and exhausts Postgres RAM. Use **PgBouncer / RDS Proxy**. |
