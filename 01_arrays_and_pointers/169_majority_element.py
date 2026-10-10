"""
LeetCode 169: Majority Element
URL: https://leetcode.com/problems/majority-element/

Pattern: Boyer-Moore Voting Algorithm (Mutual Cancellation Pattern)
Time Complexity: O(n)
Space Complexity: O(1) in-place auxiliary space
"""

from collections import Counter
from typing import List, Optional


class Solution:
    def majorityElement_counter(self, nums: List[int]) -> int:
        """
        Baseline Approach: Frequency Map / Counter
        Time: O(n), Space: O(n)
        """
        counts = Counter(nums)
        return max(counts.keys(), key=counts.get)

    def majorityElement(self, nums: List[int]) -> int:
        """
        Optimal Approach: Boyer-Moore Voting Algorithm
        Time: O(n), Space: O(1)
        """
        candidate = None
        count = 0

        for num in nums:
            if count == 0:
                candidate = num
                count = 1
            elif candidate == num:
                count += 1
            else:
                count -= 1

        return candidate


# --- Test Suite ---
def test_majority_element():
    sol = Solution()

    # Test Case 1: Standard case
    nums1 = [3, 2, 3]
    assert sol.majorityElement(nums1) == 3

    # Test Case 2: Longer case
    nums2 = [2, 2, 1, 1, 1, 2, 2]
    assert sol.majorityElement(nums2) == 2

    # Test Case 3: Single element
    nums3 = [1]
    assert sol.majorityElement(nums3) == 1

    # Test Case 4: Negative numbers
    nums4 = [-1, 1, 1, 1, 2, 1]
    assert sol.majorityElement(nums4) == 1

    # Test Case 5: All identical
    nums5 = [7, 7, 7, 7]
    assert sol.majorityElement(nums5) == 7

    print("✅ All 5 test cases passed successfully for Boyer-Moore Voting!")


if __name__ == "__main__":
    test_majority_element()
