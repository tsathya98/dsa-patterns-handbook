# LeetCode 11: Container With Most Water

> **Difficulty:** Medium | **Pattern:** Two Pointers (Opposite Ends Squeeze)
> **Link:** [LeetCode 11](https://leetcode.com/problems/container-with-most-water/)

## The problem

Given an integer array `height` of length $n$, where the $i$-th vertical line has endpoints `(i, 0)` and `(i, height[i])`, find two lines that together with the x-axis form a container holding the maximum amount of water.

$$\text{Area} = (r - l) \times \min(\text{height}[l], \text{height}[r])$$

## Why the naive way fails

Checking every pair $(l, r)$ takes $\mathcal{O}(n^2)$ time. With $n \le 10^5$, that is roughly $5 \times 10^9$ operations, which hits Time Limit Exceeded.

## The core trick

Start with the widest possible container (`l = 0`, `r = n - 1`) and shrink inward by moving one pointer at each step.

```text
Index:    0   1   2   3   4   5   6   7   8
Height:  [1,  8,  6,  2,  5,  4,  8,  3,  7]
          ▲                               ▲
         left                           right
```

Water height is capped by the shorter of the two lines. If you move the taller line inward, width decreases by 1 and the height cannot exceed the current shorter line, so area can only shrink. Moving the shorter line inward is the only move that can find a taller bar to offset the lost width.

## Step-by-step trace

Input: `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]`

| Step | `l` (`height[l]`) | `r` (`height[r]`) | Width | Bottleneck | Area | `max_area` | Move |
|---|---|---|---|---|---|---|---|
| 1 | 0 (1) | 8 (7) | 8 | 1 | 8 | 8 | `l += 1` (1 < 7) |
| 2 | 1 (8) | 8 (7) | 7 | 7 | 49 | 49 | `r -= 1` (8 > 7) |
| 3 | 1 (8) | 7 (3) | 6 | 3 | 18 | 49 | `r -= 1` (8 > 3) |
| 4 | 1 (8) | 6 (8) | 5 | 8 | 40 | 49 | `r -= 1` (tie) |

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def maxArea(self, height: list[int]) -> int:
        l, r = 0, len(height) - 1
        max_area = 0

        while l < r:
            hl, hr = height[l], height[r]
            if hl < hr:
                area = (r - l) * hl
                if area > max_area:
                    max_area = area
                l += 1
            else:
                area = (r - l) * hr
                if area > max_area:
                    max_area = area
                r -= 1

        return max_area
```

</details>

## Traps to watch for

* **Tie-breaking when `height[l] == height[r]`:** Either pointer can move (or both). Neither original bar can form a larger container with any strictly narrower partner unless *both* bars are replaced by taller ones.
* **Fast-forward micro-optimization:** When moving away from bottleneck height `h`, any subsequent bar $\le h$ has both smaller width and height $\le h$. You can skip them with `while l < r and height[l] <= hl: l += 1`, though worst-case complexity stays $\mathcal{O}(n)$.

## Complexity

* **Time:** $\mathcal{O}(n)$ because `l` or `r` steps inward on every iteration, taking $n - 1$ steps total.
* **Space:** $\mathcal{O}(1)$ auxiliary memory.
