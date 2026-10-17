# 🧩 Subarray Mechanics & The Contribution Technique

> **Course Reference:** CodeKerdos DSA — Class 6  
> **Core Concepts:** Total subarrays formula $N(N+1)/2$, Closest Min-Max subarray, and the $\mathcal{O}(N)$ Contribution Technique for total subarray sum.

---

## 1. Subarray vs Subsequence vs Subset

| Structure | Contiguous? | Order Preserved? | Total Count for Array of Size $N$ |
|---|---|---|---|
| **Subarray** | ✅ **Yes** (unbroken slice) | ✅ **Yes** | $\frac{N(N + 1)}{2}$ |
| **Subsequence** | ❌ No (can skip elements) | ✅ **Yes** | $2^N - 1$ (non-empty) |
| **Subset** | ❌ No | ❌ No (order doesn't matter) | $2^N$ |

### Why Are There $\frac{N(N+1)}{2}$ Subarrays?
* Subarrays starting at index $0$: $N$ choices ($[0,0], [0,1], \dots, [0, N-1]$)
* Subarrays starting at index $1$: $N - 1$ choices
* $\dots$
* Subarrays starting at index $N-1$: $1$ choice
$$\text{Total} = N + (N - 1) + (N - 2) + \dots + 1 = \frac{N(N + 1)}{2}$$

---

## 2. Closest Min-Max Subarray in $\mathcal{O}(N)$

Given an array, find the length of the **smallest contiguous subarray** that contains both the minimum element and the maximum element of the array.

```text
Input:  ar = [ 1 , 2 , 3 , 1 , 3 , 4 , 6 , 4 , 6 , 3 ]
Min value = 1, Max value = 6

Subarrays containing both 1 and 6:
- Indices 0 to 6: length 7
- Indices 3 to 6: length 4 (ar[3..6] = [1, 3, 4, 6])
Smallest length = 4
```

### The State-Tracking Algorithm
* Find `min_val = min(ar)` and `max_val = max(ar)`.
* If `min_val == max_val`, return $1$.
* Maintain two pointers tracking the **latest seen index** of each: `last_min = -1`, `last_max = -1`.
* Traverse from left to right:
  * When `ar[i] == min_val`: update `last_min = i`.
  * When `ar[i] == max_val`: update `last_max = i`.
  * If both `last_min != -1` and `last_max != -1`:
    $$\text{current\_len} = |\text{last\_min} - \text{last\_max}| + 1$$
    $$\text{ans} = \min(\text{ans}, \text{current\_len})$$

```python
def closest_min_max_subarray(ar: list[int]) -> int:
    n = len(ar)
    if n == 0:
        return 0

    min_val = min(ar)
    max_val = max(ar)

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
* **Time Complexity:** $\mathcal{O}(N)$ (One linear pass).
* **Auxiliary Space:** $\mathcal{O}(1)$.

---

## 3. Sum of All Subarrays: The Contribution Technique

> **Problem:** Find the sum of all elements across every possible subarray in `ar`.

### Complexity Ladder
1. **Brute Force:** Generate all $N(N+1)/2$ subarrays, loop through each to sum $\to \mathcal{O}(N^3)$.
2. **Prefix Sums:** Generate all pairs $(i, j)$ and get range sums in $\mathcal{O}(1) \to \mathcal{O}(N^2)$.
3. **The Contribution Technique:** Flip perspective from "subarrays" to **"elements"** $\to \mathcal{O}(N)$!

---

### The Derivation (Combinatorics Perspective)
Instead of asking: *"What is the sum of each subarray?"*  
Ask: **"How many subarrays contain `ar[i]`?"**

For a subarray $[L, R]$ to contain index $i$:
* Start index $L$ must be anywhere in $[0, i]$ $\implies (i + 1)$ valid choices.
* End index $R$ must be anywhere in $[i, N - 1]$ $\implies (N - i)$ valid choices.

```text
Array indices:   0    1    2   ...   i   ...   N-2   N-1
                 └─────────────┘         └──────────────┘
                    (i + 1)                   (N - i)
                 choices for L             choices for R
```

By the fundamental counting principle:
$$\text{Total subarrays containing } ar[i] = (i + 1) \times (N - i)$$

Since `ar[i]` appears in $(i + 1)(N - i)$ distinct subarrays, its total contribution to the grand sum is:
$$\text{Contribution}(ar[i]) = ar[i] \times (i + 1) \times (N - i)$$

### Total Sum Formula
$$\text{Total Sum} = \sum_{i=0}^{N-1} ar[i] \cdot (i + 1) \cdot (N - i)$$

```python
def total_subarray_sum(ar: list[int]) -> int:
    n = len(ar)
    total = 0
    for i in range(n):
        occurrences = (i + 1) * (n - i)
        total += ar[i] * occurrences
    return total
```

* **Time Complexity:** $\mathcal{O}(N)$ (Single loop, no nested passes).
* **Auxiliary Space:** $\mathcal{O}(1)$.
