# LeetCode 92: Reverse Linked List II

> **Pattern:** In-place sub-segment reversal with sentinel dummy  
> **Difficulty:** Medium  
> **Access:** Free  
> **Link:** [LeetCode 92](https://leetcode.com/problems/reverse-linked-list-ii/)

## The problem

Given the `head` of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes of the list from position `left` to position `right`, and return the reversed list.

Positions are 1-indexed. Solve it in one pass and $\mathcal{O}(1)$ auxiliary space.

```text
Input:  head = [ 1, 2, 3, 4, 5 ], left = 2, right = 4
Output: [ 1, 4, 3, 2, 5 ]
```

---

## Why we need a dummy node (and why `dummy = head` breaks)

A common mistake is trying to avoid a dummy node by setting `before_window = head` and hopping `left - 2` times:
* If `left = 2`: `left - 2 = 0` hops. `before_window` stays at node 1. This appears to work by accident.
* If `left = 1`: `left - 2 = -1` hops. The loop runs 0 times, leaving `before_window` at node 1. But node 1 was supposed to be reversed, not serve as the anchor before the cut!
* Even worse, when `left = 1`, the original `head` gets pushed into the middle or tail of the list. The new head of the whole list is node `right`. Returning `head` returns the wrong node.

**The rule:** Whenever `left = 1` is possible, the head itself moves. Anchoring with `dummy = ListNode(0, head)` gives position 1 a fixed predecessor at index 0.

---

## Approach 1: 4-step pointer reversal with two-wire reconnection

Instead of confusing pointer names like `left_prev`, think of cutting a rope into three pieces:
1. Leftover prefix: `[ 1 ]`
2. The window to flip: `[ 2 ] ──► [ 3 ] ──► [ 4 ]`
3. Leftover suffix: `[ 5 ]`

```text
Before reversal:
[ dummy ] ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ]
                ▲         ▲
          before_window  window_tail (will become tail after flip)
```

### The two reconnection wires:
After flipping nodes 2, 3, 4 using the standard 4-step reversal loop, `prev` points to node 4, and `cur` points to node 5.
* **Wire 1 (tail to suffix):** `window_tail.next = cur` (Node 2 points to Node 5).
* **Wire 2 (prefix to head):** `before_window.next = prev` (Node 1 points to Node 4).

```text
Wire 1:  [ 1 ]  ─────────────────────────►  [ 4 ] ──► [ 3 ] ──► [ 2 ]
                                                                  │
Wire 2:                                                           └──►  [ 5 ] ──► None
```

### Algorithm steps:
* **1. Anchor sentinel:** Initialize `dummy = ListNode(0, head)`, set `before_window = dummy`.
* **2. Walk to anchor:** Loop `left - 1` times: `before_window = before_window.next`.
* **3. Mark window tail:** Set `window_tail = before_window.next` and `cur = window_tail`.
* **4. Reverse window:** For `right - left + 1` iterations, run standard 4-step reversal:
  * `nxt = cur.next`
  * `cur.next = prev`
  * `prev = cur`
  * `cur = nxt`
* **5. Reconnect wires:** Set `window_tail.next = cur` and `before_window.next = prev`.
* **6. Return:** Return `dummy.next`.

<details>
<summary>Spoiler: Solution Code (Approach 1: Two-Wire Reconnect)</summary>

```python
class Solution:
    def reverseBetween(self, head: ListNode | None, left: int, right: int) -> ListNode | None:
        if not head or left == right:
            return head

        dummy = ListNode(0, head)

        # 1. Park before_window right before the cut
        before_window = dummy
        for _ in range(left - 1):
            before_window = before_window.next

        # 2. window_tail will end up as the tail of the flipped window
        window_tail = before_window.next

        # 3. Standard 4-step pointer reversal for (right - left + 1) nodes
        prev = None
        cur = window_tail
        for _ in range(right - left + 1):
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # 4. Reconnect both wires
        window_tail.next = cur        # Tail of flipped chunk connects to downstream
        before_window.next = prev     # Upstream connects to new head of flipped chunk

        return dummy.next
```

</details>

---

## Approach 2: One-pass head splicing

Instead of reversing arrows backward and reconnecting at the end, pluck each downstream node in the window and insert it directly after `before_window`:

```text
Initial:
[ dummy ] ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ]
                ▲         ▲         ▲
          before_window  cur       nxt

Iteration 1 (Splicing Node 3 after before_window):
  nxt = cur.next
  cur.next = nxt.next        (2 connects to 4)
  nxt.next = before_window.next (3 connects to 2)
  before_window.next = nxt   (1 connects to 3)

Result: [ 1 ] ──► [ 3 ] ──► [ 2 ] ──► [ 4 ] ──► [ 5 ]
```

<details>
<summary>Spoiler: Solution Code (Approach 2: Splicing)</summary>

```python
class Solution:
    def reverseBetween(self, head: ListNode | None, left: int, right: int) -> ListNode | None:
        if not head or left == right:
            return head

        dummy = ListNode(0, head)
        before_window = dummy

        for _ in range(left - 1):
            before_window = before_window.next

        cur = before_window.next

        # Repeat right - left times
        for _ in range(right - left):
            nxt = cur.next
            cur.next = nxt.next
            nxt.next = before_window.next
            before_window.next = nxt

        return dummy.next
```

</details>

---

## Traps to watch for

* **The `left == 1` trap:** If `left = 1`, the original head moves. Without `dummy`, there is no node before position 1.
* **Skipping nodes in the flip loop:** Do not add conditions like `if cur and cur.next:` inside the loop. The loop count `right - left + 1` already controls the exact boundary.
* **Forgetting the second wire in Approach 1:** If you only connect `before_window.next = prev`, the tail of the flipped segment points to `None`, stranding the rest of the list. You must also connect `window_tail.next = cur`.

---

## Complexity

* **Time:** $\mathcal{O}(n)$ single pass (advances at most `right` steps).
* **Space:** $\mathcal{O}(1)$ auxiliary memory (only pointer references).
