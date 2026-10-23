"""
LeetCode 238: Product of Array Except Self
Difficulty: Medium
URL: https://leetcode.com/problems/product-of-array-except-self/

Patterns:
1. Approach 1 (Accepted Submission): Explicit Prefix & Suffix Arrays (O(N) time, O(N) space).
2. Approach 2 (Optimal / In-Place): Two Passes Directly Inside Output Array (O(N) time, O(1) space).
"""

from typing import List


class Solution:
    def productExceptSelf_user_approach(self, nums: List[int]) -> List[int]:
        """
        User's Zero-Shot Solution: Explicit Prefix & Suffix Arrays
        Time Complexity: O(n)
        Auxiliary Space: O(n) - stores separate prefix and suffix arrays
        """
        n = len(nums)
        prefix = []
        suffix = []
        
        # 1. Build prefix products (everything to the left of i)
        tmp = 1
        for i in range(n):
            if i == 0:
                prefix.append(1)
                continue
            tmp *= nums[i - 1]
            prefix.append(tmp)
            
        # 2. Build suffix products (everything to the right of i)
        tmp = 1
        for i in range(n - 1, -1, -1):
            if i == n - 1:
                suffix.append(1)
                continue
            tmp *= nums[i + 1]
            suffix.append(tmp)
        suffix = suffix[::-1]
        
        # 3. Combine prefix * suffix
        res = []
        for i in range(n):
            res.append(prefix[i] * suffix[i])
            
        return res

    def productExceptSelf_optimized_space(self, nums: List[int]) -> List[int]:
        """
        FAANG Follow-Up: O(1) Auxiliary Space
        Directly compute prefix into output array, then accumulate suffix on the fly.
        
        Time Complexity: O(n)
        Auxiliary Space: O(1) (excluding output array)
        """
        n = len(nums)
        res = [1] * n
        
        # Forward pass: res[i] stores product of all elements to the left
        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]
            
        # Backward pass: multiply running suffix into res[i] on the fly
        suffix = 1
        for i in range(n - 1, -1, -1):
            res[i] *= suffix
            suffix *= nums[i]
            
        return res


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
        ([2, 3], [3, 2]),
        ([0, 0], [0, 0]),
    ]
    
    for nums, expected in test_cases:
        assert sol.productExceptSelf_user_approach(nums) == expected
        assert sol.productExceptSelf_optimized_space(nums) == expected
        
    print("All unit tests for LC 238 passed successfully!")
