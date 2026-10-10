"""
LeetCode 283: Move Zeroes
Pattern: Two Pointers (Formation B: Scout & Writer / Fast & Slow)
Difficulty: Easy
Link: https://leetcode.com/problems/move-zeroes/
"""

class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        
        Time Complexity: O(n) - single pass over nums
        Space Complexity: O(1) - strictly in-place modification
        """
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0], [0]),
        ([1], [1]),
        ([0, 1, 0, 0, 3, 12], [1, 3, 12, 0, 0, 0]),
        ([1, 2, 3, 4], [1, 2, 3, 4]),
        ([0, 0, 0, 1], [1, 0, 0, 0]),
    ]
    
    for original, expected in test_cases:
        arr = original.copy()
        sol.moveZeroes(arr)
        assert arr == expected, f"Failed for {original}: expected {expected}, got {arr}"
        print(f"✓ Input: {original} -> Output: {arr}")
        
    print("\nAll test cases passed successfully!")
