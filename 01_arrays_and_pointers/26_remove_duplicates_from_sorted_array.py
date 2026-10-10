"""
LeetCode 26: Remove Duplicates from Sorted Array
URL: https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Pattern: Two Pointers (Formation B: Scout & Writer / Fast & Slow)
Time Complexity: O(n)
Space Complexity: O(1) in-place auxiliary space (FAANG Requirement)
"""

from collections import Counter
from typing import List


class Solution:
    def removeDuplicates_counter(self, nums: List[int]) -> int:
        """
        User's initial solution using Counter:
        - Time: O(n)
        - Space: O(n) auxiliary space (Violates O(1) space constraint in interviews)
        """
        counter = Counter(nums)
        k = 0
        for key in counter:
            nums[k] = key
            k += 1
        return k

    def removeDuplicates(self, nums: List[int]) -> int:
        """
        Optimal Two Pointers (Scout & Writer):
        - Time: O(n)
        - Space: O(1) auxiliary space (Strict in-place)
        
        nums[0] is always unique and already at index 0.
        Writer (k) starts at index 1.
        Scout (i) scans from index 1 to n - 1.
        """
        if not nums:
            return 0

        k = 1
        for i in range(1, len(nums)):
            # If current number differs from previous neighbor, it's a NEW unique element!
            if nums[i] != nums[i - 1]:
                nums[k] = nums[i]
                k += 1
        return k


# --- Test Suite ---
def test_remove_duplicates():
    sol = Solution()

    # Test Case 1: Standard case
    nums1 = [1, 1, 2]
    k1 = sol.removeDuplicates(nums1)
    assert k1 == 2, f"Expected 2, got {k1}"
    assert nums1[:k1] == [1, 2], f"Expected [1, 2], got {nums1[:k1]}"

    # Test Case 2: Multiple duplicates
    nums2 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k2 = sol.removeDuplicates(nums2)
    assert k2 == 5, f"Expected 5, got {k2}"
    assert nums2[:k2] == [0, 1, 2, 3, 4], f"Expected [0, 1, 2, 3, 4], got {nums2[:k2]}"

    # Test Case 3: All elements identical
    nums3 = [5, 5, 5, 5]
    k3 = sol.removeDuplicates(nums3)
    assert k3 == 1, f"Expected 1, got {k3}"
    assert nums3[:k3] == [5], f"Expected [5], got {nums3[:k3]}"

    # Test Case 4: No duplicates (already unique)
    nums4 = [1, 2, 3, 4, 5]
    k4 = sol.removeDuplicates(nums4)
    assert k4 == 5, f"Expected 5, got {k4}"
    assert nums4[:k4] == [1, 2, 3, 4, 5], f"Expected [1, 2, 3, 4, 5], got {nums4[:k4]}"

    # Test Case 5: Single element
    nums5 = [42]
    k5 = sol.removeDuplicates(nums5)
    assert k5 == 1, f"Expected 1, got {k5}"
    assert nums5[:k5] == [42], f"Expected [42], got {nums5[:k5]}"

    print("✅ All 5 test cases passed successfully for O(1) in-place solution!")


if __name__ == "__main__":
    test_remove_duplicates()
