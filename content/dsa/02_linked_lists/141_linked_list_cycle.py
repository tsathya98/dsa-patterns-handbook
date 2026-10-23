"""
LeetCode 141: Linked List Cycle
https://leetcode.com/problems/linked-list-cycle/

Given head, the head of a linked list, determine if the linked list has a cycle in it.
There is a cycle in a linked list if there is some node in the list that can be reached
again by continuously following the next pointer.

Approaches:
1. Hash Set:
   - Traverse the list and store node object references in a set.
   - If a node is already in the set, a cycle exists.
   - Time: O(n), Space: O(n).

2. Fast and Slow Pointers (Floyd's Tortoise and Hare) [Optimal]:
   - slow advances 1 step, fast advances 2 steps.
   - If list terminates, fast reaches None (no cycle).
   - If cycle exists, fast laps slow from behind and they collide (slow == fast).
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
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()
        curr = head
        while curr:
            if curr in visited:
                return True
            visited.add(curr)
            curr = curr.next
        return False


# ---------------------------------------------------------------------------
# Approach 2: Floyd's Tortoise & Hare (User's Accepted Solution)
# ---------------------------------------------------------------------------

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True

        return False


# ---------------------------------------------------------------------------
# Automated Unit Tests
# ---------------------------------------------------------------------------

def run_tests():
    print("Testing LeetCode 141: Linked List Cycle...")

    for name, sol in [("HashSet", SolutionHashSet()), ("TortoiseHare", Solution())]:
        # Test 1: Empty list
        assert sol.hasCycle(None) is False, f"{name} failed on empty list"

        # Test 2: Single node, no cycle
        single = ListNode(1)
        assert sol.hasCycle(single) is False, f"{name} failed on single node without cycle"

        # Test 3: Single node with self cycle
        self_cycle = ListNode(1)
        self_cycle.next = self_cycle
        assert sol.hasCycle(self_cycle) is True, f"{name} failed on self cycle"

        # Test 4: 1 -> 2 -> None (no cycle)
        n1 = ListNode(1)
        n2 = ListNode(2)
        n1.next = n2
        assert sol.hasCycle(n1) is False, f"{name} failed on acyclic list"

        # Test 5: 3 -> 2 -> 0 -> -4 -> 2 (cycle at node with val 2)
        a = ListNode(3)
        b = ListNode(2)
        c = ListNode(0)
        d = ListNode(-4)
        a.next = b
        b.next = c
        c.next = d
        d.next = b  # cycle back to b
        assert sol.hasCycle(a) is True, f"{name} failed on cycle at node 2"

        print(f"  {name} passed all test cases!")

    print("All LeetCode 141 tests passed successfully!")


if __name__ == "__main__":
    run_tests()
