# Class 12: Advanced linked list operations and two-pointer mechanics

> **Source Notes:** [`notes/class12notes.pdf`](file:///Users/sathyat/Developer/projects/dsa/notes/class12notes.pdf) (LinkedList Class - Part 2)  
> **Prerequisites:** [Linked List Fundamentals](./01_linked_list_fundamentals.md), [Reverse First k Nodes](./02_reverse_first_k_nodes.md)

In technical interviews, linked list questions test whether you can manipulate memory pointers in $\mathcal{O}(1)$ auxiliary space without losing references or causing infinite loops.

This guide distills the 8 advanced operations covered in Class 12, focusing on the two-pointer (Tortoise and Hare) technique, pointer reversal mechanics, and cycle mathematics.

---

## 1. Reverse entire linked list ([LC 206](./206_reverse_linked_list.md))

Reverse every pointer arrow in a singly linked list in-place in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.

```text
Original: [ 2 ] ──► [ 4 ] ──► [ 6 ] ──► [ 8 ] ──► [ 10 ] ──► Null
Reversed: Null ◄── [ 2 ] ◄── [ 4 ] ◄── [ 6 ] ◄── [ 8 ] ◄── [ 10 ]
                                                              ▲
                                                             prev (New Head)
```

### Algorithm steps (4-step pointer flip):
* **1. Initialize pointers:** `prev = None`, `cur = head`.
* **2. While cur is not None:**
  * `nn = cur.next` (Bookmark forward node before breaking wire).
  * `cur.next = prev` (Flip current node's arrow backward).
  * `prev = cur` (Slide `prev` forward onto current node).
  * `cur = nn` (Slide `cur` forward onto bookmarked node).
* **3. Termination condition:** When `cur` becomes `None`, `prev` sits at the final node. Return `prev`.

```python
def reverse(head: ListNode | None) -> ListNode | None:
    prev = None
    cur = head
    while cur is not None:
        nn = cur.next     # 1. Bookmark
        cur.next = prev   # 2. Flip
        prev = cur        # 3. Advance prev
        cur = nn          # 4. Advance cur
    return prev
```

---

## 2. Reverse first k nodes

Given `head` and an integer $k$ ($k > 0, k \le n$), reverse only the first $k$ nodes and stitch them back onto the unreversed tail.

```text
Input:  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► [ 6 ] ──► Null  (k = 4)
Output: [ 4 ] ──► [ 3 ] ──► [ 2 ] ──► [ 1 ] ──► [ 5 ] ──► [ 6 ] ──► Null
```

### The bridge mechanic:
After executing the 4-step flip loop $k$ times:
* `prev` sits on the $k$-th node (Node 4, the **new head**).
* `cur` sits on the $(k+1)$-th node (Node 5, the start of the remaining list).
* `head` still points to Node 1 (the original head, which is now the **tail** of the reversed chunk).
* **The bridge line:** `head.next = cur` glues Node 1 to Node 5 in $\mathcal{O}(1)$ time.

```python
def reverse_first_k(head: ListNode | None, k: int) -> ListNode | None:
    if not head or k <= 1:
        return head

    prev = None
    cur = head
    for _ in range(k):
        if not cur:
            break
        nn = cur.next
        cur.next = prev
        prev = cur
        cur = nn

    head.next = cur  # Bridge old head to remaining list
    return prev      # prev sits on the new head
```

---

## 3. Merge two sorted linked lists ([LC 21](./21_merge_two_sorted_lists.md))

Merge two sorted lists `A` and `B` into a single sorted list in $\mathcal{O}(n + m)$ time and $\mathcal{O}(1)$ extra space by splicing existing nodes.

```text
List A: [ 2 ] ──► [ 5 ] ──► [ 10 ] ──► [ 14 ] ──► [ 19 ] ──► Null
List B: [ 3 ] ──► [ 6 ] ──► [ 9 ]  ──► [ 11 ] ──► [ 12 ] ──► Null

Merged: [ 2 ] ──► [ 3 ] ──► [ 5 ] ──► [ 6 ] ──► [ 9 ] ──► [ 10 ] ──► [ 11 ] ──► [ 12 ] ──► [ 14 ] ──► [ 19 ]
```

### Algorithm steps:
* **1. Base checks:** If `A` is None, return `B`. If `B` is None, return `A`.
* **2. Anchor with dummy:** Initialize `dummy = ListNode(0)` and worker pointer `cur = dummy`.
* **3. Compare and attach:** While both `A` and `B` are not None:
  * If `A.val <= B.val`: set `cur.next = A`, advance `A = A.next`.
  * Else: set `cur.next = B`, advance `B = B.next`.
  * Advance `cur = cur.next`.
* **4. Attach trailing nodes:** `cur.next = A if A else B` in $\mathcal{O}(1)$ time.
* **5. Return:** Return `dummy.next`.

---

## 4. Middle of linked list ([LC 876](./876_middle_of_the_linked_list.md))

### Brute force vs. optimal fast-slow pointers:
* **Brute force:** First pass counts total length $n$ in $\mathcal{O}(n)$. Second pass walks $\lfloor n / 2 \rfloor$ steps in $\mathcal{O}(n/2)$. Total time $\mathcal{O}(1.5n)$.
* **Optimal (Tortoise & Hare):** Single pass in $\mathcal{O}(n/2)$ operations using two runners starting at `head`:
  * `slow` moves 1 step at a time: $s \to s + 1$.
  * `fast` moves 2 steps at a time: $f \to f + 2$.
  * When `fast` reaches the end, `slow` sits at the exact middle node.

### Two middle variations for even-length lists:

#### Variation A: Second middle (Standard LeetCode 876)
For list `[1, 2, 3, 4]`, returns Node 3.
* **Loop condition:** `while fast and fast.next:`
* **Initialization:** `slow = head, fast = head`.

```python
def find_second_middle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

#### Variation B: First middle (Crucial for split & reorder problems like LC 143, LC 234)
For list `[1, 2, 3, 4]`, returns Node 2 (so the first half is `[1, 2]` and the second half starts at Node 3).
* **Loop condition:** `while fast.next and fast.next.next:`
* **Initialization:** `slow = head, fast = head`.

```python
def find_first_middle(head: ListNode | None) -> ListNode | None:
    if not head or not head.next:
        return head
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

---

## 5. Detect cycle in linked list (Floyd's algorithm, [LC 141](./141_linked_list_cycle.md))

Detect if a linked list contains a cycle without altering nodes.

* **Hash set brute force:** Store visited node memory IDs in a set. If a node is already in the set, a cycle exists. Time $\mathcal{O}(n)$, Space $\mathcal{O}(n)$.
* **Floyd's Tortoise and Hare:** Advance `slow` by 1 and `fast` by 2. If there is a cycle, `fast` enters the loop first and `slow` follows. Since the relative speed difference is $2 - 1 = 1$ step per iteration, the distance between them shrinks by 1 each step, guaranteeing they meet without skipping. Time $\mathcal{O}(n)$, Space $\mathcal{O}(1)$.

```python
def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

---

## 6. Find cycle start node ([LC 142](./142_linked_list_cycle_ii.md))

Given a list with a cycle, return the exact node where the cycle begins.

```text
head ──► [ a1 ] ──► [ a2 ] ──► [ a3 ] ──► [ a4 (Start of cycle) ] ──► [ a5 ]
                                                ▲                          │
                                                │                          ▼
                                            [ a8 ] ◄── [ a7 (Meeting) ] ◄── [ a6 ]
```

### The mathematical proof:
Let:
* $a$ = distance from `head` to cycle start node.
* $b$ = distance from cycle start node to the meeting point (MP).
* $l$ = length of the cycle.
* $c_1$ = number of complete cycle loops made by `slow`.
* $c_2$ = number of complete cycle loops made by `fast`.

Total distances traveled when they meet:
$$d_s = a + b + c_1 \cdot l$$
$$d_f = a + b + c_2 \cdot l$$

Because `fast` runs at twice the speed of `slow` ($d_f = 2 \cdot d_s$):
$$a + b + c_2 \cdot l = 2(a + b + c_1 \cdot l)$$
$$a + b + c_2 \cdot l = 2a + 2b + 2c_1 \cdot l$$
$$(c_2 - 2c_1) \cdot l = a + b$$
$$l \cdot (c_2 - 2c_1 - 1) + l = a + b$$
$$a = l \cdot (c_2 - 2c_1 - 1) + (l - b)$$

Let $k = c_2 - 2c_1 - 1$ (an integer $\ge 0$). Then:
$$a = k \cdot l + (l - b)$$

**The geometric consequence:**
The distance from `head` to the cycle start ($a$) is **identically equal** to walking from the meeting point to the cycle start ($(l - b)$) plus some integer number of full loop rotations ($k \cdot l$).

### Algorithm steps (Two-phase detection):
* **Phase 1 (Find Meeting Point):** Advance `slow` by 1 and `fast` by 2 until `slow == fast`. If `fast` or `fast.next` is None, return `None` (no cycle).
* **Phase 2 (Find Start Node):** Reset one pointer back to `head` (`slow = head`), leaving the other at the meeting point (`fast = MP`).
* **Step together:** Advance both pointers **1 step at a time at the same speed**.
* The node where they collide is guaranteed to be the cycle start node.

```python
def detectCycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle found

    # Phase 2: Move slow to head, advance both at 1 step/iteration
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow  # Collide at cycle start
```

---

## 7. Find length of cycle

Once a cycle is confirmed and `slow == fast` at the meeting point:
1. Keep `slow` stationary at the meeting point.
2. Advance a runner pointer `current = slow.next` and initialize `length = 1`.
3. Loop `current = current.next` until `current == slow`, incrementing `length` on each step.
4. Return `length`.

```python
def find_cycle_length(head: ListNode | None) -> int:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Count cycle length
            length = 1
            cur = slow.next
            while cur != slow:
                length += 1
                cur = cur.next
            return length
    return 0  # No cycle
```

---

## 8. Reverse nodes in k-group ([LC 25](https://leetcode.com/problems/reverse-nodes-in-k-group/)) [Hard]

Divide the linked list into blocks of $k$ consecutive nodes and reverse each block independently. If the number of nodes at the end is less than $k$, leave them as is.

```text
Input:  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► Null  (k = 2)
Output: [ 2 ] ──► [ 1 ] ──► [ 4 ] ──► [ 3 ] ──► [ 5 ] ──► Null
```

### Algorithm steps:
* **1. Sentinel anchor:** Initialize `dummy = ListNode(0, head)` and `prev_group = dummy`.
* **2. Outer loop:**
  * Find the $k$-th node ahead of `prev_group`. If fewer than $k$ nodes remain, break.
  * Save `next_group = kth_node.next`.
  * Reverse the $k$ nodes between `prev_group.next` and `kth_node`.
  * Connect `prev_group.next` to the new group head, and connect the new group tail to `next_group`.
  * Slide `prev_group` forward to the new group tail.
* **3. Return:** `dummy.next`.

```python
def reverseKGroup(head: ListNode | None, k: int) -> ListNode | None:
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

        # Reverse current group: prev_group.next to kth
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

## Summary table of operations

| # | Operation | Time Complexity | Space Complexity | Core Pattern & Notes |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Reverse List | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | 4-step pointer flip (`nn`, flip, advance `prev`, advance `cur`). |
| **2** | Reverse First K Nodes | $\mathcal{O}(k)$ | $\mathcal{O}(1)$ | Flip $k$ nodes, connect bridge: `head.next = cur`, return `prev`. |
| **3** | Merge Sorted Lists | $\mathcal{O}(n + m)$ | $\mathcal{O}(1)$ | Zipper merge with dummy head; attach remaining tail in $\mathcal{O}(1)$. |
| **4** | Find Middle (Second / First) | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Fast & slow pointers; condition controls second vs first middle. |
| **5** | Detect Cycle | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Floyd's Tortoise & Hare; collision check `slow == fast`. |
| **6** | Find Cycle Start | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Two-phase; mathematical proof $a = k \cdot l + (l - b)$. |
| **7** | Find Cycle Length | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Freeze `slow` at meeting point, walk runner around loop. |
| **8** | Reverse K-Group | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Segment verification, block reversal, and inter-group stitching. |
