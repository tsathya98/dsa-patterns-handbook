# LeetCode 875: Koko Eating Bananas

> **Difficulty:** Medium | **Pattern:** Binary Search on Answer Space `[1, max(piles)]` | **Access:** Free  
> **Link:** [https://leetcode.com/problems/koko-eating-bananas/](https://leetcode.com/problems/koko-eating-bananas/)

## The problem

Koko has `n` piles of bananas (`piles[i]`) and `h` hours before the guards return. Each hour, she chooses one pile and eats `k` bananas from it (if the pile has fewer than `k`, she eats all of them and waits until the next hour). Return the **minimum integer speed `k`** such that she can eat all bananas within `h` hours.

---

## The core trick: Binary search on speed `k`

Instead of searching the `piles` array, binary search the **eating speed `k`** in the range `[1, max(piles)]`:
* At speed `k`, a pile of size `p` takes $\lceil p / k \rceil = \text{ (p + k - 1) // k }$ hours.
* **Monotonicity:** If speed `k` finishes in $\le h$ hours (`True`), any faster speed $> k$ will also finish in $\le h$ hours. We want the **first `True` (smallest valid `k`)**.

---

## Step-by-step trace (`piles = [3, 6, 7, 11]`, `h = 8`)

**Search space:** `lo = 1`, `hi = max(piles) = 11`

**Iteration 1 (`lo = 1`, `hi = 11`):**
`mid = 6` bananas/hr.
Hours needed: `ceil(3/6) + ceil(6/6) + ceil(7/6) + ceil(11/6) = 1 + 1 + 2 + 2 = 6 <= 8` (**Valid!**).
Record `ans = 6`, try slower speed: `hi = 5`.

**Iteration 2 (`lo = 1`, `hi = 5`):**
`mid = 3` bananas/hr.
Hours needed: `ceil(3/3) + ceil(6/3) + ceil(7/3) + ceil(11/3) = 1 + 2 + 3 + 4 = 10 > 8` (**Too slow!**).
Must eat faster: `lo = mid + 1 = 4`.

**Iteration 3 (`lo = 4`, `hi = 5`):**
`mid = 4` bananas/hr.
Hours needed: `ceil(3/4) + ceil(6/4) + ceil(7/4) + ceil(11/4) = 1 + 2 + 2 + 3 = 8 <= 8` (**Valid!**).
Record `ans = 4`, try slower: `hi = 3`.

**Loop ends (`lo = 4 > hi = 3`):** Return `ans = 4`.

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        lo, hi = 1, max(piles)
        ans = hi

        while lo <= hi:
            k = lo + (hi - lo) // 2
            hours = sum((p + k - 1) // k for p in piles)

            if hours <= h:
                ans = k
                hi = k - 1  # Try to find an even smaller valid speed
            else:
                lo = k + 1  # Too slow, increase speed

        return ans
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(N \log(\max(\text{piles})))$
* **Space:** $\mathcal{O}(1)$
