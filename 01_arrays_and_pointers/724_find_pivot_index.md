# LeetCode 724: Find Pivot Index

> **Difficulty:** Easy | **Pattern:** Prefix Sum (Total Sum Conservation)  
> **LeetCode:** [724. Find Pivot Index](https://leetcode.com/problems/find-pivot-index/)

## The problem

Given an integer array `nums`, return the leftmost **pivot index** where the sum of all numbers strictly to the left of the index equals the sum of all numbers strictly to the right. If no such index exists, return `-1`. (At index `0`, the left sum is `0`; at index `n - 1`, the right sum is `0`.)

```text
Input:  nums = [1, 7, 3, 6, 5, 6]
Output: 3
Explanation: Left sum = 1 + 7 + 3 = 11, Right sum = 5 + 6 = 11. Pivot is index 3 (value 6).
```

## Why the naive way fails

Computing `sum(nums[:i]) == sum(nums[i+1:])` inside a loop slices and sums the array on every step, running in $\mathcal{O}(n^2)$ time and allocating $\mathcal{O}(n)$ slice copies.

## The core trick: Derive `right_sum` from `total`

At any index `i`, the array splits into three parts that always add up to `total = sum(nums)`:

$$\text{left\_sum} + \text{nums}[i] + \text{right\_sum} = \text{total}$$

Compute `total` once up front and maintain a running `left_sum = 0`. At each index `i`, the right sum is immediately known in $\mathcal{O}(1)$ time:

$$\text{right\_sum} = \text{total} - \text{left\_sum} - \text{nums}[i]$$

### Algorithm steps:
* **1. Compute total and initialize left sum:** Calculate `total = sum(nums)` and set `left_sum = 0`.
* **2. Iterate through indices:** For each `i, num` in `enumerate(nums)`:
  * Check equilibrium condition: if `left_sum == total - left_sum - num`, pivot found; return `i`.
  * Update running left sum: `left_sum += num`.
* **3. Termination:** If no index satisfies the condition, return `-1`.

## Step-by-step trace

Tracing `nums = [1, 7, 3, 6, 5, 6]` (`total = 28`):

| Index `i` | `num` | `left_sum` | `right_sum = 28 - left_sum - num` | `left_sum == right_sum`? | Next `left_sum` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `1` | `0` | `28 - 0 - 1 = 27` | False | `0 + 1 = 1` |
| `1` | `7` | `1` | `28 - 1 - 7 = 20` | False | `1 + 7 = 8` |
| `2` | `3` | `8` | `28 - 8 - 3 = 17` | False | `8 + 3 = 11` |
| `3` | `6` | `11` | `28 - 11 - 6 = 11` | True (return `3`) | Done |

## Traps to watch for

1. **Check before adding `num` to `left_sum`:** The pivot element `nums[i]` belongs to neither side. If you update `left_sum += num` before the equality check, `left_sum` wrongly includes the pivot.
2. **Works with negative numbers and zeros:** Unlike two-pointer squeeze approaches that break when numbers can be negative (e.g., `[-1, -1, 0, 1, 1, 0]`), the sum conservation equation holds for any integers.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def pivotIndex(self, nums: list[int]) -> int:
        total = sum(nums)
        left_sum = 0

        for i, num in enumerate(nums):
            if left_sum == total - left_sum - num:
                return i
            left_sum += num

        return -1
```

</details>

## Complexity

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n)$ | One pass for `sum(nums)` and one pass to find the pivot. |
| **Space** | $\mathcal{O}(1)$ | Uses two integer variables (`total` and `left_sum`). |
