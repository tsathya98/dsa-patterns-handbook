"""
LeetCode 55: Jump Game
Link: https://leetcode.com/problems/jump-game/
Pattern: Greedy (Horizon / Laser Reach Expansion)
Time Complexity: O(n) - Single pass
Space Complexity: O(1) - Constant auxiliary space
"""

from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_reach = 0
        target = len(nums) - 1
        
        for i, jump in enumerate(nums):
            if i > max_reach:
                return False
            max_reach = max(max_reach, i + jump)
            if max_reach >= target:
                return True
                
        return True

if __name__ == "__main__":
    sol = Solution()
    assert sol.canJump([2, 3, 1, 1, 4]) == True
    assert sol.canJump([3, 2, 1, 0, 4]) == False
    assert sol.canJump([0]) == True
    print("All test cases passed!")
