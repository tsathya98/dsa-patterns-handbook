# LeetCode 80: Remove Duplicates from Sorted Array II

> **Difficulty:** Medium | **Pattern:** Two Pointers (Scout and Writer with Lookback)  
> **Constraints:** $\mathcal{O}(n)$ time, $\mathcal{O}(1)$ auxiliary space in-place.

## The problem

Given an integer array `nums` sorted in non-decreasing order, remove duplicates in-place so that each unique element appears **at most twice**. Return `k`, the number of kept elements in the first `k` slots of `nums`.

```text
Input:  nums = [1, 1, 1, 2, 2, 3]
Output: k = 5, nums[:5] = [1, 1, 2, 2, 3]
```

## Two ways to solve it in $\mathcal{O}(1)$ space

### Approach 1: Scout and Writer with a streak counter (`tmp`)
Keep a Writer pointer `k = 1` and a streak counter `tmp = 1` tracking how many times the current value has been seen in a row:
- If `nums[i] == nums[i - 1]` and `tmp < 2`: increment `tmp += 1`, copy `nums[k] = nums[i]`, and advance `k += 1`.
- If `nums[i] != nums[i - 1]`: reset `tmp = 1`, copy `nums[k] = nums[i]`, and advance `k += 1`.
- If `nums[i] == nums[i - 1]` and `tmp >= 2`: skip it (`k` stays put).

### Approach 2: The lookback-$M$ generalization
Instead of comparing input neighbors (`nums[i]` vs `nums[i - 1]`), compare the incoming value `x` against `nums[k - 2]`, the value written two slots back in the clean prefix:
- Because the array is sorted, if `x == nums[k - 2]`, then `nums[k - 2]` and `nums[k - 1]` are already equal to `x`, so writing `x` would create a third copy.
- If `k < 2` or `x != nums[k - 2]`, it is safe to write `nums[k] = x` and advance `k += 1`.

This single pattern generalizes to any maximum duplicate limit $M$:
- Allow at most 1 copy ([LC 26](./26_remove_duplicates_from_sorted_array.md)): `if k < 1 or x != nums[k - 1]:`
- Allow at most 2 copies (LC 80): `if k < 2 or x != nums[k - 2]:`
- Allow at most $M$ copies: `if k < M or x != nums[k - M]:`

### Algorithm steps:
* **1. Initialize writer pointer:** Set `k = 0`.
* **2. Scan each element:** For each `x` in `nums`:
  * If `k < 2` or `x != nums[k - 2]`, write `nums[k] = x` and advance `k += 1`.
  * Otherwise, skip `x` since two copies already exist in the valid prefix.
* **3. Return:** `k` representing the new length with at most two duplicates per value.

## Step-by-step trace (Lookback-2)

Tracing `nums = [1, 1, 1, 2, 2, 3]`:

| Step (`i`) | `x = nums[i]` | `k` (before) | Check `k < 2 or x != nums[k - 2]` | Action | Prefix `nums[:k]` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `1` | `0` | `k < 2` (True) | Write `nums[0] = 1` | `[1]` |
| `1` | `1` | `1` | `k < 2` (True) | Write `nums[1] = 1` | `[1, 1]` |
| `2` | `1` | `2` | `1 != nums[0] (1)` (False) | Skip | `[1, 1]` |
| `3` | `2` | `2` | `2 != nums[0] (1)` (True) | Write `nums[2] = 2` | `[1, 1, 2]` |
| `4` | `2` | `3` | `2 != nums[1] (1)` (True) | Write `nums[3] = 2` | `[1, 1, 2, 2]` |
| `5` | `3` | `4` | `3 != nums[2] (2)` (True) | Write `nums[4] = 3` | `[1, 1, 2, 2, 3]` |

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
from typing import List

# Approach 1: Generalized Lookback-2 (5 lines)
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 0
        for x in nums:
            if k < 2 or x != nums[k - 2]:
                nums[k] = x
                k += 1
        return k


# Approach 2: Explicit Streak Counter
class SolutionStreak:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 1
        tmp = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1] and tmp < 2:
                tmp += 1
                nums[k] = nums[i]
                k += 1
            elif nums[i] != nums[i - 1]:
                nums[k] = nums[i]
                k += 1
                tmp = 1
        return k
```

</details>

## Complexity

| Approach | Time | Auxiliary Space | Notes |
| :--- | :--- | :--- | :--- |
| Streak Counter (`tmp`) | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Explicit state tracking, easy to trace. |
| Lookback-$M$ (`nums[k - 2]`) | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Generalizes to any duplicate cap $M$ by changing `2` to `M`. |
