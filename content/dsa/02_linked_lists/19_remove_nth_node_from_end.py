"""
LeetCode 19: Remove Nth Node From End of List
https://leetcode.com/problems/remove-nth-node-from-end-of-list/

Given the head of a linked list, remove the n-th node from the end of the list
and return its head.

Approaches:
1. Two-Pass (Length Counting & Predecessor Traversal):
   - First pass: Walk the entire list to count total length L.
   - Target predecessor index from beginning is (L - n) - 1.
   - If L == n, the head itself is being removed; return head.next.
   - Second pass: Walk L - n - 1 steps to predecessor, then bypass victim.
   - Time: O(L) in two passes (~2L operations), Space: O(1).

2. One-Pass (Fixed-Gap Measuring Stick with Sentinel Dummy Node) [Optimal]:
   - Create a sentinel `dummy` before head.
   - Initialize `left = dummy` and `right = head`.
   - Advance `right` forward by n steps.
   - Advance both `left` and `right` together until `right` is None.
   - `left` lands on predecessor of victim. Bypass with `left.next = left.next.next`.
   - Return `dummy.next` (handles head deletion naturally with zero if-checks).
   - Time: O(L) in a single pass (L operations), Space: O(1).
"""

from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


# ---------------------------------------------------------------------------
# Approach 1: Two-Pass (User's Intuitive Approach)
# ---------------------------------------------------------------------------

class SolutionTwoPass:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        if not head:
            return None

        # Pass 1: Count total number of nodes
        count = 0
        cur = head
        while cur:
            count += 1
            cur = cur.next

        # If removing the head node (n == count)
        k = count - n
        if k == 0:
            return head.next

        # Pass 2: Walk to node before victim (k - 1 hops)
        cur = head
        for _ in range(k - 1):
            cur = cur.next

        # Bypass the victim node
        if cur and cur.next:
            cur.next = cur.next.next

        return head


# ---------------------------------------------------------------------------
# Approach 2: One-Pass with Fixed-Gap & Sentinel Dummy Node (Optimal)
# ---------------------------------------------------------------------------

class SolutionOnePass:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        left = dummy
        right = head

        # Step 1: Advance right by n steps to create fixed window
        for _ in range(n):
            right = right.next

        # Step 2: Slide both pointers until right walks off list into None
        while right:
            left = left.next
            right = right.next

        # Step 3: Unlink victim node (left is at predecessor)
        left.next = left.next.next

        return dummy.next


# Default solution
Solution = SolutionOnePass


# ---------------------------------------------------------------------------
# Helper Testing Utilities
# ---------------------------------------------------------------------------

def create_list(vals: List[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    res = []
    cur = head
    while cur:
        res.append(cur.val)
        cur = cur.next
    return res


# ---------------------------------------------------------------------------
# Automated Unit Tests
# ---------------------------------------------------------------------------

def run_tests():
    print("Testing LeetCode 19: Remove Nth Node From End of List...")

    for name, sol in [("TwoPass", SolutionTwoPass()), ("OnePass", SolutionOnePass())]:
        # Test 1: Example 1 - remove 2nd from end of [1, 2, 3, 4, 5] -> [1, 2, 3, 5]
        h1 = create_list([1, 2, 3, 4, 5])
        res1 = sol.removeNthFromEnd(h1, 2)
        assert to_list(res1) == [1, 2, 3, 5], f"{name} failed on Example 1"

        # Test 2: Example 2 - remove only node [1], n = 1 -> []
        h2 = create_list([1])
        res2 = sol.removeNthFromEnd(h2, 1)
        assert to_list(res2) == [], f"{name} failed on single node"

        # Test 3: Example 3 - remove tail of [1, 2], n = 1 -> [1]
        h3 = create_list([1, 2])
        res3 = sol.removeNthFromEnd(h3, 1)
        assert to_list(res3) == [1], f"{name} failed on [1, 2], n=1"

        # Test 4: Remove head of [1, 2], n = 2 -> [2]
        h4 = create_list([1, 2])
        res4 = sol.removeNthFromEnd(h4, 2)
        assert to_list(res4) == [2], f"{name} failed on head removal [1, 2], n=2"

        # Test 5: Remove head of [1, 2, 3], n = 3 -> [2, 3]
        h5 = create_list([1, 2, 3])
        res5 = sol.removeNthFromEnd(h5, 3)
        assert to_list(res5) == [2, 3], f"{name} failed on head removal [1, 2, 3], n=3"

        print(f"  {name} passed all test cases!")

    print("All LeetCode 19 unit tests passed successfully!")


if __name__ == "__main__":
    run_tests()
