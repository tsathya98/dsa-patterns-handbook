"""
LeetCode 1721: Swapping Nodes in a Linked List
Difficulty: Medium
URL: https://leetcode.com/problems/swapping-nodes-in-a-linked-list/

Patterns:
1. Approach 1: Store Node References in Array (O(n) time, O(n) space).
2. Approach 2: The Measuring Stick / Offset Two Pointers (O(n) time, O(1) space).
"""

from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        vals = []
        cur: Optional[ListNode] = self
        while cur:
            vals.append(str(cur.val))
            cur = cur.next
        return " -> ".join(vals)


def build_linked_list(values: List[int]) -> Optional[ListNode]:
    if not values:
        return None
    head = ListNode(values[0])
    cur = head
    for v in values[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


def to_list(head: Optional[ListNode]) -> List[int]:
    res = []
    cur = head
    while cur:
        res.append(cur.val)
        cur = cur.next
    return res


# =====================================================================
# Approach 1: Store Node References in an Array
# Time Complexity:  O(n)
# Space Complexity: O(n)
# =====================================================================
class SolutionArrayNodes:
    def swapNodes(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """Stores node references and swaps values in-place on existing nodes."""
        nodes = []
        cur = head
        while cur:
            nodes.append(cur)
            cur = cur.next

        # Swap values of k-th node from start and k-th node from end
        nodes[k - 1].val, nodes[-k].val = nodes[-k].val, nodes[k - 1].val
        return head


# =====================================================================
# Approach 2: The Measuring Stick (Offset Two Pointers) - FAANG Standard
# Time Complexity:  O(n) single pass
# Space Complexity: O(1) auxiliary space
# =====================================================================
class SolutionMeasuringStick:
    def swapNodes(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """
        Two Pointers Measuring Stick:
        1. Walk `first` to the k-th node from beginning using (k - 1) steps.
        2. Set `fast = first` and `second = head`.
        3. Advance both until `fast.next` is None.
           Now `second` is the k-th node from the end!
        4. Swap values in-place.
        """
        first = head
        second = head

        # Step 1: Reach k-th node from start (k - 1 steps)
        for _ in range(k - 1):
            first = first.next

        # Step 2: Slide measuring stick to find k-th node from end
        fast = first
        while fast.next:
            fast = fast.next
            second = second.next

        # Step 3: Swap values in-place
        first.val, second.val = second.val, first.val

        return head


# =====================================================================
# Unit Tests
# =====================================================================
def run_tests():
    sol_array = SolutionArrayNodes()
    sol_stick = SolutionMeasuringStick()

    test_cases = [
        ([1, 2, 3, 4, 5], 2, [1, 4, 3, 2, 5]),
        ([7, 9, 6, 6, 7, 8, 3, 0, 9, 5], 5, [7, 9, 6, 6, 8, 7, 3, 0, 9, 5]),
        ([1], 1, [1]),
        ([1, 2], 1, [2, 1]),
        ([1, 2], 2, [2, 1]),
        ([100, 90], 2, [90, 100]),
        ([1, 2, 3], 2, [1, 2, 3]),  # k is exact center
    ]

    for vals, k, expected in test_cases:
        # Test Approach 1
        ll1 = build_linked_list(vals)
        res1 = to_list(sol_array.swapNodes(ll1, k))
        assert res1 == expected, f"Approach 1 failed on {vals}, k={k}: got {res1}, expected {expected}"

        # Test Approach 2
        ll2 = build_linked_list(vals)
        res2 = to_list(sol_stick.swapNodes(ll2, k))
        assert res2 == expected, f"Approach 2 failed on {vals}, k={k}: got {res2}, expected {expected}"

    print("✅ All unit tests passed successfully for LeetCode 1721 Swapping Nodes in a Linked List!")


if __name__ == "__main__":
    run_tests()
