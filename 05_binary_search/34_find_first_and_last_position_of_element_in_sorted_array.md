# LeetCode 34: Find First and Last Position of Element in Sorted Array

> **Difficulty:** Medium | **Pattern:** Dual Binary Search (`ans` Bookmark + Squeeze Left / Right) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

## The problem

Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value in $\mathcal{O}(\log N)$ time. If `target` is not found, return `[-1, -1]`.

---

## Why linear expansion around `mid` fails

If `nums = [8, 8, 8, 8, 8, 8, 8]` and you find `8` at `mid`, walking left and right one step at a time degrades to $\mathcal{O}(N)$ worst-case time.

---

## The core trick: Bookmark `ans = mid` and keep binary searching

Run binary search **twice** using a helper `find_bound(is_first)`:
* When `nums[mid] == target`, save `ans = mid`, and **do not return yet**:
  * To find the **first** index (`is_first = True`), squeeze left: `hi = mid - 1`.
  * To find the **last** index (`is_first = False`), squeeze right: `lo = mid + 1`.

---

## Step-by-step trace (`nums = [5, 7, 7, 8, 8, 8, 10]`, `target = 8`)

### Pass 1: Finding First Occurrence (`hi = mid - 1` on match)

**Iteration 1 (`lo = 0`, `hi = 6`):**
`mid = 3`, `nums[3] = 8 == target`!
Bookmark `ans = 3`, squeeze left: `hi = 2`.
```text
Index:   0   1   2    3    4   5   6
nums:  [ 5,  7,  7,   8,   8,  8, 10 ]
        lo          mid           hi   -> ans = 3, hi moves to 2
```

**Iteration 2 (`lo = 0`, `hi = 2`):**
`mid = 1`, `nums[1] = 7 < 8` -> `lo = 2`.

**Iteration 3 (`lo = 2`, `hi = 2`):**
`mid = 2`, `nums[2] = 7 < 8` -> `lo = 3`. Loop ends, first occurrence = `3`.

### Pass 2: Finding Last Occurrence (`lo = mid + 1` on match)

* **Iteration 1 (`lo = 0, hi = 6`):** `mid = 3` (`8 == 8`) -> `ans = 3`, squeeze right `lo = 4`.
* **Iteration 2 (`lo = 4, hi = 6`):** `mid = 5` (`8 == 8`) -> `ans = 5`, squeeze right `lo = 6`.
* **Iteration 3 (`lo = 6, hi = 6`):** `mid = 6` (`10 > 8`) -> `hi = 5`. Loop ends, last occurrence = `5`.

Result: `[3, 5]`.

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        def find_bound(is_first: bool) -> int:
            lo, hi = 0, len(nums) - 1
            ans = -1
            while lo <= hi:
                mid = lo + (hi - lo) // 2
                if nums[mid] == target:
                    ans = mid
                    if is_first:
                        hi = mid - 1  # Keep searching left
                    else:
                        lo = mid + 1  # Keep searching right
                elif nums[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return ans

        first = find_bound(True)
        if first == -1:
            return [-1, -1]
        return [first, find_bound(False)]
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(\log N)$ (two binary searches).
* **Space:** $\mathcal{O}(1)$.
