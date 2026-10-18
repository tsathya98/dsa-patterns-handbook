"""
LeetCode 203: Remove Linked List Elements
Difficulty: Easy
URL: https://leetcode.com/problems/remove-linked-list-elements/

Patterns:
1. Approach 1 (Optimal - Sentinel Dummy Node): `cur = dummy = ListNode(0, head)` (O(N) time, O(1) space).
2. Approach 2 (Two Pointers Without Dummy): Trailing head-skipping loop + prev/cur traversal (O(N) time, O(1) space).
3. Approach 3 (Recursive): Divide and conquer call stack (O(N) time, O(N) call stack space).
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
    while head:
        res.append(head.val)
        head = head.next
    return res


# =====================================================================
# Approach 1: Sentinel Dummy Node (User's Accepted Submission - Optimal)
# Time Complexity:  O(N) single pass
# Space Complexity: O(1) auxiliary space (1 dummy node)
# =====================================================================
class SolutionDummy:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        cur = dummy = ListNode(0, head)
        while cur.next:
            if cur.next.val == val:
                cur.next = cur.next.next
            else:
                cur = cur.next
        return dummy.next


# =====================================================================
# Approach 2: Without Dummy Node (Manual Head Skipping)
# Time Complexity:  O(N)
# Space Complexity: O(1)
# =====================================================================
class SolutionNoDummy:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        # 1. Skip leading target nodes
        while head and head.val == val:
            head = head.next

        # 2. Delete targets from remaining body
        cur = head
        while cur and cur.next:
            if cur.next.val == val:
                cur.next = cur.next.next
            else:
                cur = cur.next
        return head


# =====================================================================
# Approach 3: Recursive (Functional)
# Time Complexity:  O(N)
# Space Complexity: O(N) recursion stack
# =====================================================================
class SolutionRecursive:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        if not head:
            return None
        head.next = self.removeElements(head.next, val)
        return head.next if head.val == val else head


# Default entrypoint for LeetCode
Solution = SolutionDummy


# =====================================================================
# Unit Tests
# =====================================================================
def run_tests():
    sol1 = SolutionDummy()
    sol2 = SolutionNoDummy()
    sol3 = SolutionRecursive()

    test_cases = [
        ([1, 2, 6, 3, 4, 5, 6], 6, [1, 2, 3, 4, 5]),
        ([], 1, []),
        ([7, 7, 7, 7], 7, []),
        ([1, 2, 2, 1], 2, [1, 1]),
    ]

    for vals, target, expected in test_cases:
        res1 = to_list(sol1.removeElements(build_linked_list(vals), target))
        res2 = to_list(sol2.removeElements(build_linked_list(vals), target))
        res3 = to_list(sol3.removeElements(build_linked_list(vals), target))
        assert res1 == expected, f"Approach 1 failed on {vals}, val={target}"
        assert res2 == expected, f"Approach 2 failed on {vals}, val={target}"
        assert res3 == expected, f"Approach 3 failed on {vals}, val={target}"
        print(f"✓ Input: {vals}, remove {target} -> Result: {expected}")

    print("\n✅ All unit tests passed successfully for LeetCode 203 across all 3 implementations!")


if __name__ == "__main__":
    run_tests()
