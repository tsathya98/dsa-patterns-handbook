"""
LeetCode 2095: Delete the Middle Node of a Linked List
Pattern: Fast & Slow Pointers (Midpoint Predecessor)
Difficulty: Medium
Link: https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def to_list(self):
        result = []
        curr = self
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result

    @staticmethod
    def from_list(lst):
        if not lst:
            return None
        dummy = ListNode()
        curr = dummy
        for val in lst:
            curr.next = ListNode(val)
            curr = curr.next
        return dummy.next


class SolutionTrackPrev:
    """Approach 1: Previous pointer tracker"""
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return None

        prev = None
        slow = head
        fast = head

        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next

        prev.next = slow.next
        return head


class SolutionDummyOffset:
    """Approach 2: Sentinel dummy node offset"""
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        slow = dummy
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        slow.next = slow.next.next
        return dummy.next


def run_tests():
    sol1 = SolutionTrackPrev()
    sol2 = SolutionDummyOffset()

    test_cases = [
        ([1, 3, 4, 7, 1, 2, 6], [1, 3, 4, 1, 2, 6]),  # n = 7 (odd)
        ([1, 2, 3, 4], [1, 2, 4]),                    # n = 4 (even)
        ([2, 1], [2]),                                # n = 2
        ([1], []),                                    # n = 1 (single node)
    ]

    for original, expected in test_cases:
        # Test Approach 1
        h1 = ListNode.from_list(original)
        res1 = sol1.deleteMiddle(h1)
        actual1 = res1.to_list() if res1 else []
        assert actual1 == expected, f"Approach 1 failed for {original}: expected {expected}, got {actual1}"

        # Test Approach 2
        h2 = ListNode.from_list(original)
        res2 = sol2.deleteMiddle(h2)
        actual2 = res2.to_list() if res2 else []
        assert actual2 == expected, f"Approach 2 failed for {original}: expected {expected}, got {actual2}"

        print(f"✓ Input: {original} -> Output: {actual1}")

    print("\nAll unit tests passed across both approaches!")


if __name__ == "__main__":
    run_tests()
