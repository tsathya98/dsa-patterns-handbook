class Solution:
    def kthFactor_brute_force(self, n: int, k: int) -> int:
        """
        Approach 1: Brute Force Linear Scan
        Time: O(n)
        Space: O(1)
        """
        for i in range(1, n + 1):
            if n % i == 0:
                k -= 1
                if k == 0:
                    return i
        return -1

    def kthFactor_semi_optimized(self, n: int, k: int) -> int:
        """
        Approach 2: Semi-Optimized / Intuitive (Symmetric Pairs with Sort)
        Collect pairs (i, n // i) up to sqrt(n), sort, and pick index k - 1.
        Time: O(sqrt(n) + d log d) where d is number of factors
        Space: O(d)
        """
        factors = []
        i = 1
        while i * i <= n:
            if n % i == 0:
                factors.append(i)
                if i * i != n:
                    factors.append(n // i)
            i += 1

        factors.sort()
        return factors[k - 1] if k <= len(factors) else -1

    def kthFactor(self, n: int, k: int) -> int:
        """
        Approach 3: Optimized Two-Pass Count (No Sort, O(1) Space)
        Pass 1: small factors (1 to sqrt(n)) in ascending order.
        Pass 2: large factors (sqrt(n) down to 1) via (n // i) in ascending order.
        Time: O(sqrt(n))
        Space: O(1)
        """
        i = 1
        while i * i <= n:
            if n % i == 0:
                k -= 1
                if k == 0:
                    return i
            i += 1

        i -= 1
        if i * i == n:
            i -= 1

        while i >= 1:
            if n % i == 0:
                k -= 1
                if k == 0:
                    return n // i
            i -= 1

        return -1


def test_all_approaches():
    sol = Solution()
    approaches = [
        ("Brute Force", sol.kthFactor_brute_force),
        ("Semi-Optimized", sol.kthFactor_semi_optimized),
        ("Optimized", sol.kthFactor),
    ]

    test_cases = [
        (12, 3, 3),
        (7, 2, 7),
        (4, 4, -1),
        (36, 5, 6),
        (36, 6, 9),
        (36, 9, 36),
        (36, 10, -1),
        (1, 1, 1),
        (1, 2, -1),
        (13, 2, 13),
    ]

    for name, fn in approaches:
        for n, k, expected in test_cases:
            res = fn(n, k)
            assert res == expected, f"{name} failed on n={n}, k={k}: got {res}, expected {expected}"

    print("All 3 approaches (Brute, Semi-Optimized, Optimized) passed all tests!")


if __name__ == "__main__":
    test_all_approaches()
