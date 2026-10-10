"""
LeetCode 21: Merge Two Sorted Lists
Pattern: Linked List (Dummy Node + Zipper Merge Technique)
Difficulty: Easy
Link: https://leetcode.com/problems/merge-two-sorted-lists/
"""

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    # Helper for readable test printing
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


class Solution:
    def mergeTwoLists(self, list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
        """
        Time Complexity: O(n + m) - single pass through both lists
        Space Complexity: O(1) - in-place pointer stitching (zero new nodes created)
        """
        # Step 1: Create a dummy anchor node and a builder pointer (cur)
        dummy = ListNode()
        cur = dummy
        
        # Step 2: Compare and stitch nodes while both lists have elements
        while list1 and list2:
            if list1.val <= list2.val:
                cur.next = list1        # Stitch node list1
                list1 = list1.next      # Advance list1
            else:
                cur.next = list2        # Stitch node list2
                list2 = list2.next      # Advance list2
            cur = cur.next              # Advance builder cur to the newly attached node
            
        # Step 3: Attach the remaining chain of whichever list is not empty
        cur.next = list1 if list1 else list2
        
        # Step 4: Return dummy.next (skip the fake anchor node)
        return dummy.next


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [0], [0]),
        ([5], [1, 2, 4], [1, 2, 4, 5]),
        ([-9, 3], [5, 7], [-9, 3, 5, 7]),
    ]
    
    for l1_arr, l2_arr, expected in test_cases:
        l1 = ListNode.from_list(l1_arr)
        l2 = ListNode.from_list(l2_arr)
        merged = sol.mergeTwoLists(l1, l2)
        actual = merged.to_list() if merged else []
        assert actual == expected, f"Failed for {l1_arr} and {l2_arr}: expected {expected}, got {actual}"
        print(f"✓ list1={l1_arr}, list2={l2_arr} -> merged={actual}")
        
    print("\nAll test cases passed successfully!")
