"""
LeetCode 51: N-Queens
https://leetcode.com/problems/n-queens/

Place n queens on an n x n chessboard such that no two queens attack each other.
Return all distinct solutions to the n-queens puzzle.
"""


class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        """
        Backtracking with O(1) set lookup for diagonals.
        Time: O(N!) where N is the board dimension.
        Space: O(N) auxiliary sets and recursion stack.
        """
        res: list[list[str]] = []
        board: list[list[str]] = [["."] * n for _ in range(n)]

        cols: set[int] = set()
        diag: set[int] = set()       # row - col is constant on main diagonals
        anti_diag: set[int] = set()  # row + col is constant on anti diagonals

        def backtrack(row: int) -> None:
            if row == n:
                res.append(["".join(r) for r in board])
                return

            for col in range(n):
                if col in cols or (row - col) in diag or (row + col) in anti_diag:
                    continue

                # 1. Choose
                board[row][col] = "Q"
                cols.add(col)
                diag.add(row - col)
                anti_diag.add(row + col)

                # 2. Explore
                backtrack(row + 1)

                # 3. Undo
                board[row][col] = "."
                cols.remove(col)
                diag.remove(row - col)
                anti_diag.remove(row + col)

        backtrack(0)
        return res


if __name__ == "__main__":
    sol = Solution()
    ans4 = sol.solveNQueens(4)
    assert len(ans4) == 2
    assert [".Q..", "...Q", "Q...", "..Q."] in ans4
    assert ["..Q.", "Q...", "...Q", ".Q.."] in ans4
    assert len(sol.solveNQueens(1)) == 1
    print("N-Queens tests passed!")
