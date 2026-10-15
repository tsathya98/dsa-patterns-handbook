# ⚡ Caching Strategies, Patterns & Redis Deep Dive

> **Target:** System Design Interviews (FAANG)  
> **Key Concept:** Caching sits between compute and storage to reduce latency from ~10–50ms (disk/DB) to <1ms (in-memory RAM).

---

## 🧭 1. The 4 Core Caching Strategies

```text
1. Cache-Aside (Lazy Loading)              2. Write-Through
   App ──1. Check Cache─> [ Cache ]           App ──1. Write Data──> [ Cache ]
    │         │ (Miss)                                                    │
    │         ▼                                                           ▼ 2. Synchronous Write
    └───2. Read DB─────> [ Database ]                                [ Database ]

3. Write-Behind (Write-Back / Async)       4. Refresh-Ahead
   App ──1. Write Data──> [ Cache ]           App ─── Read Data ───> [ Cache ]
                            │                                            ▲
                            │ (Async Batch Write)                        │ (Auto-Refresh before expiry)
                            ▼                                            │
                       [ Database ]                                 [ Database ]
```

| Strategy | Read Path | Write Path | Pros | Cons / Traps |
| :--- | :--- | :--- | :--- | :--- |
| **Cache-Aside (Lazy Loading)** | Look in cache. On miss, read DB, store in cache, return to user. | Write directly to DB, invalidate (delete) cache entry. | Only requested data is cached; cache failures don't kill the app. | Cache miss penalty (3 round trips); stale data if invalidation fails. |
| **Write-Through** | Read from cache. | Write to cache first; cache synchronously writes to DB before returning success. | High consistency; read hits are always fresh. | Higher write latency (writes wait for both cache and DB). |
| **Write-Behind (Write-Back)** | Read from cache. | Write to cache only; cache asynchronously flushes writes to DB in batches. | Blazing fast writes; absorbs write spikes (e.g. IoT telemetry). | High risk of data loss if cache node crashes before flushing to DB. |
| **Refresh-Ahead** | Read from cache. | System predicts hot keys and reloads from DB before the TTL expires. | Ultra-low read latency for predictable hot keys (e.g. top headlines). | High complexity; wasted resources if predictions are inaccurate. |

---

## 🗑️ 2. Cache Eviction Policies

When the cache reaches memory limits, which keys get thrown out?

1. **LRU (Least Recently Used):** Evicts the item that hasn't been accessed for the longest time. *(Default for 95% of interview architectures).*
2. **LFU (Least Frequently Used):** Tracks access counts; evicts the item accessed the fewest number of times. *(Great for historical assets).*
3. **FIFO (First-In, First-Out):** Evicts the oldest added key regardless of recent access.
4. **TTL (Time-To-Live):** Keys automatically expire after a specified duration (e.g., `SET key val EX 3600`).

---

## 💥 3. The 3 Classic Cache Disasters (Interview Grilling)

### Disaster 1: Cache Penetration
* **The Problem:** Malicious client queries IDs that **do not exist** in either cache or database (e.g., `user_id = -999999`). Every request bypasses the cache and hammers the DB directly.
* **The Solutions:**
  1. **Cache Null Values:** Store `key: null` in Redis with a short TTL (e.g., 60 seconds).
  2. **Bloom Filter:** Place a space-efficient Bloom filter in front of the cache. If the Bloom filter says *"ID definitely does not exist"*, reject the request immediately without touching the DB.

### Disaster 2: Cache Avalanche
* **The Problem:** Thousands of cached keys are set with the exact same TTL (e.g., 2 hours). When that hour arrives, all keys expire simultaneously, causing a tidal wave of queries to flood the database at once.
* **The Solution:**
  * **Add Jitter (Random Variation):** Set TTL to `base_time + random_variance` (e.g., `7200s + rand(0, 300)s`). This staggers expirations smoothly.

### Disaster 3: Cache Breakdown (Thundering Herd / Cache Stampede)
* **The Problem:** A single ultra-hot key (e.g. a viral tweet from Elon Musk) expires. At that exact millisecond, 50,000 concurrent requests get a cache miss and all execute the heavy DB query in parallel.
* **The Solutions:**
  1. **Distributed Mutex Lock:** Only the first request acquires a Redis lock (`SETNX lock_key 1 EX 5`) to query the DB and repopulate the cache. All other 49,999 requests wait or serve a slightly stale read.
  2. **Soft Expiration (Probabilistic Early Refresh):** Recompute the key in background when it reaches 80% of its lifetime.

---

## 🏎️ 4. Redis Data Structures for FAANG Interviews

Redis is an in-memory data structure server, not just a plain string store:

| Data Structure | Use Case in System Design | Example Interview Problem |
| :--- | :--- | :--- |
| **String** | Key-value caching, distributed locks (`SETNX`), counters. | URL Shortener, Rate Limiting (Token Bucket). |
| **Hash** | Storing structured objects with multiple fields. | User profile data (`HSET user:101 name "John" age 28`). |
| **Sorted Set (ZSET)** | Elements sorted by a floating-point score (SkipList + HashMap). | **Leaderboards**, Top-K trending items, Sliding Window Rate Limiter. |
| **List** | Ordered sequence of strings (doubly-linked list). | Activity feeds, lightweight pub/sub queue. |
| **Bitmap** | Bit-level manipulation (1 bit per entity). | Tracking daily active users (`SETBIT user_active:2026-10-15 user_id 1`). 100M users = ~12 MB memory! |
| **HyperLogLog** | Probabilistic cardinality estimator (counts unique items with <1% error). | Unique page views / daily unique visitors with fixed 12 KB memory footprint. |
