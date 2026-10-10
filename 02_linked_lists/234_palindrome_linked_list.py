"""
LeetCode 234: Palindrome Linked List
Difficulty: Easy / Medium follow-up
URL: https://leetcode.com/problems/palindrome-linked-list/

This file contains two solutions:
1. Approach 1 (Baseline): Convert to Array + Two Pointers Squeeze (O(n) time, O(n) space).
2. Approach 2 (FAANG-Worthy): In-Place Triple Crown (O(n) time, O(1) space).
   - Step 1: Find middle via Tortoise & Hare (Fast & Slow).
   - Step 2: Reverse the second half using Conga Line 4-beat dance.
   - Step 3: Compare first half and reversed second half.
   - Step 4: (Optional Bonus) Restore the list.
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
# Approach 1: Convert to Array + Two Pointers Squeeze
# Time Complexity:  O(n)
# Space Complexity: O(n) auxiliary memory for `lst`
# =====================================================================
class SolutionArrayTwoPointers:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """
        Dumps node values into an array, then applies two pointers squeeze.
        Why squeeze is better than `lst == lst[::-1]`:
        1. No duplicate array allocation (O(1) extra space on top of `lst`).
        2. Instant O(1) early return upon the first mismatch.
        """
        lst = []
        cur = head
        while cur:
            lst.append(cur.val)
            cur = cur.next

        l = 0
        r = len(lst) - 1

        while l < r:
            if lst[l] != lst[r]:
                return False  # Early exit on mismatch!
            l += 1
            r -= 1

        return True


# =====================================================================
# Approach 2: The FAANG In-Place Triple Crown
# Time Complexity:  O(n)
# Space Complexity: O(1) in-place auxiliary space
# =====================================================================
# =====================================================================
# Approach 2: The FAANG In-Place Triple Crown (Embedded / Inlined)
# Time Complexity:  O(n)
# Space Complexity: O(1) in-place auxiliary space
# =====================================================================
class SolutionInPlaceEmbedded:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """
        In-place palindrome check with the 4-beat reversal dance
        embedded directly inline without helper functions.
        """
        if not head or not head.next:
            return True

        # 1. Find midpoint (Tortoise & Hare)
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2. Reverse 2nd half in-place (embedded 4-beat Conga Line dance)
        prev = None
        cur = slow.next
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # 3. Compare 1st half and reversed 2nd half
        first = head
        second = prev  # prev is head of the reversed 2nd half
        while second:
            if first.val != second.val:
                return False
            first = first.next
            second = second.next

        return True


# =====================================================================
# Approach 2 (With Helper & Restoration): Modular Clean Architecture
# =====================================================================
class SolutionInPlace:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """
        Checks palindrome in-place without creating an auxiliary array.
        3-Step Process:
        1. Fast & Slow pointers to locate the end of the first half.
        2. Reverse the second half using the 4-beat dance (prev, cur, nxt).
        3. Compare first half and reversed second half.
        4. (Best Practice) Restore the list back to its original order.
        """
        if not head or not head.next:
            return True

        # -------------------------------------------------------------
        # Step 1: Find end of first half using Fast & Slow pointers
        # When fast reaches the end, slow is at the middle.
        # For [1, 2, 2, 1], slow ends at first 2.
        # For [1, 2, 3, 2, 1], slow ends at 3.
        # -------------------------------------------------------------
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # -------------------------------------------------------------
        # Step 2: Reverse the second half starting at slow.next
        # [1, 2] and [2, 1] -> second half [2, 1] reversed becomes [1, 2]
        # -------------------------------------------------------------
        second_half_head = self._reverse_list(slow.next)

        # -------------------------------------------------------------
        # Step 3: Compare the two halves
        # -------------------------------------------------------------
        first_half = head
        second_half = second_half_head
        is_palindrome = True

        while is_palindrome and second_half:
            if first_half.val != second_half.val:
                is_palindrome = False
            first_half = first_half.next
            second_half = second_half.next

        # -------------------------------------------------------------
        # Step 4: Restore list (Optional bonus in FAANG interviews!)
        # Re-reversing the second half leaves the input list intact.
        # -------------------------------------------------------------
        slow.next = self._reverse_list(second_half_head)

        return is_palindrome

    def _reverse_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Classic Conga Line 4-beat in-place reversal (LC 206)."""
        prev = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        return prev


# =====================================================================
# Tests & Verification
# =====================================================================
def run_tests():
    sol1 = SolutionArrayTwoPointers()
    sol2 = SolutionInPlace()
    sol_embedded = SolutionInPlaceEmbedded()

    test_cases = [
        ([1, 2, 2, 1], True),           # Even length palindrome
        ([1, 2, 3, 2, 1], True),        # Odd length palindrome
        ([1, 2], False),                # Even length non-palindrome
        ([1], True),                    # Single node
        ([1, 0, 0], False),             # Mismatch at end
        ([9, 2, 3, 4, 1], False),       # Immediate first-pair mismatch
        ([1, 1], True),                 # Two equal nodes
        ([1, 2, 3, 4, 2, 1], False),    # Symmetry broken in middle
    ]

    for values, expected in test_cases:
        # Test Approach 1
        ll1 = build_linked_list(values)
        res1 = sol1.isPalindrome(ll1)
        assert res1 == expected, f"Approach 1 failed on {values}: got {res1}, expected {expected}"

        # Test Approach 2 Embedded
        ll_emb = build_linked_list(values)
        res_emb = sol_embedded.isPalindrome(ll_emb)
        assert res_emb == expected, f"Approach 2 Embedded failed on {values}: got {res_emb}, expected {expected}"

        # Test Approach 2 (and check if list is preserved after restoration)
        ll2 = build_linked_list(values)
        res2 = sol2.isPalindrome(ll2)
        assert res2 == expected, f"Approach 2 failed on {values}: got {res2}, expected {expected}"
        restored = to_list(ll2)
        assert restored == values, f"List was not restored properly! Expected {values}, got {restored}"

    print("✅ All unit tests passed successfully for all 3 implementations!")


if __name__ == "__main__":
    run_tests()
