"""
LeetCode 13: Roman to Integer
Difficulty: Easy
Pattern: Hash Map / Lookahead Comparison

Key Intuition:
- Lookahead: if dct[s[i]] < dct[s[i + 1]], subtract; otherwise add.
- Avoids nested dictionary-in-list checks, jumping from 10 ms to 2-3 ms.
"""


class SolutionInitial:
    """Initial working solution with sub dictionary and while loop (10 ms)."""

    def romanToInt(self, s: str) -> int:
        dct = {
            "I": 1, "V": 5, "X": 10, "L": 50,
            "C": 100, "D": 500, "M": 1000
        }
        sub = {
            "I": ["V", "X"],
            "X": ["L", "C"],
            "C": ["D", "M"]
        }
        total = 0
        i = 0
        while i < len(s):
            if i < len(s) - 1 and s[i] in sub and s[i + 1] in sub[s[i]]:
                total -= dct[s[i]]
            else:
                total += dct[s[i]]
            i += 1
        return total


class SolutionOptimized:
    """Optimized direct comparison solution with for loop (2-3 ms)."""

    def romanToInt(self, s: str) -> int:
        dct = {
            "I": 1, "V": 5, "X": 10, "L": 50,
            "C": 100, "D": 500, "M": 1000
        }
        total = 0
        n = len(s)
        for i in range(n):
            if i < n - 1 and dct[s[i]] < dct[s[i + 1]]:
                total -= dct[s[i]]
            else:
                total += dct[s[i]]
        return total


class SolutionReplace:
    """The str.replace trick (0-1 ms)."""

    def romanToInt(self, s: str) -> int:
        translations = {
            "I": 1, "V": 5, "X": 10, "L": 50,
            "C": 100, "D": 500, "M": 1000
        }
        s = (s.replace("IV", "IIII")
              .replace("IX", "VIIII")
              .replace("XL", "XXXX")
              .replace("XC", "LXXXX")
              .replace("CD", "CCCC")
              .replace("CM", "DCCCC"))
        return sum(translations[c] for c in s)


if __name__ == "__main__":
    test_cases = [
        ("III", 3),
        ("LVIII", 58),
        ("MCMXCIV", 1994),
        ("IV", 4),
        ("IX", 9),
    ]

    s1 = SolutionInitial()
    s2 = SolutionOptimized()
    s3 = SolutionReplace()

    print("Running tests for LeetCode 13: Roman to Integer...")
    for idx, (roman, expected) in enumerate(test_cases, 1):
        assert s1.romanToInt(roman) == expected, f"Test {idx} failed on SolutionInitial"
        assert s2.romanToInt(roman) == expected, f"Test {idx} failed on SolutionOptimized"
        assert s3.romanToInt(roman) == expected, f"Test {idx} failed on SolutionReplace"
        print(f"Test case {idx}: s='{roman}' -> {expected} (Passed)")

    print("\nAll Roman to Integer tests passed successfully!")
