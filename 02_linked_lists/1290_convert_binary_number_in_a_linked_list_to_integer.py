from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


class Solution:
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        lst = []
        cur = head
        while cur:
            lst.append(cur.val)
            cur = cur.next
        tot = 0
        for i in range(len(lst) - 1, -1, -1):
            tot += lst[len(lst) - i - 1] * 2**i
        return tot
