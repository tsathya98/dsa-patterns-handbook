from typing import List


class Solution:
    def maxSubArray_brute(self, nums: List[int]) -> int:
        """
        Approach 1: Brute Force Nested Loops
        Time: O(N^2)
        Space: O(1)
        """
        n = len(nums)
        max_sum = float("-inf")
        for i in range(n):
            curr_sum = 0
            for j in range(i, n):
                curr_sum += nums[j]
                max_sum = max(max_sum, curr_sum)
        return int(max_sum)

    def maxSubArray_divide_and_conquer(self, nums: List[int]) -> int:
        """
        Approach 2: Divide and Conquer
        Split in half, max subarray is either purely in left, purely in right,
        or crosses the midpoint.
        Time: O(N log N)
        Space: O(log N) call stack
        """
        def cross_sum(left: int, mid: int, right: int) -> int:
            left_sum = float("-inf")
            curr = 0
            for i in range(mid, left - 1, -1):
                curr += nums[i]
                left_sum = max(left_sum, curr)

            right_sum = float("-inf")
            curr = 0
            for i in range(mid + 1, right + 1):
                curr += nums[i]
                right_sum = max(right_sum, curr)

            return int(left_sum + right_sum)

        def helper(left: int, right: int) -> int:
            if left == right:
                return nums[left]
            mid = (left + right) // 2
            left_best = helper(left, mid)
            right_best = helper(mid + 1, right)
            cross_best = cross_sum(left, mid, right)
            return max(left_best, right_best, cross_best)

        return helper(0, len(nums) - 1)

    def maxSubArray(self, nums: List[int]) -> int:
        """
        Approach 3: Kadane's Algorithm
        Time: O(N) single pass
        Space: O(1) auxiliary
        """
        max_sum = float("-inf")
        cur_sum = 0
        for num in nums:
            cur_sum = max(cur_sum + num, num)
            max_sum = max(max_sum, cur_sum)
        return int(max_sum)


if __name__ == "__main__":
    test_cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-5, -2, -8], -2),  # All-negative edge case
    ]

    sol = Solution()
    approaches = [
        ("Brute Force", sol.maxSubArray_brute),
        ("Divide & Conquer", sol.maxSubArray_divide_and_conquer),
        ("Kadane Optimal", sol.maxSubArray),
    ]

    for name, fn in approaches:
        for nums, expected in test_cases:
            res = fn(nums)
            assert res == expected, f"{name} failed on {nums}: got {res}, expected {expected}"

    print("All 3 approaches for Kadane's Algorithm (LC 53) passed successfully!")
