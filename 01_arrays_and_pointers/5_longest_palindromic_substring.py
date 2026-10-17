"""
LeetCode 5: Longest Palindromic Substring
Difficulty: Medium
Pattern: Two Pointers Formation F (Outward Expand Around Center / The Flashlight Beam)
Time Complexity: O(n^2)
Auxiliary Space: O(1) (ignoring output string slice)
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        def _expand(l: int, r: int) -> str:
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l + 1 : r]

        max_len = 0
        max_pal = ""
        for i in range(len(s)):
            pal = _expand(i, i)
            if len(pal) > max_len:
                max_len = len(pal)
                max_pal = pal
            pal = _expand(i, i + 1)
            if len(pal) > max_len:
                max_len = len(pal)
                max_pal = pal
        return max_pal

    def longestPalindromeNoInnerSlice(self, s: str) -> str:
        """
        Zero-Slice Micro-Optimization:
        Instead of slicing a string on every single center (2n slices),
        return (start, length) or indices and slice ONCE at the very end!
        """
        n = len(s)
        if n <= 1:
            return s

        best_start = 0
        max_len = 1

        for i in range(n):
            # 1. Odd length center (i, i)
            l, r = i, i
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            if r - l - 1 > max_len:
                max_len = r - l - 1
                best_start = l + 1

            # 2. Even length center (i, i + 1)
            l, r = i, i + 1
            while l >= 0 and r < n and s[l] == s[r]:
                l -= 1
                r += 1
            if r - l - 1 > max_len:
                max_len = r - l - 1
                best_start = l + 1

        return s[best_start : best_start + max_len]
