# LeetCode 88: Merge Sorted Array

> **Difficulty:** Easy | **Pattern:** Two Pointers (Tail-Buffer / Reverse Placement)  
> **Constraints:** $\mathcal{O}(m + n)$ time, $\mathcal{O}(1)$ auxiliary space in-place.

## The problem

Given two sorted integer arrays `nums1` and `nums2` with `m` and `n` valid elements respectively, merge `nums2` into `nums1` in-place so `nums1` becomes a single sorted array of length `m + n`. The array `nums1` has a total length of `m + n`, where the last `n` slots are padded with `0`s to hold the merged result.

## Why merging from the front fails

Writing `nums1[m:] = nums2; nums1.sort()` takes $\mathcal{O}((m + n) \log(m + n))$ time and ignores that both arrays are already sorted.

If you try to merge left-to-right into `nums1[0]`, you immediately overwrite unread values in `nums1`:

```text
nums1 = [ 2, 5, 6, 0, 0, 0 ], m = 3
nums2 = [ 1, 3, 4 ],          n = 3

Comparing nums1[0] (2) and nums2[0] (1):
Writing 1 into nums1[0] overwrites 2 before 2 has been placed anywhere.
```

## The core trick: Fill backward from the tail buffer

The only safe place to write without destroying unread numbers is the zero-padded tail at the end of `nums1`. And in a sorted array, the numbers that belong at the back are the **largest** numbers.

Start three pointers at the back and move right-to-left:
- `p1 = m - 1`: last valid element in `nums1`
- `p2 = n - 1`: last element in `nums2`
- `p = m + n - 1`: write pointer at the very end of `nums1`

```text
nums1 = [ 2 , 5 , 6 , 0 , 0 , 0 ]     nums2 = [ 1 , 3 , 4 ]
                  ^           ^                         ^
                  p1          p                         p2
```

At each step, compare `nums1[p1]` and `nums2[p2]`, place the larger value at `nums1[p]`, and decrement the corresponding pointers.

### Algorithm steps:
* **1. Initialize three pointers at tails:** Set `p1 = m - 1` (last item in `nums1`), `p2 = n - 1` (last item in `nums2`), and writer pointer `p = m + n - 1` (end of `nums1` buffer).
* **2. Merge from back to front:** While `p1 >= 0` and `p2 >= 0`:
  * If `nums1[p1] > nums2[p2]`, write `nums1[p] = nums1[p1]` and decrement `p1 -= 1`.
  * Otherwise, write `nums1[p] = nums2[p2]` and decrement `p2 -= 1`.
  * Decrement writer `p -= 1`.
* **3. Flush remaining elements from nums2:** While `p2 >= 0`, write `nums1[p] = nums2[p2]` and decrement both `p2 -= 1` and `p -= 1` (any remaining `nums1` elements are already in their correct places).
* **4. Termination:** `nums1` is sorted in-place in $\mathcal{O}(m + n)$ time and $\mathcal{O}(1)$ space.

## Step-by-step trace

Tracing `nums1 = [2, 5, 6, 0, 0, 0]` (`m = 3`) and `nums2 = [1, 3, 4]` (`n = 3`):

| Step | `p1` (`nums1[p1]`) | `p2` (`nums2[p2]`) | Larger value | Write to `nums1[p]` | `nums1` after step |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `2` (`6`) | `2` (`4`) | `6` (from `nums1`) | `nums1[5] = 6` | `[2, 5, 6, 0, 0, 6]` |
| 2 | `1` (`5`) | `2` (`4`) | `5` (from `nums1`) | `nums1[4] = 5` | `[2, 5, 6, 0, 5, 6]` |
| 3 | `0` (`2`) | `2` (`4`) | `4` (from `nums2`) | `nums1[3] = 4` | `[2, 5, 6, 4, 5, 6]` |
| 4 | `0` (`2`) | `1` (`3`) | `3` (from `nums2`) | `nums1[2] = 3` | `[2, 5, 3, 4, 5, 6]` |
| 5 | `0` (`2`) | `0` (`1`) | `2` (from `nums1`) | `nums1[1] = 2` | `[2, 2, 3, 4, 5, 6]` |
| Cleanup | `-1` (done) | `0` (`1`) | Copy remaining `nums2` | `nums1[0] = 1` | `[1, 2, 3, 4, 5, 6]` |

### Why we only clean up `p2 >= 0` (and not `p1 >= 0`)

If `p1` runs out first (`p1 < 0`), the remaining smallest elements are still sitting in `nums2` and must be copied into `nums1[:p2 + 1]`. If `p2` runs out first (`p2 < 0`), the remaining smallest elements are already in `nums1[:p1 + 1]` in sorted order, so no extra work is needed.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        p1 = m - 1
        p2 = n - 1
        p = m + n - 1

        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p1 -= 1
            else:
                nums1[p] = nums2[p2]
                p2 -= 1
            p -= 1

        # Copy any leftover smaller elements from nums2
        while p2 >= 0:
            nums1[p] = nums2[p2]
            p2 -= 1
            p -= 1
```

</details>

## Complexity & related problems

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(m + n)$ | Each step places one element into its final position in `nums1`. |
| **Space** | $\mathcal{O}(1)$ | Uses three integer pointers (`p1`, `p2`, `p`). |

Other problems that use reverse in-place traversal to avoid overwriting or extra memory:
- **LC 977: Squares of a Sorted Array** (compare outer extremes, fill result array from back to front)
- **LC 844: Backspace String Compare** (scan right-to-left to count `#` backspaces in $\mathcal{O}(1)$ space)
- **[LC 66: Plus One](./66_plus_one.md)** (propagate carry from right to left)
