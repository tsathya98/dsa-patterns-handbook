"""
LeetCode 78: Subsets
https://leetcode.com/problems/subsets/

Given an integer array nums of unique elements, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.
"""


class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        """
        Standard Backtracking (start index increment).
        Time: O(n * 2^n)
        Space: O(n) recursion call stack.
        """
        res: list[list[int]] = []
        path: list[int] = []

        def backtrack(start: int) -> None:
            # Every state reached in the search tree is a valid subset
            res.append(path[:])

            for i in range(start, len(nums)):
                path.append(nums[i])      # 1. Choose
                backtrack(i + 1)           # 2. Explore
                path.pop()                 # 3. Undo

        backtrack(0)
        return res

    def subsetsPickSkip(self, nums: list[int]) -> list[list[int]]:
        """
        Alternative Pick/Skip Binary Decision Tree (from Cohort).
        """
        res: list[list[int]] = []
        path: list[int] = []

        def dfs(i: int) -> None:
            if i == len(nums):
                res.append(path[:])
                return

            # Branch 1: Pick nums[i]
            path.append(nums[i])
            dfs(i + 1)
            path.pop()

            # Branch 2: Skip nums[i]
            dfs(i + 1)

        dfs(0)
        return res


if __name__ == "__main__":
    sol = Solution()
    ans = sol.subsets([1, 2, 3])
    assert len(ans) == 8
    assert [] in ans
    assert [1] in ans
    assert [1, 2, 3] in ans

    ans2 = sol.subsetsPickSkip([1, 2, 3])
    assert len(ans2) == 8
    print("Subsets tests passed!")
