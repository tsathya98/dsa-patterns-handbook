# 53. Maximum Subarray

> **Difficulty:** Medium | **Pattern:** Kadane's Algorithm (Running Prefix Reset)

## The Problem
Find the contiguous subarray inside `nums` that has the largest sum, and return that sum.

```text
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6  (from subarray [4, -1, 2, 1])
```

## Why the naive way fails
Checking every possible subarray `[i..j]` takes $\mathcal{O}(n^2)$ time. On an array of $10^5$ numbers, that's $5 \times 10^9$ steps and an instant Time Limit Exceeded (TLE).

## The core trick: drop negative baggage
Walk through the array while keeping a running `current_sum`. Before adding today's number `num`, ask one question:

**Is my running sum from the past negative?**
- If `current_sum < 0`, adding it to `num` only drags `num` down. Throw the past away and start fresh at `num`.
- If `current_sum >= 0`, keep it and add `num`.

In code, that choice is just:
```python
current_sum = max(num, current_sum + num)
```

Notice that a dip isn't fatal as long as the running total stays positive:
```text
Subarray:  [ 4,  -1,   2,   1 ]
Running:     4 -> 3 -> 5 -> 6 (Max!)
```
Even though `-1` dropped the total from `4` to `3`, keeping that `+3` cushion let us reach `6` when `2` and `1` showed up. We only reset when the running sum drops below `0`.

## Trace
| `num` | `current_sum + num` | Start fresh (`num`) | New `current_sum` | `max_sum` |
| :--- | :--- | :--- | :--- | :--- |
| `-2` | (init) | `-2` | `-2` | `-2` |
| `1` | `-2 + 1 = -1` | `1` (reset) | `1` | `1` |
| `-3` | `1 + (-3) = -2` | `-3` | `-2` | `1` |
| `4` | `-2 + 4 = 2` | `4` (reset) | `4` | `4` |
| `-1` | `4 + (-1) = 3` | `-1` | `3` | `4` |
| `2` | `3 + 2 = 5` | `2` | `5` | `5` |
| `1` | `5 + 1 = 6` | `1` | `6` | `6` |

## Traps to watch for
- **All-negative arrays (`[-5, -2, -8]`):** Never initialize `max_sum = 0` or reset negative sums to `0`, or you'll return `0` instead of `-2`. Initialize both `current_sum` and `max_sum` to `nums[0]`.

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        current_sum = nums[0]
        max_sum = nums[0]

        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum
```

</details>

## Complexity
- **Time:** $\mathcal{O}(n)$, single pass.
- **Space:** $\mathcal{O}(1)$, two variables.
