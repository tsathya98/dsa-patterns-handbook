# Linked List Master Cheat Sheet

> Full 11-type classification: [90% Linked List Taxonomy Guide](../02_linked_lists/linked_list_90_percent_taxonomy.md)

## 1. What a linked list actually is

An array stores items side by side in memory, so `arr[2]` is an instant $\mathcal{O}(1)$ jump. A linked list scatters nodes across memory. Each node only knows its own value and the memory address (`.next`) of the next node:

```python
ListNode(val=10, next=ListNode(val=20, next=ListNode(val=30, next=None)))
```

```text
[ val: 10 | next ] ──► [ val: 20 | next ] ──► [ val: 30 | next: None ]
```

Calling `len(head)` crashes because a node has no idea how many nodes follow it. Finding the length takes an $\mathcal{O}(n)$ walk.

---

## 2. Dummy vs. `cur` (Anchor and Hand)

Whenever you build or splice a linked list, start with:
```python
dummy = ListNode(0)
cur = dummy
```

| Variable | Role | Moves? | Why you need it |
| :--- | :--- | :--- | :--- |
| `dummy` | Fixed anchor | No | Stays glued to the start so you never lose the front of your list. |
| `cur` | Moving hand | Yes | Walks to the end (`cur = cur.next`) to attach the next node. |
| `dummy.next` | Real head | - | Skips the fake `0` placeholder and returns the real first node. |

**When to `return dummy.next` vs `return head`:**
- Created a fake placeholder `dummy = ListNode(0)`? Return `dummy.next`.
- Modified the input list in place (`cur = head`)? Return `head`.

---

## 3. The 6 Core Patterns

### Pattern 1: Zipper Merge ([LC 21](../02_linked_lists/21_merge_two_sorted_lists.md))
Compare the front of both sorted lists, attach the smaller node to `cur.next`, and step forward.

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode()
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

### Pattern 2: In-Place Arrow Reversal ([LC 206](../02_linked_lists/206_reverse_linked_list.md))
Flip every pointer in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space using three pointers (`prev`, `cur`, `nxt`). You must bookmark `nxt = cur.next` before flipping `cur.next = prev`, or you lose the rest of the list.

```text
None ◄── [ 1 ]      [ 2 ] ──► [ 3 ] ──► None
           ▲          ▲         ▲
          prev       cur       nxt
```

### Algorithm steps:
* **1. Initialize pointers:** Set `prev = None` and `cur = head` before beginning traversal.
* **2. Bookmark and reverse:** While `cur` is not None, save `nxt = cur.next` so the forward chain is preserved, then point `cur.next = prev` backward.
* **3. Advance sliding window:** Shift pointers forward via `prev = cur` and `cur = nxt`. When `cur` reaches None, return `prev` as the new head in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ memory.


```python
def reverseList(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next      # 1. Bookmark next node
        cur.next = prev     # 2. Flip arrow backward
        prev = cur          # 3. Advance prev
        cur = nxt           # 4. Advance cur
    return prev             # cur is None; prev sits on the new head
```

**Common bugs:**
- Writing `while cur and cur.next:` stops one node early and leaves the last node disconnected. Use `while cur:`.
- Returning `cur` returns `None`. Always return `prev`.

### Pattern 3: Tortoise & Hare / Fast & Slow ([LC 141](../02_linked_lists/141_linked_list_cycle.md), LC 876)
`slow` moves 1 step; `fast` moves 2 steps.
- If they meet (`slow is fast`), there is a cycle.
- If `fast` hits the end (`None`), `slow` is sitting at the middle node.

```python
def findMiddle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

### Pattern 4: Half-Reversal ("Triple Crown") ([LC 234](../02_linked_lists/234_palindrome_linked_list.md), [LC 143](../02_linked_lists/143_reorder_list.md))
Solves palindrome checking or list folding in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space:
1. Find the end of the first half (`while fast.next and fast.next.next`).
2. Reverse the second half (`slow.next`) in place.
3. Walk two pointers inward from `head` and `second_half`.

*(Note: Dumping values into a Python list and running a two-pointer squeeze `l < r` is a fine $\mathcal{O}(n)$ space starting point in interviews, and beats `lst == lst[::-1]` because it exits early on mismatches without copying the array. Follow up with the in-place reversal for $\mathcal{O}(1)$ space.)*

### Pattern 5: Fixed-Gap Measuring Stick ([LC 19](../02_linked_lists/19_remove_nth_node_from_end.md), [LC 1721](../02_linked_lists/1721_swapping_nodes_in_a_linked_list.md))
To find the $k$-th node from the end in one pass:
1. Advance `fast` by `k - 1` steps from `head` (reaching the $k$-th node takes `k - 1` hops, not `k`).
2. Start `slow = head` and move both 1 step at a time until `fast.next is None`.
3. `slow` lands on the $k$-th node from the end.

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

### Pattern 6: Stream Accumulator / Horner's Rule ([LC 1290](../02_linked_lists/1290_convert_binary_number_in_a_linked_list_to_integer.md))
Convert digits or bits left-to-right in $\mathcal{O}(1)$ space by shifting the running total left and adding the new bit. Avoid `s += str(head.val)`, which copies strings in $\mathcal{O}(n^2)$ time.

```python
def getDecimalValue(head):
    ans = 0
    while head:
        ans = (ans << 1) | head.val
        head = head.next
    return ans
```

---

## 4. Five Rules That Prevent `AttributeError`

1. **Attach nodes, not values:** Write `cur.next = list1`, never `cur.next = list1.val`.
2. **Guard `.next` checks:** Use `while list1 and list2:`, not `or`.
3. **Save `cur.next` before overwriting it:** In reversals, `nxt = cur.next` always comes first.
4. **Never move `dummy`:** Advance `cur = cur.next` so `dummy` stays at the front.
5. **Sorted vs. unsorted deduplication ([LC 83](../02_linked_lists/83_remove_duplicates_from_sorted_list.md)):** Sorted lists only need adjacent comparisons (`cur.val == cur.next.val`, $\mathcal{O}(1)$ space). Unsorted lists require a hash set ($\mathcal{O}(n)$ space).
