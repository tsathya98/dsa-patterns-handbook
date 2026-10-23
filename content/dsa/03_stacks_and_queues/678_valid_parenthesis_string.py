from typing import List

class Solution:
    def checkValidString(self, s: str) -> bool:
        """
        LC 678: Valid Parenthesis String
        
        Two Stacks Approach:
        - open_stack: stores indices of '('
        - star_stack: stores indices of '*'
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        open_stack = []
        star_stack = []
        
        for i, ch in enumerate(s):
            if ch == '(':
                open_stack.append(i)
            elif ch == '*':
                star_stack.append(i)
            else: # ch == ')'
                # Greedily consume '(' first!
                if open_stack:
                    open_stack.pop()
                # If no '(', use a '*' to act as '('
                elif star_stack:
                    star_stack.pop()
                # No '(' and no '*' to balance this ')'
                else:
                    return False
        
        # Balance remaining '(' with '*' that appear AFTER them
        while open_stack and star_stack:
            # A '*' can only close a '(' if it comes AFTER it (star index > open index)
            if open_stack[-1] < star_stack[-1]:
                open_stack.pop()
                star_stack.pop()
            else:
                # The '(' came after the '*' (e.g., "*("), so '*' cannot close it
                return False
                
        # If all '(' are matched, remaining '*' can simply act as empty strings ""
        return len(open_stack) == 0


if __name__ == "__main__":
    sol = Solution()
    
    # Base test cases
    assert sol.checkValidString("()") == True
    assert sol.checkValidString("(*)") == True
    assert sol.checkValidString("(*))") == True
    assert sol.checkValidString(")*(") == False
    assert sol.checkValidString("*( ") == False
    
    # Complex case from LeetCode
    long_case = "(((((*(()((((*((**(((()()((())((((()))())())())())()())))))))())()()((((((()))((())(()))())"
    assert sol.checkValidString(long_case) == False
    
    print("All unit tests for LC 678 passed successfully!")
