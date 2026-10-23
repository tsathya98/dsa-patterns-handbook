# LeetCode 92: Reverse Linked List II

> **Pattern:** In-place sub-segment reversal with sentinel dummy  
> **Difficulty:** Medium  
> **Access:** Free  
> **Link:** [LeetCode 92](https://leetcode.com/problems/reverse-linked-list-ii/)  
> **Video references:**  
> * [NeetCode: Reverse Linked List II - LeetCode 92](https://www.youtube.com/watch?v=RF_M9tX4Eag)  
> * [Logic First / Full Animated Demo: Reverse Linked List 2](https://www.youtube.com/watch?v=oDL8vuu2Q0E)

---

## The problem

Given the `head` of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes of the list from position `left` to position `right`, and return the reversed list.

Positions are 1-indexed. Solve it in one pass and $\mathcal{O}(1)$ auxiliary space.

```text
Input:  head = [ 1, 2, 3, 4, 5 ], left = 2, right = 4
Output: [ 1, 4, 3, 2, 5 ]
```

---

## Core mental model: Extension of standard reversal

In LeetCode 206, reversing an entire list uses a standard 4-step pointer flip until `cur` reaches `None`:

```python
prev = None
cur = head
while cur:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
```

LeetCode 92 is the exact same logic with only three differences:
1. **Starting point:** Do not start reversing at `head`. First hop `left - 1` times to reach the node right before `left` (`left_prev`).
2. **Loop count:** Instead of looping `while cur:` until the end, loop for exactly `right - left + 1` iterations.
3. **Reconnection:** After the loop finishes, reconnect the two loose ends back to the main list.

---

## Why we need a dummy node (The `left == 1` trap)

A common bug is trying to avoid a dummy node by starting at `head` and looping `left - 2` times:
* If `left = 2`: `left - 2 = 0` hops. `left_prev` stays at node 1. This appears to work by accident.
* If `left = 1`: `left - 2 = -1` hops. The loop runs 0 times, leaving `left_prev` at node 1. But node 1 was supposed to be reversed, not serve as the node before the sublist!
* When `left = 1`, the original `head` moves into the tail of the reversed section. The new head of the entire list is node `right`. Returning `head` returns the wrong node.

**The rule:** Anchoring with `dummy = ListNode(0, head)` gives position 1 a fixed predecessor at index 0. `left_prev = dummy` works identically whether `left = 1` or `left = 500`.

---

## The 3 phases (NeetCode method)

```text
Initial State:
[ dummy ] ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ]
                ▲         ▲
            left_prev    cur
```

### Phase 1: Reach the node at position `left`
Start `left_prev = dummy` and `cur = head`.
Advance both pointers `left - 1` times.
Now:
* `left_prev` sits right before position `left` (node 1).
* `cur` sits at position `left` (node 2).

### Phase 2: Reverse the sublist
Run standard reversal for exactly `right - left + 1` nodes:
```text
After reversal loop:
[ dummy ] ──► [ 1 ]             [ 4 ] ──► [ 3 ] ──► [ 2 ] ──► None       [ 5 ] ──► None
                ▲                 ▲                   ▲                    ▲
            left_prev            prev           left_prev.next            cur
```
Notice:
* `prev` points to the new head of the reversed chunk (node 4).
* `cur` points to the remainder of the list (node 5).
* `left_prev.next` is still node 2 (the original left node, now the tail of the reversed chunk).

### Phase 3: Reconnect the two loose ends
* **Wire 1 (tail of reversed chunk to remainder):**
  `left_prev.next.next = cur` (Node 2 points to Node 5).
* **Wire 2 (upstream prefix to new reversed head):**
  `left_prev.next = prev` (Node 1 points to Node 4).

```text
Wire 1:  [ 1 ]  ─────────────────────────►  [ 4 ] ──► [ 3 ] ──► [ 2 ]
                                                                  │
Wire 2:                                                           └──►  [ 5 ] ──► None
```

> **Order matters:** Always set `left_prev.next.next = cur` before `left_prev.next = prev`. If you overwrite `left_prev.next` first, you lose the reference to node 2.

---

### Algorithm steps:
* **1. Initialize dummy:** Set `dummy = ListNode(0, head)`. Set `left_prev = dummy` and `cur = head`.
* **2. Locate boundary:** Loop `left - 1` times: `left_prev = cur`, `cur = cur.next`.
* **3. Reverse sublist:** Set `prev = None`. Loop `right - left + 1` times:
  * `nxt = cur.next`
  * `cur.next = prev`
  * `prev = cur`
  * `cur = nxt`
* **4. Reconnect:** Set `left_prev.next.next = cur`, then `left_prev.next = prev`.
* **5. Return:** Return `dummy.next`.

---

## Solution code

<details>
<summary>Spoiler: Solution Code (Phase-Based Pointer Reversal)</summary>

```python
class Solution:
    def reverseBetween(self, head: ListNode | None, left: int, right: int) -> ListNode | None:
        if not head or left == right:
            return head

        dummy = ListNode(0, head)

        # Phase 1: Reach node at position left
        left_prev = dummy
        cur = head
        for _ in range(left - 1):
            left_prev = cur
            cur = cur.next

        # Phase 2: Reverse from left to right (right - left + 1 nodes)
        prev = None
        for _ in range(right - left + 1):
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # Phase 3: Reconnect both loose ends
        left_prev.next.next = cur   # Node 2 connects to Node 5
        left_prev.next = prev        # Node 1 connects to Node 4

        return dummy.next
```

</details>

---

## Traps to watch for

* **The `left == 1` crash:** If `left = 1`, `head` changes. Without `dummy`, `left_prev` would have to be `None`, requiring messy special branching. `dummy` makes `left = 1` behave like any other index.
* **Skipping nodes in the loop:** Never add guard conditions like `if cur and cur.next:` inside the reversal loop. The loop count `right - left + 1` is mathematically exact.
* **Reconnection order bug:** Writing `left_prev.next = prev` first overwrites `left_prev.next`. When you then do `left_prev.next.next = cur`, you accidentally write `prev.next = cur` (node 4 points to 5), corrupting the sublist.

---

## Complexity

* **Time:** $\mathcal{O}(n)$ single pass (advances at most `right` steps).
* **Space:** $\mathcal{O}(1)$ auxiliary memory (only 4 pointer variables: `dummy`, `left_prev`, `prev`, `cur`).
