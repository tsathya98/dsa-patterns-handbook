# LeetCode 1482: Minimum Number of Days to Make m Bouquets

> **Difficulty:** Medium | **Pattern:** Binary Search on Answer + Greedy Adjacent Streak Count | **Access:** Free  
> **Link:** [https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)

## The problem

You are given `bloomDay`, an integer `m` (number of bouquets needed), and an integer `k` (adjacent flowers required per bouquet). Return the **minimum number of days** you need to wait to make `m` bouquets from the garden. If it is impossible, return `-1`.

---

## The core trick: Binary search on `day` + greedy streak counter

1. **Impossible check first:** If `m * k > len(bloomDay)`, you don't even have enough flowers in the entire garden. Immediately return `-1`.
2. **Binary search on `day` in `[min(bloomDay), max(bloomDay)]`:**
   * For a candidate `day`, sweep left-to-right counting consecutive bloomed flowers (`b <= day`):
     * If `b <= day`, increment `streak += 1`. Whenever `streak == k`, increment `bouquets += 1` and reset `streak = 0`.
     * If `b > day` (unbloomed flower breaks adjacency), reset `streak = 0`.
   * If `bouquets >= m`, `day` is feasible (`ans = day`, squeeze left `hi = day - 1`). Otherwise `lo = day + 1`.

---

## Step-by-step trace (`bloomDay = [1, 10, 3, 10, 2]`, `m = 3`, `k = 1`)

Total flowers needed = `3 * 1 = 3 <= 5`. Search range: `lo = 1, hi = 10`.

**Iteration 1 (`lo = 1`, `hi = 10`):**
`day = 5`. Which flowers have bloomed (`<= 5`)?
`[1 (✓), 10 (✗), 3 (✓), 10 (✗), 2 (✓)]` -> `3` bouquets of size `1`!
Since `3 >= 3` (Valid!), record `ans = 5`, try earlier: `hi = 4`.

**Iteration 2 (`lo = 1`, `hi = 4`):**
`day = 2`. Which flowers have bloomed (`<= 2`)?
`[1 (✓), 10 (✗), 3 (✗), 10 (✗), 2 (✓)]` -> only `2` bouquets (`< 3`, Invalid!).
Need more days: `lo = 3`.

**Iteration 3 (`lo = 3`, `hi = 4`):**
`day = 3`. Which flowers have bloomed (`<= 3`)?
`[1 (✓), 10 (✗), 3 (✓), 10 (✗), 2 (✓)]` -> `3` bouquets (`>= 3`, Valid!).
Record `ans = 3`, try earlier: `hi = 2`.

**Loop ends (`lo = 3 > hi = 2`):** Return `ans = 3`.

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def minDays(self, bloomDay: list[int], m: int, k: int) -> int:
        if m * k > len(bloomDay):
            return -1

        def can_make(day: int) -> bool:
            bouquets = 0
            streak = 0
            for b in bloomDay:
                if b <= day:
                    streak += 1
                    if streak == k:
                        bouquets += 1
                        streak = 0
                else:
                    streak = 0
            return bouquets >= m

        lo, hi = min(bloomDay), max(bloomDay)
        ans = hi

        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if can_make(mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        return ans
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(N \log(\max(\text{bloomDay})))$
* **Space:** $\mathcal{O}(1)$
