# LeetCode 1492: The kth Factor of n

> **Pattern:** Symmetric factor pairing ($\mathcal{O}(\sqrt{N})$ iteration)  
> **Difficulty:** Medium  
> **Course reference:** CodeKerdos Class 3 Homework  
> **Link:** [LeetCode 1492](https://leetcode.com/problems/the-kth-factor-of-n/)

## The problem

Given two positive integers `n` and `k`, return the `k`-th factor of `n` in ascending order. If there are fewer than `k` factors, return `-1`.

```text
Input:  n = 12, k = 3
Output: 3 (Factors are [1, 2, 3, 4, 6, 12], 3rd factor is 3)
```

---

## Why `.sort()` is a trap in interviews

Collecting both `i` and `n // i` in an array and calling `lst.sort()` works on small inputs, but wastes time and memory:
1. `lst.sort()` costs $\mathcal{O}(d \log d)$ extra time on $d$ factors.
2. Allocating `lst` takes $\mathcal{O}(d)$ auxiliary memory when only a single integer is requested.

---

## The intuition bridge: Why factor pairs are already sorted

Every factor $i \le \sqrt{n}$ has a twin partner $n // i \ge \sqrt{n}$. Take $n = 24$:

```text
Small factors (i climbs 1 -> 4):       1,  2,  3,  4   (Ascending)
Large factors (n // i shrinks 24 -> 6): 24, 12,  8,  6   (Descending)
```

Notice the pattern:
- The small factors are already sorted ascending: `[1, 2, 3, 4]`.
- The large factors are sorted descending: `[24, 12, 8, 6]`.
- If you walk `i` backwards from $4$ down to $1$, the value of `n // i` naturally ascends: `6, 8, 12, 24`!

```text
Pass 1: i goes UP (1 -> 4)      ==>  Generates: 1, 2, 3, 4
Pass 2: i goes DOWN (4 -> 1)    ==>  n // i generates: 6, 8, 12, 24
Full combined order:                 1, 2, 3, 4, 6, 8, 12, 24
```

---

## Algorithm steps:

* **1. Pass 1 (Check small factors):** Loop `i` from $1$ while `i * i <= n`.
  * If `n % i == 0`, decrement `k`.
  * If `k == 0`, return `i` immediately.
* **2. Rewind `i`:** After the loop exits, `i` has overshot $\lfloor\sqrt{n}\rfloor$. Decrement `i` by 1.
* **3. Avoid square root duplicate:** If `i * i == n` (e.g. $6 \times 6 = 36$), decrement `i` once more so the square root is not visited twice.
* **4. Pass 2 (Check large partners):** Loop `i` backwards down to $1$.
  * If `n % i == 0`, decrement `k`.
  * If `k == 0`, return `n // i`.
* **5. Fallback:** If `k > 0` after both passes, fewer than `k` factors exist. Return `-1`.

---

<details>
<summary>Spoiler: Solution Code (O(sqrt(N)) Time, O(1) Space)</summary>

```python
class Solution:
    def kthFactor(self, n: int, k: int) -> int:
        i = 1
        # Pass 1: Check small factors (1 to sqrt(n))
        while i * i <= n:
            if n % i == 0:
                k -= 1
                if k == 0:
                    return i
            i += 1

        # Rewind i back to the largest valid integer checked
        i -= 1

        # Skip square root duplicate if n is a perfect square
        if i * i == n:
            i -= 1

        # Pass 2: Check large factors in ascending order by stepping i downward
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

## Complexity

* **Time Complexity:** $\mathcal{O}(\sqrt{n})$. At most $2\lfloor\sqrt{n}\rfloor$ loop steps.
* **Auxiliary Space:** $\mathcal{O}(1)$. Only an integer pointer `i` and input counter `k`.
