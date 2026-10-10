"""
LeetCode 122: Best Time to Buy and Sell Stock II
Difficulty: Medium
Pattern: Greedy (Valley-to-Peak / Telescoping Daily Increments)

Key Intuition:
- Unlimited transactions mean we can capture every single upward price movement.
- Mathematical equivalence: (C - A) == (B - A) + (C - B)
- We do not need to track valleys or hold unrealized profit; simply accumulate prices[i] - prices[i - 1] whenever positive.
"""

from typing import List


class SolutionValleyToPeak:
    """User's Valley-to-Peak approach: Tracks local buy valley x and cashes out on drop or end."""

    def maxProfit(self, prices: List[int]) -> int:
        prof = 0
        x = 0
        temp_prof = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                temp_prof = prices[i] - prices[x]
                if i == len(prices) - 1:
                    prof += temp_prof
            else:
                prof += temp_prof
                temp_prof = 0
                x = i
        return prof


class SolutionGreedy:
    """Optimal 3-line Greedy solution: Accumulates all positive daily differences."""

    def maxProfit(self, prices: List[int]) -> int:
        prof = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                prof += prices[i] - prices[i - 1]
        return prof


if __name__ == "__main__":
    test_cases = [
        ([7, 1, 5, 3, 6, 4], 7),
        ([1, 2, 3, 4, 5], 4),
        ([7, 6, 4, 3, 1], 0),
        ([2, 4, 1], 2),
        ([1], 0),
    ]

    sol_valley = SolutionValleyToPeak()
    sol_greedy = SolutionGreedy()

    print("Running tests for LeetCode 122: Best Time to Buy and Sell Stock II...")
    for idx, (prices, expected) in enumerate(test_cases, 1):
        res1 = sol_valley.maxProfit(prices)
        res2 = sol_greedy.maxProfit(prices)
        assert res1 == expected, f"Test {idx} failed on ValleyToPeak: got {res1}, expected {expected}"
        assert res2 == expected, f"Test {idx} failed on Greedy: got {res2}, expected {expected}"
        print(f"Test case {idx}: prices={prices} -> profit={res1} (Passed)")

    print("\nAll tests passed successfully!")
