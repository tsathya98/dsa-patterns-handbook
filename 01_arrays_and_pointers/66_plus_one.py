"""
LeetCode 66: Plus One
URL: https://leetcode.com/problems/plus-one/

Patterns:
1. One-Liner (Pythonic string-integer conversion - works in Python, fails on 64-bit integer overflow in C++/Java).
2. Schoolbook Addition / The Car Odometer Pattern (Optimal O(n) time, O(1) auxiliary space).
"""

from typing import List


class SolutionOneLiner:
    def plusOne(self, digits: List[int]) -> List[int]:
        """
        Python string conversion one-liner.
        Caution: Interviewers usually reject this because large arrays overflow 64-bit ints in C++/Java.
        """
        return [int(x) for x in str(int("".join(map(str, digits))) + 1)]


class SolutionOdometer:
    def plusOne(self, digits: List[int]) -> List[int]:
        """
        The Car Odometer Pattern (Schoolbook Addition):
        - Walk from right to left (end to index 0).
        - If digit < 9: increment and return immediately (O(1) best case).
        - If digit == 9: roll over to 0 and continue loop to carry 1 leftward.
        - If loop finishes: all digits were 9 (e.g. [9,9,9] became [0,0,0]).
          Prepend [1] to get [1, 0, 0, 0].
        """
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits

            digits[i] = 0

        # If we exited the loop, every single digit was 9 and rolled over to 0!
        return [1] + digits


def run_tests():
    sol1 = SolutionOneLiner()
    sol2 = SolutionOdometer()

    test_cases = [
        ([1, 2, 3], [1, 2, 4]),
        ([4, 3, 2, 1], [4, 3, 2, 2]),
        ([9], [1, 0]),
        ([9, 9, 9], [1, 0, 0, 0]),
        ([1, 2, 9], [1, 3, 0]),
        ([0], [1]),
        ([8, 9, 9, 9], [9, 0, 0, 0]),
    ]

    for digits, expected in test_cases:
        res1 = sol1.plusOne(digits.copy())
        res2 = sol2.plusOne(digits.copy())
        assert res1 == expected, f"OneLiner failed on {digits}: got {res1}, expected {expected}"
        assert res2 == expected, f"Odometer failed on {digits}: got {res2}, expected {expected}"

    print("✅ All unit tests passed successfully for LeetCode 66 Plus One!")


if __name__ == "__main__":
    run_tests()
