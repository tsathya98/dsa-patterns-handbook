# LeetCode 169: Majority Element

> **Difficulty:** Easy | **Pattern:** Boyer-Moore Voting Algorithm (Mutual Cancellation)
> **Link:** [LeetCode 169](https://leetcode.com/problems/majority-element/)

## The problem

Given an array `nums` of size $n$, return the majority element. The majority element appears strictly more than $\lfloor n / 2 \rfloor$ times and is guaranteed to exist. Solve it in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ auxiliary space.

## Why the naive way fails

A hash map (`Counter(nums)`) runs in $\mathcal{O}(n)$ time but uses $\mathcal{O}(n)$ space. Sorting the array and returning `nums[n // 2]` uses $\mathcal{O}(1)$ extra space (ignoring sort internals) but costs $\mathcal{O}(n \log n)$ time.

## The core trick

Because the majority element appears more than $\frac{n}{2}$ times, its frequency exceeds all other elements combined:

$$\text{Count}(\text{majority}) - \text{Count}(\text{all others}) > 0$$

Boyer-Moore voting pairs off distinct elements 1-for-1:
* Maintain a `candidate` and a `count = 0`.
* When `count == 0`, adopt the current number as `candidate` and set `count = 1`.
* Otherwise, increment `count` if `num == candidate`, or decrement `count` if `num != candidate`.

```text
nums = [ 1,  2,  1,  2,   3,  3,  3 ]
        └─────────────┘  └─────────┘
         Two 1s, two 2s   Remainder
         cancel (count=0) 3 wins
```

Whenever `count` drops to `0`, the prefix inspected so far contains at most 50% of any single value, so discarding that prefix leaves the true majority element still holding $> 50\%$ of the remaining suffix.

### Algorithm steps (Boyer-Moore voting):
* **1. Initialize trackers:** Set `candidate = None` and `count = 0`.
* **2. Iterate through numbers:** For each `num` in `nums`:
  * If `count == 0`, assign current number as new leader: `candidate = num` and `count = 1`.
  * Else if `num == candidate`, increment `count += 1`.
  * Otherwise, cancel out with different number: decrement `count -= 1`.
* **3. Return:** `candidate` in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.

## Step-by-step trace

Input: `nums = [2, 2, 1, 1, 1, 2, 2]`

| Step | `num` | `count` (before) | Action | `candidate` | `count` (after) |
|---|---|---|---|---|---|
| 1 | 2 | 0 | Reset candidate to 2 | 2 | 1 |
| 2 | 2 | 1 | Match (`2 == 2`) | 2 | 2 |
| 3 | 1 | 2 | Mismatch (`1 != 2`) | 2 | 1 |
| 4 | 1 | 1 | Mismatch (`1 != 2`) | 2 | 0 |
| 5 | 1 | 0 | Reset candidate to 1 | 1 | 1 |
| 6 | 2 | 1 | Mismatch (`2 != 1`) | 1 | 0 |
| 7 | 2 | 0 | Reset candidate to 2 | 2 | 1 |

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        candidate = None
        count = 0

        for num in nums:
            if count == 0:
                candidate = num
                count = 1
            elif candidate == num:
                count += 1
            else:
                count -= 1

        return candidate
```

</details>

## Traps to watch for

* **When a majority element is not guaranteed:** Boyer-Moore always returns *some* survivor even on `[1, 2, 3]`. If the problem does not guarantee a $> \lfloor n/2 \rfloor$ majority, you must run a second pass (`nums.count(candidate) > len(nums) // 2`) to verify the winner.
* **Using `if / elif` on reset:** Setting `candidate = num` and `count = 1` inside the `if count == 0:` branch avoids a redundant `if candidate == num:` check on the same iteration.

## Complexity

* **Time:** $\mathcal{O}(n)$ for a single pass.
* **Space:** $\mathcal{O}(1)$ using two scalar variables.
