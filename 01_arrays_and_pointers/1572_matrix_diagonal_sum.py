class Solution:
    def diagonalSum_brute_force(self, mat: list[list[int]]) -> int:
        """
        Approach 1: Brute Force Full Grid Scan
        Time: O(N^2)
        Space: O(1)
        """
        n = len(mat)
        total = 0
        for r in range(n):
            for c in range(n):
                if r == c or r + c == n - 1:
                    total += mat[r][c]
        return total

    def diagonalSum_semi_optimized(self, mat: list[list[int]]) -> int:
        """
        Approach 2: Semi-Optimized / Intuitive Single Loop with Branching
        Check i == n - 1 - i inside the loop to avoid double counting the center.
        Time: O(N)
        Space: O(1)
        """
        n = len(mat)
        total = 0
        for i in range(n):
            if i == n - 1 - i:
                total += mat[i][i]
                continue
            total += mat[i][i] + mat[i][n - 1 - i]
        return total

    def diagonalSum(self, mat: list[list[int]]) -> int:
        """
        Approach 3: Optimized Single Loop (Branchless Hot Loop)
        Accumulate both diagonals directly, subtract center once at the end if n is odd.
        Time: O(N)
        Space: O(1)
        """
        n = len(mat)
        total = 0
        for i in range(n):
            total += mat[i][i] + mat[i][n - 1 - i]

        if n % 2 == 1:
            total -= mat[n // 2][n // 2]

        return total


def test_diagonal_sum():
    sol = Solution()
    approaches = [
        ("Brute Force", sol.diagonalSum_brute_force),
        ("Semi-Optimized In-Loop Branch", sol.diagonalSum_semi_optimized),
        ("Optimized Branchless", sol.diagonalSum),
    ]

    test_cases = [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 25),
        ([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]], 8),
        ([[5]], 5),
        ([[1, 2], [3, 4]], 10),
    ]

    for name, fn in approaches:
        for mat, expected in test_cases:
            res = fn(mat)
            assert res == expected, f"{name} failed on {mat}: got {res}, expected {expected}"

    print("All 3 approaches for LC 1572 passed successfully!")


if __name__ == "__main__":
    test_diagonal_sum()
