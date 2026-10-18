# LeetCode 707: Design Linked List

> **Pattern:** Doubly linked list with sentinel head and tail  
> **Difficulty:** Medium  
> **Access:** Free  
> **Link:** [LeetCode 707](https://leetcode.com/problems/design-linked-list/)

## The problem

Design your implementation of the linked list. You can choose to use a singly or doubly linked list.

Implement the `MyLinkedList` class:
* `MyLinkedList()`: Initializes the `MyLinkedList` object.
* `int get(int index)`: Get the value of the `index`-th node. If the index is invalid, return `-1`.
* `void addAtHead(int val)`: Add a node of value `val` before the first element.
* `void addAtTail(int val)`: Append a node of value `val` as the last element.
* `void addAtIndex(int index, int val)`: Add a node of value `val` before the `index`-th node. If `index == length`, append to tail. If `index > length`, do not insert.
* `void deleteAtIndex(int index)`: Delete the `index`-th node if valid.

## The core trick

The cleanest way to implement a linked list without getting bogged down in null checks and edge cases is a **Doubly Linked List with two sentinel nodes: `head` and `tail`**:

```text
[ head (sentinel) ] ◄──► [ node 0 ] ◄──► [ node 1 ] ◄──► [ tail (sentinel) ]
```

### Why two sentinels eliminate bugs:
1. `head.next` is always the first real node (or `tail` if empty).
2. `tail.prev` is always the last real node (or `head` if empty).
3. Inserting at head is just inserting between `head` and `head.next`.
4. Inserting at tail is just inserting between `tail.prev` and `tail`.
5. Deleting node `curr` is just `curr.prev.next = curr.next` and `curr.next.prev = curr.prev`.
6. You **never check for None** when wiring arrows, because sentinel nodes are permanent.

### Bidirectional index optimization:
Track `self.size`. To access `index`:
* If `index < size - index`: walk forward from `head`.
* Else: walk backward from `tail`.
This cuts lookup time in half.

### Algorithm steps:
* **1. Constructor:** Create dummy `head` and `tail`, link `head.next = tail`, `tail.prev = head`, set `size = 0`.
* **2. Insert helper:** Write a helper `_insert(pred, succ, val)`:
  * Create `new_node = ListNode(val, next=succ, prev=pred)`.
  * Wire `pred.next = new_node`, `succ.prev = new_node`.
  * Increment `size += 1`.
* **3. Delete helper:** Write a helper `_delete(node)`:
  * Wire `node.prev.next = node.next`.
  * Wire `node.next.prev = node.prev`.
  * Decrement `size -= 1`.

## Traps to watch for

* **Index boundary conditions:** In `get(index)` and `deleteAtIndex(index)`, valid indices are `0 <= index < size`. In `addAtIndex(index)`, valid indices are `0 <= index <= size` (allowing insertion at tail).
* **Negative index handling:** Negative indices should be rejected or clamped according to problem constraints (`if index < 0: return`).

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Node:
    def __init__(self, val: int = 0, prev: "Node" = None, next: "Node" = None):
        self.val = val
        self.prev = prev
        self.next = next

class MyLinkedList:
    def __init__(self):
        self.head = Node(0)
        self.tail = Node(0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1

        # Bidirectional search optimization
        if index < self.size - index:
            cur = self.head.next
            for _ in range(index):
                cur = cur.next
        else:
            cur = self.tail.prev
            for _ in range(self.size - 1 - index):
                cur = cur.prev

        return cur.val

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
            cur = self.head.next
            for _ in range(index):
                cur = cur.next
        else:
            cur = self.tail.prev
            for _ in range(self.size - 1 - index):
                cur = cur.prev

        # Remove cur
        cur.prev.next = cur.next
        cur.next.prev = cur.prev
        self.size -= 1

    def _insert_between(self, pred: Node, succ: Node, val: int) -> None:
        new_node = Node(val, prev=pred, next=succ)
        pred.next = new_node
        succ.prev = new_node
        self.size += 1
```

</details>

## Complexity

* **`addAtHead`, `addAtTail`:** $\mathcal{O}(1)$ time.
* **`get`, `addAtIndex`, `deleteAtIndex`:** $\mathcal{O}(\min(k, n - k))$ time.
* **Space:** $\mathcal{O}(n)$ total memory for $n$ elements.
