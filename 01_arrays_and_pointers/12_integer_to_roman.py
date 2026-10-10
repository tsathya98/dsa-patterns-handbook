"""
LeetCode 12: Integer to Roman
Pattern: Greedy Subtraction (ATM / Cashier Pattern)
Difficulty: Medium
"""

class SolutionWhile:
    """
    Approach 1: Whiteboard Friendly (Repeated Subtraction)
    Time Complexity: O(1) - at most 15 inner loop iterations
    Space Complexity: O(1) - fixed symbol mapping
    """
    def intToRoman(self, num: int) -> str:
        dct = {
            1000: 'M', 900: 'CM', 500: 'D', 400: 'CD',
            100: 'C',  90: 'XC',  50: 'L',  40: 'XL',
            10: 'X',   9: 'IX',   5: 'V',   4: 'IV',
            1: 'I'
        }
        tot = []
        for number in dct:
            while num >= number:
                tot.append(dct[number])
                num -= number
        return "".join(tot)


class SolutionMath:
    """
    Approach 2: Mathematical Division & Modulo
    Time Complexity: O(1) - 13 constant operations
    Space Complexity: O(1) - fixed symbol mapping
    """
    def intToRoman(self, num: int) -> str:
        values = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"),  (90, "XC"),  (50, "L"),  (40, "XL"),
            (10, "X"),   (9, "IX"),   (5, "V"),   (4, "IV"),
            (1, "I")
        ]
        res = []
        for val, sym in values:
            if num == 0:
                break
            count = num // val
            if count:
                res.append(sym * count)
                num %= val
        return "".join(res)


if __name__ == "__main__":
    sol_while = SolutionWhile()
    sol_math = SolutionMath()

    test_cases = [
        (3749, "MMMDCCXLIX"),
        (58, "LVIII"),
        (1994, "MCMXCIV"),
        (1, "I"),
        (3999, "MMMCMXCIX")
    ]

    for num, expected in test_cases:
        actual_while = sol_while.intToRoman(num)
        actual_math = sol_math.intToRoman(num)
        assert actual_while == expected, f"While failed for {num}: expected {expected}, got {actual_while}"
        assert actual_math == expected, f"Math failed for {num}: expected {expected}, got {actual_math}"
        print(f"✓ num = {num:4d} -> Roman = '{expected}'")

    print("\nAll test cases passed successfully!")
