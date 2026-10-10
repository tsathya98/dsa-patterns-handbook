class Solution:
    def isPalindrome(self, s: str) -> bool:
        """
        LC 125: Valid Palindrome
        Two Pointers Formation A: Inward Squeeze
        
        Time Complexity: O(n)
        Auxiliary Space: O(1) - strictly in-place, zero string recreation
        """
        l, r = 0, len(s) - 1
        
        while l < r:
            if not s[l].isalnum():
                l += 1
            elif not s[r].isalnum():
                r -= 1
            elif s[l].lower() == s[r].lower():
                l += 1
                r -= 1
            else:
                return False
                
        return True


if __name__ == "__main__":
    sol = Solution()
    
    # Test cases
    assert sol.isPalindrome("A man, a plan, a canal: Panama") == True
    assert sol.isPalindrome("race a car") == False
    assert sol.isPalindrome(" ") == True
    assert sol.isPalindrome("0P") == False
    assert sol.isPalindrome("a.") == True
    assert sol.isPalindrome(".,") == True
    
    print("All unit tests for LC 125 passed successfully!")
