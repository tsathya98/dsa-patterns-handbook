"""
LeetCode 20: Valid Parentheses
URL: https://leetcode.com/problems/valid-parentheses/

Patterns:
1. Baseline: Map Closing -> Opening with stack (The standard textbook approach)
2. Optimized: The "Push-Expected" Pattern + Odd-Length Pruning (0ms, Beats 100%)
"""

class SolutionBaseline:
    def isValid(self, s: str) -> bool:
        """Standard stack approach with closing -> opening dictionary."""
        dct = {
            '}': '{',
            ']': '[',
            ')': '('
        }
        stack = []
        for ch in s:
            if ch not in dct:
                stack.append(ch)
            elif not stack or stack[-1] != dct[ch]:
                return False
            else:
                stack.pop()
        return not stack


class SolutionOptimized:
    def isValid(self, s: str) -> bool:
        """
        Optimized FAANG-grade approach:
        1. Instant O(1) early exit: valid parentheses must have even length!
        2. Push-Expected pattern: push the expected closing bracket.
        3. Direct C iteration via `for ch in s`.
        4. Combined peek & pop via `stack.pop() != ch`.
        """
        if len(s) % 2 != 0:
            return False

        mapping = {'(': ')', '[': ']', '{': '}'}
        stack = []

        for ch in s:
            if ch in mapping:
                stack.append(mapping[ch])  # Push expected closing bracket
            elif not stack or stack.pop() != ch:
                return False

        return not stack


def run_tests():
    sol_base = SolutionBaseline()
    sol_opt = SolutionOptimized()

    test_cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("]", False),
        ("((", False),
        ("", True),
        ("({[()]})", True),
        ("({[([{}])]})", True),
        ("(((((((((()", False),
    ]

    for s, expected in test_cases:
        res1 = sol_base.isValid(s)
        res2 = sol_opt.isValid(s)
        assert res1 == expected, f"Baseline failed on {s}: got {res1}, expected {expected}"
        assert res2 == expected, f"Optimized failed on {s}: got {res2}, expected {expected}"

    print("✅ All unit tests passed successfully for both Baseline & Optimized solutions!")


if __name__ == "__main__":
    run_tests()
