from collections import Counter
from typing import List


class Solution:
    def missingNumber_sort(self, nums: List[int]) -> int:
        """
        Approach 1: Brute Force Sorting
        Time: O(N log N)
        Space: O(1) beyond sort
        """
        nums.sort()
        for i, val in enumerate(nums):
            if i != val:
                return i
        return len(nums)

    def missingNumber_counter(self, nums: List[int]) -> int:
        """
        Approach 2: Semi-Optimized Hash Set / Counter (User's Solution)
        Time: O(N)
        Space: O(N)
        """
        dct = Counter(nums)
        n = len(nums)
        for i in range(n + 1):
            if i not in dct:
                return i
        return -1

    def missingNumber_math(self, nums: List[int]) -> int:
        """
        Approach 3: Optimized Gauss Sum Formula
        Sum of 0 to n is n * (n + 1) // 2.
        Time: O(N)
        Space: O(1)
        """
        n = len(nums)
        expected_sum = n * (n + 1) // 2
        return expected_sum - sum(nums)

    def missingNumber(self, nums: List[int]) -> int:
        """
        Approach 4: Optimal Bitwise XOR (Gold Standard FAANG)
        Every number from 0..n and in nums appears twice except the missing one.
        x ^ x = 0, x ^ 0 = x.
        Time: O(N)
        Space: O(1)
        """
        ans = len(nums)
        for i, num in enumerate(nums):
            ans ^= i ^ num
        return ans


def test_missing_number():
    sol = Solution()
    approaches = [
        ("Sorting", sol.missingNumber_sort),
        ("Counter / Hash Set", sol.missingNumber_counter),
        ("Gauss Math Sum", sol.missingNumber_math),
        ("Bitwise XOR Optimal", sol.missingNumber),
    ]

    test_cases = [
        ([3, 0, 1], 2),
        ([0, 1], 2),
        ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8),
        ([0], 1),
        ([1], 0),
    ]

    for name, fn in approaches:
        for nums_in, expected in test_cases:
            nums = list(nums_in)  # Copy to avoid sort mutating in-place
            res = fn(nums)
            assert res == expected, f"{name} failed on {nums_in}: got {res}, expected {expected}"

    print("All 4 approaches for LC 268 passed successfully!")


if __name__ == "__main__":
    test_missing_number()
