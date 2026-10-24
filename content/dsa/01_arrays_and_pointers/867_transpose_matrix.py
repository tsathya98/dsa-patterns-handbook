"""
LeetCode 867: Transpose Matrix
Given a 2D integer array matrix, return the transpose of matrix.
The transpose of a matrix is the matrix flipped over its main diagonal,
switching the matrix's row and column indices.
"""

from typing import List


class Solution:
    def transpose_nested_loop(self, matrix: List[List[int]]) -> List[List[int]]:
        """
        Approach 1: Clean Coordinate Mapping (FAANG Standard)
        Allocates a new matrix with swapped dimensions (C rows x R cols).
        Iterates over matrix cells (i, j) and writes to mat[j][i].
        Time: O(R * C)
        Space: O(R * C) for result matrix
        """
        R = len(matrix)
        C = len(matrix[0])

        mat = [[0 for _ in range(R)] for _ in range(C)]

        for i in range(R):
            for j in range(C):
                mat[j][i] = matrix[i][j]

        return mat

    def transpose_zip(self, matrix: List[List[int]]) -> List[List[int]]:
        """
        Approach 2: Pythonic Zip Trick
        Unpacks all rows as arguments to zip(*matrix), which groups
        matching column indices into tuples at compiled C speed.
        Time: O(R * C)
        Space: O(R * C)
        """
        return [list(col) for col in zip(*matrix)]

    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        return self.transpose_nested_loop(matrix)


def test_transpose_matrix():
    sol = Solution()
    approaches = [
        ("Nested Loop", sol.transpose_nested_loop),
        ("Zip Trick", sol.transpose_zip),
        ("Default Transpose", sol.transpose),
    ]

    test_cases = [
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
        ),
        (
            [[1, 2, 3], [4, 5, 6]],
            [[1, 4], [2, 5], [3, 6]],
        ),
        (
            [[1]],
            [[1]],
        ),
        (
            [[1, 2], [3, 4]],
            [[1, 3], [2, 4]],
        ),
        (
            [[1, 2, 3, 4]],
            [[1], [2], [3], [4]],
        ),
    ]

    for name, fn in approaches:
        for mat, expected in test_cases:
            res = fn(mat)
            assert res == expected, f"{name} failed on {mat}: got {res}, expected {expected}"

    print("All Transpose Matrix tests passed!")


if __name__ == "__main__":
    test_transpose_matrix()
