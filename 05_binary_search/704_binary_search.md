# LeetCode 704: Binary Search

> **Difficulty:** Easy | **Pattern:** Standard Closed-Interval Binary Search (`lo <= hi`) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/binary-search/](https://leetcode.com/problems/binary-search/)

## The problem

Given an array of integers `nums` sorted in ascending order and an integer `target`, write a function to search `target` in `nums`. If `target` exists, return its index. Otherwise, return `-1`. You must write an algorithm with $\mathcal{O}(\log N)$ runtime complexity.

---

## The core trick: Halving the closed search space `[lo, hi]`

Maintain two pointers `lo = 0` and `hi = len(nums) - 1`.
While `lo <= hi`:
1. Compute `mid = lo + (hi - lo) // 2`.
2. If `nums[mid] == target`, return `mid`.
3. If `nums[mid] < target`, every index $\le \text{mid}$ is too small, so set `lo = mid + 1`.
4. If `nums[mid] > target`, every index $\ge \text{mid}$ is too large, so set `hi = mid - 1`.

---

## Step-by-step trace (`nums = [-1, 0, 3, 5, 9, 12]`, `target = 9`)

**Iteration 1 (`lo = 0`, `hi = 5`):**
`mid = 0 + (5 - 0) // 2 = 2`, `nums[2] = 3`.
Since `3 < 9`, discard left half -> `lo = mid + 1 = 3`.
```text
Index:    0    1    2    3    4    5
nums:  [ -1,   0,   3,   5,   9,  12 ]
         lo        mid            hi
                   (3 < 9 -> lo moves to 3)
```

**Iteration 2 (`lo = 3`, `hi = 5`):**
`mid = 3 + (5 - 3) // 2 = 4`, `nums[4] = 9`.
Since `nums[4] == 9`, return `4`!
```text
Index:    0    1    2    3    4    5
nums:  [  x,   x,   x,   5,   9,  12 ]
                        lo   mid  hi
                             (9 == 9 -> Found at index 4!)
```

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1

        return -1
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(\log N)$
* **Space:** $\mathcal{O}(1)$
