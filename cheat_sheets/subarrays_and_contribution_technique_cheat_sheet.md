# Subarrays & Contribution Technique Cheat Sheet

> Guide: [Subarray Mechanics & Contribution Technique](../01_arrays_and_pointers/00_subarray_mechanics_and_contribution_technique.md)

## 1. Subarray vs. Subsequence vs. Subset

| Term | Contiguous? | Order Preserved? | Total Count for Length $N$ |
| :--- | :--- | :--- | :--- |
| **Subarray** | Yes | Yes | $\frac{N(N + 1)}{2}$ |
| **Subsequence** | No | Yes | $2^N - 1$ (non-empty) |
| **Subset** | No | No | $2^N$ |

---

## 2. The $\mathcal{O}(N)$ Contribution Technique
**Problem:** Find the grand total sum of all $\frac{N(N+1)}{2}$ subarrays of `arr`.

Instead of generating every subarray ($\mathcal{O}(N^3)$) or summing every pair of prefix sums ($\mathcal{O}(N^2)$), count how many subarrays include index `i`:
- A subarray `[L..R]` contains index `i` if and only if $0 \le L \le i$ and $i \le R \le N - 1$.
- Number of choices for start $L$: $i + 1$.
- Number of choices for end $R$: $N - i$.
- Total subarrays containing `arr[i]`: $(i + 1)(N - i)$.

$$\text{Total Sum of All Subarrays} = \sum_{i=0}^{N-1} \text{arr}[i] \cdot (i + 1) \cdot (N - i)$$

```python
def total_subarray_sum(arr: list[int]) -> int:
    n = len(arr)
    return sum(val * (i + 1) * (n - i) for i, val in enumerate(arr))
```

### Algorithm steps:
* **1. Start index permutations:** Calculate available starting boundaries $L \in [0, i]$, giving exactly $(i + 1)$ valid left endpoints.
* **2. End index permutations:** Calculate available ending boundaries $R \in [i, N - 1]$, giving exactly $(N - i)$ valid right endpoints.
* **3. Contribution aggregation:** Multiply occurrences $(i + 1) \cdot (N - i)$ by element value $\text{arr}[i]$ and sum across all indices in $\mathcal{O}(N)$ time and $\mathcal{O}(1)$ space.


---

## 3. Core Subarray Scan Patterns

| Problem | Strategy | Time / Space | How It Works |
| :--- | :--- | :--- | :--- |
| **Leaders in Array** | Right-to-left max scan | $\mathcal{O}(N)$ / $\mathcal{O}(1)$ | Walk from $N-1$ down to $0$ tracking `max_right`; `arr[i]` is a leader if `arr[i] > max_right`. |
| **Closest Min-Max Subarray** | Last-seen index tracking | $\mathcal{O}(N)$ / $\mathcal{O}(1)$ | Track `last_min_idx` and `last_max_idx`; whenever either updates, record `abs(last_min_idx - last_max_idx) + 1`. |
| **Count Pairs `(i < j)` with `s[i]=='a', s[j]=='g'`** | Running suffix/prefix counter | $\mathcal{O}(N)$ / $\mathcal{O}(1)$ | Count `'a'`s seen so far; each `'g'` forms a valid pair with every `'a'` before it (`ans += a_count`). |
| **Maximum Subarray ([LC 53](../01_arrays_and_pointers/53_maximum_subarray.md))** | Kadane's Algorithm | $\mathcal{O}(N)$ / $\mathcal{O}(1)$ | Reset running sum to `nums[i]` whenever the previous prefix sum drops below `0`. |
| **Subarray Sum Equals K (LC 560)** | Prefix sum + hash map | $\mathcal{O}(N)$ / $\mathcal{O}(N)$ | Store frequencies of past prefix sums; add `freq[cur_sum - k]` at each step. |
