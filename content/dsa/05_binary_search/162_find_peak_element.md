# LeetCode 162: Find Peak Element

> **Difficulty:** Medium | **Pattern:** Binary Search by Local Slope (`nums[mid] < nums[mid + 1]`) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/find-peak-element/](https://leetcode.com/problems/find-peak-element/)

## The problem

A peak element is an element that is strictly greater than its neighbors (`nums[-1] = nums[n] = -∞` at boundaries). Given a 0-indexed integer array `nums` where `nums[i] != nums[i + 1]`, find any peak element and return its index in $\mathcal{O}(\log N)$ time.

---

## Why binary search works on an unsorted array

Because `nums[-1] = -∞` and `nums[n] = -∞` and adjacent values are never equal, **following an uphill slope guarantees you will hit a peak**:
* Either the slope keeps rising all the way to the boundary (making the boundary itself a peak), or it eventually drops (making the turning point a peak).

---

## The core trick: Compare `nums[mid]` with `nums[mid + 1]`

Use a converging `[lo, hi]` interval (`while lo < hi`):
* If `nums[mid] < nums[mid + 1]`: we are on a **rising slope**, so a peak definitely exists to the right (`lo = mid + 1`).
* Otherwise (`nums[mid] > nums[mid + 1]`): we are on a **falling slope**, so `mid` itself or something to its left is a peak (`hi = mid`).

---

## Step-by-step trace (`nums = [1, 2, 1, 3, 5, 6, 4]`)

**Iteration 1 (`lo = 0`, `hi = 6`):**
`mid = 3`. Compare `nums[3] = 3` vs `nums[4] = 5`.
Since `3 < 5` (rising slope ↗), move `lo = mid + 1 = 4`.
```text
Index:   0   1   2    3    4   5   6
nums:  [ 1,  2,  1,   3,   5,  6,  4 ]
        lo           mid          hi   (3 < 5 ↗ -> lo = 4)
```

**Iteration 2 (`lo = 4`, `hi = 6`):**
`mid = 5`. Compare `nums[5] = 6` vs `nums[6] = 4`.
Since `6 > 4` (falling slope ↘), move `hi = mid = 5`.
```text
Index:   0   1   2    3    4    5    6
nums:  [ x,  x,  x,   x,   5,   6,   4 ]
                          lo   mid   hi  (6 > 4 ↘ -> hi = 5)
```

**Iteration 3 (`lo = 4`, `hi = 5`):**
`mid = 4`. Compare `nums[4] = 5` vs `nums[5] = 6`.
Since `5 < 6` (rising slope ↗), move `lo = mid + 1 = 5`.

**Loop ends (`lo == hi == 5`):** Return `5` (`nums[5] = 6` is a peak!).

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        lo, hi = 0, len(nums) - 1

        while lo < hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] < nums[mid + 1]:
                lo = mid + 1    # Rising slope: peak is strictly to the right
            else:
                hi = mid        # Falling slope: mid or left holds a peak

        return lo
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(\log N)$
* **Space:** $\mathcal{O}(1)$
