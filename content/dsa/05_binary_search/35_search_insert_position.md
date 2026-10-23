# LeetCode 35: Search Insert Position

> **Difficulty:** Easy | **Pattern:** Lower Bound Binary Search (First Index with `nums[i] >= target`) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/search-insert-position/](https://leetcode.com/problems/search-insert-position/)

## The problem

Given a sorted array of distinct integers `nums` and a `target` value, return the index if the target is found. If not, return the index where it would be if it were inserted in order. Must run in $\mathcal{O}(\log N)$ time.

---

## The core trick: Why `lo` lands on the exact insertion index

Run standard binary search (`while lo <= hi`):
* Every index strictly to the **left of `lo`** has `nums[i] < target`.
* Every index strictly to the **right of `hi`** has `nums[i] > target`.
When the loop ends because `lo > hi` (`lo == hi + 1`), `lo` is guaranteed to be the **first index where `nums[i] >= target`** (or `len(nums)` if all elements are smaller than `target`).

---

## Step-by-step trace (`nums = [1, 3, 5, 6]`, `target = 2`)

**Iteration 1 (`lo = 0`, `hi = 3`):**
`mid = 1`, `nums[1] = 3`. Since `3 > 2`, move `hi = mid - 1 = 0`.
```text
Index:   0    1    2    3
nums:  [ 1,   3,   5,   6 ]
        lo   mid       hi   (3 > 2 -> hi = 0)
```

**Iteration 2 (`lo = 0`, `hi = 0`):**
`mid = 0`, `nums[0] = 1`. Since `1 < 2`, move `lo = mid + 1 = 1`.
```text
Index:   0    1    2    3
nums:  [ 1,   3,   5,   6 ]
      lo,hi                 (1 < 2 -> lo = 1)
```

**Loop ends (`lo = 1 > hi = 0`):**
Return `lo = 1` (inserting `2` at index `1` gives `[1, 2, 3, 5, 6]`).

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1

        return lo
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(\log N)$
* **Space:** $\mathcal{O}(1)$
