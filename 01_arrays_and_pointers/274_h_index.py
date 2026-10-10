"""
LeetCode 274: H-Index
Link: https://leetcode.com/problems/h-index/
Pattern: Sorting + Rank Comparison
Time Complexity: O(n log n)
Space Complexity: O(1)
"""

from typing import List

class Solution:
    def hIndex(self, citations: List[int]) -> int:
        citations.sort(reverse=True)
        h_index = 0
        
        for i, c in enumerate(citations):
            if c >= i + 1:
                h_index = i + 1
            else:
                break
                
        return h_index

if __name__ == "__main__":
    sol = Solution()
    assert sol.hIndex([3, 0, 6, 1, 5]) == 3
    assert sol.hIndex([1, 3, 1]) == 1
    assert sol.hIndex([100]) == 1
    assert sol.hIndex([0]) == 0
    print("All test cases passed!")
