# LeetCode 707: Design Linked List

> **Pattern:** Sentinel node design (Singly vs. Doubly Linked List)  
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
* `void addAtIndex(int index, int val)`: Add a node of value `val` before the `index`-th node. If `index == length`, append to tail. If `index > length`, do not insert. If `index < 0`, insert at head.
* `void deleteAtIndex(int index)`: Delete the `index`-th node if valid.

---

## The two standard designs

LeetCode explicitly allows either a **Singly Linked List** or a **Doubly Linked List**. Here is how both work and why you would pick one over the other:

| Feature | Approach 1: Singly Linked List | Approach 2: Doubly Linked List |
| :--- | :--- | :--- |
| **Pointers per node** | 1 (`next`) | 2 (`prev`, `next`) |
| **Sentinels used** | 1 (`dummy` at index -1) | 2 (`head` at index -1, `tail` at index $n$) |
| **Implementation difficulty** | Beginner friendly, fewer pointer reassignments | More pointers to rewire, bidirectional logic |
| **Access time (`get`)** | $\mathcal{O}(k)$ (must walk from front) | $\mathcal{O}(\min(k, n - k))$ (walks from closest end) |
| **Tail insertion (`addAtTail`)** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ |
| **Head insertion (`addAtHead`)** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Memory per node** | 1 pointer reference (8 bytes) | 2 pointer references (16 bytes) |

---

## Approach 1: Singly linked list (Sentinel dummy head)

The most intuitive approach when learning linked lists. 

Without a sentinel node, inserting or deleting at index 0 requires special `if self.head is None:` or `self.head = self.head.next` branch logic. With a sentinel `dummy` node at virtual index `-1`, every real node (including index 0) has a guaranteed predecessor.

```text
Virtual Index:       -1              0            1            2
                 [ dummy (0) ] ──► [ 10 ] ──► [ 20 ] ──► [ 30 ] ──► None
                      ▲              ▲
                      │              │
                   Anchor        Real Head
```

### The predecessor pattern
Notice that both `addAtIndex` and `deleteAtIndex` need to modify the node **before** the target:
* To insert before index `k`, you need the node at index `k - 1`.
* To delete index `k`, you need the node at index `k - 1` so you can bypass index `k`.

Starting at `dummy` (index -1) and moving forward `k` steps lands you precisely on the predecessor at index `k - 1`.

### Algorithm steps:
* **1. Constructor (`__init__`):** Create `self.dummy = SinglyNode(0)` and initialize `self.size = 0`.
* **2. Lookup (`get`):**
  * If `index < 0` or `index >= self.size`, return `-1`.
  * Start at `curr = self.dummy.next`. Walk forward `index` times. Return `curr.val`.
* **3. Insert (`addAtIndex`):**
  * If `index > self.size`, return without inserting.
  * If `index < 0`, clamp to `index = 0`.
  * Start at `pred = self.dummy`. Walk forward `index` times.
  * Splice: `to_add = SinglyNode(val, next=pred.next)`, then `pred.next = to_add`.
  * Increment `self.size += 1`.
* **4. Head and tail wrappers:**
  * `addAtHead(val)` is simply `self.addAtIndex(0, val)`.
  * `addAtTail(val)` is simply `self.addAtIndex(self.size, val)`.
* **5. Delete (`deleteAtIndex`):**
  * If `index < 0` or `index >= self.size`, return.
  * Start at `pred = self.dummy`. Walk forward `index` times.
  * Bypass: `pred.next = pred.next.next`.
  * Decrement `self.size -= 1`.

<details>
<summary>Spoiler: Approach 1 Solution Code (Singly Linked List)</summary>

```python
class SinglyNode:
    def __init__(self, val: int = 0, next: "SinglyNode" = None):
        self.val = val
        self.next = next


class MyLinkedList:
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

        # Step forward index times to land on predecessor (index - 1)
        pred = self.dummy
        for _ in range(index):
            pred = pred.next

        # Wire new node between pred and pred.next
        to_add = SinglyNode(val, next=pred.next)
        pred.next = to_add
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return

        # Step forward index times to land on predecessor (index - 1)
        pred = self.dummy
        for _ in range(index):
            pred = pred.next

        # Bypass the target node
        pred.next = pred.next.next
        self.size -= 1
```

</details>

---

## Approach 2: Doubly linked list (Sentinel head & tail)

When you need $\mathcal{O}(1)$ tail additions and faster lookups on indices near the end of the list, a doubly linked list with two sentinel nodes (`head` and `tail`) is standard.

```text
[ head (sentinel) ] ◄──► [ node 0 ] ◄──► [ node 1 ] ◄──► [ tail (sentinel) ]
```

### Why two sentinels simplify doubly linked logic:
1. `head.next` is always the first real node (or `tail` if empty).
2. `tail.prev` is always the last real node (or `head` if empty).
3. Inserting at head is just inserting between `head` and `head.next`.
4. Inserting at tail is just inserting between `tail.prev` and `tail`.
5. Deleting node `curr` is just `curr.prev.next = curr.next` and `curr.next.prev = curr.prev`.
6. You never check for `None` during rewiring because sentinels are permanent boundaries.

### Bidirectional search optimization:
To reach `index`:
* If `index < self.size - index`: walk forward from `head` (`index` hops).
* Else: walk backward from `tail` (`self.size - index` hops).
This cuts traversal time in half.

### Algorithm steps:
* **1. Constructor:** Create dummy `head` and `tail`, link `head.next = tail`, `tail.prev = head`, set `size = 0`.
* **2. Insert helper (`_insert_between`):**
  * Create `new_node = DoublyNode(val, prev=pred, next=succ)`.
  * Wire `pred.next = new_node` and `succ.prev = new_node`.
  * Increment `self.size += 1`.
* **3. Delete helper (`_delete`):**
  * Wire `node.prev.next = node.next`.
  * Wire `node.next.prev = node.prev`.
  * Decrement `self.size -= 1`.

<details>
<summary>Spoiler: Approach 2 Solution Code (Doubly Linked List)</summary>

```python
class DoublyNode:
    def __init__(self, val: int = 0, prev: "DoublyNode" = None, next: "DoublyNode" = None):
        self.val = val
        self.prev = prev
        self.next = next


class MyLinkedList:
    def __init__(self):
        self.head = DoublyNode(0)
        self.tail = DoublyNode(0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1

        # Bidirectional search: pick closer end
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

        # Remove curr by rewiring neighbors
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        self.size -= 1

    def _insert_between(self, pred: DoublyNode, succ: DoublyNode, val: int) -> None:
        new_node = DoublyNode(val, prev=pred, next=succ)
        pred.next = new_node
        succ.prev = new_node
        self.size += 1
```

</details>

---

## Traps to watch for

* **Valid index bounds vary by operation:**
  * For `get(index)` and `deleteAtIndex(index)`: the index must be strictly valid (`0 <= index < size`). If `index == size`, there is no node to read or delete.
  * For `addAtIndex(index, val)`: `index == size` is valid because it represents appending to the tail. Any `index > size` is rejected.
* **Negative index specification:** LeetCode specifies that if `index < 0` in `addAtIndex`, the node should be inserted at the head (`index = 0`). In `get` and `deleteAtIndex`, negative indices are invalid and should return `-1` or do nothing.
* **Size synchronization:** Every insertion must increment `self.size += 1`, and every deletion must decrement `self.size -= 1`. Forgetting this corrupts index bounds checks on subsequent calls.

---

## Complexity

| Operation | Approach 1 (Singly) | Approach 2 (Doubly) |
| :--- | :--- | :--- |
| **`addAtHead`** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **`addAtTail`** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ |
| **`get(index)`** | $\mathcal{O}(k)$ | $\mathcal{O}(\min(k, n - k))$ |
| **`addAtIndex(index)`** | $\mathcal{O}(k)$ | $\mathcal{O}(\min(k, n - k))$ |
| **`deleteAtIndex(index)`** | $\mathcal{O}(k)$ | $\mathcal{O}(\min(k, n - k))$ |
| **Auxiliary Space** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
