# LeetCode 55: Jump Game

> **Difficulty:** Medium | **Pattern:** Greedy (Farthest Reachable Horizon)  
> **Source Code:** [`55_jump_game.py`](55_jump_game.py)

## The problem

Given an integer array `nums` where `nums[i]` is your maximum jump length from index `i`, return `True` if you can reach the last index (`len(nums) - 1`) starting from index `0`, or `False` otherwise.

```text
Example 1:
Input:  nums = [2, 3, 1, 1, 4]
Output: True (Jump 1 step from index 0 to 1, then 3 steps to index 4)

Example 2:
Input:  nums = [3, 2, 1, 0, 4]
Output: False (Indices 0, 1, and 2 all land at most on index 3, which has jump power 0)
```

## The core trick: Track the farthest reachable index

Trying to simulate every possible combination of hops builds a branching recursion tree. You only need to track one number as you walk left to right: `max_reach`, the farthest index reachable so far.

At each index `i`, check three things in order:
1. **Can I reach index `i`?** If `i > max_reach`, you hit a gap that no previous jump could cross. Return `False`.
2. **How far can I reach from here?** Update `max_reach = max(max_reach, i + nums[i])`.
3. **Did I reach the end?** If `max_reach >= len(nums) - 1`, return `True` early.

### Algorithm steps:
* **1. Initialize reach boundary:** Set `max_reach = 0` and target index `target = len(nums) - 1`.
* **2. Scan indices sequentially:** For each index `i` and jump value `jump` in `enumerate(nums)`:
  * If `i > max_reach`, the current index is unreachable; return `False`.
  * Update farthest reachable position: `max_reach = max(max_reach, i + jump)`.
  * If `max_reach >= target`, return `True` early.
* **3. Termination:** Return `True` if loop finishes without becoming stranded.

## Step-by-step trace

Tracing `nums = [3, 2, 1, 0, 4]`:

| Index `i` | `nums[i]` | `i > max_reach`? | `i + nums[i]` | Updated `max_reach` | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `3` | `0 > 0` (False) | `0 + 3 = 3` | `3` | Keep going |
| `1` | `2` | `1 > 3` (False) | `1 + 2 = 3` | `3` | Keep going |
| `2` | `1` | `2 > 3` (False) | `2 + 1 = 3` | `3` | Keep going |
| `3` | `0` | `3 > 3` (False) | `3 + 0 = 3` | `3` | Stuck at `3` |
| `4` | `4` | `4 > 3` (True) | Unreachable | `3` | Return `False` |

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_reach = 0
        target = len(nums) - 1

        for i, jump in enumerate(nums):
            if i > max_reach:
                return False

            max_reach = max(max_reach, i + jump)

            if max_reach >= target:
                return True

        return True
```

</details>

## Complexity

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n)$ | Single linear pass through `nums`. |
| **Space** | $\mathcal{O}(1)$ | Tracks a single integer variable `max_reach`. |
