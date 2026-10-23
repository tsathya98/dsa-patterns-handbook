# Distributed failure modes, traffic spikes, and latency

> **Target:** System design interviews (L4 to L6)  
> **Core concept:** Production outages usually start with a small dependency slowdown or synchronized traffic burst that cascades across services. This guide covers traffic spikes, fault isolation, tail latency, and authorization pitfalls.

## 1. Traffic spikes and overload patterns

```text
Without Jitter (Synchronized Spike):     With Jitter (Smoothed Load):
Requests                                 Requests
  ▲      █          █                      ▲    ▄█▄   ▄█▄   ▄█▄
  │      █          █                      │   █████ █████ █████
  └──────┴──────────┴────> Time            └───┴─────┴─────┴─────> Time
       9:00       9:05                        9:00  9:01  9:02
```

### 1. Thundering herd
* **What happens:** Thousands of clients or scheduled workers wake up at the same instant and hit one backend service together.
* **Example:** A live sports app sends a push notification to 2 million phones when a goal is scored, and every client app immediately calls `GET /match/score` at the exact same second.
* **Fix:** Add random jitter to client polling/reconnect timers (`delay + random(0, 15s)`) and serve broadcast read traffic from CDN edge caches.

### 2. Cache stampede (dogpile)
* **What happens:** A heavily read cache key expires, and thousands of concurrent requests miss the cache at once and run the same expensive database query in parallel.
* **Example:** The homepage leaderboard cache key expires at midnight, triggering 10,000 concurrent `GROUP BY` queries against the primary database.
* **Fixes:**
  1. **Singleflight / per-key mutex:** Only the first request acquires a short lock (`SETNX`) and queries the database while the other 9,999 requests wait briefly for the cache to refill.
  2. **Logical early refresh:** Refresh hot keys asynchronously in the background when they reach 80% of their TTL.

### 3. Cache avalanche
* **What happens:** Thousands of distinct cache keys expire at the same timestamp because they were populated together with an identical TTL.
* **Example:** A daily batch job warms 1 million product keys at noon with `EX 7200`. At 2:00 PM, all 1 million keys expire together.
* **Fix:** Add random jitter to every TTL (`7200 + random(0, 600)` seconds) so expirations spread across a 10-minute window.

### 4. Retry storm
* **What happens:** A downstream service slows down and starts timing out. Upstream callers immediately retry failed requests 3 or 4 times, multiplying traffic on the struggling service until it crashes completely.
* **Example:** Database CPU hits 95% and drops 10% of queries. App servers retry immediately up to 3 times, turning 10,000 QPS into 30,000+ QPS.
* **Fix:** Use **exponential backoff with jitter** (`base * 2^attempt + rand_ms`), cap retries (or use a per-process retry budget where at most 10% of requests may be retries), and trip a **circuit breaker** when error rates stay high.

### 5. Hot key / hot partition (celebrity problem)
* **What happens:** One specific key or shard receives a huge fraction of total reads or writes while the rest of the cluster sits mostly idle.
* **Example:** A celebrity account with 100 million followers posts an update. The single cache shard or database partition holding `user_id = celebrity` maxes out its NIC and CPU.
* **Fixes:**
  * **For reads:** Use a short-TTL in-process local cache on app servers, or replicate the key across $K$ cache keys (`post:123#1` .. `post:123#10`) and have readers pick a random suffix.
  * **For writes (like counters):** Split the counter across $K$ sub-keys (`likes:123#1` .. `likes:123#20`), increment a random shard on write, and sum the $K$ shards on read.

### 6. Missing rate limiting
* **What happens:** One buggy script or scraper consumes most of your backend capacity and starves normal users.
* **Fix:** Enforce per-user, per-IP, and per-API-key rate limits (token bucket or sliding window) at the API gateway, returning `HTTP 429 Too Many Requests`.

### 7. Backpressure
* **What happens:** A fast producer pushes work into a slower consumer faster than the consumer can drain it, causing unbounded in-memory queues to grow until the consumer crashes with `OOMKilled`.
* **Fix:** Use bounded queues everywhere. When the queue fills up, block the producer, apply TCP flow control, or reject new work with `HTTP 429` / `503`.

### 8. Load shedding
* **What happens:** When a server is overloaded beyond its capacity, trying to accept and process every request causes all of them to queue up and miss their client timeouts, dropping useful throughput (goodput) to zero.
* **Fix:** Shed excess load early at the entry point. Drop low-priority requests or reject requests whose remaining deadline budget is already too short (`503 Service Unavailable`), keeping latency low for the requests you do accept.

## 2. Fault isolation and stopping cascading failures

```text
Bulkhead Pattern (Isolated Pools):
App Server
 ├── [ Thread Pool A (10 threads) ] ──> Payment Service (Healthy)
 └── [ Thread Pool B (5 threads)  ] ──> Recommendations (Hanging - Only Pool B fills up)
```

### 1. Cascading failure
* **What happens:** Service C hangs $\to$ Service B blocks all its worker threads waiting on Service C $\to$ Service A blocks waiting on Service B $\to$ the entire application goes down.
* **Fix:** Combine strict network **timeouts**, **circuit breakers**, and **bulkhead** resource pools.

### 2. Timeouts and deadline propagation
* **What happens:** Making a network or database call without a timeout lets a hung connection tie up a worker thread indefinitely.
* **Fix:** Set explicit connection and read/write timeouts on every RPC and SQL query, and propagate a remaining **deadline budget** across service hops (via gRPC contexts or HTTP headers) so downstream services abort work if the caller has already timed out.

### 3. Circuit breaker
* **What happens:** When a downstream dependency is down, callers keep sending requests and waiting for timeouts on every call.
* **Fix:** Wrap calls in a circuit breaker state machine (`Closed` $\to$ `Open` $\to$ `Half-Open`). When failures cross a threshold (such as 50% over 10 seconds), trip the breaker to `Open` and fail fast in 0ms without making network calls. After a cool-down period, move to `Half-Open` and allow a few probe requests through to check if the dependency recovered.

* **Circuit breaker states:**
  * **Closed (Normal):** Requests pass through normally. Success and failure rates are tracked in a sliding time window.
  * **Open (Trip):** When failure rate exceeds threshold (e.g., 50% over 10s), trip breaker to Open. All subsequent calls fail fast immediately in 0ms without hitting the downstream dependency.
  * **Half-Open (Probe):** After a cooldown sleep window (e.g., 30s), transition to Half-Open and allow a limited trial quota of probe requests through. If probes succeed, reset to Closed; if probes fail, return to Open for another cooldown.


### 4. Bulkhead isolation
* **What happens:** If all downstream dependencies share a single thread pool or connection pool, one slow endpoint consumes every thread in the pool and blocks unrelated endpoints.
* **Fix:** Partition threads, connection pools, or worker queues per dependency (like watertight compartments in a ship). If the PDF export pool saturates its 10 threads, the remaining 190 threads still serve checkout and login requests.

### 5. Graceful degradation
* **What happens:** A non-critical microservice (like "People You May Know" or personalized recommendations) fails, and the caller returns a `500` error for the entire page.
* **Fix:** Catch failures on non-essential dependencies and fall back to cached static defaults or omit the widget so the core page still renders.

### 6. Single point of failure (SPOF)
* **What happens:** A single non-redundant component (one load balancer, one primary DB without standby, one NAT gateway in a single AZ) fails and takes down the whole system.
* **Fix:** Run redundant instances across multiple availability zones with automated health checks and failover at every tier.

## 3. Speed and latency bottlenecks

### 1. Tail latency ($p99$ and $p99.9$)
* **What happens:** Mean/average latency hides severe slowdowns affecting your heaviest users. If 99 requests take 10ms and 1 request takes 5,000ms (due to a GC pause, lock wait, or cold disk read), the average is 60ms, but 1% of requests take 5 seconds.
* **Fix:** Define SLAs and alerts on **$p95$, $p99$, and $p99.9$ percentiles**, not averages.

### 2. Fan-out tail amplification
* **What happens:** When a single user request fans out to query $M$ backend shards in parallel and waits for all $M$ responses, overall request latency equals the **slowest** shard. If each shard has a 1% chance of hitting a $p99$ hiccup, a request touching 100 shards has a $1 - (0.99)^{100} \approx 63\%$ chance of being slow.
* **Fix:** Use **hedged requests**: if a shard does not respond within the $p95$ latency window (for example, 15ms), send a duplicate read to a replica and use whichever response returns first.

### 3. N+1 query problem
* **What happens:** Application code runs 1 query to fetch $N$ parent rows (`SELECT * FROM posts LIMIT 50`), then loops over the results and runs $N$ separate queries to fetch each child row (`SELECT * FROM users WHERE id = ?`), paying 51 sequential network round trips.
* **Fix:** Replace the loop with a single batch query (`SELECT * FROM users WHERE id IN (...)`) or a SQL `JOIN`, reducing 51 round trips to 1 or 2.

### 4. Head-of-line (HOL) blocking
* **What happens:** One slow, resource-heavy job at the front of a FIFO queue (or HTTP/1.1 connection) blocks hundreds of small, sub-millisecond jobs waiting behind it.
* **Fix:** Split queues by job size/priority (fast lane vs. heavy batch lane) and use multiplexed protocols (`HTTP/2` or `HTTP/3` over QUIC).

### 5. Database connection exhaustion
* **What happens:** Opening a new database connection per request (especially from thousands of autoscaled serverless functions) pays a TCP + TLS handshake cost and exhausts Postgres `max_connections`.
* **Fix:** Place a connection pooler (**PgBouncer** or **RDS Proxy**) in front of the database to multiplex thousands of client connections over a small pool of persistent database connections.

### 6. Noisy neighbor in multi-tenant systems
* **What happens:** One tenant runs an expensive bulk export or unindexed query that saturates shared CPU, memory, or disk IOPS, degrading latency for every other tenant on the same cluster.
* **Fix:** Enforce per-tenant rate limits, query concurrency quotas, fair scheduling across tenant queues, and dedicated shards/cells for large enterprise tenants.

## 4. Security failure modes in system design

### 1. Confused deputy
* **What happens:** A low-privilege caller tricks a privileged internal service (the "deputy") into executing an action using the service's own admin credentials instead of checking the caller's permissions.
* **Fix:** Propagate the end-user identity downstream (for example, via On-Behalf-Of / OBO tokens or signed claims) and authorize against the original user's permissions at the resource layer.

### 2. Over-privileged service accounts (violating least privilege)
* **What happens:** Microservices share a single superuser database credential (`READ/WRITE/DROP`), so a bug or SQL injection in a minor read-only service compromises the entire database.
* **Fix:** Grant each service an IAM role or database user scoped strictly to the tables and verbs (`SELECT` vs. `INSERT/UPDATE`) it needs.

### 3. Perimeter-only auth (missing defense in depth)
* **What happens:** Internal services trust any request arriving from inside the VPC because they assume the API gateway already checked authentication. A single misconfigured route or SSRF bug exposes every internal service.
* **Fix:** Verify service-to-service identity (mTLS) and validate user authorization tokens again at the service and data layers (such as Postgres Row-Level Security).
