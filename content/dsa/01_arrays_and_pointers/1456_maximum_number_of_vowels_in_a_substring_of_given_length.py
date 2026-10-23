"""
LeetCode 1456: Maximum Number of Vowels in a Substring of Given Length
Pattern: Fixed-Size Sliding Window (Running Differential on Frequencies / Counters)
Difficulty: Medium
Link: https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/
"""

class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        """
        Time Complexity: O(n) - 1 pass over string s
        Space Complexity: O(1) - small fixed set of 5 vowels
        """
        vowels = {'a', 'e', 'i', 'o', 'u'}
        
        # 1. Base window of size k
        count = 0
        for i in range(k):
            if s[i] in vowels:
                count += 1
                
        max_count = count
        # Early exit: you can never exceed k vowels in a window of size k!
        if max_count == k:
            return k
            
        # 2. Slide window from index k to len(s)
        # entering element: s[i]
        # leaving element:  s[i - k]
        for i in range(k, len(s)):
            if s[i] in vowels:
                count += 1
            if s[i - k] in vowels:
                count -= 1
                
            if count > max_count:
                max_count = count
                if max_count == k:
                    return k
                    
        return max_count


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ("abciiidef", 3, 3),
        ("aeiou", 2, 2),
        ("leetcode", 3, 2),
        ("rhythms", 4, 0),
        ("tryhard", 4, 1),
    ]
    
    for s, k, expected in test_cases:
        actual = sol.maxVowels(s, k)
        assert actual == expected, f"Failed on s='{s}', k={k}: expected {expected}, got {actual}"
        print(f"✓ s='{s}', k={k} -> max_vowels = {actual}")
        
    print("\nAll test cases passed!")
