"""
LeetCode 206: Reverse Linked List
Pattern: Linked List In-Place Arrow Reversal (The Conga Line 4-Beat Dance)
Difficulty: Easy
Link: https://leetcode.com/problems/reverse-linked-list/
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def to_list(self):
        result = []
        curr = self
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result

    @staticmethod
    def from_list(lst):
        if not lst:
            return None
        dummy = ListNode()
        curr = dummy
        for val in lst:
            curr.next = ListNode(val)
            curr = curr.next
        return dummy.next


class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        """
        Time Complexity: O(n) - exactly one pass through the list
        Space Complexity: O(1) - in-place reversal, 0 new nodes allocated
        """
        prev = None
        cur = head
        
        while cur:
            nxt = cur.next    # Beat 1 (Spotter): Hold child in front so they don't run off
            cur.next = prev   # Beat 2 (Turn Around): Grab backpack of person behind you
            prev = cur        # Beat 3 (Slide Prev): You are now the person behind for next round
            cur = nxt         # Beat 4 (Slide Cur): Next child's turn to turn around
            
        return prev           # prev is holding onto the last node (the new head!)


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ([1, 2], [2, 1]),
        ([], []),
        ([1], [1]),
    ]
    
    for original, expected in test_cases:
        h = ListNode.from_list(original)
        rev = sol.reverseList(h)
        actual = rev.to_list() if rev else []
        assert actual == expected, f"Failed for {original}: expected {expected}, got {actual}"
        print(f"✓ Input: {original} -> Reversed: {actual}")
        
    print("\nAll test cases passed successfully!")
