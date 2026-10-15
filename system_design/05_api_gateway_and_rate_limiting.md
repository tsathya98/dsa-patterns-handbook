# 🚪 API Gateway & Rate Limiting Architecture

> **Target:** System Design Interviews (FAANG)  
> **Key Focus:** Defending backend services from abuse, cascading failures, and unauthorized traffic while providing a unified API entry point.

---

## 🏛️ 1. What Does an API Gateway Do?

An **API Gateway** is a reverse proxy that sits between external clients and internal microservices.

```text
[ Mobile / Web Clients ]
           │ (Single Entrypoint)
           ▼
┌──────────────────────────────────────────────┐
│             API GATEWAY                      │
│ 1. SSL / TLS Termination                    │
│ 2. Authentication & Authorization (JWT check)│
│ 3. Rate Limiting & Throttling (Redis)       │
│ 4. Request Routing & Protocol Translation   │
│ 5. Metrics, Logging & Distributed Tracing   │
└───────┬──────────────┬──────────────┬────────┘
        │              │              │
        ▼              ▼              ▼
  [ User Service ] [ Order Service ] [ Payment Service ]
```

---

## ⏱️ 2. The 5 Rate Limiting Algorithms Compared

Rate limiters protect APIs from DDoS, brute-force logins, web scraping, and server overloads:

| Algorithm | How It Works | Pros | Cons / Traps |
| :--- | :--- | :--- | :--- |
| **Token Bucket** | Tokens refill at a steady rate $r$. Each request consumes 1 token. If bucket is empty $\to$ reject. | Allows **bursts** of traffic up to bucket capacity; memory efficient. | Tuning token refill rate and bucket size requires testing. |
| **Leaky Bucket** | Requests enter a FIFO queue and leak out at a **constant, smooth rate**. If queue overflows $\to$ drop. | Enforces a perfectly smooth, constant egress rate. | Bursts of requests can fill the queue and experience high latency. |
| **Fixed Window Counter** | Divides timeline into fixed windows (e.g. 1 minute). Counter resets every minute. | Extremely simple and memory-efficient (1 integer per user). | **Window Boundary Spike Trap!** $2\times$ quota can slip through at window boundary (e.g. 100 requests at 00:59 + 100 at 01:00). |
| **Sliding Window Log** | Stores timestamp of every request in a Redis Sorted Set (`ZSET`). Removes logs older than window. | Perfectly accurate; zero boundary spikes. | **Heavy memory consumption!** Storing thousands of timestamps per user balloons RAM. |
| **Sliding Window Counter** | Combines Fixed Window + Weighted Average of previous window. | Accurate enough (<1% error); low memory footprint (stores only 2 counters). | Slight approximation assuming even distribution in previous window. |

---

## ⚡ 3. Distributed Rate Limiter: Redis + Lua Scripting

In production, multiple API Gateway nodes must share the same rate limit state:

```text
[ Gateway Node 1 ] ──┐
[ Gateway Node 2 ] ──┼──> [ Redis Cluster ] ── (Atomic Lua Script)
[ Gateway Node 3 ] ──┘
```

### The Concurrency Trap (Race Conditions):
If two requests arrive simultaneously at Gateway 1 and Gateway 2:
1. Both read `current_count = 99` from Redis.
2. Both increment and write back `100`.
3. An extra request slips past the limit!

### The Production Fix: Atomic Redis Lua Script
Redis executes Lua scripts **atomically on a single thread**, guaranteeing no race conditions:

```lua
-- KEYS[1]: User rate limit key (e.g., 'rate_limit:user_101')
-- ARGV[1]: Max limit (e.g., 100)
-- ARGV[2]: Window size in seconds (e.g., 60)

local current = redis.call('INCR', KEYS[1])
if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[2])
end

if current > tonumber(ARGV[1]) then
    return 0 -- Rejected (HTTP 429)
else
    return 1 -- Allowed (HTTP 200)
end
```

---

## 📡 4. Standard Rate Limiting HTTP Headers

When returning responses, always inform the client of their quota:

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1729000060
Retry-After: 30
```
