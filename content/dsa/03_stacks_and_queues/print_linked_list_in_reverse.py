"""
Print a Linked List in Reverse Order

Given the head of a singly linked list, print or return the elements of the
linked list from the tail node to the head node.
Constraints:
- 0 <= Number of nodes <= 10^5
- -10^9 <= Node.val <= 10^9
- Expected Time: O(N)
- Expected Space: O(N) auxiliary space (using recursion or a stack)
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


def build_linked_list(arr: List[int]) -> Optional[ListNode]:
    if not arr:
        return None
    dummy = ListNode(0)
    curr = dummy
    for x in arr:
        curr.next = ListNode(x)
        curr = curr.next
    return dummy.next


def linked_list_to_array(head: Optional[ListNode]) -> List[int]:
    out = []
    curr = head
    while curr:
        out.append(curr.val)
        curr = curr.next
    return out


class Solution:
    def print_reverse_stack(self, head: Optional[ListNode]) -> List[int]:
        """
        Approach 1: Explicit Heap-Allocated Stack (FAANG Standard)
        Traverses the list, pushes values onto an explicit stack, and pops them.
        Safe against call-stack overflow on large inputs (N = 10^5).
        Preserves the input list without mutation.
        Time: O(N)
        Space: O(N)
        """
        if not head:
            return []

        stack = []
        curr = head
        while curr:
            stack.append(curr.val)
            curr = curr.next

        # In competitive programming portal, print(*reversed(stack))
        return stack[::-1]

    def print_reverse_recursion(self, head: Optional[ListNode]) -> List[int]:
        """
        Approach 2: Recursive Post-Order Traversal
        Intuitive 3-liner, but hits Python's default recursion limit (1000 frames)
        if N = 10^5, resulting in RecursionError / StackOverflowError.
        Time: O(N)
        Space: O(N) call stack frames.
        """
        out: List[int] = []

        def helper(node: Optional[ListNode]) -> None:
            if not node:
                return
            helper(node.next)
            out.append(node.val)

        helper(head)
        return out

    def print_reverse_followup_o1_space(self, head: Optional[ListNode]) -> tuple[List[int], bool]:
        """
        Approach 3: Follow-Up O(1) Auxiliary Space (Reverse, Collect, Reverse Back)
        If the interviewer requires O(1) extra space, mutate the list in-place,
        collect/print values, and reverse it back to preserve caller immutability.
        Returns: (reversed_values, is_original_structure_restored)
        Time: O(N) (3 passes)
        Space: O(1) auxiliary space (excluding output collection)
        """
        if not head:
            return [], True

        def reverse(node: Optional[ListNode]) -> Optional[ListNode]:
            prev = None
            curr = node
            while curr:
                nxt = curr.next
                curr.next = prev
                prev = curr
                curr = nxt
            return prev

        # Step 1: Reverse in-place
        new_head = reverse(head)

        # Step 2: Collect reversed order
        out = []
        curr = new_head
        while curr:
            out.append(curr.val)
            curr = curr.next

        # Step 3: Reverse back to preserve original list contract
        restored_head = reverse(new_head)
        is_restored = (restored_head == head)

        return out, is_restored


def test_print_linked_list_in_reverse():
    sol = Solution()

    test_cases = [
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ([10], [10]),
        ([], []),
        ([4, 2, 9, 7], [7, 9, 2, 4]),
    ]

    for arr, expected in test_cases:
        # Test Approach 1: Stack
        head1 = build_linked_list(arr)
        res1 = sol.print_reverse_stack(head1)
        assert res1 == expected, f"Stack failed on {arr}: got {res1}, expected {expected}"
        assert linked_list_to_array(head1) == arr, "Stack mutated input list!"

        # Test Approach 2: Recursion
        head2 = build_linked_list(arr)
        res2 = sol.print_reverse_recursion(head2)
        assert res2 == expected, f"Recursion failed on {arr}: got {res2}, expected {expected}"

        # Test Approach 3: O(1) Reverse-Print-Reverse
        head3 = build_linked_list(arr)
        res3, restored = sol.print_reverse_followup_o1_space(head3)
        assert res3 == expected, f"O(1) failed on {arr}: got {res3}, expected {expected}"
        assert restored, "Original linked list was not restored after O(1) reversal!"
        assert linked_list_to_array(head3) == arr, "Input data corrupted after restoration!"

    print("All Print Linked List in Reverse tests passed!")


if __name__ == "__main__":
    test_print_linked_list_in_reverse()
