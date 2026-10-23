# LeetCode 1492: The kth Factor of n

> **Pattern:** Symmetric factor pairing ($\mathcal{O}(\sqrt{N})$ iteration)  
> **Difficulty:** Medium | **Course reference:** CodeKerdos Class 3 Homework  
> **Source Code:** [`1492_the_kth_factor_of_n.py`](1492_the_kth_factor_of_n.py) | **Link:** [LeetCode 1492](https://leetcode.com/problems/the-kth-factor-of-n/)

## The problem

Given two positive integers `n` and `k`, return the `k`-th factor of `n` in ascending order. If there are fewer than `k` factors, return `-1`.

```text
Input:  n = 12, k = 3
Output: 3 (Factors are [1, 2, 3, 4, 6, 12], 3rd factor is 3)
```

---

## Approach 1: Brute force (linear scan)

Loop `i` from $1$ to $n$. Check if `n % i == 0`, decrement `k`, and return `i` when `k == 0`.
* **Pros:** Trivially simple to write.
* **Cons:** Runs in $\mathcal{O}(n)$ time. If $n = 10^9$, it times out (TLE).

---

## Approach 2: Semi-optimized (symmetric pairs with sort)

Since factors come in pairs `(i, n // i)`, loop only while `i * i <= n`. Store both `i` and `n // i` in an array `factors` (handling perfect squares once), sort the array, and return `factors[k - 1]`.

```text
n = 24:
Pairs found: (1, 24), (2, 12), (3, 8), (4, 6)
factors list: [1, 24, 2, 12, 3, 8, 4, 6]  -> .sort() -> [1, 2, 3, 4, 6, 8, 12, 24]
```

* **Pros:** Cuts the search loop to $\mathcal{O}(\sqrt{n})$ iterations. Highly intuitive.
* **Cons:** Requires $\mathcal{O}(d)$ extra memory and pays an $\mathcal{O}(d \log d)$ sorting penalty.

---

## Approach 3: Optimized (two-pass monotonic count in $\mathcal{O}(1)$ space)

Notice that factor pairs are already sorted:
* Small factors `i` ascend: `1, 2, 3, 4`.
* Large factors `n // i` descend: `24, 12, 8, 6`. Stepping `i` backward from $4$ down to $1$ generates `n // i` in ascending order: `6, 8, 12, 24`!

```text
Pass 1: i goes UP (1 -> 4)    ==> Generates: 1, 2, 3, 4
Pass 2: i goes DOWN (4 -> 1)  ==> n // i generates: 6, 8, 12, 24
Full combined order:              1, 2, 3, 4, 6, 8, 12, 24
```

### Algorithm steps:
* **1. Pass 1 (Small factors):** Loop `i` from $1$ while `i * i <= n`. On factor, decrement `k`. If `k == 0`, return `i`.
* **2. Rewind `i`:** Decrement `i` by 1 to reset it to the largest integer tested.
* **3. Handle square root:** If `i * i == n`, decrement `i` again so the square root is not visited twice.
* **4. Pass 2 (Large factors):** Loop `i` down to $1$. On factor, decrement `k`. If `k == 0`, return `n // i`.
* **5. Fallback:** If `k > 0`, return `-1`.

---

<details>
<summary>Spoiler: Solution Code (All 3 Approaches)</summary>

```python
class Solution:
    # Approach 1: Brute force (O(N) time, O(1) space)
    def kthFactor_brute(self, n: int, k: int) -> int:
        for i in range(1, n + 1):
            if n % i == 0:
                k -= 1
                if k == 0:
                    return i
        return -1

    # Approach 2: Semi-optimized (O(sqrt(N) + d log d) time, O(d) space)
    def kthFactor_semi_opt(self, n: int, k: int) -> int:
        factors = []
        i = 1
        while i * i <= n:
            if n % i == 0:
                factors.append(i)
                if i * i != n:
                    factors.append(n // i)
            i += 1
        factors.sort()
        return factors[k - 1] if k <= len(factors) else -1

    # Approach 3: Optimized two-pass (O(sqrt(N)) time, O(1) space)
    def kthFactor(self, n: int, k: int) -> int:
        i = 1
        while i * i <= n:
            if n % i == 0:
                k -= 1
                if k == 0:
                    return i
            i += 1

        i -= 1
        if i * i == n:
            i -= 1

        while i >= 1:
            if n % i == 0:
                k -= 1
                if k == 0:
                    return n // i
            i -= 1

        return -1
```

</details>

---

## Complexity comparison

| Approach | Time Complexity | Auxiliary Space | Status |
|---|---|---|---|
| **1. Brute Force** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | TLE on large $n$ |
| **2. Semi-Optimized** | $\mathcal{O}(\sqrt{n} + d \log d)$ | $\mathcal{O}(d)$ | Accepted, but uses sort & list |
| **3. Optimized** | $\mathcal{O}(\sqrt{n})$ | $\mathcal{O}(1)$ | Optimal FAANG bar |
