"""
LeetCode 92: Reverse Linked List II

Given the head of a singly linked list and two integers left and right where left <= right,
reverse the nodes of the list from position left to position right, and return the reversed list.
"""

from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


def build_linked_list(arr: List[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cur = dummy
    for x in arr:
        cur.next = ListNode(x)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    res = []
    cur = head
    while cur:
        res.append(cur.val)
        cur = cur.next
    return res


class SolutionLeftPrev:
    """
    NeetCode 3-Phase Pointer Reversal using left_prev.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """

    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if not head or left == right:
            return head

        dummy = ListNode(0, head)

        # Phase 1: Reach node at position left
        left_prev = dummy
        cur = head
        for _ in range(left - 1):
            left_prev = cur
            cur = cur.next

        # Phase 2: Reverse from left to right (right - left + 1 nodes)
        prev = None
        for _ in range(right - left + 1):
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # Phase 3: Reconnect both loose ends
        left_prev.next.next = cur   # Tail of flipped chunk connects to remainder
        left_prev.next = prev        # Upstream connects to new head of flipped chunk

        return dummy.next


# --- Test Suite ---
def test_reverse_between():
    sol = SolutionLeftPrev()

    test_cases = [
        # (input_list, left, right, expected)
        ([1, 2, 3, 4, 5], 2, 4, [1, 4, 3, 2, 5]),
        ([5], 1, 1, [5]),
        ([1, 2, 3, 4, 5], 1, 5, [5, 4, 3, 2, 1]),  # Full reversal (left == 1)
        ([1, 2, 3, 4, 5], 1, 2, [2, 1, 3, 4, 5]),  # Reversal from head
        ([1, 2, 3, 4, 5], 4, 5, [1, 2, 3, 5, 4]),  # Reversal at tail
        ([1, 2, 3], 2, 2, [1, 2, 3]),              # Single node window
    ]

    for arr, l, r, expected in test_cases:
        h = build_linked_list(arr)
        res = to_list(sol.reverseBetween(h, l, r))
        assert res == expected, f"Solution failed for {arr}, left={l}, right={r}. Got {res}"

    print("All LeetCode 92 test cases passed!")


if __name__ == "__main__":
    test_reverse_between()
