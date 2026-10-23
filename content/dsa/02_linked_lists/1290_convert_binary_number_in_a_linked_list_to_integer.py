"""
LeetCode 1290: Convert Binary Number in a Linked List to Integer
Difficulty: Easy
URL: https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/

Patterns:
1. Approach 1 (Accepted Submission): Array Collection + Reverse Powers of 2 (O(N) time, O(N) space).
2. Approach 2 (Optimal Arithmetic): Horner's Rule / Left-to-Right Base-2 Accumulation (O(N) time, O(1) space).
3. Approach 3 (Bitwise Operations): Left Shift `<< 1` & Bitwise OR `|` (O(N) time, O(1) space).
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
# Approach 1: Array Collection + Reverse Powers (User's Accepted Submission)
# Time Complexity:  O(N) single pass to collect + O(N) to compute
# Space Complexity: O(N) array storage
# =====================================================================
class SolutionArray:
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        lst = []
        cur = head
        while cur:
            lst.append(cur.val)
            cur = cur.next
        tot = 0
        for i in range(len(lst) - 1, -1, -1):
            tot += lst[len(lst) - i - 1] * (2 ** i)
        return tot


# =====================================================================
# Approach 2: Horner's Rule / Arithmetic Base-2 Accumulation (Optimal)
# Time Complexity:  O(N) single pass
# Space Complexity: O(1) in-place
# =====================================================================
class SolutionHorner:
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        ans = 0
        while head:
            ans = ans * 2 + head.val
            head = head.next
        return ans


# =====================================================================
# Approach 3: Bitwise Shift & OR (Low-Level Systems Grade)
# Time Complexity:  O(N) single pass
# Space Complexity: O(1) in-place
# =====================================================================
class SolutionBitwise:
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        ans = 0
        while head:
            ans = (ans << 1) | head.val
            head = head.next
        return ans


# Default entrypoint for LeetCode
Solution = SolutionArray


# =====================================================================
# Unit Tests
# =====================================================================
def run_tests():
    sol1 = SolutionArray()
    sol2 = SolutionHorner()
    sol3 = SolutionBitwise()

    test_cases = [
        ([1, 0, 1], 5),
        ([0], 0),
        ([1], 1),
        ([1, 1, 1, 1], 15),
        ([1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], 18880),
        ([0, 0], 0),
    ]

    for bits, expected in test_cases:
        res1 = sol1.getDecimalValue(build_linked_list(bits))
        res2 = sol2.getDecimalValue(build_linked_list(bits))
        res3 = sol3.getDecimalValue(build_linked_list(bits))
        assert res1 == expected, f"Approach 1 failed on {bits}: got {res1}, expected {expected}"
        assert res2 == expected, f"Approach 2 failed on {bits}: got {res2}, expected {expected}"
        assert res3 == expected, f"Approach 3 failed on {bits}: got {res3}, expected {expected}"
        print(f"✓ Input: {bits} -> Decimal: {expected}")

    print("\n✅ All unit tests passed successfully for LeetCode 1290 across all 3 implementations!")


if __name__ == "__main__":
    run_tests()
