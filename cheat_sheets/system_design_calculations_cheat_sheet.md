# Back-of-the-Envelope Calculations Cheat Sheet

Round numbers aggressively in interviews so you can do the math in your head in 30 seconds.

## 1. Powers of 2 & Storage Units

| Power | Exact | Interview Approximation | Unit |
| :--- | :--- | :--- | :--- |
| $2^{10}$ | $1,024$ | $10^3$ ($1,000$) | **1 KB** |
| $2^{20}$ | $1,048,576$ | $10^6$ (1 Million) | **1 MB** |
| $2^{30}$ | $1,073,741,824$ | $10^9$ (1 Billion) | **1 GB** |
| $2^{40}$ | $\approx 1.1 \times 10^{12}$ | $10^{12}$ (1 Trillion) | **1 TB** |
| $2^{50}$ | $\approx 1.1 \times 10^{15}$ | $10^{15}$ | **1 PB** |

---

## 2. Latency Numbers That Matter

| Operation | Latency | Takeaway |
| :--- | :--- | :--- |
| L1 / L2 cache read | `0.5 ns` / `7 ns` | Instant CPU register speed |
| Main memory (RAM) read | `100 ns` | **RAM is 1,000x faster than SSD** |
| Sequential 1 MB read from RAM | `0.25 ms` | Fast in-memory scan |
| Random SSD read / 1 MB sequential SSD | `0.1 ms` / `1 ms` | Database disk hit |
| Same-datacenter network round trip | `0.5 ms` | Microservice RPC overhead |
| Cross-continent network round trip (US to EU) | `150 ms` | Put a CDN at the edge |

---

## 3. QPS Mental Math (`1 Day ≈ 100,000 Seconds`)

Exact seconds in a day: $24 \times 3600 = 86,400 \approx \mathbf{10^5\text{ seconds}}$.

$$\text{Average QPS} \approx \frac{\text{Daily Requests}}{100,000}, \qquad \text{Peak QPS} \approx 2 \times \text{Average QPS}$$

| Daily Volume | Average QPS | Peak QPS (2x–3x) |
| :--- | :--- | :--- |
| 1 Million / day | `10 QPS` | `20–30 QPS` |
| 10 Million / day | `100 QPS` | `200–300 QPS` |
| 100 Million / day | `1,000 QPS` | `2,000–3,000 QPS` |
| 1 Billion / day | `10,000 QPS` | `20,000–30,000 QPS` |

---

## 4. Typical Record Sizes

| Item | Size |
| :--- | :--- |
| 64-bit integer ID / timestamp | `8 B` |
| UUID | `16 B` |
| Short URL / tweet / chat message row | `300 B - 500 B` |
| User profile metadata | `1 KB - 2 KB` |
| Thumbnail image | `20 KB - 50 KB` |
| High-res photo | `2 MB` |
| 1-minute compressed video | `20 MB - 50 MB` |

---

## 5. Worked 60-Second Template (100M DAU, 10:1 Read/Write)
1. **Write QPS:** $100\text{M writes/day} / 100,000\text{ s} = \mathbf{1,000\text{ writes/s}}$ (Peak: `2,000 writes/s`).
2. **Read QPS:** $1,000 \times 10 = \mathbf{10,000\text{ reads/s}}$ (Peak: `20,000 reads/s`).
3. **Storage (5 years):** $100\text{M/day} \times 500\text{ B} = 50\text{ GB/day} \approx 18\text{ TB/year} \implies \mathbf{90\text{ TB over 5 years}}$.
4. **Redis Cache RAM (20% hot working set):** $20\% \times 50\text{ GB/day} \times 10\text{ days} \approx \mathbf{100\text{ GB RAM}}$ (fits on 1–2 Redis nodes).
