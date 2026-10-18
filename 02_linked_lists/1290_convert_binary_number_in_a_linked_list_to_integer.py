"""
LeetCode 1290: Convert Binary Number in a Linked List to Integer

Approach 1: Array conversion + reverse indexing (User's Accepted Solution)
- Time: O(N)
- Space: O(N)
- Walk list, collect bit values in array, then accumulate powers of 2 from right to left.

Approach 2: Stream accumulation / Horner's rule (Optimal Follow-up)
- Time: O(N)
- Space: O(1)
- Multiply running total by 2 and add current bit on each step without extra storage.
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


class Solution:
    # Approach 1: Array Conversion + Reverse Powers (O(N) Time, O(N) Space)
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        lst = []
        cur = head
        while cur:
            lst.append(cur.val)
            cur = cur.next
        tot = 0
        for i in range(len(lst) - 1, -1, -1):
            tot += lst[len(lst) - i - 1] * (2 ** i)
        return tot

    # Approach 2: Stream Accumulation / Horner's Rule (O(N) Time, O(1) Space)
    def getDecimalValueOptimal(self, head: Optional[ListNode]) -> int:
        total = 0
        cur = head
        while cur:
            total = total * 2 + cur.val
            cur = cur.next
        return total
