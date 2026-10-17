# ⚡ Time & Space Complexity Master Cheat Sheet

> **Quick Reference:** Spot Big O in 3 seconds across loop patterns, data structures, and memory allocations.

---

## 🚀 1. The 3-Second Loop Pattern Decision Table

| Loop Pattern | Code Signature | Big O | Why? |
|---|---|:---:|---|
| **Linear Scan** | `for x in arr:` or `while i < n: i += 1` | **$\mathcal{O}(N)$** | Visits each item once. |
| **Halving / Doubling** | `while i > 0: i //= 2` or `i *= 2` | **$\mathcal{O}(\log N)$** | Number of steps is $\log_2(N)$. |
| **Square Root Scan** | `while i * i <= N: i += 1` | **$\mathcal{O}(\sqrt{N})$** | Factors, prime checks. Runs $\lfloor\sqrt{N}\rfloor$ times. |
| **Independent Nested** | `for i in range(N): for j in range(N):` | **$\mathcal{O}(N^2)$** | $N \times N$ matrix scan. |
| **Shrinking Triangle** | `for i in range(N): for j in range(i, N):` | **$\mathcal{O}(N^2)$** | $\frac{N(N+1)}{2}$ steps. Drop constants. |
| **Nested + Doubling** | `for i in range(N): while j < N: j *= 2` | **$\mathcal{O}(N \log N)$** | Outer $N \times$ inner $\log N$. |
| **Three Nested with Break** | 3 nested loops, but inner loop has `break` | **$\mathcal{O}(N^2)$** | Inner loop terminates on iteration 1. |
| **Divide & Conquer** | Splitting array in half + merging | **$\mathcal{O}(N \log N)$** | Merge Sort, Quick Sort (average). |

---

## 📊 2. Complexity Speed Hierarchy (Fastest to Slowest)

$$\mathcal{O}(1) < \mathcal{O}(\log N) < \mathcal{O}(N) < \mathcal{O}(N \log N) < \mathcal{O}(N^2) < \mathcal{O}(2^N) < \mathcal{O}(N!)$$

```text
N = 1,000 operations check:
• O(1)        ~ 1 step
• O(log N)    ~ 10 steps
• O(N)        ~ 1,000 steps
• O(N log N)  ~ 10,000 steps
• O(N²)       ~ 1,000,000 steps (Safe for N <= 10⁴)
• O(2ᴺ)       ~ 10³⁰⁰ steps (💥 TLE for N > 25!)
• O(N!)       ~ Universe ends (💥 TLE for N > 12!)
```

---

## 💾 3. Space Complexity (Auxiliary Memory) Cheat Sheet

| Code Pattern | Extra Memory Allocated | Space Complexity |
|---|---|:---:|
| Simple variables (`total`, `count`, `l`, `r`) | No new data structures | **$\mathcal{O}(1)$** |
| Recursion tree of depth $H$ | Call stack frames | **$\mathcal{O}(H)$** |
| Array clone / slicing (`arr[:]`, `tmp += s[j]`) | Full copy of elements | **$\mathcal{O}(N)$** |
| Hash Table / Set (`seen = set()`, `dct = {}`) | Stores up to $N$ keys | **$\mathcal{O}(N)$** |
| 2D DP Table (`[[0]*N for _ in range(N)]`) | $N \times N$ cells | **$\mathcal{O}(N^2)$** |

---

## 🧼 4. The 3 Simplification Rules

1. **Drop Constant Multipliers:** $5N \implies \mathcal{O}(N)$.
2. **Drop Constant Divisors:** $\frac{N}{3} \implies \mathcal{O}(N)$.
3. **Drop Non-Dominant Terms:** $N^2 + 100N + 5000 \implies \mathcal{O}(N^2)$.
