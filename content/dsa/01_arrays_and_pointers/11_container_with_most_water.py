"""
LeetCode 11: Container With Most Water
Difficulty: Medium
Pattern: Two Pointers (Shrinking Window / Opposite Ends)

Explanation:
-------------
The problem asks us to find two vertical lines that, together with the x-axis,
hold the maximum amount of water.

Area Formula:
    area = width * min(height[l], height[r])
    where width = r - l

Why Two Pointers (O(n)):
1. We start at the widest possible boundaries: left pointer `l = 0` and right pointer `r = len(height) - 1`.
2. The water level is limited by the shorter line (the bottleneck).
3. If we move the taller line inward, the width shrinks and height cannot exceed the current bottleneck,
   meaning the area is guaranteed to be smaller or equal.
4. Therefore, the only way to potentially find a larger container is to move the shorter line inward,
   hoping to find a taller line that compensates for the loss in width.

Complexity:
- Time: O(n) - pointers converge in at most n - 1 steps.
- Space: O(1) - constant auxiliary memory.

Interview Finding (Google / FAANG):
- The standard solution (Solution) is the expected primary interview solution.
- The fast-forward optimization (SolutionOptimized) skips bars shorter than the previous bottleneck,
  improving real-world runtime significantly.
"""

from typing import List


class Solution:
    """Standard Optimal Two-Pointer Solution (User's Solution)."""

    def maxArea(self, height: List[int]) -> int:
        l = 0
        r = len(height) - 1
        max_area = 0

        while l < r:
            min_h = min(height[l], height[r])
            width = r - l
            curr_area = width * min_h
            max_area = max(curr_area, max_area)

            if height[l] < height[r]:
                l += 1
            else:
                r -= 1

        return max_area


class SolutionOptimized:
    """Fast-Forward Two-Pointer Solution (Skips non-promising bars)."""

    def maxArea(self, height: List[int]) -> int:
        l = 0
        r = len(height) - 1
        max_area = 0

        while l < r:
            hl, hr = height[l], height[r]

            if hl < hr:
                area = (r - l) * hl
                if area > max_area:
                    max_area = area
                # Fast-forward past any heights <= current bottleneck
                while l < r and height[l] <= hl:
                    l += 1
            else:
                area = (r - l) * hr
                if area > max_area:
                    max_area = area
                # Fast-forward past any heights <= current bottleneck
                while l < r and height[r] <= hr:
                    r -= 1

        return max_area


if __name__ == "__main__":
    test_cases = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
    ]

    sol = Solution()
    sol_opt = SolutionOptimized()

    print("Running tests for LeetCode 11: Container With Most Water...")
    for idx, (heights, expected) in enumerate(test_cases, 1):
        res1 = sol.maxArea(heights)
        res2 = sol_opt.maxArea(heights)
        assert res1 == expected, f"Test {idx} failed on Solution: got {res1}, expected {expected}"
        assert res2 == expected, f"Test {idx} failed on SolutionOptimized: got {res2}, expected {expected}"
        print(f"Test case {idx}: heights={heights} -> max_area={res1} (Passed)")

    print("\nAll test cases passed successfully!")
