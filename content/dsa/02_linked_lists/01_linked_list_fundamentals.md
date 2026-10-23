# Linked list fundamentals

A linked list is a linear data structure consisting of node objects linked sequentially. Unlike arrays, where elements occupy one contiguous block of physical memory, linked list nodes can be scattered anywhere across heap memory, held together by references.

Understanding linked lists comes down to two fundamentals: how nodes are organized in physical memory, and what pointer assignments actually change.

---

## Array vs. linked list in physical memory

The fundamental trade-offs between arrays and linked lists stem directly from how they are laid out in hardware memory.

### 1. Array contiguous memory layout

In an array `arr = [1, 6, 0, 4, 2]`, memory is allocated in one uninterrupted physical block:

```text
Memory Address:  10048    10052    10056    10060    10064   (4 bytes per int)
Array Index:      [ 0 ]    [ 1 ]    [ 2 ]    [ 3 ]    [ 4 ]
Value:              1        6        0        4        2
```

* **Instant random access in $\mathcal{O}(1)$ time:** Jumping to index `i` requires no iteration. The computer calculates the exact physical byte address instantly using a closed-form formula:
  $$\text{Address}(i) = \text{Base Address} + i \times \text{Element Size}$$
  For index 3: $10048 + 3 \times 4 = 10060$.
* **Expensive insertions and deletions in $\mathcal{O}(n)$ time:** Because elements must remain contiguous with no gaps, inserting `7` at index 0 forces every subsequent element to shift right by one slot:
  ```text
  Insert 7 at index 0:
  [ 7 ] ──► [ 1 ] ──► [ 6 ] ──► [ 0 ] ──► [ 4 ] ──► [ 2 ]
  (All 5 original items shifted right. In an array of 10,000 items, all 10,000 shift.)
  ```

---

### 2. Linked list scattered heap layout

In a linked list, each node is an independent object allocated wherever free heap memory exists. Each node stores two fields:
1. `data`: the payload value.
2. `next`: the reference (memory address) of the next node, or `None` if it is the tail.

```text
[ Address: #ad1 ]          [ Address: #bd4 ]          [ Address: #ef7 ]
┌────────┬───────┐         ┌────────┬───────┐         ┌────────┬───────┐
│ data: 1│ #bd4  ├────────►│ data: 2│ #ef7  ├────────►│ data: 3│ None  │
└────────┴───────┘         └────────┴───────┘         └────────┴───────┘
     ▲
     │
   head (Kept at start, points to #ad1)
```

* **Sequential access in $\mathcal{O}(n)$ time:** Nodes do not sit side by side. There is no formula to calculate the address of index `k`. To reach the 500th node, you must start at `head` and hop through 499 individual `.next` pointers.
* **Instant insertion and deletion at head in $\mathcal{O}(1)$ time:** Adding an element to the front does not move any existing nodes. You allocate a new node, point its `.next` to the current `head`, and redirect `head` to the new node. Whether the list contains 3 nodes or 10,000,000 nodes, rewiring takes constant time.
* **Instant splicing in $\mathcal{O}(1)$ time (once located):** To remove a node in the middle, you simply bypass its address (`curr.next = curr.next.next`). The bypass itself is $\mathcal{O}(1)$, though walking to the node takes $\mathcal{O}(n)$ traversal time.

---

### Complexity comparison

| Operation | Array | Linked List (Singly) | Why the difference exists |
| :--- | :--- | :--- | :--- |
| **Access by index (`arr[i]`)** | $\mathcal{O}(1)$ | $\mathcal{O}(n)$ | Arrays calculate address via math; linked lists must hop pointers. |
| **Insert at head** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Arrays must shift all $n$ items right; linked lists wire one pointer. |
| **Insert at tail (no tail pointer)** | $\mathcal{O}(1)$ amortized | $\mathcal{O}(n)$ | Arrays append to preallocated capacity; linked lists must traverse to end. |
| **Insert at tail (with tail pointer)** | $\mathcal{O}(1)$ amortized | $\mathcal{O}(1)$ | Direct pointer update in both. |
| **Insert at position $k$** | $\mathcal{O}(n)$ | $\mathcal{O}(k)$ | Array shifts $n - k$ items; linked list walks $k$ steps then splices in $\mathcal{O}(1)$. |
| **Delete at head** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Array shifts all items left; linked list runs `head = head.next`. |
| **Delete by value (search + delete)** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Both require linear search; array shifts elements, linked list relinks pointers. |
| **Memory overhead** | Low (data only) | Higher | Linked list stores an extra 8-byte pointer reference per node. |

---

## Node anatomy and manual wiring

A singly linked node consists of a data container and an outgoing reference.

```python
class Node:
    def __init__(self, data: int):
        self.data: int = data       # The value stored in this node
        self.next: 'Node' = None    # Points to the next Node (None if tail)
```

### Manual node construction and linking

```python
# 1. Create independent nodes in memory
n1 = Node(4)
n2 = Node(5)

# 2. Wire the pointer arrow manually
n1.next = n2

# 3. Inspect values through the chain
print(n1.data)        # Output: 4
print(n2.data)        # Output: 5
print(n1.next.data)   # Output: 5 (hopping through n1's outgoing link)
print(n1.next)        # Output: <Node object at #ad1>
print(n2.next)        # Output: None
```

```text
n1 [ data: 4 | next: #ad1 ] ────► n2 [ data: 5 | next: None ]
```

---

## The two pointer operations

Most linked list bugs happen when these two operations get confused:

### 1. Mutating the wire (`curr.next = ...`)
When `.next` is on the **left** side of `=`, you are physically altering where a node's outgoing arrow points in heap memory.
* Example: `curr.next = new_node` splices `new_node` directly after `curr`.
* Warning: Any nodes previously attached to `curr.next` are detached unless saved in a bookmark variable beforehand.

### 2. Moving your finger (`curr = curr.next`)
When a variable name is on the **left** side of `=`, no nodes in memory are modified. You are only advancing your local label one step forward along the existing chain.

```text
Before:
  [ Node 1 ] ────► [ Node 2 ]
      ▲
      │
     curr

Operation: curr = curr.next

After:
  [ Node 1 ] ────► [ Node 2 ]
                       ▲
                       │
                      curr   (List structure unchanged; only local label moved)
```

### Algorithm steps:
* **1. Inspect assignment expression:** Check whether `.next` sits on the left side of `=`.
* **2. Identify operation type:**
  * If `.next` is on the left (`curr.next = target`): mutate the outgoing wire in memory, altering the chain structure.
  * If `.next` is on the right (`curr = curr.next`): move your reference pointer forward along the chain without modifying any node.
* **3. Preserve downstream links:** Save a bookmark (`nxt = curr.next`) before mutating wires to prevent orphaned nodes.
* **4. Complete pointer update:** Conclude rewiring or advance the reference to complete the step.

---

## Why losing the head loses the list

Variables in Python are references pointing to objects in memory. In a singly linked list, each node is accessible only through the node preceding it.

Given `head -> [1] -> [2] -> [3] -> None`, if you run `head = head.next` without preserving a reference to `[1]`, nothing points to `[1]` anymore. Because pointers only move forward, you can never traverse back to `[1]`, and Python's garbage collector frees it from memory.

To traverse a list without destroying your anchor, always assign a worker pointer:
```python
curr = head
while curr:
    print(curr.data)
    curr = curr.next
# head is still preserved at the start of the list
```

---

## Essential linked list operations

### 1. Traversal and display

Walking every node in the chain to read values or compute size.

```text
head ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► None
           ▲
           │
          curr (advances step by step until curr is None)
```

* **Time Complexity:** $\mathcal{O}(n)$
* **Space Complexity:** $\mathcal{O}(1)$ auxiliary space

```python
def traverse(head: Node) -> list[int]:
    result = []
    curr = head
    while curr is not None:
        result.append(curr.data)
        curr = curr.next
    return result

def get_size(head: Node) -> int:
    count = 0
    curr = head
    while curr is not None:
        count += 1
        curr = curr.next
    return count
```

---

### 2. Insert at beginning (`insert_at_start`)

Inserts a new node before the current head, making the new node the first element.

```text
Initial:          head ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► None
New node:  [ 1 ]

Step 1: new_node.next = head
           [ 1 ] ─────────► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► None
                             ▲
                             │
                            head

Step 2: return new_node (new head)
  head ──► [ 1 ] ─────────► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► None
```

### Algorithm steps:
* **1. Create node:** Allocate `new_node = Node(value)`.
* **2. Wire outgoing arrow:** Set `new_node.next = head`.
* **3. Return new anchor:** Return `new_node` as the new head of the list.

* **Time Complexity:** $\mathcal{O}(1)$ constant time (no loops).
* **Space Complexity:** $\mathcal{O}(1)$ one node allocated.

```python
def insert_at_beginning(head: Node, value: int) -> Node:
    new_node = Node(value)
    new_node.next = head
    return new_node
```

---

### 3. Insert at end (`insert_at_end`)

Traverses to the final node (where `curr.next is None`) and connects the new node.

```text
Initial:   head ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► None
New node:  [ 4 ]

Walk to tail:
           head ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► None
                                          ▲
                                          │
                                         curr (curr.next is None)

Relink: curr.next = new_node
           head ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► None
```

### Algorithm steps:
* **1. Create node:** Allocate `new_node = Node(value)`.
* **2. Check empty list:** If `head is None`, the new node is the head; return `new_node`.
* **3. Walk to tail:** Traverse using `curr = head` while `curr.next is not None`. When the loop finishes, `curr` points to the last node.
* **4. Attach node:** Set `curr.next = new_node`.
* **5. Return head:** Return original `head`.

* **Time Complexity:** $\mathcal{O}(n)$ to locate the tail.
* **Space Complexity:** $\mathcal{O}(1)$.

```python
def insert_at_end(head: Node, value: int) -> Node:
    new_node = Node(value)
    if head is None:
        return new_node

    curr = head
    while curr.next is not None:
        curr = curr.next

    curr.next = new_node
    return head
```

---

### 4. Insert at arbitrary position (`insert_at_position`)

Inserts a new node at a given 0-based index.

```text
List:      0         1         2
         [ 1 ] ──► [ 2 ] ──► [ 4 ] ──► None

Insert 3 at position 2:
Walk to position - 1 (Node 2):
         [ 1 ] ──► [ 2 ] ──► [ 4 ] ──► None
                     ▲
                    curr

Step 1: new_node.next = curr.next
         [ 3 ] ──────────────► [ 4 ]
           ▲
           │ (new node points to node 4)

Step 2: curr.next = new_node
         [ 2 ] ──► [ 3 ] ──► [ 4 ]
```

### Algorithm steps:
* **1. Handle front insertion:** If `position == 0`, run `new_node.next = head; return new_node`.
* **2. Locate predecessor:** Walk `position - 1` steps to land on `curr`, the node immediately before the target index.
* **3. Guard out-of-bounds:** If `curr is None` before completing hops, the position exceeds list length; raise an error.
* **4. Wire downstream link first:** Set `new_node.next = curr.next`.
* **5. Wire upstream link second:** Set `curr.next = new_node`.
  *(Caution: If steps 4 and 5 are swapped, `curr.next` is overwritten first, permanently disconnecting and losing the rest of the list).*

* **Time Complexity:** $\mathcal{O}(\text{position})$ time to reach the slot.
* **Space Complexity:** $\mathcal{O}(1)$.

```python
def insert_at_position(head: Node, value: int, position: int) -> Node:
    if position < 0:
        raise IndexError("Position cannot be negative")

    new_node = Node(value)
    if position == 0:
        new_node.next = head
        return new_node

    curr = head
    for _ in range(position - 1):
        if curr is None:
            raise IndexError("Position out of bounds")
        curr = curr.next

    if curr is None:
        raise IndexError("Position out of bounds")

    new_node.next = curr.next
    curr.next = new_node
    return head
```

---

### 5. Delete at start (`delete_at_start`)

Removes the first node by advancing the head reference.

```text
Before:   head ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► None
After:              (X) head ──► [ 2 ] ──► [ 3 ] ──► None
```

* **Time Complexity:** $\mathcal{O}(1)$
* **Space Complexity:** $\mathcal{O}(1)$

```python
def delete_at_start(head: Node) -> Node:
    if head is None:
        return None
    return head.next
```

---

### 6. Delete by value (`delete_by_value`)

Deletes the first node containing a given target value.

Because singly linked nodes cannot look backward, deletion requires stopping at the **predecessor** of the node to be removed. We check one node ahead using the lookahead condition `curr.next.data == value`.

```text
Delete 4 from: [ 1 ] ──► [ 2 ] ──► [ 4 ] ──► [ 5 ] ──► None

Lookahead check: curr is [ 2 ], curr.next is [ 4 ]
Since curr.next.data == 4:
Bypass: curr.next = curr.next.next

[ 1 ] ──► [ 2 ] ──────────────► [ 5 ] ──► None
            │                      ▲
            └─── (bypasses [ 4 ]) ─┘
```

### Algorithm steps:
* **1. Check empty list:** If `head is None`, return `None`.
* **2. Check head match:** If `head.data == value`, delete head by returning `head.next`.
* **3. Lookahead traversal:** While `curr.next is not None`:
  * If `curr.next.data == value`:
    * Bypass node: set `curr.next = curr.next.next`.
    * Return `head`.
  * Otherwise, step forward: `curr = curr.next`.
* **4. Return head:** If loop finishes without a match, value was not in list; return unchanged `head`.

* **Time Complexity:** $\mathcal{O}(n)$ search + $\mathcal{O}(1)$ pointer splice.
* **Space Complexity:** $\mathcal{O}(1)$.

```python
def delete_by_value(head: Node, value: int) -> Node:
    if head is None:
        return None

    # Case 1: Value is at the head
    if head.data == value:
        return head.next

    # Case 2: Value is in the middle or tail
    curr = head
    while curr.next is not None:
        if curr.next.data == value:
            curr.next = curr.next.next
            return head
        curr = curr.next

    return head
```

---

## Complete class-based implementation: LinkedList wrapper

In production applications, linked list mechanics are encapsulated inside a `LinkedList` class that hides pointer manipulation behind clean instance methods.

```python
class Node:
    def __init__(self, data: int):
        self.data: int = data
        self.next: 'Node' = None

class LinkedList:
    def __init__(self):
        self.head: Node = None

    def is_empty(self) -> bool:
        return self.head is None

    def insert_at_start(self, data: int) -> None:
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data: int) -> None:
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = new_node

    def delete_at_start(self) -> None:
        if self.head is not None:
            self.head = self.head.next

    def delete_by_value(self, value: int) -> None:
        if self.head is None:
            return

        if self.head.data == value:
            self.head = self.head.next
            return

        curr = self.head
        while curr.next is not None:
            if curr.next.data == value:
                curr.next = curr.next.next
                return
            curr = curr.next

    def display(self) -> str:
        vals = []
        curr = self.head
        while curr is not None:
            vals.append(str(curr.data))
            curr = curr.next
        return " -> ".join(vals) + " -> None" if vals else "None"

    def size(self) -> int:
        count = 0
        curr = self.head
        while curr is not None:
            count += 1
            curr = curr.next
        return count
```

---

## The dummy node pattern (Anchor and hand)

In algorithm problems, implementing special cases for head deletion or head insertion adds branching logic. The dummy node (or sentinel node) eliminates edge cases:

```python
dummy = ListNode(0)
cur = dummy
```

| Variable | Role | Moves? | Why you need it |
| :--- | :--- | :--- | :--- |
| `dummy` | Fixed anchor | No | Stays fixed at index -1 so you never lose the head of the chain. |
| `cur` | Moving hand | Yes | Walks forward (`cur = cur.next`) to attach or splice nodes. |
| `dummy.next` | Real head | - | Skips placeholder `0` and returns the true first node. |

```text
Step 0: dummy = ListNode(0); cur = dummy
[ dummy (0) ] ──► None
     ▲
     │
   dummy
    cur

Step 1: cur.next = ListNode(10); cur = cur.next
[ dummy (0) ] ──► [ 10 ] ──► None
     ▲               ▲
     │               │
   dummy            cur

Step 2: cur.next = ListNode(20); cur = cur.next
[ dummy (0) ] ──► [ 10 ] ──► [ 20 ] ──► None
     ▲                          ▲
     │                          │
   dummy                       cur

Return: dummy.next (Points directly to [ 10 ])
```

**When to `return dummy.next` vs `return head`:**
* If you created a fake anchor `dummy = ListNode(0)` to build or splice: return `dummy.next`.
* If you modified nodes in place using `cur = head` without altering the first node: return `head`.

### The golden rule: When do you need a dummy node?

Ask yourself one question: **"Can the very first node (`head`) change, get deleted, or move?"**

| Scenario | Do you need `dummy`? | Why | Example Problems |
| :--- | :--- | :--- | :--- |
| **Deleting nodes** | **YES** | The target to delete might be `head` itself | LC 203 (Remove Elements)<br/>LC 19 (Remove Nth Node)<br/>LC 2095 (Delete Middle) |
| **Reversing a subsegment** | **YES** | The subsegment might start at `1` (`left == 1`), changing the list head | LC 92 (Reverse II)<br/>LC 25 (Reverse k-Group)<br/>LC 24 (Swap Pairs) |
| **Building a new list** | **YES** | Need an immovable anchor while an active pointer appends nodes | LC 21 (Merge Two Sorted Lists)<br/>LC 2 (Add Two Numbers) |
| **Read-only / Searching** | **NO** | Only inspecting data or cycle checks; head never moves | LC 876 (Middle of List)<br/>LC 141 (Cycle Detection)<br/>LC 160 (Intersection) |
| **Reversing the ENTIRE list** | **NO** | Entire list flips. `prev` naturally ends up on the new head | LC 206 (Reverse Linked List) |

---

## The 6 core FAANG linked list patterns

Across coding interviews, 95% of linked list questions reduce to one of these six patterns:

### Pattern 1: Zipper merge
Used in: [LC 21 (Merge Two Sorted Lists)](21_merge_two_sorted_lists.md)

Compare values at the heads of two lists, link the smaller node to `cur.next`, advance that list's pointer, and advance `cur`. When one list runs out, attach the remaining tail directly in $\mathcal{O}(1)$ time.

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode(0)
    cur = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            cur.next = list1
            list1 = list1.next
        else:
            cur.next = list2
            list2 = list2.next
        cur = cur.next
    cur.next = list1 if list1 else list2
    return dummy.next
```

### Pattern 2: In-place arrow reversal
Used in: [LC 206 (Reverse Linked List)](206_reverse_linked_list.md), [Tutorial (Reverse First k Nodes)](02_reverse_first_k_nodes.md)

Reverses pointer arrows using three pointers: `prev`, `cur`, and `nxt`. You must bookmark `nxt = cur.next` before overwriting `cur.next = prev`, otherwise you orphan the remainder of the chain.

```text
None ◄── [ 1 ]      [ 2 ] ──► [ 3 ] ──► None
           ▲          ▲         ▲
          prev       cur       nxt
```

### Algorithm steps:
* **1. Initialize pointers:** Set `prev = None` and `cur = head`.
* **2. Bookmark next:** While `cur` is not None, save `nxt = cur.next`.
* **3. Flip arrow backward:** Set `cur.next = prev`.
* **4. Advance pointers:** Move `prev = cur` and `cur = nxt`.
* **5. Return new head:** When `cur` becomes None, `prev` sits at the old tail, which is the new head.

```python
def reverseList(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next      # 1. Bookmark next node
        cur.next = prev     # 2. Flip arrow backward
        prev = cur          # 3. Advance prev
        cur = nxt           # 4. Advance cur
    return prev             # prev is the new head
```

### Pattern 3: Tortoise and hare (Fast & slow pointers)
Used in: [LC 141 & 142 (Linked List Cycle)](141_linked_list_cycle.md), [LC 876 (Middle of the Linked List)](876_middle_of_the_linked_list.md)

`slow` advances 1 step at a time; `fast` advances 2 steps at a time.
* **Midpoint finding:** When `fast` reaches the end (`fast is None` or `fast.next is None`), `slow` sits at the middle node.
* **Cycle detection:** If the list has a cycle, `fast` laps `slow` from behind and they eventually point to the exact same node (`slow is fast`).

```python
def findMiddle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

### Pattern 4: Half-reversal (Triple crown)
Used in: [LC 234 (Palindrome Linked List)](234_palindrome_linked_list.md), [LC 143 (Reorder List)](143_reorder_list.md)

Solves palindrome checking or folding a list inward in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ extra space without allocating new arrays:
1. Find the midpoint using fast and slow pointers (`while fast.next and fast.next.next:`).
2. Split the list into two halves and reverse the second half in place.
3. Walk two pointers simultaneously: one from the head of the first half, one from the head of the reversed second half. Compare values (for palindrome) or interleave arrows alternately (for reorder).

### Pattern 5: Fixed-gap measuring stick
Used in: [LC 19 (Remove Nth Node From End)](19_remove_nth_node_from_end.md), [LC 1721 (Swapping Nodes in a Linked List)](1721_swapping_nodes_in_a_linked_list.md)

To find the $k$-th node from the end in a single pass without knowing the total length $n$:
1. Place a scout pointer `fast` at `head` and walk it forward by $k - 1$ steps.
2. Place a writer pointer `slow` at `head`.
3. Advance both `fast` and `slow` 1 step at a time until `fast.next is None`.
4. Because the gap between them is fixed, when `fast` reaches the final node, `slow` lands on the $k$-th node from the end.

```python
def swapNodes(head, k):
    first = second = head
    for _ in range(k - 1):
        first = first.next
    fast = first
    while fast.next:
        fast = fast.next
        second = second.next
    first.val, second.val = second.val, first.val
    return head
```

### Pattern 6: Stream accumulator (Horner's rule)
Used in: [LC 1290 (Convert Binary Number in a Linked List to Integer)](1290_convert_binary_number_in_a_linked_list_to_integer.md)

Process stream digits or bits left to right without converting to strings or allocating extra memory. Multiply the accumulator by the base (or bit-shift left) and add the incoming node's value. This runs in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space, avoiding $\mathcal{O}(n^2)$ string concatenation overhead.

```python
def getDecimalValue(head):
    ans = 0
    while head:
        ans = (ans << 1) | head.val
        head = head.next
    return ans
```

---

## Five rules that prevent AttributeError

Almost every linked list crash is `AttributeError: 'NoneType' object has no attribute 'next'`. Follow these five checks:

* **1. Wire nodes, not values:** Write `cur.next = list1`, never `cur.next = list1.val`.
* **2. Guard double dereferences:** Before reading `node.next.val` or `node.next.next`, always guard with `while node and node.next:`.
* **3. Always bookmark before mutating:** Once you run `cur.next = ...`, the original downstream node is gone unless you saved `nxt = curr.next` beforehand.
* **4. Advance the worker pointer:** When building a list with `cur.next = node`, never forget to step forward with `cur = cur.next`. Forgetting this overwrites the same slot repeatedly and drops previous nodes.
* **5. Verify your return target:** If you used an anchor `dummy = ListNode(0)`, return `dummy.next`. If you reversed a chain, return `prev` (because `cur` has fallen off the edge into `None`). If you modified the list in place without changing the first node, return `head`.

---

## Related study guides and code in this section

* [Implementation: Linked List Fundamentals Python Code (Test Suite)](01_linked_list_fundamentals.py)
* [Tutorial: Reverse First k Nodes Step-by-Step](02_reverse_first_k_nodes.md)
* [Deep Dive: Fast and Slow Pointers (Cycles, Midpoints, and Reversals)](03_fast_and_slow_pointers_cycle_detection_midpoints.md)
* [Classification: 90% Linked List Taxonomy Guide](linked_list_90_percent_taxonomy.md)
* [Quick Reference: Linked List Master Cheat Sheet](../../cheat-sheets/linked_list_master_cheat_sheet.md)
