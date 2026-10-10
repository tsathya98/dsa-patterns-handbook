"""
LeetCode 189: Rotate Array
URL: https://leetcode.com/problems/rotate-array/

Approaches:
1. Slicing with in-place slice replacement: O(n) time, O(n) space
2. Triple Reversal Algorithm (Two Pointers Squeeze): O(n) time, O(1) space (FAANG Requirement)
"""

from typing import List


class Solution:
    def rotate_slice(self, nums: List[int], k: int) -> None:
        """
        User's Pythonic Slice Solution:
        - Time: O(n)
        - Space: O(n) auxiliary memory for creating slices
        """
        k %= len(nums)
        nums[:] = nums[len(nums) - k :] + nums[: len(nums) - k]

    def rotate(self, nums: List[int], k: int) -> None:
        """
        The Triple Reversal Algorithm (Two Pointers Squeeze):
        - Time: O(n)
        - Space: O(1) strictly in-place auxiliary space
        
        Step 1: Reverse entire array.
        Step 2: Reverse first k elements.
        Step 3: Reverse remaining n - k elements.
        """
        n = len(nums)
        k %= n

        def reverse_sub(start: int, end: int) -> None:
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1

        # 1. Reverse entire array
        reverse_sub(0, n - 1)
        # 2. Reverse first k elements
        reverse_sub(0, k - 1)
        # 3. Reverse the rest
        reverse_sub(k, n - 1)


# --- Test Suite ---
def test_rotate_array():
    sol = Solution()

    # Test Case 1: Standard rotation
    nums1 = [1, 2, 3, 4, 5, 6, 7]
    sol.rotate(nums1, 3)
    assert nums1 == [5, 6, 7, 1, 2, 3, 4], f"Test 1 Failed: {nums1}"

    # Test Case 2: Negative numbers
    nums2 = [-1, -100, 3, 99]
    sol.rotate(nums2, 2)
    assert nums2 == [3, 99, -1, -100], f"Test 2 Failed: {nums2}"

    # Test Case 3: k larger than array length (k = 10, len = 4 -> k % 4 = 2)
    nums3 = [1, 2, 3, 4]
    sol.rotate(nums3, 10)
    assert nums3 == [3, 4, 1, 2], f"Test 3 Failed: {nums3}"

    # Test Case 4: k is multiple of len(nums) (no change)
    nums4 = [1, 2, 3]
    sol.rotate(nums4, 3)
    assert nums4 == [1, 2, 3], f"Test 4 Failed: {nums4}"

    # Test Case 5: Single element
    nums5 = [10]
    sol.rotate(nums5, 5)
    assert nums5 == [10], f"Test 5 Failed: {nums5}"

    # Test User's Slice method
    nums_slice = [1, 2, 3, 4, 5, 6, 7]
    sol.rotate_slice(nums_slice, 3)
    assert nums_slice == [5, 6, 7, 1, 2, 3, 4]

    print("✅ All 5 test cases passed successfully for both approaches!")


if __name__ == "__main__":
    test_rotate_array()
