"""
LeetCode 290: Word Pattern
Pattern: HashMaps / Bijective (1-to-1) Mapping
Difficulty: Easy
Link: https://leetcode.com/problems/word-pattern/
"""

class SolutionUser:
    """
    Approach 1: Single Map + `in dct.values()`
    Works for LeetCode's constraints because |pattern| <= 300 and unique letters <= 26.
    Note: `in dct.values()` is an O(k) linear scan of the values.
    """
    def wordPattern(self, pattern: str, s: str) -> bool:
        lst = s.split(" ")
        if len(pattern) != len(lst):
            return False
        dct = {}
        for i in range(len(pattern)):
            if pattern[i] not in dct:
                if lst[i] in dct.values():  # O(k) linear search across values
                    return False
                dct[pattern[i]] = lst[i]
            elif dct[pattern[i]] != lst[i]:
                return False
        return True


class SolutionTwoMaps:
    """
    Approach 2: Pure O(n) Two-Way (Bijective) Mapping
    Uses two HashMaps (or HashMap + Set) to ensure 100% O(1) lookups for both directions.
    Guaranteed O(n) regardless of alphabet size.
    """
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(" ")
        if len(pattern) != len(words):
            return False
            
        p_to_w = {}
        w_to_p = {}
        
        for p, w in zip(pattern, words):
            if (p in p_to_w and p_to_w[p] != w) or (w in w_to_p and w_to_p[w] != p):
                return False
            p_to_w[p] = w
            w_to_p[w] = p
            
        return True


class SolutionCanonicalZip:
    """
    Approach 3: Pythonic Canonical Comparison
    Compares the first occurrence index or zip lengths.
    len(set(pattern)) == len(set(words)) == len(set(zip(pattern, words)))
    """
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(" ")
        if len(pattern) != len(words):
            return False
        return len(set(pattern)) == len(set(words)) == len(set(zip(pattern, words)))


if __name__ == "__main__":
    sol1 = SolutionUser()
    sol2 = SolutionTwoMaps()
    sol3 = SolutionCanonicalZip()
    
    test_cases = [
        ("abba", "dog cat cat dog", True),
        ("abba", "dog cat cat fish", False),
        ("aaaa", "dog cat cat dog", False),
        ("abba", "dog dog dog dog", False),
        ("abc", "dog cat", False),
    ]
    
    for pat, text, expected in test_cases:
        for sol in [sol1, sol2, sol3]:
            actual = sol.wordPattern(pat, text)
            assert actual == expected, f"Failed on '{pat}' / '{text}' with {sol.__class__.__name__}"
        print(f"✓ pattern='{pat}', s='{text}' -> {expected}")
        
    print("\nAll solutions passed all test cases successfully!")
