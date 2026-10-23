"""
LeetCode 228: Summary Ranges
URL: https://leetcode.com/problems/summary-ranges/

Pattern: Two Pointers Formation D (Anchor & Scout / Interval Chunking)
"""

from typing import List


class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        """
        Two Pointers Formation D: Anchor & Scout.
        - `start = nums[i]` anchors the beginning of the contiguous chunk.
        - Inner `while` advances `i` as long as consecutive condition holds.
        - Eliminates the 'lost final range' bug and handles empty lists naturally.
        """
        res: List[str] = []
        i = 0
        n = len(nums)

        while i < n:
            start = nums[i]

            # Fast-forward i as long as the run is consecutive
            while i + 1 < n and nums[i + 1] == nums[i] + 1:
                i += 1

            # Format the output based on whether it is a single number or a range
            if start == nums[i]:
                res.append(str(start))
            else:
                res.append(f"{start}->{nums[i]}")

            # Advance to start the next chunk
            i += 1

        return res


def run_tests():
    sol = Solution()

    test_cases = [
        ([0, 1, 2, 4, 5, 7], ["0->2", "4->5", "7"]),
        ([0, 2, 3, 4, 6, 8, 9], ["0", "2->4", "6", "8->9"]),
        ([], []),
        ([-1], ["-1"]),
        ([0], ["0"]),
        ([1, 2, 3, 4, 5], ["1->5"]),
        ([-3, -2, -1, 1, 2], ["-3->-1", "1->2"]),
    ]

    for nums, expected in test_cases:
        res = sol.summaryRanges(nums)
        assert res == expected, f"Failed on {nums}: got {res}, expected {expected}"

    print("✅ All unit tests passed successfully for LeetCode 228 Summary Ranges!")


if __name__ == "__main__":
    run_tests()
