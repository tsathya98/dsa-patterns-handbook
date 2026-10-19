"""
LeetCode 160: Intersection of Two Linked Lists
Pattern: Two Pointers (Length Offset & Track Switch) / Hash Set
Difficulty: Easy
Link: https://leetcode.com/problems/intersection-of-two-linked-lists/
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
    def create_intersecting_lists(listA_vals: list[int], listB_vals: list[int], common_vals: list[int]):
        """
        Helper to construct two intersecting lists sharing common_vals in memory.
        """
        # Build shared segment
        common_head = None
        common_curr = None
        if common_vals:
            common_head = ListNode(common_vals[0])
            common_curr = common_head
            for v in common_vals[1:]:
                common_curr.next = ListNode(v)
                common_curr = common_curr.next

        # Build list A prefix
        headA = None
        currA = None
        if listA_vals:
            headA = ListNode(listA_vals[0])
            currA = headA
            for v in listA_vals[1:]:
                currA.next = ListNode(v)
                currA = currA.next

        # Build list B prefix
        headB = None
        currB = None
        if listB_vals:
            headB = ListNode(listB_vals[0])
            currB = headB
            for v in listB_vals[1:]:
                currB.next = ListNode(v)
                currB = currB.next

        # Attach shared segment
        if currA:
            currA.next = common_head
        else:
            headA = common_head

        if currB:
            currB.next = common_head
        else:
            headB = common_head

        return headA, headB, common_head


class SolutionHashSet:
    """Approach 1: Hash set of node references"""
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        seen = set()
        curA = headA
        while curA:
            seen.add(curA)
            curA = curA.next

        curB = headB
        while curB:
            if curB in seen:
                return curB
            curB = curB.next

        return None


class SolutionLengthOffset:
    """Approach 2: Length difference offset (O(1) space)"""
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        lenA, lenB = 0, 0
        curA, curB = headA, headB

        while curA:
            lenA += 1
            curA = curA.next

        while curB:
            lenB += 1
            curB = curB.next

        curA, curB = headA, headB

        if lenA > lenB:
            for _ in range(lenA - lenB):
                curA = curA.next
        else:
            for _ in range(lenB - lenA):
                curB = curB.next

        while curA and curB:
            if curA == curB:
                return curA
            curA = curA.next
            curB = curB.next

        return None


class SolutionTrackSwitch:
    """Approach 3: Two-pointer track switch (Optimal O(1) space)"""
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        pA, pB = headA, headB

        while pA != pB:
            pA = pA.next if pA else headB
            pB = pB.next if pB else headA

        return pA


def run_tests():
    sol_set = SolutionHashSet()
    sol_len = SolutionLengthOffset()
    sol_switch = SolutionTrackSwitch()

    # Test Case 1: Intersecting lists
    # listA = [4, 1, 8, 4, 5], listB = [5, 6, 1, 8, 4, 5], intersect at 8
    hA1, hB1, expected1 = ListNode.create_intersecting_lists([4, 1], [5, 6, 1], [8, 4, 5])
    assert sol_set.getIntersectionNode(hA1, hB1) is expected1
    assert sol_len.getIntersectionNode(hA1, hB1) is expected1
    assert sol_switch.getIntersectionNode(hA1, hB1) is expected1
    print("✓ Test 1 Passed: Intersected list (different lengths)")

    # Test Case 2: Intersecting lists with same prefix lengths
    # listA = [1, 9, 1, 2, 4], listB = [3, 2, 4], intersect at 2
    hA2, hB2, expected2 = ListNode.create_intersecting_lists([1, 9, 1], [3], [2, 4])
    assert sol_set.getIntersectionNode(hA2, hB2) is expected2
    assert sol_len.getIntersectionNode(hA2, hB2) is expected2
    assert sol_switch.getIntersectionNode(hA2, hB2) is expected2
    print("✓ Test 2 Passed: Intersected list (prefix length difference = 2)")

    # Test Case 3: No intersection
    # listA = [2, 6, 4], listB = [1, 5]
    hA3, hB3, expected3 = ListNode.create_intersecting_lists([2, 6, 4], [1, 5], [])
    assert sol_set.getIntersectionNode(hA3, hB3) is None
    assert sol_len.getIntersectionNode(hA3, hB3) is None
    assert sol_switch.getIntersectionNode(hA3, hB3) is None
    print("✓ Test 3 Passed: Completely disjoint lists (return None)")

    # Test Case 4: Complete overlap (headA is headB)
    hA4, hB4, expected4 = ListNode.create_intersecting_lists([], [], [1, 2, 3])
    assert sol_set.getIntersectionNode(hA4, hB4) is expected4
    assert sol_len.getIntersectionNode(hA4, hB4) is expected4
    assert sol_switch.getIntersectionNode(hA4, hB4) is expected4
    print("✓ Test 4 Passed: 100% shared list from head")

    print("\nAll unit tests passed across all 3 approaches!")


if __name__ == "__main__":
    run_tests()
