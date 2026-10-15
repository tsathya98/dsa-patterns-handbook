# 🔢 Back-of-the-Envelope Calculations Cheat Sheet

> **Target:** FAANG System Design Interviews  
> **Rule of Thumb:** Speed and order-of-magnitude estimation matter more than precise decimals. Round numbers to make mental math fast!

---

## 💾 1. Powers of 2 & Storage Units

| Power | Approximation | Value | Storage Name |
| :--- | :--- | :--- | :--- |
| $2^{10}$ | $1,000$ | $1,024$ | **1 Kilobyte (KB)** |
| $2^{20}$ | $1,000,000$ (1 Million) | $1,048,576$ | **1 Megabyte (MB)** |
| $2^{30}$ | $1,000,000,000$ (1 Billion) | $1,073,741,824$ | **1 Gigabyte (GB)** |
| $2^{40}$ | $1,000,000,000,000$ (1 Trillion) | $1,099,511,627,776$ | **1 Terabyte (TB)** |
| $2^{50}$ | $10^{15}$ | $1,125,899,906,842,624$ | **1 Petabyte (PB)** |

---

## ⚡ 2. Latency Numbers Every Engineer Must Know

```text
L1 Cache Reference:              ~0.5 ns
L2 Cache Reference:              ~7 ns
Main Memory (RAM) Access:        ~100 ns
Read 1 MB sequentially from RAM: ~250,000 ns (0.25 ms)
Read 1 MB sequentially from SSD: ~1,000,000 ns (1 ms)
Disk Seek (HDD):                 ~10,000,000 ns (10 ms)
Send packet California to Netherlands & back: ~150 ms
```

### Key Intuition:
* **RAM is ~10,000x faster than Disk!** (Always place an in-memory cache in front of DB queries for hot data).
* **Network across oceans is slow (~150 ms)!** (Always use a multi-region CDN for static assets).

---

## ⏱️ 3. Time Conversions & Mental Math Shortcuts

* **Seconds in a Day:** $24 \times 60 \times 60 = 86,400 \approx \mathbf{100,000}$ *(Round to 100k in interviews!)*
* **Requests to QPS Formula:**
  $$\text{Average QPS} = \frac{\text{Daily Requests}}{86,400} \approx \frac{\text{Daily Requests}}{100,000}$$
  $$\text{Peak QPS} \approx 2 \times \text{Average QPS}$$

### Quick Cheat Examples:
* **10 Million requests/day:** $\frac{10,000,000}{100,000} \approx \mathbf{100\text{ QPS}}$
* **100 Million requests/day:** $\frac{100,000,000}{100,000} \approx \mathbf{1,000\text{ QPS}}$ (Peak: ~2,000–3,000 QPS)
* **1 Billion requests/day:** $\frac{1,000,000,000}{100,000} \approx \mathbf{10,000\text{ QPS}}$ (Peak: ~20,000–30,000 QPS)

---

## 📦 4. Common Sizing Benchmarks

| Data Item | Typical Size Assumption |
| :--- | :--- |
| **UUID / ID** | 16 bytes (or 8-byte 64-bit integer) |
| **Short URL record** | ~500 bytes (ID, original URL, short code, timestamp, user ID) |
| **Tweet / Chat message** | ~300 bytes – 500 bytes |
| **User Profile Metadata** | ~1 KB – 2 KB |
| **Thumbnail Image** | ~20 KB – 50 KB |
| **High-Res Photo** | ~2 MB – 5 MB |
| **Standard Video (1 min)** | ~20 MB – 50 MB |

---

## 📐 5. High-Yield Estimation Template

When given a problem with **100M DAU**:
1. **Reads vs. Writes:** State the ratio (e.g. 10:1 or 100:1).
2. **Write QPS:** $\frac{100\text{M writes}}{100,000\text{s}} = 1,000\text{ writes/sec}$.
3. **Read QPS:** $1,000 \times 10 = 10,000\text{ reads/sec}$.
4. **Storage (5 Years):**
   $$100\text{M writes/day} \times 500\text{ bytes} = 50\text{ GB/day}$$
   $$50\text{ GB/day} \times 365 \approx 18\text{ TB/year} \implies \mathbf{90\text{ TB in 5 years}}.$$
5. **Cache RAM (80/20 Pareto Rule):**
   * 20% of hot daily reads generate 80% of traffic.
   * Daily read data = $1\text{B reads} \times 500\text{ bytes} = 500\text{ GB}$.
   * Cache $20\% \implies \mathbf{100\text{ GB RAM}}$ (Can fit comfortably on 1–2 Redis nodes!).
