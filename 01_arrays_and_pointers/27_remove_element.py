"""
LeetCode 27: Remove Element
URL: https://leetcode.com/problems/remove-element/

Pattern: Two Pointers (Formation B: Scout & Writer / Fast & Slow)
Time Complexity: O(n)
Space Complexity: O(1) in-place auxiliary space
"""

from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        Scout & Writer Pattern:
        - i (Scout / Fast): Inspects every element.
        - k (Writer / Slow): Marks the boundary for the next valid element.
        """
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k

    def removeElement_swap_with_tail(self, nums: List[int], val: int) -> int:
        """
        Alternative: Two Pointers Squeeze (Optimal when elements to remove are rare)
        Reduces number of assignments/writes.
        """
        i = 0
        n = len(nums)
        while i < n:
            if nums[i] == val:
                nums[i] = nums[n - 1]
                n -= 1
            else:
                i += 1
        return n


# --- Test Suite ---
def test_remove_element():
    sol = Solution()

    # Test Case 1: Standard case
    nums1 = [3, 2, 2, 3]
    k1 = sol.removeElement(nums1, 3)
    assert k1 == 2, f"Expected k=2, got {k1}"
    assert sorted(nums1[:k1]) == [2, 2], f"Expected [2, 2], got {nums1[:k1]}"

    # Test Case 2: Multiple elements, mixed order
    nums2 = [0, 1, 2, 2, 3, 0, 4, 2]
    k2 = sol.removeElement(nums2, 2)
    assert k2 == 5, f"Expected k=5, got {k2}"
    assert sorted(nums2[:k2]) == [0, 0, 1, 3, 4], f"Expected [0, 0, 1, 3, 4], got {nums2[:k2]}"

    # Test Case 3: All elements equal val
    nums3 = [7, 7, 7]
    k3 = sol.removeElement(nums3, 7)
    assert k3 == 0, f"Expected k=0, got {k3}"
    assert nums3[:k3] == [], f"Expected [], got {nums3[:k3]}"

    # Test Case 4: No elements equal val
    nums4 = [1, 2, 3]
    k4 = sol.removeElement(nums4, 5)
    assert k4 == 3, f"Expected k=3, got {k4}"
    assert nums4[:k4] == [1, 2, 3], f"Expected [1, 2, 3], got {nums4[:k4]}"

    # Test Case 5: Empty array
    nums5 = []
    k5 = sol.removeElement(nums5, 1)
    assert k5 == 0, f"Expected k=0, got {k5}"

    # Verify alternative approach passes as well
    nums_alt = [0, 1, 2, 2, 3, 0, 4, 2]
    k_alt = sol.removeElement_swap_with_tail(nums_alt, 2)
    assert k_alt == 5
    assert sorted(nums_alt[:k_alt]) == [0, 0, 1, 3, 4]

    print("✅ All 5 test cases passed successfully for both approaches!")


if __name__ == "__main__":
    test_remove_element()
