class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        """
        LC 392: Is Subsequence
        Pattern: Two Pointers Formation C (Two Conveyor Belts)
        
        Time Complexity: O(len(t)) - single pass through target string
        Auxiliary Space: O(1) - strictly zero extra memory
        """
        p1, p2 = 0, 0
        
        while p1 < len(s) and p2 < len(t):
            if s[p1] == t[p2]:
                p1 += 1
            p2 += 1
            
        return p1 == len(s)


if __name__ == "__main__":
    sol = Solution()
    
    # Test cases
    assert sol.isSubsequence("abc", "ahbgdc") == True
    assert sol.isSubsequence("axc", "ahbgdc") == False
    assert sol.isSubsequence("", "ahbgdc") == True
    assert sol.isSubsequence("b", "c") == False
    assert sol.isSubsequence("abc", "") == False
    assert sol.isSubsequence("", "") == True
    
    print("All unit tests for LC 392 passed successfully!")
