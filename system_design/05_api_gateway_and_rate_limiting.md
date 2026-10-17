# API gateway and rate limiting architecture

> **Target:** System design interviews  
> **Core concept:** Centralizing TLS termination, authentication, routing, and rate limiting at the edge so backend microservices stay simple and protected from traffic abuse.

## 1. What an API gateway does

An API gateway is an L7 reverse proxy sitting between external clients and internal microservices.

```text
[ Mobile / Web Clients ]
           │ (Single Entrypoint)
           ▼
┌──────────────────────────────────────────────┐
│             API GATEWAY                      │
│ 1. TLS Termination                           │
│ 2. Authentication & Authorization (JWT check)│
│ 3. Rate Limiting & Throttling (Redis)        │
│ 4. Request Routing & Protocol Translation    │
│ 5. Metrics, Logging & Distributed Tracing    │
└───────┬──────────────┬──────────────┬────────┘
        │              │              │
        ▼              ▼              ▼
  [ User Service ] [ Order Service ] [ Payment Service ]
```

### Gateway request evaluation steps:
* **1. Edge ingress:** Terminate SSL/TLS and inspect JWT bearer tokens / API keys.
* **2. Rate limit evaluation:** Execute atomic Redis Lua script (Token Bucket or Sliding Window Log) against caller ID / IP.
* **3. Rejection:** If quota exceeded, return `HTTP 429 Too Many Requests` immediately with a `Retry-After: <seconds>` header.
* **4. Upstream routing:** If within limit, append verified user context headers (`X-User-Id`, `X-Scopes`) and route request to the target microservice.


## 2. Five rate limiting algorithms compared

Rate limiters cap how many requests a user, IP address, or API key can send within a time window to block brute-force logins, scrapers, and noisy neighbors:

| Algorithm | How it works | Pros | Cons and edge cases |
| :--- | :--- | :--- | :--- |
| **Token bucket** | Bucket holds up to $B$ tokens and refills at rate $r$ tokens/sec. Each request consumes 1 token; empty bucket rejects with `429`. | Allows short bursts up to bucket capacity $B$; only stores `{tokens, last_refill_ts}` per key. | Requires tuning two parameters (bucket capacity $B$ and refill rate $r$). |
| **Leaky bucket** | Requests enter a bounded FIFO queue and drain out to workers at a constant rate. Full queue drops new requests. | Smooths bursty traffic into a flat, predictable downstream rate. | Bursts sit in the queue and add latency instead of finishing quickly. |
| **Fixed window counter** | Increments an integer counter for the current time bucket (such as `rate:u1:14:01`) with a TTL of 60s. | One integer (`INCR`) per user per window. | **Boundary burst:** A client can send $100$ requests at `14:00:59` and $100$ more at `14:01:00` ($2\times$ the intended limit in 2 seconds). |
| **Sliding window log** | Stores the exact timestamp of every request in a Redis Sorted Set (`ZSET`) and trims entries older than `now - window` via `ZREMRANGEBYSCORE`. | Exact sliding window with no boundary burst. | High memory footprint: storing 10,000 timestamps per user uses megabytes of RAM. |
| **Sliding window counter** | Approximates the sliding window count using `curr_window_count + prev_window_count * overlap_fraction`. | Smooths boundary bursts while storing only two integer counters per user. | Slight approximation because it assumes requests in the previous window arrived at a uniform rate. |

## 3. Distributed rate limiting with Redis and Lua

When multiple API gateway nodes enforce a shared quota, a naive read-then-write check (`GET` followed by `INCR`) has a race condition:

```text
[ Gateway Node 1 ] ──┐
[ Gateway Node 2 ] ──┼──> [ Redis Cluster ] ── (Atomic Lua Script)
[ Gateway Node 3 ] ──┘
```

### The read-modify-write race condition
If a user's limit is 100 and two requests arrive at Gateway 1 and Gateway 2 at the same millisecond when `count == 99`:
1. Both gateways read `99`.
2. Both gateways see `99 < 100` and increment the key, letting 101 requests through (or if `INCR` and `EXPIRE` are separate network calls, a crash between them leaves a key with no TTL that blocks the user forever).

### Atomic Redis Lua script
Redis executes a Lua script atomically on its single command thread, so no other command can interleave between `INCR` and `EXPIRE`:

```lua
-- KEYS[1]: Rate limit key (e.g., 'rate_limit:user_101:287150')
-- ARGV[1]: Max allowed requests (e.g., 100)
-- ARGV[2]: Window size in seconds (e.g., 60)

local current = redis.call('INCR', KEYS[1])
if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[2])
end

if current > tonumber(ARGV[1]) then
    return 0 -- Reject (HTTP 429)
else
    return 1 -- Allow (HTTP 200)
end
```

## 4. Standard rate limit HTTP response headers

Return standard rate limit headers so well-behaved clients know their remaining quota and when to retry:

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1729000060
Retry-After: 30
```
