"""
LeetCode 150: Evaluate Reverse Polish Notation
Evaluate the value of an arithmetic expression in Reverse Polish Notation (Postfix).
Valid operators: '+', '-', '*', '/'.
Division truncates toward zero.
"""

from typing import List


class Solution:
    def evalRPN_brute_force(self, tokens: List[str]) -> int:
        """
        Approach 1: In-place Array Reduction / Slicing
        Repeatedly find the first operator, compute the result of the two operands
        before it, and replace the 3 elements with the result.
        Time: O(N^2) due to repeated O(N) list removals/shifts.
        Space: O(N) auxiliary copies.
        """
        curr = tokens[:]
        ops = {"+", "-", "*", "/"}

        while len(curr) > 1:
            i = 0
            while i < len(curr) and curr[i] not in ops:
                i += 1

            op = curr[i]
            left = int(curr[i - 2])
            right = int(curr[i - 1])

            if op == "+":
                res = left + right
            elif op == "-":
                res = left - right
            elif op == "*":
                res = left * right
            else:
                res = int(left / right)

            curr = curr[: i - 2] + [str(res)] + curr[i + 1 :]

        return int(curr[0])

    def evalRPN_stack_user(self, tokens: List[str]) -> int:
        """
        Approach 2: User's Stack Solution (Accepted)
        Time: O(N)
        Space: O(N)
        """
        stack = []
        for token in tokens:
            if token not in "+-*/":
                stack.append(int(token))
            else:
                a = stack.pop()
                b = stack.pop()
                if token == "+":
                    stack.append(b + a)
                elif token == "-":
                    stack.append(b - a)
                elif token == "*":
                    stack.append(b * a)
                elif token == "/":
                    stack.append(int(b / a))
        return stack[0]

    def evalRPN(self, tokens: List[str]) -> int:
        """
        Approach 3: Clean Optimized Stack (FAANG Benchmark)
        Explicit set lookup, clear left/right operand naming, int(a / b) truncation.
        Time: O(N) single pass.
        Space: O(N) stack.
        """
        stack: List[int] = []
        ops = {"+", "-", "*", "/"}

        for token in tokens:
            if token not in ops:
                stack.append(int(token))
            else:
                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "*":
                    stack.append(left * right)
                else:
                    stack.append(int(left / right))

        return stack[0]


def test_eval_rpn():
    sol = Solution()
    approaches = [
        ("Array Reduction (Brute Force)", sol.evalRPN_brute_force),
        ("User Stack", sol.evalRPN_stack_user),
        ("Optimized Stack (FAANG)", sol.evalRPN),
    ]

    test_cases = [
        (["2", "1", "+", "3", "*"], 9),
        (["4", "13", "5", "/", "+"], 6),
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
        (["4", "3", "-"], 1),
        (["3", "4", "-"], -1),
        (["-3", "2", "/"], -1),  # Tests truncate toward zero (-1.5 -> -1)
        (["3", "-2", "/"], -1),
        (["18"], 18),
    ]

    for name, fn in approaches:
        for tokens, expected in test_cases:
            res = fn(tokens)
            assert res == expected, f"{name} failed on {tokens}: got {res}, expected {expected}"

    print("All Evaluate Reverse Polish Notation tests passed!")


if __name__ == "__main__":
    test_eval_rpn()
