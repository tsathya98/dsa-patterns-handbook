# LeetCode 540: Single Element in a Sorted Array

> **Difficulty:** Medium | **Pattern:** Index Parity Invariant (`mid ^ 1` or Even-Index Alignment) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/single-element-in-a-sorted-array/](https://leetcode.com/problems/single-element-in-a-sorted-array/)

## The problem

You are given a sorted array `nums` consisting of only integers where every element appears **exactly twice**, except for one element which appears **exactly once**. Return the single element in $\mathcal{O}(\log N)$ time and $\mathcal{O}(1)$ space.

---

## The core trick: Even/Odd pair index alignment

Before the single element appears, every duplicate pair starts at an **EVEN** index and ends at an **ODD** index: `(0, 1), (2, 3), (4, 5)`.
Once the single element appears (taking up 1 slot), every pair after it gets shifted by 1 and starts at an **ODD** index and ends at an **EVEN** index!

```text
Index:    0  1    2  3    4    5  6    7  8
nums:   [ 1, 1,   2, 2,   3,   4, 4,   8, 8 ]
         (even,   (even,  ^   (odd,   (odd,
          odd)     odd) single even)   even)
```

In binary search (`while lo < hi`):
1. Snap `mid` to an **even** index: `if mid % 2 == 1: mid -= 1`.
2. Check if the pair `(mid, mid + 1)` is intact:
   * If `nums[mid] == nums[mid + 1]`: the single element hasn't appeared yet -> search right (`lo = mid + 2`).
   * If `nums[mid] != nums[mid + 1]`: the alignment is broken here or to the left -> search left (`hi = mid`).

---

## Step-by-step trace (`nums = [1, 1, 2, 3, 3, 4, 4, 8, 8]`)

**Iteration 1 (`lo = 0`, `hi = 8`):**
`mid = 4` (already even). Compare `nums[4] = 3` vs `nums[5] = 4`.
Since `3 != 4`, the pair `(4, 5)` is broken! The single element is at `<= 4` -> `hi = 4`.
```text
Index:   0  1  2  3   4   5  6  7  8
nums:  [ 1, 1, 2, 3,  3,  4, 4, 8, 8 ]
        lo           mid           hi   (nums[4] != nums[5] -> hi = 4)
```

**Iteration 2 (`lo = 0`, `hi = 4`):**
`mid = 2` (even). Compare `nums[2] = 2` vs `nums[3] = 3`.
Since `2 != 3`, broken! -> `hi = 2`.
```text
Index:   0  1   2   3   4
nums:  [ 1, 1,  2,  3,  3 ]
        lo     mid     hi   (nums[2] != nums[3] -> hi = 2)
```

**Iteration 3 (`lo = 0`, `hi = 2`):**
`mid = 1` (odd -> snap to even `mid = 0`). Compare `nums[0] = 1` vs `nums[1] = 1`.
Since `1 == 1`, pair `(0, 1)` is intact! -> `lo = mid + 2 = 2`.

**Loop ends (`lo == hi == 2`):** Return `nums[2] = 2`.

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def singleNonDuplicate(self, nums: list[int]) -> int:
        lo, hi = 0, len(nums) - 1

        while lo < hi:
            mid = lo + (hi - lo) // 2
            if mid % 2 == 1:
                mid -= 1  # Always align mid to an even index

            if nums[mid] == nums[mid + 1]:
                lo = mid + 2  # Pair is intact, single element is on the right
            else:
                hi = mid      # Pair is broken, single element is at mid or left

        return nums[lo]
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(\log N)$
* **Space:** $\mathcal{O}(1)$
