"""
LeetCode 459: Repeated Substring Pattern
https://leetcode.com/problems/repeated-substring-pattern/

Given a string s, check if it can be constructed by taking a substring of it
and appending multiple copies of the substring together.
"""


class Solution:
    def repeatedSubstringPattern(self, s: str) -> bool:
        """
        Approach 1: String Doubling / Periodic Rotation Trick.
        Time: O(n) average (via Python's optimized Boyer-Moore-Horspool substring search).
        Space: O(n) to store the doubled string.
        """
        # If s has a repeating unit, rotating it by that unit's length produces s again.
        # Doubling s contains all cyclic shifts. Removing the first and last characters
        # excludes the trivial identity shifts at index 0 and index n.
        return s in (s + s)[1:-1]

    def repeatedSubstringPatternDivisors(self, s: str) -> bool:
        """
        Approach 2: Divisor Chunking (The direct intuitive way).
        Time: O(n * sqrt(n)) or O(n^2) worst case.
        Space: O(n) for string reconstruction comparison.
        """
        n = len(s)
        # The repeating substring can at most be half the string's length
        for length in range(1, (n // 2) + 1):
            if n % length == 0:
                chunk = s[:length]
                if chunk * (n // length) == s:
                    return True
        return False


if __name__ == "__main__":
    sol = Solution()
    assert sol.repeatedSubstringPattern("abab") is True
    assert sol.repeatedSubstringPattern("aba") is False
    assert sol.repeatedSubstringPattern("abcabcabcabc") is True
    assert sol.repeatedSubstringPatternDivisors("abab") is True
    assert sol.repeatedSubstringPatternDivisors("aba") is False
    assert sol.repeatedSubstringPatternDivisors("abcabcabcabc") is True
    print("All tests passed!")
