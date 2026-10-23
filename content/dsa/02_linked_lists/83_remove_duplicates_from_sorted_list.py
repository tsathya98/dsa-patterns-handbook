"""
LeetCode 83: Remove Duplicates from Sorted List
Pattern: Linked List In-Place Pointer Skipping
Difficulty: Easy
Link: https://leetcode.com/problems/remove-duplicates-from-sorted-list/
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
    def deleteDuplicates(self, head: ListNode | None) -> ListNode | None:
        """
        Time Complexity: O(n) - single pass through list
        Space Complexity: O(1) - in-place pointer adjustments
        """
        cur = head
        while cur and cur.next:
            if cur.val == cur.next.val:
                cur.next = cur.next.next  # Skip duplicate! Cur stays put to re-check.
            else:
                cur = cur.next            # No duplicate, safe to advance cur.
                
        return head  # Return head directly (head was a REAL starting node, not a dummy!)


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ([1, 1, 2], [1, 2]),
        ([1, 1, 2, 3, 3], [1, 2, 3]),
        ([1, 1, 1], [1]),
        ([], []),
        ([1], [1]),
        ([1, 2, 3], [1, 2, 3]),
    ]
    
    for original, expected in test_cases:
        h = ListNode.from_list(original)
        res = sol.deleteDuplicates(h)
        actual = res.to_list() if res else []
        assert actual == expected, f"Failed for {original}: expected {expected}, got {actual}"
        print(f"✓ Input: {original} -> Output: {actual}")
        
    print("\nAll test cases passed successfully!")
