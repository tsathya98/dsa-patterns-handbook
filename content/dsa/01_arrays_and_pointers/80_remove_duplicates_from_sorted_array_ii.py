"""
LeetCode 80: Remove Duplicates from Sorted Array II
URL: https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/

Pattern: Two Pointers (Formation B: Scout & Writer / Fast & Slow with Streak Counter)
Time Complexity: O(n)
Space Complexity: O(1) in-place auxiliary space
"""

from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        User's Intuitive Solution:
        - Scout & Writer with a consecutive duplicate streak counter `tmp`.
        - Allows at most 2 occurrences of any number.
        - Time: O(n), Space: O(1)
        """
        k = 1
        tmp = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1] and tmp < 2:
                tmp += 1
                nums[k] = nums[i]
                k += 1
            elif nums[i] != nums[i - 1]:
                nums[k] = nums[i]
                k += 1
                tmp = 1
        return k

    def removeDuplicates_lookback(self, nums: List[int], max_dups: int = 2) -> int:
        """
        The Senior FAANG 'Lookback K' Generalization:
        - If allowed at most 1 copy (LC 26): compare with nums[k - 1]
        - If allowed at most 2 copies (LC 80): compare with nums[k - 2]
        - If allowed at most M copies: compare with nums[k - M]
        """
        k = 0
        for x in nums:
            # If we haven't written max_dups yet, OR current item is strictly greater
            # than the item written max_dups spots ago, it's safe to write!
            if k < max_dups or x != nums[k - max_dups]:
                nums[k] = x
                k += 1
        return k


# --- Test Suite ---
def test_remove_duplicates_ii():
    sol = Solution()

    # Test Case 1: Standard case from problem description
    nums1 = [1, 1, 1, 2, 2, 3]
    k1 = sol.removeDuplicates(nums1)
    assert k1 == 5, f"Expected 5, got {k1}"
    assert nums1[:k1] == [1, 1, 2, 2, 3], f"Expected [1, 1, 2, 2, 3], got {nums1[:k1]}"

    # Test Case 2: Longer duplicates
    nums2 = [0, 0, 1, 1, 1, 1, 2, 3, 3]
    k2 = sol.removeDuplicates(nums2)
    assert k2 == 7, f"Expected 7, got {k2}"
    assert nums2[:k2] == [0, 0, 1, 1, 2, 3, 3], f"Expected [0, 0, 1, 1, 2, 3, 3], got {nums2[:k2]}"

    # Test Case 3: All elements identical (more than 2)
    nums3 = [4, 4, 4, 4, 4]
    k3 = sol.removeDuplicates(nums3)
    assert k3 == 2, f"Expected 2, got {k3}"
    assert nums3[:k3] == [4, 4], f"Expected [4, 4], got {nums3[:k3]}"

    # Test Case 4: Single element
    nums4 = [99]
    k4 = sol.removeDuplicates(nums4)
    assert k4 == 1, f"Expected 1, got {k4}"
    assert nums4[:k4] == [99], f"Expected [99], got {nums4[:k4]}"

    # Test Case 5: Already valid (at most 2 of each)
    nums5 = [1, 1, 2, 2, 3]
    k5 = sol.removeDuplicates(nums5)
    assert k5 == 5, f"Expected 5, got {k5}"
    assert nums5[:k5] == [1, 1, 2, 2, 3], f"Expected [1, 1, 2, 2, 3], got {nums5[:k5]}"

    # Test Case 6: Verify Lookback generalization
    nums_gen = [0, 0, 1, 1, 1, 1, 2, 3, 3]
    k_gen = sol.removeDuplicates_lookback(nums_gen, max_dups=2)
    assert k_gen == 7
    assert nums_gen[:k_gen] == [0, 0, 1, 1, 2, 3, 3]

    print("✅ All 6 test cases passed successfully for both approaches!")


if __name__ == "__main__":
    test_remove_duplicates_ii()
