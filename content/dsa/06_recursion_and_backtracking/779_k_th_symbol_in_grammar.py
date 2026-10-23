"""
LeetCode 779: K-th Symbol in Grammar
https://leetcode.com/problems/k-th-symbol-in-grammar/

We build a table of n rows (1-indexed). Row 1 is "0".
For subsequent rows, replace each 0 with "01", and each 1 with "10".
Given n and k, return the k-th (1-indexed) symbol in the n-th row.
"""


class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        """
        Divide and Conquer / Symmetry Reflection.
        Time: O(n) calls.
        Space: O(n) recursion stack depth.
        """
        if n == 1 and k == 1:
            return 0

        # Row n has 2^(n-1) elements. The midpoint divides it into two halves of size 2^(n-2).
        mid = 2 ** (n - 2)

        if k <= mid:
            # First half is identical to row n-1
            return self.kthGrammar(n - 1, k)
        else:
            # Second half is the exact bit-flip of row n-1 at position (k - mid)
            return 1 - self.kthGrammar(n - 1, k - mid)

    def kthGrammarBitTrick(self, n: int, k: int) -> int:
        """
        Observation: The value is the parity of 1-bits in (k - 1).
        Time: O(1)
        Space: O(1)
        """
        return (k - 1).bit_count() % 2


if __name__ == "__main__":
    sol = Solution()
    assert sol.kthGrammar(1, 1) == 0
    assert sol.kthGrammar(2, 1) == 0
    assert sol.kthGrammar(2, 2) == 1
    assert sol.kthGrammar(4, 5) == 1
    assert sol.kthGrammarBitTrick(4, 5) == 1
    print("K-th Symbol in Grammar tests passed!")
