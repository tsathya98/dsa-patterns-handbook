# 🧩 Subarrays & Contribution Technique Cheat Sheet

> **Scope:** Subarray combinatorics, the $\mathcal{O}(N)$ Contribution Technique, reverse iteration patterns, and state tracking.

---

## 1. Subarray Combinatorics & Formulas

* **Subarray:** Contiguous unbroken slice of an array.
* **Total Subarrays in array of size $N$:**
  $$\text{Count} = \frac{N(N + 1)}{2}$$

| Term | Contiguous? | Order Matter? | Total Combinations |
|---|---|---|---|
| **Subarray** | ✅ Yes | ✅ Yes | $\frac{N(N + 1)}{2}$ |
| **Subsequence** | ❌ No | ✅ Yes | $2^N - 1$ |
| **Subset** | ❌ No | ❌ No | $2^N$ |

---

## 2. The $\mathcal{O}(N)$ Contribution Technique

> **Problem:** Find the sum of all elements across all $\frac{N(N+1)}{2}$ subarrays.

* **Brute Force:** $\mathcal{O}(N^3)$ (generate all subarrays, sum elements).
* **Prefix Sums:** $\mathcal{O}(N^2)$ (all pairs $(i, j)$ with prefix differences).
* **The Contribution Invariant:** Ask how many subarrays contain `arr[i]`:
  * Valid starts for $L \in [0, i] \implies (i + 1)$ choices.
  * Valid ends for $R \in [i, N - 1] \implies (N - i)$ choices.
  $$\text{Occurrences of } arr[i] = (i + 1) \times (N - i)$$
  $$\text{Grand Total} = \sum_{i=0}^{N-1} arr[i] \cdot (i + 1) \cdot (N - i)$$

```python
def total_subarray_sum(arr: list[int]) -> int:
    n = len(arr)
    return sum(val * (i + 1) * (n - i) for i, val in enumerate(arr))
```
* **Time:** $\mathcal{O}(N)$ | **Space:** $\mathcal{O}(1)$.

---

## 3. High-Yield Subarray Patterns Matrix

| Problem | Core Strategy | Time | Space | One-Line Intuition |
|---|---|---|---|---|
| **Leaders in Array** | Right-to-Left Scan | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Track `max_so_far` from $N-1$ down to $0$. Element is leader if `arr[i] > max_so_far`. |
| **Closest Min-Max** | State Index Tracking | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Track `last_min` and `last_max` indices; update $\min(\text{len}, |last\_min - last\_max| + 1)$. |
| **Count Pairs $(a, g)$** | Suffix Counter | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Scan right-to-left; count $g$'s; when seeing $a$, add running $g\_count$ to total. |
| **Maximum Subarray (LC 53)** | Kadane's Algorithm | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | If running sum drops below $0$, declare bankruptcy and reset `curr_sum = 0`. |
| **Subarray Sum Equals K (LC 560)** | Prefix Sum + HashMap | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Check if `curr_prefix - k` exists in prefix frequency hash map. |
