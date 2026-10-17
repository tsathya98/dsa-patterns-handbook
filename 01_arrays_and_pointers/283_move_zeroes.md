# LeetCode 283: Move Zeroes

> **Difficulty:** Easy | **Pattern:** Two Pointers (Scout and Writer)  
> **LeetCode:** [283. Move Zeroes](https://leetcode.com/problems/move-zeroes/)

## The problem

Given an integer array `nums`, move all `0`s to the end while keeping the relative order of the non-zero elements. Modify `nums` in-place in $\mathcal{O}(1)$ extra space.

```text
Input:  nums = [0, 1, 0, 3, 12]
Output: [1, 3, 12, 0, 0]
```

## The core trick: Swap across the wall of zeros

Deleting each `0` and shifting the remaining elements left takes $\mathcal{O}(n^2)$ time. Instead, use two pointers moving left to right:
- **`fast` (Scout):** Scans every index looking for non-zero numbers.
- **`slow` (Writer):** Points to the leftmost `0` (the front of the wall of zeros), which is where the next non-zero number belongs.

At every step, the array is partitioned into three regions:

```text
[ Non-Zeros (0 .. slow-1) ] | [ Wall of 0s (slow .. fast-1) ] | [ Unexplored (fast .. n-1) ]
                              ^                                 ^
                            slow                              fast
```

Whenever `nums[fast] != 0`, swap `nums[slow]` and `nums[fast]`, then advance `slow += 1`.

### Algorithm steps:
* **1. Initialize slow pointer:** Set `slow = 0` to mark the position where the next non-zero element belongs.
* **2. Iterate fast pointer:** Loop `fast` from `0` to `len(nums) - 1`.
* **3. Swap non-zeros forward:**
  * If `nums[fast] != 0`, swap `nums[slow]` and `nums[fast]`, then advance `slow += 1`.
  * If `nums[fast] == 0`, skip and leave `slow` waiting on the zero.
* **4. Termination:** Modifies array in-place in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.

### Why `slow += 1` always lands on a zero

Every element between `slow` and `fast - 1` is guaranteed to be `0`. When you swap `nums[slow]` with `nums[fast]`, the non-zero value goes to `slow`, the `0` gets kicked to `fast`, and `slow + 1` is already the next `0` in the wall. If `slow == fast` (no zeros seen yet), the element swaps with itself and both pointers step forward together.

## Step-by-step trace

Tracing `nums = [0, 1, 0, 0, 3, 12]`:

| `fast` | `nums[fast]` | `slow` (before) | Action | Array after step | `slow` (after) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `0` | `0` | Skip (`slow` waits at `0`) | `[0, 1, 0, 0, 3, 12]` | `0` |
| `1` | `1` | `0` | Swap indices `0` and `1` | `[1, 0, 0, 0, 3, 12]` | `1` |
| `2` | `0` | `1` | Skip (wall of 0s grows) | `[1, 0, 0, 0, 3, 12]` | `1` |
| `3` | `0` | `1` | Skip (wall of 0s grows) | `[1, 0, 0, 0, 3, 12]` | `1` |
| `4` | `3` | `1` | Swap indices `1` and `4` | `[1, 3, 0, 0, 0, 12]` | `2` |
| `5` | `12` | `2` | Swap indices `2` and `5` | `[1, 3, 12, 0, 0, 0]` | `3` |

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1
```

</details>

## Complexity

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n)$ | Single pass with `fast`; each element is visited once. |
| **Space** | $\mathcal{O}(1)$ | Swaps elements in-place using two integer pointers. |
