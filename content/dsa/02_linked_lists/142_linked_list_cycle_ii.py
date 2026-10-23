"""
LeetCode 142: Linked List Cycle II
https://leetcode.com/problems/linked-list-cycle-ii/

Given the head of a linked list, return the node where the cycle begins.
If there is no cycle, return null.

Approaches:
1. Hash Set:
   - Traverse the list and store node object references in a set.
   - The first node already present in the set is the cycle entrance.
   - Time: O(n), Space: O(n).

2. Floyd's Tortoise and Hare (Two-Phase Pointer Alignment) [Optimal]:
   - Phase 1: slow moves 1x, fast moves 2x. If fast hits None, no cycle. Break when slow == fast.
   - Phase 2: Place one pointer at head, keep other at collision point. Move both 1x.
     They are mathematically guaranteed to meet at the cycle entrance (a = k*l + (l - b)).
   - Time: O(n), Space: O(1).
"""

from typing import Optional


class ListNode:
    def __init__(self, x: int):
        self.val = x
        self.next: Optional["ListNode"] = None


# ---------------------------------------------------------------------------
# Approach 1: Hash Set
# ---------------------------------------------------------------------------

class SolutionHashSet:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited = set()
        curr = head
        while curr:
            if curr in visited:
                return curr
            visited.add(curr)
            curr = curr.next
        return None


# ---------------------------------------------------------------------------
class SolutionGuardCheck:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = slow = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break

        if not fast or not fast.next:
            return None

        p1 = head
        p2 = slow
        while p1 != p2:
            p1 = p1.next
            p2 = p2.next

        return p1


class Solution:
    """Optimal Pythonic solution with while...else and pointer reuse."""
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = slow = head

        # Phase 1: Detect cycle and find meeting point
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return None

        # Phase 2: Find cycle entrance
        while head != slow:
            head = head.next
            slow = slow.next

        return head


# ---------------------------------------------------------------------------
# Automated Unit Tests
# ---------------------------------------------------------------------------

def run_tests():
    print("Testing LeetCode 142: Linked List Cycle II...")

    for name, sol in [("HashSet", SolutionHashSet()), ("GuardCheck", SolutionGuardCheck()), ("WhileElseOptimal", Solution())]:
        # Test 1: Empty list
        assert sol.detectCycle(None) is None, f"{name} failed on empty list"

        # Test 2: Single node, no cycle
        single = ListNode(1)
        assert sol.detectCycle(single) is None, f"{name} failed on single node"

        # Test 3: Single node with self cycle
        self_cycle = ListNode(1)
        self_cycle.next = self_cycle
        assert sol.detectCycle(self_cycle) is self_cycle, f"{name} failed on self cycle"

        # Test 4: 1 -> 2 -> None (no cycle)
        n1 = ListNode(1)
        n2 = ListNode(2)
        n1.next = n2
        assert sol.detectCycle(n1) is None, f"{name} failed on acyclic list"

        # Test 5: 3 -> 2 -> 0 -> -4 -> 2 (cycle entrance at node 2)
        a = ListNode(3)
        b = ListNode(2)
        c = ListNode(0)
        d = ListNode(-4)
        a.next = b
        b.next = c
        c.next = d
        d.next = b  # cycle back to node b
        res = sol.detectCycle(a)
        assert res is b, f"{name} expected node b (val=2), got {res}"
        assert res.val == 2

        print(f"  {name} passed all test cases!")

    print("All LeetCode 142 tests passed successfully!")


if __name__ == "__main__":
    run_tests()
