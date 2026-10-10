"""
LeetCode 1290: Convert Binary Number in a Linked List to Integer
Difficulty: Easy
URL: https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/

Patterns:
1. Approach 1 (Baseline): Two-Pass String Accumulation with Exponentiation (O(n) time, O(n) space).
2. Approach 2 (Optimal Arithmetic): Horner's Rule / Base-2 Shift (O(n) time, O(1) space).
3. Approach 3 (Bitwise / Systems Grade): Bit Shift & Bitwise OR (O(n) time, O(1) space).
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
# Approach 1: Two-Pass String Accumulation (Baseline)
# Time Complexity:  O(n^2) string copying in Python + O(n log k) powers
# Space Complexity: O(n)
# =====================================================================
class SolutionString:
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        num = ""
        while head:
            num += str(head.val)
            head = head.next
        binary = 0
        for i in range(len(num)):
            binary += int(num[i]) * (2 ** (len(num) - 1 - i))
        return binary


# =====================================================================
# Approach 2: Horner's Rule (Arithmetic Base-2 Accumulation)
# Time Complexity:  O(n) single pass
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
# Approach 3: Bitwise Operations (Nvidia / Low-Level Systems Grade)
# Time Complexity:  O(n) single pass
# Space Complexity: O(1) in-place
# =====================================================================
class SolutionBitwise:
    def getDecimalValue(self, head: Optional[ListNode]) -> int:
        ans = 0
        while head:
            ans = (ans << 1) | head.val
            head = head.next
        return ans


# =====================================================================
# Unit Tests
# =====================================================================
def run_tests():
    sol1 = SolutionString()
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

    print("✅ All unit tests passed successfully for LeetCode 1290 across all 3 implementations!")


if __name__ == "__main__":
    run_tests()
