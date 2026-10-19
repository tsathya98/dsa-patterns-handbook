class Solution:
    def kthFactor(self, n: int, k: int) -> int:
        """
        Find the kth factor of n in O(sqrt(n)) time and O(1) auxiliary space.

        Intuition:
        - Factor pairs (i, n // i) are symmetric around sqrt(n).
        - Pass 1: Loop i from 1 to floor(sqrt(n)). Small factors are naturally ascending.
          Decrement k on each hit. If k == 0, return i.
        - Pass 2: If k > 0, the answer lies in the large partner factors.
          Walking i backwards from floor(sqrt(n)) down to 1 generates (n // i) in ascending order!
          Skip i if i * i == n to prevent double-counting the square root.
        """
        # Pass 1: Check small factors (1 to sqrt(n))
        i = 1
        while i * i <= n:
            if n % i == 0:
                k -= 1
                if k == 0:
                    return i
            i += 1

        # Step back to the largest checked integer
        i -= 1

        # If n is a perfect square, skip the square root so it is not checked twice
        if i * i == n:
            i -= 1

        # Pass 2: Check large factors in ascending order by walking i backward
        while i >= 1:
            if n % i == 0:
                k -= 1
                if k == 0:
                    return n // i
            i -= 1

        return -1


def test_kth_factor():
    sol = Solution()

    # LeetCode examples
    assert sol.kthFactor(12, 3) == 3, "Factors of 12: [1, 2, 3, 4, 6, 12], 3rd is 3"
    assert sol.kthFactor(7, 2) == 7, "Factors of 7: [1, 7], 2nd is 7"
    assert sol.kthFactor(4, 4) == -1, "Factors of 4: [1, 2, 4], 4th does not exist"

    # Perfect square case (36: [1, 2, 3, 4, 6, 9, 12, 18, 36])
    assert sol.kthFactor(36, 5) == 6, "5th factor of 36 is 6 (square root)"
    assert sol.kthFactor(36, 6) == 9, "6th factor of 36 is 9 (first large partner)"
    assert sol.kthFactor(36, 9) == 36, "9th factor of 36 is 36"
    assert sol.kthFactor(36, 10) == -1, "10th factor of 36 does not exist"

    # Prime case
    assert sol.kthFactor(13, 1) == 1
    assert sol.kthFactor(13, 2) == 13
    assert sol.kthFactor(13, 3) == -1

    # N = 1 boundary
    assert sol.kthFactor(1, 1) == 1
    assert sol.kthFactor(1, 2) == -1

    print("All 1492 tests passed successfully!")


if __name__ == "__main__":
    test_kth_factor()
