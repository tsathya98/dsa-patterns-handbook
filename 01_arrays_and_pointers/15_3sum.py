"""
LeetCode 15: 3Sum
Difficulty: Medium
Pattern: Two Pointers (1 Fixed Anchor + The Squeeze)

Core Idea:
1. Sort the array so numbers go from Smallest -> Largest.
2. Fix an anchor `p1` with an outer for-loop.
3. Squeeze `p2` and `p3` inward like Two Sum II.
4. Skip duplicate anchors and duplicate inner values (Clothing Rack Analogy).
"""

from typing import List


class SolutionSetDeduplication:
    """Initial Working Version: Uses set() to deduplicate (2325 ms on LeetCode)."""

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        out = set()
        nums.sort()
        for p1 in range(len(nums) - 2):
            p2 = p1 + 1
            p3 = len(nums) - 1
            while p2 < p3:
                total = nums[p1] + nums[p2] + nums[p3]
                if total == 0:
                    out.add((nums[p1], nums[p2], nums[p3]))
                    p2 += 1
                    p3 -= 1
                elif total > 0:
                    p3 -= 1
                else:
                    p2 += 1
        return [list(t) for t in out]


class SolutionOptimized:
    """User's Optimized Version: In-place duplicate skipping and early exit (~450 ms on LeetCode)."""

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        out = []    
        nums.sort()
        for p1 in range(len(nums)-2):
            if nums[p1] > 0:
                break
            if p1 > 0 and nums[p1] == nums[p1-1]:
                continue
            p2 = p1 + 1
            p3 = len(nums) - 1
            while p2 < p3:
                total = nums[p1] + nums[p2] + nums[p3]
                if total == 0:
                    out.append([nums[p1], nums[p2], nums[p3]])
                    p2 += 1
                    while p2 < p3 and nums[p2] == nums[p2-1]:
                        p2 += 1
                    p3 -= 1
                    while p2 < p3 and nums[p3] == nums[p3+1]:
                        p3 -= 1
                elif total > 0:
                    p3 -= 1
                else:
                    p2 += 1
        return out


class SolutionUserAccepted:
    """User's Accepted Version: Two Pointers with in-place deduplication."""

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        lst = []
        for i in range(1, len(nums)):
            pivot = i - 1
            if i != 1 and nums[pivot] == nums[pivot - 1]:
                continue
            l, r = i, len(nums) - 1
            while l < r:
                summation = nums[pivot] + nums[l] + nums[r]
                if summation == 0:
                    lst.append([nums[pivot], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
                    while l < r and nums[r] == nums[r + 1]:
                        r -= 1
                elif summation > 0:
                    r -= 1
                else:
                    l += 1
        return lst



if __name__ == "__main__":
    test_cases = [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([-2, 0, 0, 2, 2], [[-2, 0, 2]]),
    ]

    sol_set = SolutionSetDeduplication()
    sol_opt = SolutionOptimized()
    sol_user = SolutionUserAccepted()

    print("Running tests for LeetCode 15: 3Sum...")
    for idx, (nums, expected) in enumerate(test_cases, 1):
        res1 = sorted([sorted(x) for x in sol_set.threeSum(list(nums))])
        res2 = sorted([sorted(x) for x in sol_opt.threeSum(list(nums))])
        res3 = sorted([sorted(x) for x in sol_user.threeSum(list(nums))])
        exp = sorted([sorted(x) for x in expected])
        assert res1 == exp, f"Test {idx} failed on Set version: got {res1}, expected {exp}"
        assert res2 == exp, f"Test {idx} failed on Optimized version: got {res2}, expected {exp}"
        assert res3 == exp, f"Test {idx} failed on User version: got {res3}, expected {exp}"
        print(f"Test case {idx}: nums={nums} -> {res3} (Passed)")

    print("\nAll 3Sum tests passed successfully!")
