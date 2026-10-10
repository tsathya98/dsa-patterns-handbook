"""
LeetCode 724: Find Pivot Index (also LC 1991: Find the Middle Index in Array)
Pattern: Prefix Sum (The Seesaw Balance / Conservation of Total Sum)
Difficulty: Easy
Link: https://leetcode.com/problems/find-pivot-index/
"""

class Solution:
    def pivotIndex(self, nums: list[int]) -> int:
        """
        Time Complexity: O(n) - exactly two linear passes (sum + scan)
        Space Complexity: O(1) - single scalar variable left_sum
        """
        total = sum(nums)
        left_sum = 0
        
        for i, num in enumerate(nums):
            # Seesaw balance condition:
            # left_sum == total - left_sum - num (which is right_sum)
            if left_sum == total - left_sum - num:
                return i
            left_sum += num
            
        return -1


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ([1, 7, 3, 6, 5, 6], 3),
        ([1, 2, 3], -1),
        ([2, 1, -1], 0),
        ([0], 0),
        ([-1, -1, -1, -1, -1, 0], 2),
        ([-1, -1, 0, 1, 1, 0], 5),
    ]
    
    for nums, expected in test_cases:
        actual = sol.pivotIndex(nums)
        assert actual == expected, f"Failed for nums={nums}: expected {expected}, got {actual}"
        print(f"✓ nums={nums} -> pivot index = {actual}")
        
    print("\nAll test cases passed successfully!")
