"""
LeetCode 876: Middle of the Linked List
Difficulty: Easy
URL: https://leetcode.com/problems/middle-of-the-linked-list/

Patterns:
1. Approach 1 (Optimal - Tortoise & Hare): Fast & Slow Pointers (O(N) time, O(1) space).
2. Approach 2 (Two-Pass Counting): Count total length N, then advance N // 2 steps (O(N) time, O(1) space).
3. Approach 3 (Array Indexing): Store all nodes in an array, return arr[len // 2] (O(N) time, O(N) space).
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


# =====================================================================
# Approach 1: Fast & Slow Pointers (User's Accepted Submission - Optimal)
# Time Complexity:  O(N) single pass (fast moves at 2x speed)
# Space Complexity: O(1) auxiliary space
# =====================================================================
class SolutionFastSlow:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast = slow = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow


# =====================================================================
# Approach 2: Two-Pass Counting (Baseline)
# Time Complexity:  O(N) (first pass counts N, second pass walks N//2)
# Space Complexity: O(1)
# =====================================================================
class SolutionCounting:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        count = 0
        cur = head
        while cur:
            count += 1
            cur = cur.next

        cur = head
        for _ in range(count // 2):
            cur = cur.next
        return cur


# =====================================================================
# Approach 3: Array Indexing (Space Trade-off)
# Time Complexity:  O(N)
# Space Complexity: O(N) array storage
# =====================================================================
class SolutionArray:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        arr = []
        cur = head
        while cur:
            arr.append(cur)
            cur = cur.next
        return arr[len(arr) // 2] if arr else None


# Default entrypoint for LeetCode
Solution = SolutionFastSlow


# =====================================================================
# Unit Tests
# =====================================================================
def run_tests():
    sol1 = SolutionFastSlow()
    sol2 = SolutionCounting()
    sol3 = SolutionArray()

    test_cases = [
        ([1, 2, 3, 4, 5], 3),
        ([1, 2, 3, 4, 5, 6], 4),
        ([1], 1),
        ([1, 2], 2),
    ]

    for vals, expected_val in test_cases:
        res1 = sol1.middleNode(build_linked_list(vals))
        res2 = sol2.middleNode(build_linked_list(vals))
        res3 = sol3.middleNode(build_linked_list(vals))
        assert res1 and res1.val == expected_val, f"Approach 1 failed on {vals}"
        assert res2 and res2.val == expected_val, f"Approach 2 failed on {vals}"
        assert res3 and res3.val == expected_val, f"Approach 3 failed on {vals}"
        print(f"✓ Input: {vals} -> Middle node value: {expected_val}")

    print("\n✅ All unit tests passed successfully for LeetCode 876 across all 3 implementations!")


if __name__ == "__main__":
    run_tests()
