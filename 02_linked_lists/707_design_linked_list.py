"""
LeetCode 707: Design Linked List
https://leetcode.com/problems/design-linked-list/

Design your implementation of the linked list.
You can choose to use a singly or doubly linked list.

Approaches:
1. Singly Linked List with Sentinel Dummy Node:
   - Tracks `dummy` (index -1 anchor) and `size`.
   - Eliminates special head insertion/deletion checks.
   - Time: O(1) for addAtHead, O(k) for get/addAtIndex/deleteAtIndex, O(n) for addAtTail.
   - Space: O(1) auxiliary.

2. Doubly Linked List with Sentinel Head & Tail:
   - Tracks `head` (sentinel) and `tail` (sentinel) with prev and next pointers.
   - Bidirectional search optimization: searches from head if index < size // 2, else tail.
   - Time: O(1) for addAtHead and addAtTail, O(min(k, n - k)) for get/addAtIndex/deleteAtIndex.
   - Space: O(1) auxiliary.
"""

from typing import Optional


# ===========================================================================
# Approach 1: Singly Linked List with Sentinel Dummy Node
# ===========================================================================

class SinglyNode:
    def __init__(self, val: int = 0, next: Optional["SinglyNode"] = None):
        self.val: int = val
        self.next: Optional["SinglyNode"] = next


class MyLinkedListSingly:
    """
    Singly linked list implementation using a single sentinel dummy head.
    dummy sits at virtual index -1, ensuring the predecessor of index 0
    always exists without needing special-case branching.
    """
    def __init__(self):
        self.dummy = SinglyNode(0)  # Virtual anchor at index -1
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1

        curr = self.dummy.next
        for _ in range(index):
            curr = curr.next
        return curr.val

    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index > self.size:
            return
        if index < 0:
            index = 0

        # Find the predecessor node (the node at index - 1)
        pred = self.dummy
        for _ in range(index):
            pred = pred.next

        # Splice the new node between pred and pred.next
        to_add = SinglyNode(val, next=pred.next)
        pred.next = to_add
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return

        # Find the predecessor node (the node at index - 1)
        pred = self.dummy
        for _ in range(index):
            pred = pred.next

        # Bypass the target node
        pred.next = pred.next.next
        self.size -= 1


# ===========================================================================
# Approach 2: Doubly Linked List with Sentinel Head & Tail
# ===========================================================================

class DoublyNode:
    def __init__(self, val: int = 0, prev: Optional["DoublyNode"] = None, next: Optional["DoublyNode"] = None):
        self.val: int = val
        self.prev: Optional["DoublyNode"] = prev
        self.next: Optional["DoublyNode"] = next


class MyLinkedListDoubly:
    """
    Doubly linked list implementation with two sentinels (head and tail).
    Supports bidirectional traversal to halve lookup time on indices past midpoint.
    """
    def __init__(self):
        self.head = DoublyNode(0)
        self.tail = DoublyNode(0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1

        # Search from whichever end is closer
        if index < self.size - index:
            curr = self.head.next
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.tail.prev
            for _ in range(self.size - 1 - index):
                curr = curr.prev

        return curr.val

    def addAtHead(self, val: int) -> None:
        self._insert_between(self.head, self.head.next, val)

    def addAtTail(self, val: int) -> None:
        self._insert_between(self.tail.prev, self.tail, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return

        if index < self.size - index:
            pred = self.head
            for _ in range(index):
                pred = pred.next
            succ = pred.next
        else:
            succ = self.tail
            for _ in range(self.size - index):
                succ = succ.prev
            pred = succ.prev

        self._insert_between(pred, succ, val)

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return

        if index < self.size - index:
            curr = self.head.next
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.tail.prev
            for _ in range(self.size - 1 - index):
                curr = curr.prev

        # Remove curr by rewiring neighbor pointers
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        self.size -= 1

    def _insert_between(self, pred: DoublyNode, succ: DoublyNode, val: int) -> None:
        new_node = DoublyNode(val, prev=pred, next=succ)
        pred.next = new_node
        succ.prev = new_node
        self.size += 1


# Default class for submission compatibility
MyLinkedList = MyLinkedListSingly


# ===========================================================================
# Automated Test Suite
# ===========================================================================

def run_tests():
    print("Testing LeetCode 707: Design Linked List...")

    for name, cls in [("Singly", MyLinkedListSingly), ("Doubly", MyLinkedListDoubly)]:
        print(f"  Testing {name} implementation...")

        # Test case from problem description:
        # ["MyLinkedList", "addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"]
        # [[], [1], [3], [1, 2], [1], [1], [1]]
        # Output: [null, null, null, null, 2, null, 3]
        obj = cls()
        obj.addAtHead(1)         # List: 1
        obj.addAtTail(3)         # List: 1 -> 3
        obj.addAtIndex(1, 2)     # List: 1 -> 2 -> 3
        assert obj.get(1) == 2, f"Expected 2, got {obj.get(1)}"
        obj.deleteAtIndex(1)     # List: 1 -> 3
        assert obj.get(1) == 3, f"Expected 3, got {obj.get(1)}"
        assert obj.get(0) == 1, f"Expected 1, got {obj.get(0)}"
        assert obj.get(2) == -1, f"Expected -1 (out of bounds), got {obj.get(2)}"

        # Edge cases: head insertion/deletion and negative/large indices
        obj2 = cls()
        obj2.addAtHead(5)
        obj2.addAtHead(4)        # List: 4 -> 5
        assert obj2.get(0) == 4
        assert obj2.get(1) == 5
        obj2.deleteAtIndex(0)    # List: 5
        assert obj2.get(0) == 5
        obj2.deleteAtIndex(0)    # List empty
        assert obj2.get(0) == -1

        # Out of bounds insertions
        obj3 = cls()
        obj3.addAtIndex(1, 100)  # index > size (0), should not insert
        assert obj3.get(0) == -1
        obj3.addAtIndex(0, 100)  # valid insertion at index 0
        assert obj3.get(0) == 100

        print(f"  {name} implementation passed all test cases!")

    print("All LeetCode 707 test suites passed successfully!")


if __name__ == "__main__":
    run_tests()
