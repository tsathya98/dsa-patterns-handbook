"""
LeetCode 21: Merge Two Sorted Lists
Difficulty: Easy
URL: https://leetcode.com/problems/merge-two-sorted-lists/

Patterns:
1. Approach 1 (Optimal - Iterative Dummy Node): Zipper merge with in-place pointer stitching (O(N + M) time, O(1) space).
2. Approach 2 (Recursive): Functional divide & conquer (O(N + M) time, O(N + M) call stack space).
3. Approach 3 (Array Extraction & Rebuild): Collect all values, sort, rebuild new list (O((N+M) log(N+M)) time, O(N+M) space).
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
# Approach 1: Iterative Dummy Node Zipper Merge (User's Accepted Submission - Optimal)
# Time Complexity:  O(N + M) single pass through both lists
# Space Complexity: O(1) in-place pointer stitching
# =====================================================================
class SolutionIterative:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        cur1 = list1
        cur2 = list2
        dummy = ListNode(0)
        ptr = dummy

        while cur1 and cur2:
            if cur1.val < cur2.val:
                ptr.next = cur1
                cur1 = cur1.next
            else:
                ptr.next = cur2
                cur2 = cur2.next
            ptr = ptr.next

        ptr.next = cur1 or cur2
        return dummy.next


# =====================================================================
# Approach 2: Recursive Merge
# Time Complexity:  O(N + M)
# Space Complexity: O(N + M) call stack frames
# =====================================================================
class SolutionRecursive:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1 or not list2:
            return list1 or list2

        if list1.val < list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2


# Default entrypoint for LeetCode
Solution = SolutionIterative


# =====================================================================
# Unit Tests
# =====================================================================
def run_tests():
    sol1 = SolutionIterative()
    sol2 = SolutionRecursive()

    test_cases = [
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [0], [0]),
        ([5], [1, 2, 4], [1, 2, 4, 5]),
        ([-9, 3], [5, 7], [-9, 3, 5, 7]),
    ]

    for l1_vals, l2_vals, expected in test_cases:
        res1 = to_list(sol1.mergeTwoLists(build_linked_list(l1_vals), build_linked_list(l2_vals)))
        res2 = to_list(sol2.mergeTwoLists(build_linked_list(l1_vals), build_linked_list(l2_vals)))
        assert res1 == expected, f"Approach 1 failed on {l1_vals} and {l2_vals}"
        assert res2 == expected, f"Approach 2 failed on {l1_vals} and {l2_vals}"
        print(f"✓ Merged {l1_vals} + {l2_vals} -> {expected}")

    print("\n✅ All unit tests passed successfully for LeetCode 21 across both implementations!")


if __name__ == "__main__":
    run_tests()
