"""
LeetCode 234: Palindrome Linked List
Difficulty: Easy (with Medium O(1) Space Follow-Up)
URL: https://leetcode.com/problems/palindrome-linked-list/

Patterns:
1. Approach 1 (Accepted Submission): Array Conversion + Two-Pointer Squeeze (O(N) time, O(N) space).
2. Approach 2 (Optimal Interview Standard): Fast/Slow Midpoint + In-Place Reversal (O(N) time, O(1) space).
3. Approach 3 (Optimal with Restoration): O(1) Space + Restore Original List Structure (O(N) time, O(1) space).
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
# Approach 1: Array Conversion + Two-Pointer Squeeze (User's Accepted Submission)
# Time Complexity:  O(N) single pass to copy + O(N/2) pointer comparison
# Space Complexity: O(N) array storage
# =====================================================================
class SolutionArray:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        lst = []
        cur = head
        while cur:
            lst.append(cur.val)
            cur = cur.next

        l, r = 0, len(lst) - 1
        while l < r:
            if lst[l] != lst[r]:
                return False
            l += 1
            r -= 1
        return True


# =====================================================================
# Approach 2: Fast/Slow Midpoint + In-Place Reversal (Optimal O(1) Space)
# Time Complexity:  O(N) total (O(N/2) find mid + O(N/2) reverse + O(N/2) compare)
# Space Complexity: O(1) auxiliary space
# =====================================================================
class SolutionOptimal:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if not head or not head.next:
            return True

        # 1. Stop slow at the end of the first half
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2. Reverse second half in-place starting at slow.next
        prev = None
        cur = slow.next
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # 3. Compare both halves inward
        first, second = head, prev
        while second:
            if first.val != second.val:
                return False
            first = first.next
            second = second.next

        return True


# Default entrypoint for LeetCode
Solution = SolutionArray


# =====================================================================
# Unit Tests
# =====================================================================
def run_tests():
    sol1 = SolutionArray()
    sol2 = SolutionOptimal()

    test_cases = [
        ([1, 2, 2, 1], True),
        ([1, 2], False),
        ([1], True),
        ([1, 2, 3, 2, 1], True),
        ([1, 2, 3, 4, 1], False),
        ([], True),
    ]

    for vals, expected in test_cases:
        res1 = sol1.isPalindrome(build_linked_list(vals))
        res2 = sol2.isPalindrome(build_linked_list(vals))
        assert res1 == expected, f"Approach 1 failed on {vals}: got {res1}, expected {expected}"
        assert res2 == expected, f"Approach 2 failed on {vals}: got {res2}, expected {expected}"
        print(f"✓ Input: {vals} -> isPalindrome: {expected}")

    print("\n✅ All unit tests passed successfully for LeetCode 234 across both implementations!")


if __name__ == "__main__":
    run_tests()
