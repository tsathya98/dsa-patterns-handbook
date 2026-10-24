"""
LeetCode 48: Rotate Image
You are given an n x n 2D matrix representing an image, rotate the image
by 90 degrees (clockwise).
You have to rotate the image in-place, which means you have to modify
the input 2D matrix directly. DO NOT allocate another 2D matrix.
"""

from typing import List


class Solution:
    def rotate_reverse_then_transpose(self, matrix: List[List[int]]) -> None:
        """
        Approach 1: Reverse Rows then Transpose (User's Optimal Solution)
        Step 1: Reverse rows top-to-bottom (vertical flip).
        Step 2: Transpose across main diagonal (swap matrix[i][j] and matrix[j][i]).
        Time: O(N^2)
        Space: O(1) in-place
        """
        matrix.reverse()
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    def rotate_transpose_then_reverse_rows(self, matrix: List[List[int]]) -> None:
        """
        Approach 2: Transpose then Reverse Each Row (Textbook Linear Algebra)
        Step 1: Transpose across main diagonal.
        Step 2: Reverse each row left-to-right (horizontal flip).
        Time: O(N^2)
        Space: O(1) in-place
        """
        n = len(matrix)
        # Transpose
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # Reverse each row
        for row in matrix:
            row.reverse()

    def rotate(self, matrix: List[List[int]]) -> None:
        self.rotate_reverse_then_transpose(matrix)


def test_rotate_image():
    sol = Solution()

    test_cases = [
        (
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[7, 4, 1], [8, 5, 2], [9, 6, 3]],
        ),
        (
            [
                [5, 1, 9, 11],
                [2, 4, 8, 10],
                [13, 3, 6, 7],
                [15, 14, 12, 16],
            ],
            [
                [15, 13, 2, 5],
                [14, 3, 4, 1],
                [12, 6, 8, 9],
                [16, 7, 10, 11],
            ],
        ),
        ([[1]], [[1]]),
    ]

    for original, expected in test_cases:
        # Test Approach 1
        mat1 = [row[:] for row in original]
        sol.rotate_reverse_then_transpose(mat1)
        assert mat1 == expected, f"Approach 1 failed on {original}: got {mat1}, expected {expected}"

        # Test Approach 2
        mat2 = [row[:] for row in original]
        sol.rotate_transpose_then_reverse_rows(mat2)
        assert mat2 == expected, f"Approach 2 failed on {original}: got {mat2}, expected {expected}"

    print("All Rotate Image tests passed!")


if __name__ == "__main__":
    test_rotate_image()
