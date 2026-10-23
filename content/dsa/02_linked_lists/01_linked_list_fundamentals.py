"""
Linked List Fundamentals and Core Operations
Comprehensive implementation of Singly Linked List operations based on fundamental concepts.

Covers two main implementation patterns:
1. Object-Oriented Wrapper (`LinkedList` class with encapsulated head)
2. Functional Pointer Manipulation (Direct `ListNode` manipulation common in LeetCode)

Operations covered:
- Node creation and manual pointer wiring
- Traversal, display, and size counting: O(n) time, O(1) space
- Insertion at start / beginning: O(1) time, O(1) space
- Insertion at end: O(n) time, O(1) space
- Insertion at arbitrary 0-based position: O(k) time, O(1) space
- Deletion at start: O(1) time, O(1) space
- Deletion by value (Lookahead pointer pattern): O(n) time, O(1) space
"""

from typing import Optional, List


# ---------------------------------------------------------------------------
# 1. Core Node Definition
# ---------------------------------------------------------------------------

class Node:
    """
    Represents a single node in a singly linked list.
    Contains data and a reference to the next node.
    """
    def __init__(self, data: int, next: Optional["Node"] = None):
        self.data: int = data
        self.next: Optional["Node"] = next

    def __repr__(self) -> str:
        return f"Node({self.data})"


# Alias ListNode for LeetCode convention compatibility
ListNode = Node


# ---------------------------------------------------------------------------
# 2. Functional Pointer Operations (Standalone Functions)
# ---------------------------------------------------------------------------

def create_list(values: List[int]) -> Optional[Node]:
    """
    Build a singly linked list from a Python list of integers.
    Time: O(n), Space: O(n) for the node allocations.
    """
    if not values:
        return None

    head = Node(values[0])
    curr = head
    for val in values[1:]:
        curr.next = Node(val)
        curr = curr.next
    return head


def to_list(head: Optional[Node]) -> List[int]:
    """
    Traverse a linked list and convert node values into a Python list.
    Time: O(n), Space: O(n) for the output list.
    """
    result = []
    curr = head
    while curr is not None:
        result.append(curr.data)
        curr = curr.next
    return result


def display(head: Optional[Node]) -> str:
    """
    Return a clean string representation: '1 -> 2 -> 3 -> None'.
    """
    vals = to_list(head)
    if not vals:
        return "None"
    return " -> ".join(map(str, vals)) + " -> None"


def get_size(head: Optional[Node]) -> int:
    """
    Count total number of nodes by traversing the chain.
    Time: O(n), Space: O(1).
    """
    count = 0
    curr = head
    while curr is not None:
        count += 1
        curr = curr.next
    return count


def insert_at_beginning(head: Optional[Node], value: int) -> Node:
    """
    Insert a new node with value at the front of the list.
    Returns the new head node.

    Time Complexity: O(1) - single pointer redirection.
    Space Complexity: O(1) - one new node allocated.
    """
    new_node = Node(value)
    new_node.next = head
    return new_node


def insert_at_end(head: Optional[Node], value: int) -> Node:
    """
    Insert a new node with value at the tail of the list.
    Returns the head of the modified list.

    Time Complexity: O(n) - must walk to the last node.
    Space Complexity: O(1) - one new node allocated.
    """
    new_node = Node(value)
    if head is None:
        return new_node

    curr = head
    while curr.next is not None:
        curr = curr.next

    curr.next = new_node
    return head


def insert_at_position(head: Optional[Node], value: int, position: int) -> Node:
    """
    Insert a new node at a specified 0-based position.
    position 0 inserts at the beginning.
    Raises IndexError if position is out of bounds.

    Time Complexity: O(position) - walks position - 1 steps.
    Space Complexity: O(1).
    """
    if position < 0:
        raise IndexError("Position cannot be negative")

    new_node = Node(value)

    # Case 1: Insert at beginning
    if position == 0:
        new_node.next = head
        return new_node

    # Case 2: Walk to node at position - 1
    curr = head
    for _ in range(position - 1):
        if curr is None:
            raise IndexError("Position out of bounds")
        curr = curr.next

    if curr is None:
        raise IndexError("Position out of bounds")

    # Wire new node between curr and curr.next
    new_node.next = curr.next
    curr.next = new_node
    return head


def delete_at_start(head: Optional[Node]) -> Optional[Node]:
    """
    Delete the first node of the list and return the new head.
    Time Complexity: O(1).
    Space Complexity: O(1).
    """
    if head is None:
        return None
    return head.next


def delete_by_value(head: Optional[Node], value: int) -> Optional[Node]:
    """
    Delete the first occurrence of a node holding value.
    Uses the lookahead pointer pattern (curr.next.data == value).

    Time Complexity: O(n) - walks until target found.
    Space Complexity: O(1) - in-place relinking.
    """
    if head is None:
        return None

    # Case 1: Target value is at the head node
    if head.data == value:
        return head.next

    # Case 2: Target is in the middle or at tail
    curr = head
    while curr.next is not None:
        if curr.next.data == value:
            # Bypass the target node
            curr.next = curr.next.next
            return head
        curr = curr.next

    return head  # Target value not found, list unchanged


# ---------------------------------------------------------------------------
# 3. Object-Oriented Wrapper: LinkedList Class
# ---------------------------------------------------------------------------

class LinkedList:
    """
    Encapsulated Singly Linked List class.
    Tracks head reference and provides high-level instance methods.
    """
    def __init__(self):
        self.head: Optional[Node] = None

    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return get_size(self.head)

    def display(self) -> str:
        return display(self.head)

    def to_list(self) -> List[int]:
        return to_list(self.head)

    def insert_at_start(self, data: int) -> None:
        """O(1) insertion at front."""
        self.head = insert_at_beginning(self.head, data)

    def insert_at_end(self, data: int) -> None:
        """O(n) insertion at tail."""
        self.head = insert_at_end(self.head, data)

    def insert_at_position(self, data: int, position: int) -> None:
        """O(k) insertion at 0-based position."""
        self.head = insert_at_position(self.head, data, position)

    def delete_at_start(self) -> None:
        """O(1) deletion at front."""
        self.head = delete_at_start(self.head)

    def delete_by_value(self, value: int) -> None:
        """O(n) deletion of first matching node."""
        self.head = delete_by_value(self.head, value)


# ---------------------------------------------------------------------------
# 4. Automated Unit Tests
# ---------------------------------------------------------------------------

def run_tests():
    print("Running Linked List Fundamentals unit tests...")

    # Test 1: Manual node linking
    n1 = Node(4)
    n2 = Node(5)
    n1.next = n2
    assert n1.data == 4
    assert n1.next.data == 5
    assert n1.next.next is None
    assert to_list(n1) == [4, 5]

    # Test 2: create_list and to_list
    head = create_list([1, 2, 3, 4, 5])
    assert to_list(head) == [1, 2, 3, 4, 5]
    assert get_size(head) == 5
    assert display(head) == "1 -> 2 -> 3 -> 4 -> 5 -> None"

    # Test 3: insert_at_beginning
    head = create_list([2, 3, 4])
    head = insert_at_beginning(head, 1)
    assert to_list(head) == [1, 2, 3, 4]
    # Beginning on empty list
    empty_head = insert_at_beginning(None, 10)
    assert to_list(empty_head) == [10]

    # Test 4: insert_at_end
    head = create_list([1, 2, 3])
    head = insert_at_end(head, 4)
    assert to_list(head) == [1, 2, 3, 4]
    empty_end = insert_at_end(None, 99)
    assert to_list(empty_end) == [99]

    # Test 5: insert_at_position
    head = create_list([1, 2, 4])
    # Insert 3 at position 2 -> [1, 2, 3, 4]
    head = insert_at_position(head, 3, 2)
    assert to_list(head) == [1, 2, 3, 4]

    # Insert 0 at position 0 -> [0, 1, 2, 3, 4]
    head = insert_at_position(head, 0, 0)
    assert to_list(head) == [0, 1, 2, 3, 4]

    # Insert 5 at position 5 (tail) -> [0, 1, 2, 3, 4, 5]
    head = insert_at_position(head, 5, 5)
    assert to_list(head) == [0, 1, 2, 3, 4, 5]

    # Test out of bounds index
    try:
        insert_at_position(head, 99, 100)
        assert False, "Expected IndexError"
    except IndexError:
        pass

    # Test 6: delete_at_start
    head = create_list([10, 20, 30])
    head = delete_at_start(head)
    assert to_list(head) == [20, 30]
    head = delete_at_start(head)
    assert to_list(head) == [30]
    head = delete_at_start(head)
    assert head is None
    assert delete_at_start(None) is None

    # Test 7: delete_by_value
    head = create_list([1, 2, 4, 5])
    # Delete middle
    head = delete_by_value(head, 4)
    assert to_list(head) == [1, 2, 5]
    # Delete head
    head = delete_by_value(head, 1)
    assert to_list(head) == [2, 5]
    # Delete tail
    head = delete_by_value(head, 5)
    assert to_list(head) == [2]
    # Delete non-existent value
    head = delete_by_value(head, 999)
    assert to_list(head) == [2]
    # Delete only element
    head = delete_by_value(head, 2)
    assert head is None

    # Test 8: LinkedList class wrapper
    ll = LinkedList()
    assert ll.is_empty() is True
    assert ll.size() == 0

    ll.insert_at_start(5)
    ll.insert_at_start(3)
    ll.insert_at_start(2)
    ll.insert_at_start(1)
    ll.insert_at_start(5)
    # [5, 1, 2, 3, 5]
    assert ll.to_list() == [5, 1, 2, 3, 5]
    assert ll.size() == 5

    ll.delete_at_start()
    # [1, 2, 3, 5]
    assert ll.to_list() == [1, 2, 3, 5]

    ll.delete_by_value(3)
    # [1, 2, 5]
    assert ll.to_list() == [1, 2, 5]

    ll.insert_at_end(99)
    # [1, 2, 5, 99]
    assert ll.to_list() == [1, 2, 5, 99]

    ll.insert_at_position(50, 2)
    # [1, 2, 50, 5, 99]
    assert ll.to_list() == [1, 2, 50, 5, 99]

    print("All Linked List Fundamentals unit tests passed successfully!")


if __name__ == "__main__":
    run_tests()
