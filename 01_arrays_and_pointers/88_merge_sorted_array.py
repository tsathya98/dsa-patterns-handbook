"""
LeetCode 88: Merge Sorted Array
URL: https://leetcode.com/problems/merge-sorted-array/

Pattern: Two Pointers (Formation E: The Tail-Buffer / Reverse Placement Pattern)
Time Complexity: O(m + n)
Space Complexity: O(1) in-place auxiliary space
"""

from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # p1 points to the last valid number in nums1
        p1 = m - 1
        # p2 points to the last number in nums2
        p2 = n - 1
        # p points to the write destination at the very end of nums1 (the safe buffer)
        p = m + n - 1

        # Compare from the back and place the larger element at index p
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p1 -= 1
            else:
                nums1[p] = nums2[p2]
                p2 -= 1
            p -= 1

        # If nums2 still has elements remaining, copy them into nums1.
        # Note: If nums1 has elements remaining, they are already in their correct places!
        while p2 >= 0:
            nums1[p] = nums2[p2]
            p2 -= 1
            p -= 1


# --- Test Suite ---
def test_merge_sorted_array():
    sol = Solution()

    # Test Case 1: Standard merge
    nums1 = [1, 2, 3, 0, 0, 0]
    nums2 = [2, 5, 6]
    sol.merge(nums1, 3, nums2, 3)
    assert nums1 == [1, 2, 2, 3, 5, 6], f"Test 1 Failed: {nums1}"

    # Test Case 2: nums2 is empty
    nums1 = [1]
    nums2 = []
    sol.merge(nums1, 1, nums2, 0)
    assert nums1 == [1], f"Test 2 Failed: {nums1}"

    # Test Case 3: nums1 is empty (only holds 0s for buffer)
    nums1 = [0]
    nums2 = [1]
    sol.merge(nums1, 0, nums2, 1)
    assert nums1 == [1], f"Test 3 Failed: {nums1}"

    # Test Case 4: nums2 elements are all smaller than nums1 elements
    nums1 = [4, 5, 6, 0, 0, 0]
    nums2 = [1, 2, 3]
    sol.merge(nums1, 3, nums2, 3)
    assert nums1 == [1, 2, 3, 4, 5, 6], f"Test 4 Failed: {nums1}"

    # Test Case 5: Duplicate elements across both arrays
    nums1 = [2, 2, 2, 0, 0, 0]
    nums2 = [2, 2, 2]
    sol.merge(nums1, 3, nums2, 3)
    assert nums1 == [2, 2, 2, 2, 2, 2], f"Test 5 Failed: {nums1}"

    print("✅ All 5 test cases passed successfully!")


if __name__ == "__main__":
    test_merge_sorted_array()
