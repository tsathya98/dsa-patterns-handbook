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


class SolutionTwoWireReconnect:
    """
    Approach 1: 4-Step Reverse + 2-Wire Reconnect.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """

    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if not head or left == right:
            return head

        dummy = ListNode(0, head)

        # 1. Park before_window right before the cut
        before_window = dummy
        for _ in range(left - 1):
            before_window = before_window.next

        # 2. window_tail will end up as the tail of the flipped window
        window_tail = before_window.next

        # 3. Standard 4-step pointer reversal for (right - left + 1) nodes
        prev = None
        cur = window_tail
        for _ in range(right - left + 1):
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # 4. Reconnect both wires
        window_tail.next = cur        # Tail of flipped chunk connects to downstream
        before_window.next = prev     # Upstream connects to new head of flipped chunk

        return dummy.next


class SolutionSplicing:
    """
    Approach 2: One-Pass Head Splicing.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """

    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        if not head or left == right:
            return head

        dummy = ListNode(0, head)
        before_window = dummy

        for _ in range(left - 1):
            before_window = before_window.next

        cur = before_window.next

        # Repeat right - left times
        for _ in range(right - left):
            nxt = cur.next
            cur.next = nxt.next
            nxt.next = before_window.next
            before_window.next = nxt

        return dummy.next


# --- Test Suite ---
def test_reverse_between():
    sol1 = SolutionTwoWireReconnect()
    sol2 = SolutionSplicing()

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
        # Test Approach 1
        h1 = build_linked_list(arr)
        res1 = to_list(sol1.reverseBetween(h1, l, r))
        assert res1 == expected, f"Approach 1 failed for {arr}, left={l}, right={r}. Got {res1}"

        # Test Approach 2
        h2 = build_linked_list(arr)
        res2 = to_list(sol2.reverseBetween(h2, l, r))
        assert res2 == expected, f"Approach 2 failed for {arr}, left={l}, right={r}. Got {res2}"

    print("All LeetCode 92 test cases passed for both approaches!")


if __name__ == "__main__":
    test_reverse_between()
