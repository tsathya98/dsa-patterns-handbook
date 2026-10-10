"""
LeetCode 53: Maximum Subarray
Pattern: Kadane's Algorithm (Greedy Prefix Reset)
Complexity: O(n) Time, O(1) Space

Core Logic:
- current_sum = max(num, current_sum + num)
- max_sum = max(max_sum, current_sum)
"""

from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        current_sum = nums[0]
        max_sum = nums[0]

        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum


if __name__ == "__main__":
    test_cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-5, -2, -8], -2),  # All-negative edge case
    ]

    sol = Solution()
    print("Running tests for Kadane's Algorithm (LeetCode 53)...")
    for idx, (nums, expected) in enumerate(test_cases, 1):
        res = sol.maxSubArray(nums)
        assert res == expected, f"Test {idx} failed: got {res}, expected {expected}"
        print(f"Test case {idx}: nums={nums} -> max_sum={res} (Passed)")

    print("\nAll Kadane tests passed successfully!")
