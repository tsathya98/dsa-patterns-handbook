# Linked list fundamentals

If linked lists feel slippery, the confusion usually comes down to two things: how nodes sit in memory and what a pointer assignment actually changes.

## Array vs. linked list in memory

In an array `[10, 20, 30]`, memory is allocated in one contiguous block:
- Address 101: `10`
- Address 102: `20`
- Address 103: `30`

Because the items sit side by side, jumping to index `2` is instant math (`101 + 2 = 103`) in $\mathcal{O}(1)$ time. Inserting a new item at the front, however, forces every element to shift one spot to the right in $\mathcal{O}(n)$ time.

In a linked list, nodes can live anywhere in memory. Each node holds its own value and the memory address of the next node:
- Address `0x100`: value is `10`, next node is at `0x850`.
- Address `0x850`: value is `20`, next node is at `0x320`.
- Address `0x320`: value is `30`, next node is `None`.

```text
[ Address: 0x100 ]        [ Address: 0x850 ]        [ Address: 0x320 ]
┌────────┬───────┐        ┌────────┬───────┐        ┌────────┬───────┐
│ val: 10│ 0x850 ├───────►│ val: 20│ 0x320 ├───────►│ val: 30│ None  │
└────────┴───────┘        └────────┴───────┘        └────────┴───────┘
```

A singly linked node has no idea what came before it. It only knows its own `val` and its `.next` pointer. Calling `len(head)` will crash because nodes do not store the chain length; finding the length always requires an $\mathcal{O}(n)$ traversal.

## Node anatomy in Python

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val     # The data stored in this node
        self.next = next   # Reference to the next ListNode (or None)
```

When you write:
```python
node_a = ListNode(10)
node_b = ListNode(20)
node_a.next = node_b
```
you are wiring `node_a`'s pointer so it leads to `node_b`.

## The two pointer operations

Most linked list bugs happen when these two lines get mixed up:

### 1. Mutating the wire (`curr.next = ...`)
When `.next` is on the left side of `=`, you are physically changing where a node's outgoing arrow points in memory. For example, `curr.next = ListNode(5)` attaches a new node right after `curr`.

### 2. Moving your finger (`curr = curr.next`)
When a variable name is on the left side of `=`, no nodes in memory change. You are just moving your `curr` label one step forward along the existing chain.

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
                      curr   (The list did not change; only the label moved)
```

### Algorithm steps:
* **1. Inspect assignment expression:** Check whether `.next` sits on the left side of the equals sign.
* **2. Identify operation type:**
  * If `.next` is on the left (`curr.next = target`): mutate the outgoing wire in heap memory, altering the list structure.
  * If `.next` is on the right (`curr = curr.next`): move your reference pointer forward along the chain without modifying any node.
* **3. Preserve downstream links:** Save a bookmark (`nxt = curr.next`) before mutating wires to prevent orphaned nodes.
* **4. Complete pointer update:** Conclude rewiring or advance the reference to complete the step.

## Why losing the head loses the list

Variables in Python are labels pointing to objects in memory. Given `head -> [1] -> [2] -> [3] -> None`, if you run `head = head.next` without saving another reference to `[1]`, nothing points to `[1]` anymore. Since arrows only go forward, you can never walk back to `[1]`, and Python's garbage collector frees it from memory.

## The dummy node pattern (Anchor and Hand)

Whenever you build a new linked list, or might delete or replace the original head node, start with a dummy node:

```python
dummy = ListNode(0)
cur = dummy
```

| Variable | Role | Moves? | Why you need it |
| :--- | :--- | :--- | :--- |
| `dummy` | Fixed anchor | No | Stays glued to the front so you never lose the head of the list. |
| `cur` | Moving hand | Yes | Walks to the end (`cur = cur.next`) to attach each new node. |
| `dummy.next` | Real head | - | Skips the initial placeholder `0` and returns the true first node. |

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

Return: dummy.next  (Points directly to [ 10 ])
```

**When to `return dummy.next` vs `return head`:**
- If you created a fake anchor `dummy = ListNode(0)` to build or splice: return `dummy.next`.
- If you modified nodes in place using `cur = head`: return `head`.

---

## The 6 core linked list patterns

Across FAANG interviews, roughly 95% of linked list questions reduce to one of these six patterns:

### Pattern 1: Zipper merge
Used in: [LC 21 (Merge Two Sorted Lists)](./21_merge_two_sorted_lists.md)

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
Used in: [LC 206 (Reverse Linked List)](./206_reverse_linked_list.md), [Tutorial (Reverse First k Nodes)](./02_reverse_first_k_nodes.md)

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
    return prev             # prev is the new head; cur is None
```

### Pattern 3: Tortoise and hare (Fast & slow pointers)
Used in: [LC 141 & 142 (Linked List Cycle)](./141_linked_list_cycle.md), LC 876 (Middle of the Linked List)

`slow` advances 1 step at a time; `fast` advances 2 steps at a time.
- **Midpoint finding:** When `fast` reaches the end (`fast is None` or `fast.next is None`), `slow` is guaranteed to sit at the middle node.
- **Cycle detection:** If the list has a cycle, `fast` laps `slow` from behind and they eventually point to the exact same node (`slow is fast`).

```python
def findMiddle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

### Pattern 4: Half-reversal (Triple crown)
Used in: [LC 234 (Palindrome Linked List)](./234_palindrome_linked_list.md), [LC 143 (Reorder List)](./143_reorder_list.md)

Solves palindrome checking or folding a list inward in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ extra space without allocating new arrays:
1. Find the midpoint using fast and slow pointers.
2. Split the list into two halves and reverse the second half in place.
3. Walk two pointers simultaneously: one from the head of the first half, one from the head of the reversed second half. Compare values (for palindrome) or interleave arrows alternately (for reorder).

### Pattern 5: Fixed-gap measuring stick
Used in: [LC 19 (Remove Nth Node From End)](./19_remove_nth_node_from_end.md), [LC 1721 (Swapping Nodes in a Linked List)](./1721_swapping_nodes_in_a_linked_list.md)

To find the $k$-th node from the end in a single pass without knowing the total length $n$:
1. Place a scout pointer `fast` at `head` and walk it forward by $k - 1$ steps (it takes $k - 1$ hops to reach the $k$-th node).
2. Place a writer pointer `slow` at `head`.
3. Advance both `fast` and `slow` 1 step at a time until `fast.next is None`.
4. Because the gap between them is fixed, when `fast` reaches the final node, `slow` lands precisely on the $k$-th node from the end.

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
Used in: [LC 1290 (Convert Binary Number in a Linked List to Integer)](./1290_convert_binary_number_in_a_linked_list_to_integer.md)

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
* **3. Always bookmark before mutating:** Once you run `cur.next = ...`, the original downstream node is gone unless you saved `nxt = cur.next` beforehand.
* **4. Advance the worker pointer:** When building a list with `cur.next = node`, never forget to step forward with `cur = cur.next`. Forgetting this overwrites the same slot repeatedly and drops previous nodes.
* **5. Verify your return target:** If you used an anchor `dummy = ListNode(0)`, return `dummy.next`. If you reversed a chain, return `prev` (because `cur` has fallen off the edge into `None`). If you modified the list in place without changing the first node, return `head`.

---

## Related study guides in this section

* [Tutorial: Reverse First k Nodes Step-by-Step](./02_reverse_first_k_nodes.md)
* [Classification: 90% Linked List Taxonomy Guide](./linked_list_90_percent_taxonomy.md)
* [Quick Reference: Linked List Master Cheat Sheet](../cheat_sheets/linked_list_master_cheat_sheet.md)
