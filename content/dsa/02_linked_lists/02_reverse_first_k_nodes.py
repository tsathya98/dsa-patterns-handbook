"""
Reverse First K Nodes of a Linked List
Given the head of a linked list and an integer k (k > 0, k <= n),
reverse the first k nodes and connect them with the remainder of the list.

Example:
Input:  1 -> 2 -> 3 -> 4 -> 5 -> 6 -> Null, k = 4
Output: 4 -> 3 -> 2 -> 1 -> 5 -> 6 -> Null

Time Complexity: O(k) single pass over first k nodes
Space Complexity: O(1) in-place pointer mutation
"""

from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


class Solution:
    def reverseFirstK(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """
        Reverse first k nodes in-place using O(1) extra space.
        """
        if not head or k <= 1:
            return head

        prev = None
        cur = head

        # Step 1: Reverse first k nodes
        # After k iterations:
        # - prev is at the k-th node (the new head!)
        # - cur is at the (k+1)-th node (start of remaining list)
        # - head is still at node 1 (now the tail of reversed part)
        count = k
        while count > 0 and cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
            count -= 1

        # Step 2: The Bridge
        # Connect original head (node 1) to the remaining list (node 5)
        head.next = cur

        # Step 3: Return prev (node 4 is the new head of the entire list)
        return prev


def to_list(head: Optional[ListNode]) -> list[int]:
    res = []
    curr = head
    while curr:
        res.append(curr.val)
        curr = curr.next
    return res


def from_list(vals: list[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


if __name__ == "__main__":
    sol = Solution()

    # Test 1: Standard k=4
    head1 = from_list([1, 2, 3, 4, 5, 6])
    res1 = sol.reverseFirstK(head1, 4)
    assert to_list(res1) == [4, 3, 2, 1, 5, 6]

    # Test 2: k = len(list) (full reversal)
    head2 = from_list([1, 2, 3])
    res2 = sol.reverseFirstK(head2, 3)
    assert to_list(res2) == [3, 2, 1]

    # Test 3: k = 1 (no change)
    head3 = from_list([1, 2, 3])
    res3 = sol.reverseFirstK(head3, 1)
    assert to_list(res3) == [1, 2, 3]

    print("All tests passed!")
