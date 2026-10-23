"""
LeetCode 234: Palindrome Linked List
Difficulty: Easy (with Medium O(1) Space Follow-Up)
URL: https://leetcode.com/problems/palindrome-linked-list/

Patterns:
1. Approach 1 (Array Conversion): Collect node values into a list + Two-pointer squeeze (O(N) time, O(N) space).
2. Approach 2 (User's Accepted Optimal Solution): Fast/Slow Midpoint + In-Place Second Half Reversal (O(N) time, O(1) space).
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
# Approach 1: Array Conversion + Two-Pointer Squeeze (Intuitive Baseline)
# Time Complexity:  O(N)
# Space Complexity: O(N) array allocation
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
# Approach 2: Fast/Slow Midpoint + In-Place Reversal (User's Accepted Optimal)
# Time Complexity:  O(N) single pass through the list
# Space Complexity: O(1) strictly in-place auxiliary space
# =====================================================================
class SolutionOptimal:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if not head or not head.next:
            return True

        # 1. Find midpoint (slow stops at end of first half)
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2. Reverse second half in-place
        prev = None
        cur = slow.next
        while cur:
            nn = cur.next
            cur.next = prev
            prev = cur
            cur = nn

        # 3. Compare first half and reversed second half inward
        first = head
        second = prev
        while first and second:
            if first.val != second.val:
                return False
            first = first.next
            second = second.next

        return True


# Default entrypoint for LeetCode
Solution = SolutionOptimal


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
        assert res1 == expected, f"Approach 1 failed on {vals}"
        assert res2 == expected, f"Approach 2 failed on {vals}"
        print(f"✓ Input: {vals} -> isPalindrome: {expected}")

    print("\n✅ All unit tests passed successfully for LeetCode 234 across both implementations!")


if __name__ == "__main__":
    run_tests()
