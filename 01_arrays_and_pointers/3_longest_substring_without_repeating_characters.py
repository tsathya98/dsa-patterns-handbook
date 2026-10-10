class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        LC 3: Longest Substring Without Repeating Characters
        Pattern: Dynamic Sliding Window (The Rubber Band)
        
        Time Complexity: O(n) - each character added and removed from set at most once
        Auxiliary Space: O(min(n, m)) where m is charset size (at most 128 ASCII chars)
        """
        seen = set()
        left = 0
        max_len = 0
        
        for right in range(len(s)):
            # If incoming character is already in window, shrink from left until duplicate is removed
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
                
            seen.add(s[right])
            max_len = max(max_len, right - left + 1)
            
        return max_len

    def lengthOfLongestSubstring_user(self, s: str) -> int:
        """User's Accepted Version using seen.discard and len(seen) - Beats 95% Memory."""
        seen = set()
        max_cnt = 0
        left = 0
        for i, c in enumerate(s):
            while c in seen:
                seen.discard(s[left])
                left += 1
            seen.add(c)
            max_cnt = max(max_cnt, len(seen))
        return max_cnt

    def lengthOfLongestSubstring_hashmap_jump(self, s: str) -> int:
        """
        Optimal 1-Pass Jump: Uses dict to jump `left` directly past the duplicate.
        """
        last_seen = {}
        left = 0
        max_len = 0
        
        for right, char in enumerate(s):
            if char in last_seen and last_seen[char] >= left:
                left = last_seen[char] + 1
            last_seen[char] = right
            max_len = max(max_len, right - left + 1)
            
        return max_len


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        (" ", 1),
        ("au", 2),
        ("dvdf", 3),
        ("abcdefghijklmnopqrstuvwxyz", 26),
    ]
    
    for string, expected in test_cases:
        assert sol.lengthOfLongestSubstring(string) == expected, f"Failed on {string}"
        assert sol.lengthOfLongestSubstring_user(string) == expected, f"Failed on {string} (user)"
        assert sol.lengthOfLongestSubstring_hashmap_jump(string) == expected, f"Failed on {string} (jump)"
        
    print("All unit tests for LC 3 passed successfully!")
