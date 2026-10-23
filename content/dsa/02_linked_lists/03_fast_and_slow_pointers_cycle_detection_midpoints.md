# Fast and slow pointers (cycles, midpoints, and reversals)

Most linked list tricks come down to running two pointers at different speeds: `slow` steps 1 node at a time, `fast` steps 2 nodes at a time. The speed gap is always 1, which lets you find midpoints in one pass, detect loops without extra memory, and locate where a cycle starts.

---

## 1. Finding the middle node ([LC 876](876_middle_of_the_linked_list.md))

Two passes works (count $n$, then walk $n // 2$), but fast and slow pointers do it in one pass:
* `slow = slow.next` (moves 1x)
* `fast = fast.next.next` (moves 2x)

When `fast` hits the end, `slow` is sitting on the middle.

```text
Odd length: [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None
Start:   s=1, f=1
Step 1:  s=2, f=3
Step 2:  s=3, f=5  (f.next is None; loop ends. slow sits on 3)
```

### Even length: second middle vs. first middle
For `[1, 2, 3, 4]`, which middle you want depends on what you are doing:

* **Second middle (Node 3):** Standard for LC 876. Use `while fast and fast.next:`.
* **First middle (Node 2):** Needed when splitting a list into two halves before reversing (like Palindrome LC 234 or Reorder List LC 143). Use `while fast.next and fast.next.next:`.

```python
# Second middle (standard)
def find_second_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# First middle (for splitting in half)
def find_first_middle(head):
    if not head or not head.next:
        return head
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

---

## 2. Cycle detection (Floyd's algorithm, [LC 141](141_linked_list_cycle.md))

You could dump visited node ids into a set, but that takes $\mathcal{O}(n)$ memory.

With two pointers, if there is a cycle, `fast` enters the loop first and `slow` follows. Because `fast` gains 1 step on `slow` on every iteration, the gap between them closes by 1 until `slow == fast`.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

If `fast` or `fast.next` hits `None`, there is no cycle.

---

## 3. Finding where the cycle starts ([LC 142](142_linked_list_cycle_ii.md))

Once `slow == fast`, they are at the meeting point inside the loop. To find the node where the loop actually begins:
1. Leave `fast` at the meeting point.
2. Put `slow` back at `head`.
3. Step both by 1 at the same speed.
4. The node where they collide is the cycle start.

```text
head ──► [ a1 ] ──► [ a2 ] ──► [ a3 ] ──► [ a4 (Cycle Start) ] ──► [ a5 ]
                                                ▲                        │
                                                │                        ▼
                                            [ a8 ] ◄── [ a7 (Meeting) ] ◄── [ a6 ]
```

### Why this works (the distance math)
Let:
* $a$ = distance from `head` to cycle start.
* $b$ = distance from cycle start to meeting point.
* $l$ = length of the cycle.
* $c_1$ = full loops slow completed.
* $c_2$ = full loops fast completed.

Total distance when they meet:
$$d_s = a + b + c_1 \cdot l$$
$$d_f = a + b + c_2 \cdot l$$

Because `fast` travels at double the speed of `slow` ($d_f = 2 d_s$):
$$a + b + c_2 \cdot l = 2(a + b + c_1 \cdot l)$$
$$a + b + c_2 \cdot l = 2a + 2b + 2c_1 \cdot l$$
$$(c_2 - 2c_1) \cdot l = a + b$$
$$l \cdot (c_2 - 2c_1 - 1) + l = a + b$$
$$a = l \cdot (c_2 - 2c_1 - 1) + (l - b)$$

Let $k = c_2 - 2c_1 - 1$. Then:
$$a = k \cdot l + (l - b)$$

This says walking $a$ steps from `head` puts you at the exact same node as walking $(l - b)$ steps from the meeting point. So stepping both by 1 makes them hit the cycle start together.

```python
def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None

    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    return slow
```

---

## 4. Finding cycle length

Once you know a cycle exists and `slow == fast`:
1. Keep `slow` right where it is.
2. Walk a pointer `cur = slow.next` around the loop, counting steps until `cur == slow`.

```python
def get_cycle_length(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            length = 1
            cur = slow.next
            while cur != slow:
                length += 1
                cur = cur.next
            return length
    return 0
```

---

## 5. In-place pointer reversal ([LC 206](206_reverse_linked_list.md))

Flips every arrow backward using 3 pointers. You have to save `nxt = cur.next` before you overwrite `cur.next = prev`, or you drop the rest of the list.

```text
Step 1: nxt = cur.next      (save rest of list)
Step 2: cur.next = prev     (flip arrow backward)
Step 3: prev = cur          (slide prev forward)
Step 4: cur = nxt           (slide cur forward)
```

```python
def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev  # cur fell off to None; prev sits on new head
```

---

## 6. Reversing the first k nodes ([Tutorial](02_reverse_first_k_nodes.md))

When reversing only a prefix of length $k$, the original `head` becomes the tail of that reversed chunk.

After running the 4-step flip loop $k$ times:
* `prev` sits at the $k$-th node (the new head).
* `cur` sits at the $(k+1)$-th node (start of remaining list).
* `head` is still holding the first node (now the end of the reversed piece).
* Connect the bridge: `head.next = cur`.
* Return `prev`.

```python
def reverse_first_k(head, k):
    if not head or k <= 1:
        return head
    prev = None
    cur = head
    for _ in range(k):
        if not cur:
            break
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    head.next = cur
    return prev
```

---

## 7. Zipper merge ([LC 21](21_merge_two_sorted_lists.md))

Splices two sorted lists into one sorted list without allocating new nodes:

1. Put a `dummy` node at the front and set `cur = dummy`.
2. Compare `l1.val` and `l2.val`. Attach whichever is smaller to `cur.next`, then advance that list's pointer.
3. Advance `cur = cur.next`.
4. When one list runs out, attach the remaining tail directly: `cur.next = l1 if l1 else l2`.
5. Return `dummy.next`.

```python
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    cur = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 if l1 else l2
    return dummy.next
```

---

## 8. Reverse nodes in k-group ([LC 25](https://leetcode.com/problems/reverse-nodes-in-k-group/))

Divide the list into chunks of $k$ nodes and reverse each chunk. If the last chunk has fewer than $k$ nodes, leave it alone.

1. Anchor with `dummy = ListNode(0, head)` and set `prev_group = dummy`.
2. Check if at least $k$ nodes remain ahead of `prev_group`. If not, stop.
3. Save `next_group = kth_node.next`.
4. Reverse the $k$ nodes between `prev_group.next` and `kth_node`.
5. Connect `prev_group.next = kth_node` and connect the group's new tail to `next_group`.
6. Move `prev_group` to the group's new tail and repeat.

```python
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    prev_group = dummy

    def get_kth(curr, steps):
        while curr and steps > 0:
            curr = curr.next
            steps -= 1
        return curr

    while True:
        kth = get_kth(prev_group, k)
        if not kth:
            break
        next_group = kth.next

        # Reverse this group
        prev = next_group
        cur = prev_group.next
        while cur != next_group:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        temp = prev_group.next
        prev_group.next = kth
        prev_group = temp

    return dummy.next
```

---

## Quick reference

| Task | Pointers used | Key condition | Return value |
| :--- | :--- | :--- | :--- |
| **Middle (second)** | `slow` (1x), `fast` (2x) | `while fast and fast.next:` | `slow` |
| **Middle (first)** | `slow` (1x), `fast` (2x) | `while fast.next and fast.next.next:` | `slow` |
| **Cycle check** | `slow` (1x), `fast` (2x) | `if slow == fast:` | `True` / `False` |
| **Cycle entrance** | Reset `slow = head` | `while slow != fast:` (both 1x) | `slow` |
| **Cycle length** | Freeze `slow`, walk `cur` | `while cur != slow:` | `length` |
| **Reversal** | `prev, cur, nxt` | `while cur:` | `prev` |
| **First k nodes** | Loop $k$ times | `head.next = cur` | `prev` |
| **Zipper merge** | `dummy, cur, l1, l2` | `while l1 and l2:` | `dummy.next` |
| **k-Group reversal** | `prev_group, kth, next_group` | Check $k$ nodes remain | `dummy.next` |
