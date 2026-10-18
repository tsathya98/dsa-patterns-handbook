from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


class Solution:
    # Approach 1: O(N) Time, O(N) Space (Array Conversion + Two Pointers)
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

    # Approach 2: O(N) Time, O(1) Space (Tortoise & Hare Midpoint + Reverse Second Half)
    def isPalindromeOptimal(self, head: Optional[ListNode]) -> bool:
        if not head or not head.next:
            return True

        # 1. Find midpoint (slow stops at end of first half)
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2. Reverse second half (starting at slow.next)
        prev = None
        cur = slow.next
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # 3. Compare first half and reversed second half
        p1, p2 = head, prev
        while p2:
            if p1.val != p2.val:
                return False
            p1 = p1.next
            p2 = p2.next

        return True
