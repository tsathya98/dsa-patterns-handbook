"""
LeetCode 241: Different Ways to Add Parentheses
https://leetcode.com/problems/different-ways-to-add-parentheses/

Given a string expression of numbers and operators, return all possible results
from computing all the different possible ways to group numbers and operators.
"""


class Solution:
    def diffWaysToCompute(self, expression: str) -> list[int]:
        """
        Divide and Conquer on Operators with memoization.
        Time: O(Catalan(n)) combinations.
        Space: O(Catalan(n)) result storage and recursion depth.
        """
        memo: dict[str, list[int]] = {}

        def compute(expr: str) -> list[int]:
            if expr in memo:
                return memo[expr]

            res: list[int] = []

            for i, ch in enumerate(expr):
                if ch in "+-*":
                    left_results = compute(expr[:i])
                    right_results = compute(expr[i + 1:])

                    for l in left_results:
                        for r in right_results:
                            if ch == "+":
                                res.append(l + r)
                            elif ch == "-":
                                res.append(l - r)
                            elif ch == "*":
                                res.append(l * r)

            # Base case: purely a number without operators
            if not res:
                res.append(int(expr))

            memo[expr] = res
            return res

        return compute(expression)


if __name__ == "__main__":
    sol = Solution()
    ans1 = sorted(sol.diffWaysToCompute("2-1-1"))
    assert ans1 == [0, 2]
    ans2 = sorted(sol.diffWaysToCompute("2*3-4*5"))
    assert ans2 == [-34, -14, -10, -10, 10]
    print("Different Ways to Add Parentheses tests passed!")
