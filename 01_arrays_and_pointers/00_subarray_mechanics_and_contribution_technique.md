# Subarray mechanics and the contribution technique

> **Course reference:** CodeKerdos DSA, Class 6
> **Core concepts:** Total subarrays formula $N(N+1)/2$, closest min-max subarray, and the $\mathcal{O}(N)$ contribution technique.

## Subarray vs subsequence vs subset

| Structure | Contiguous? | Order preserved? | Count for size $N$ |
|---|---|---|---|
| Subarray | Yes (unbroken slice) | Yes | $\frac{N(N + 1)}{2}$ |
| Subsequence | No (can skip elements) | Yes | $2^N - 1$ (non-empty) |
| Subset | No | No | $2^N$ |

An array of size $N$ has $N$ subarrays starting at index $0$, $N - 1$ starting at index $1$, down to $1$ starting at index $N - 1$. Summing $N + (N - 1) + \dots + 1$ gives $\frac{N(N + 1)}{2}$.

## Closest min-max subarray in $\mathcal{O}(N)$

Find the length of the shortest contiguous subarray containing both the global minimum and global maximum of `ar`.

If `min_val == max_val`, the answer is $1$. Otherwise, scan left to right while tracking `last_min` and `last_max` (the most recent indices where `min_val` and `max_val` appeared). Whenever you hit a min or max and both indices have been seen, update `min_len = min(min_len, abs(last_min - last_max) + 1)`.

| Index $i$ | `ar[i]` | `last_min` (val=1) | `last_max` (val=6) | Candidate length | `min_len` |
|---|---|---|---|---|---|
| 0 | 1 | 0 | -1 | - | 10 |
| 3 | 1 | 3 | -1 | - | 10 |
| 6 | 6 | 3 | 6 | $6 - 3 + 1 = 4$ | 4 |
| 8 | 6 | 3 | 8 | $8 - 3 + 1 = 6$ | 4 |

<details>
<summary>Spoiler: Solution Code</summary>

```python
def closest_min_max_subarray(ar: list[int]) -> int:
    n = len(ar)
    if n == 0:
        return 0

    min_val, max_val = min(ar), max(ar)
    if min_val == max_val:
        return 1

    last_min = -1
    last_max = -1
    min_len = n

    for i, val in enumerate(ar):
        if val == min_val:
            last_min = i
            if last_max != -1:
                min_len = min(min_len, i - last_max + 1)
        elif val == max_val:
            last_max = i
            if last_min != -1:
                min_len = min(min_len, i - last_min + 1)

    return min_len
```

</details>

## Sum of all subarrays: the contribution technique

Find the sum of elements across all $\frac{N(N+1)}{2}$ subarrays. Generating every subarray takes $\mathcal{O}(N^3)$ time, and using prefix sums still takes $\mathcal{O}(N^2)$. Instead of summing each subarray separately, count how many subarrays include index $i$.

```text
Array indices:   0    1    2   ...   i   ...   N-2   N-1
                 └─────────────┘         └──────────────┘
                    (i + 1)                   (N - i)
                 choices for L             choices for R
```

For a subarray $[L, R]$ to contain index $i$, the start index $L$ has $i + 1$ choices ($0 \le L \le i$) and the end index $R$ has $N - i$ choices ($i \le R \le N - 1$). Thus `ar[i]` appears in $(i + 1)(N - i)$ subarrays, contributing $ar[i] \cdot (i + 1) \cdot (N - i)$ to the total sum:

$$\text{Total Sum} = \sum_{i=0}^{N-1} ar[i] \cdot (i + 1) \cdot (N - i)$$

<details>
<summary>Spoiler: Solution Code</summary>

```python
def total_subarray_sum(ar: list[int]) -> int:
    n = len(ar)
    total = 0
    for i in range(n):
        total += ar[i] * (i + 1) * (n - i)
    return total
```

</details>

* **Time complexity:** $\mathcal{O}(N)$ for both algorithms.
* **Space complexity:** $\mathcal{O}(1)$.
