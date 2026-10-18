"""
LeetCode 234: Palindrome Linked List

Approach 1: Array conversion + Two-pointer squeeze (User's Accepted Solution)
- Time: O(N)
- Space: O(N)
- Collect all node values in a Python list, then squeeze l and r pointers inward.

Approach 2: Fast/slow midpoint + In-place reversal (Optimal Follow-up)
- Time: O(N)
- Space: O(1)
- Find midpoint using fast/slow pointers, reverse the second half in-place, and compare inward.
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


class Solution:
    # Approach 1: Array Conversion + Two-Pointer Squeeze (O(N) Time, O(N) Space)
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        lst = []
        cur = head
        while cur:
            lst.append(cur.val)
            cur = cur.next

        l, r = 0, len(lst) - 1
        while l < r:
            if lst[l] != lst[r]:
                return False
            l += 1
            r -= 1
        return True

    # Approach 2: Fast/Slow Midpoint + In-Place Reversal (O(N) Time, O(1) Space)
    def isPalindromeOptimal(self, head: Optional[ListNode]) -> bool:
        if not head or not head.next:
            return True

        # 1. Stop slow at the end of the first half
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2. Reverse second half in-place starting at slow.next
        prev = None
        cur = slow.next
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # 3. Compare both halves inward
        first, second = head, prev
        while second:
            if first.val != second.val:
                return False
            first = first.next
            second = second.next

        return True
