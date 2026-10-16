# 🛡️ Distributed Failure Modes, Traffic Spikes & Latency Guide

> **Target:** FAANG System Design Interviews (L4–L6)  
> **Core Idea:** Systems rarely fail because of normal traffic. They fail when a small hiccup triggers a chain reaction. Here is how to spot and fix every traffic, failure, latency, and security trap.

---

## 🌊 1. Too Much Traffic at Once

When traffic spikes or synchronizes unexpectedly, your servers get crushed.

```text
Without Jitter (Thundering Herd):        With Jitter (Smoothed Load):
Requests                                 Requests
  ▲      █          █                      ▲    ▄█▄   ▄█▄   ▄█▄
  │      █          █                      │   █████ █████ █████
  └──────┴──────────┴────> Time            └───┴─────┴─────┴─────> Time
       9:00       9:05                        9:00  9:01  9:02
```

### 1. Thundering Herd
* **What goes wrong:** Thousands of clients or background jobs wake up at the exact same millisecond and hammer one service together.
* **Real-World Example:** You run a "6-hour sync job" for everyone who signed up during a 9:00 AM promo. At 3:00 PM sharp, 500,000 jobs fire at once and crash the database.
* **The Fix:** **Add Random Jitter.** Instead of scheduling at `3:00:00 PM`, schedule at `3:00 PM + random(0, 300 seconds)` so the spike flattens into a smooth wave.

### 2. Cache Stampede (Dogpile)
* **What goes wrong:** One super popular cache key expires. Instantly, 10,000 concurrent requests see a "cache miss" and all rush to the database to recompute the exact same row.
* **Real-World Example:** The homepage leaderboard cache expires at midnight. 10,000 users loading the page at `00:00:01` all trigger the expensive `GROUP BY` SQL query simultaneously.
* **The Fix:**
  1. **Singleflight / Mutex Lock:** The first request grabs a lock (`SETNX`) and queries the DB; the other 9,999 wait 20ms for the cache to populate.
  2. **Early Refresh:** Refresh the key in the background at 80% of its TTL before it actually expires.

### 3. Cache Avalanche
* **What goes wrong:** Thousands of *different* cache entries expire at the same moment because they were loaded together with the same TTL.
* **Real-World Example:** After a server reboot at noon, you warm up 1 million product cache keys with a `2-hour TTL`. At 2:00 PM sharp, all 1 million keys vanish at once.
* **The Fix:** **Stagger TTLs with Jitter.** Set TTL to `7200s + random(0, 600s)` so keys expire gradually over a 10-minute window.

### 4. Retry Storm
* **What goes wrong:** A downstream service slows down and starts timing out. Every caller immediately retries, doubling and tripling the load on the already dying service until it completely melts.
* **Real-World Example:** Payment DB CPU hits 95% and drops a few requests. The API servers blindly retry 3 times immediately, turning 10,000 QPS into 40,000 QPS and killing the DB.
* **The Fix:** **Exponential Backoff + Jitter + Retry Cap.** Wait `1s, 2s, 4s + random_ms`, cap retries at 3, and use a **Circuit Breaker** to stop retrying if failure rates exceed 50%.

### 5. Hot Key / Hot Partition ("The Celebrity Problem")
* **What goes wrong:** Traffic isn't spread evenly—one specific key or database shard gets 90% of all reads or writes, melting the single server holding it.
* **Real-World Example:** Justin Bieber posts a photo. Shard #4 (which holds `user_id = bieber`) gets 5 million requests/sec while Shards #1–#3 sit idle.
* **The Fix:**
  * **For Reads:** Cache the key locally in app server memory or replicate across multiple cache keys (`bieber#1` through `bieber#10`) and read from a random suffix.
  * **For Writes:** Shard the counter (`likes_bieber_1` .. `likes_bieber_20`), write to a random shard, and sum them up on read.

### 6. Rate Limiting
* **What goes wrong:** One buggy script or scraper consumes 95% of your server capacity, starving every other customer.
* **Real-World Example:** A single customer runs an infinite `while(true)` loop calling your `/export` API 5,000 times a second.
* **The Fix:** **Token Bucket or Sliding Window Rate Limiter** at the API Gateway per `user_id` or `IP`, returning `HTTP 429 Too Many Requests`.

### 7. Backpressure
* **What goes wrong:** A fast producer pumps data into a slow consumer faster than the consumer can process it, until the consumer runs out of RAM (`OOMKilled`).
* **Real-World Example:** Log agents send 50,000 events/sec to an indexer that can only write 10,000/sec. The indexer's in-memory queue grows to 32 GB and crashes.
* **The Fix:** **Bounded Queues + Flow Control.** Cap the queue size; when full, block the producer or tell it to slow down (`TCP window size` or `HTTP 429`).

### 8. Load Shedding
* **What goes wrong:** When a server is overloaded (e.g., 100% CPU), it tries to process everything anyway, causing *every* request to time out so zero requests succeed.
* **Real-World Example:** Your server can handle 1,000 QPS. During a surge of 3,000 QPS, all 3,000 requests take 35 seconds and time out. Good throughput drops to zero.
* **The Fix:** **Fail Fast (`503 Service Unavailable` / `429`).** Reject excess or low-priority requests immediately at the door so the core 1,000 QPS finish in <50ms.

---

## 🔥 2. Failures Spreading (Fault Isolation)

How to stop one broken dependency from pulling down your entire company.

```text
Bulkhead Pattern (Isolated Pools):
App Server
 ├── [ Thread Pool A (10 threads) ] ──> Payment Service (Healthy ✅)
 └── [ Thread Pool B (5 threads)  ] ──> Recommendations (Hanging ❌ - Only Pool B fills up!)
```

### 1. Cascading Failure
* **What goes wrong:** Service C hangs $\to$ Service B's threads all block waiting for C $\to$ Service A's threads all block waiting for B $\to$ the entire platform goes dark.
* **Real-World Example:** An analytics database locks up. Because the checkout page synchronously calls Analytics, all web server worker threads get stuck waiting, and users can't even load the login page.
* **The Fix:** Combine **Timeouts**, **Circuit Breakers**, and **Bulkheads**.

### 2. Timeouts & Deadlines
* **What goes wrong:** Calling a network dependency without a timeout means a hung socket ties up your thread/connection forever.
* **Real-World Example:** A database query hangs on a lock. Without `statement_timeout`, 100 web workers wait 20 minutes until the whole cluster runs out of sockets.
* **The Fix:** Put a strict timeout on **every** network call (e.g., `2s`), and pass a **Deadline Budget** downstream (if the user has 75s total and Step 1 took 70s, Step 2 gets a `5s` deadline—not a fresh 60s).

### 3. Circuit Breaker
* **What goes wrong:** You know a downstream service is dead, yet you keep sending it 10,000 requests/sec, wasting threads and preventing it from recovering.
* **Real-World Example:** The recommendation microservice is down. Every page load still waits 3 seconds for it to time out before rendering.
* **The Fix:** **State Machine (`Closed` $\to$ `Open` $\to$ `Half-Open`).** After $N$ consecutive failures, **trip the breaker (`Open`)** and fail instantly (0ms) for 30 seconds. Then let 1 test request through (`Half-Open`) to see if it recovered.

### 4. Bulkhead
* **What goes wrong:** Named after ship hull compartments. If all dependencies share one thread/connection pool, one slow dependency drains the entire pool and starves healthy features.
* **Real-World Example:** A slow "PDF Export" endpoint eats all 200 worker threads on your server, so fast `/healthz` and `/login` requests can't get a thread.
* **The Fix:** **Isolate Resource Pools.** Give PDF Export its own capped pool of 10 threads; even if it maxes out, the other 190 threads serve normal users cleanly.

### 5. Graceful Degradation
* **What goes wrong:** One minor widget fails (e.g., "Recommended Stickers"), and your backend returns a `500 Internal Server Error`, breaking the entire screen.
* **Real-World Example:** Netflix's personalized recommendation engine fails. Instead of showing a blank error screen, it falls back to a pre-cached static list of "Top 10 Movies Today".
* **The Fix:** Return **stale cached data** (e.g., last good dashboard snapshot) or hide the non-critical UI component so the core user journey still works.

### 6. Single Point of Failure (SPOF)
* **What goes wrong:** One piece of hardware or single instance dies and brings down the entire system.
* **Real-World Example:** You have 10 app servers, 3 DB replicas, and **1 Load Balancer**. That 1 Load Balancer crashes, and nobody can reach your 10 healthy servers.
* **The Fix:** **Redundancy at every layer**—multiple orchestrator replicas, Active-Passive load balancers with floating IPs, and Multi-AZ database failover.

---

## ⚡ 3. Speed & Latency Bottlenecks

### 1. Tail Latency ($p99$ / $p99.9$)
* **What goes wrong:** Your *average* latency looks great (`40ms`), so you think users are happy. Meanwhile, the slowest 1% ($p99$) takes `8 seconds`—and your biggest enterprise customers with the most data are always in that 1%.
* **Real-World Example:** 99 requests hit RAM (`5ms`), 1 request hits a GC pause or cold disk read (`5,000ms`). Average is `55ms`, but 1 in 100 clicks feels broken.
* **The Fix:** Always monitor and alert on **$p95$ and $p99$**, never `mean/average`.

### 2. Fan-Out Amplification
* **What goes wrong:** One user request fans out to call 50 backend shards in parallel. Because you must wait for all 50 to finish, your overall response time equals the **slowest** of the 50 servers!
* **Real-World Example:** Searching across 100 Elasticsearch shards. Even if each shard only has a 1% chance of being slow ($p99$), the probability that *at least one* of the 100 shards is slow is $1 - (0.99)^{100} = \mathbf{63\%}$!
* **The Fix:** **Hedged Requests.** If a shard hasn't replied within the $p95$ window (e.g., `15ms`), fire a duplicate request to a replica and take whichever answers first.

### 3. N+1 Query Problem
* **What goes wrong:** Code fetches a list of $N$ parent items (1 query), then loops over the list firing 1 query per item to fetch its details ($N$ queries).
* **Real-World Example:** `SELECT * FROM posts LIMIT 50` (1 query), followed by a `for` loop running `SELECT * FROM users WHERE id = post.author_id` 50 separate times. 51 network round-trips!
* **The Fix:** **Batch Lookup or JOIN.** Collect all IDs and run a single `SELECT * FROM users WHERE id IN (1, 2, ... 50)`—cutting 51 round-trips down to 2.

### 4. Head-of-Line (HOL) Blocking
* **What goes wrong:** One giant, slow item at the front of a single queue blocks 1,000 tiny, fast items waiting behind it.
* **Real-World Example:** Like getting stuck behind someone with 300 coupons at a single grocery checkout lane when you only want to buy a pack of gum.
* **The Fix:** **Separate Lanes (Fast Lane vs. Heavy Lane)** or multiplex streams (like `HTTP/2` & `HTTP/3 QUIC`, or splitting "express jobs" and "batch jobs" into separate worker queues).

### 5. Connection Pooling
* **What goes wrong:** Opening a brand new database connection on every HTTP request requires a TCP 3-way handshake, TLS negotiation, and Postgres process fork (~30ms overhead + high DB RAM usage).
* **Real-World Example:** 500 serverless functions spin up and open 500 fresh Postgres connections simultaneously, exhausting `max_connections` and crashing the DB.
* **The Fix:** **Connection Pooler (PgBouncer / RDS Proxy).** Keep a warm pool of 10–20 open connections per pod and reuse them across thousands of short requests.

### 6. Noisy Neighbor
* **What goes wrong:** In a multi-tenant system, one heavy customer runs a massive report that eats 100% of shared CPU/Disk IOPS, making the app laggy for every other customer on that machine.
* **Real-World Example:** Tenant A imports 10 million rows at 2 PM, starving Tenant B's live dashboard queries on the same database.
* **The Fix:** **Per-Tenant Quotas, Fair Queuing, and Resource Isolation** (cgroups, per-tenant rate limits, or dedicated shards for enterprise whales).

---

## 🔐 4. Security Ideas That Show Up in Design Rounds

### 1. Confused Deputy
* **What goes wrong:** A low-privilege user tricks a high-privilege backend service (the "deputy") into performing an action using the *service's* own god-mode credentials instead of the user's permissions.
* **Real-World Example:** An anonymous caller hits your Orchestrator. Because no user token was passed, the Orchestrator accidentally falls back to its own internal `admin_service_token` and fetches private company data for the anonymous user.
* **The Fix:** **Propagate Caller Identity (OBO / On-Behalf-Of tokens)** and verify permissions against the *original user's* identity at the resource layer—never fall back to a privileged service token for user requests.

### 2. Least Privilege
* **What goes wrong:** Every microservice is given a master `READ/WRITE/DELETE` database credential "just to make development easy." If one service has a bug or gets compromised, it can wipe the whole database.
* **Real-World Example:** A read-only analytics service has `DROP TABLE` permissions and accidentally runs a destructive migration.
* **The Fix:** Scope every service token and IAM role to the **bare minimum permissions** required (e.g., Memory service token gets `SELECT`-only access on specific tables).

### 3. Defense in Depth
* **What goes wrong:** Relying on a single perimeter wall ("The API Gateway checks auth, so internal services don't need to check anything"). If one misconfigured route bypasses the gateway, the backend is wide open.
* **Real-World Example:** An internal admin tool assumes any request inside the VPC is trusted. A SSRF bug in another service allows an attacker to call it directly.
* **The Fix:** **Layer your defenses.** The API Gateway validates the JWT, the orchestrator checks workspace access, and the database/tool enforces row-level security (`RLS`) or token verification again.
