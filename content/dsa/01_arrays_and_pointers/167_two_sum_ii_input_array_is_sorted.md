# LeetCode 167: Two Sum II - Input Array Is Sorted

> **Difficulty:** Medium | **Pattern:** Two Pointers (Inward Squeeze)
> **Source Code:** [`167_two_sum_ii_input_array_is_sorted.py`](167_two_sum_ii_input_array_is_sorted.py)

## The problem

Given a 1-indexed array of integers `numbers` sorted in non-decreasing order, find two numbers that add up to `target`. Return their 1-based indices `[index1, index2]`. Your solution must use $\mathcal{O}(1)$ extra space.

## Why the naive way fails

Checking all pairs takes $\mathcal{O}(n^2)$ time. Using a hash map like in Two Sum I runs in $\mathcal{O}(n)$ time, but violates the strict $\mathcal{O}(1)$ extra space constraint and ignores the fact that the input is already sorted.

## The core trick

Place `l = 0` at the smallest element and `r = len(numbers) - 1` at the largest element. At each step, compute `cur_sum = numbers[l] + numbers[r]`:
* If `cur_sum == target`, return `[l + 1, r + 1]`.
* If `cur_sum < target`, the sum is too small; move `l += 1` to pick a larger number.
* If `cur_sum > target`, the sum is too large; move `r -= 1` to pick a smaller number.

```text
  l ──►                        ◄── r
[ 2,      7,      11,      15 ],   target = 9
```

### Algorithm steps:
* **1. Initialize two pointers:** Set `l = 0` and `r = len(numbers) - 1`.
* **2. Squeeze while l < r:**
  * Compute `cur_sum = numbers[l] + numbers[r]`.
  * If `cur_sum == target`, return 1-based indices `[l + 1, r + 1]`.
  * If `cur_sum < target`, sum is too small; advance `l += 1`.
  * If `cur_sum > target`, sum is too large; retreat `r -= 1`.
* **3. Termination:** Guaranteed unique solution exists, terminating in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.

## Step-by-step trace

Input: `numbers = [2, 7, 11, 15]`, `target = 9`

| Step | `l` (`numbers[l]`) | `r` (`numbers[r]`) | `cur_sum` | Comparison | Action |
|---|---|---|---|---|---|
| 1 | 0 (2) | 3 (15) | 17 | $17 > 9$ | Too big: `r -= 1` |
| 2 | 0 (2) | 2 (11) | 13 | $13 > 9$ | Too big: `r -= 1` |
| 3 | 0 (2) | 1 (7) | 9 | $9 == 9$ | Match: return `[1, 2]` |

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        l, r = 0, len(numbers) - 1

        while l < r:
            cur_sum = numbers[l] + numbers[r]
            if cur_sum == target:
                return [l + 1, r + 1]
            elif cur_sum < target:
                l += 1
            else:
                r -= 1

        return []
```

</details>

## Traps to watch for

* **1-based return indices:** The problem specifies a 1-indexed return format. Remember to add `1` to both indices (`[l + 1, r + 1]`) when returning.
* **Why we never miss the valid pair:** Suppose the true answer is $(i^*, j^*)$ with $i^* < j^*$. One of the pointers (`l` or `r`) must reach its target position first. If `l` reaches $i^*$ first while $r > j^*$, then `numbers[i*] + numbers[r] > target`, which forces `r` to decrement until it reaches $j^*$ without ever moving `l` past $i^*$.

## Complexity

* **Time:** $\mathcal{O}(n)$ as each step moves `l` right or `r` left by 1.
* **Space:** $\mathcal{O}(1)$ auxiliary space.
