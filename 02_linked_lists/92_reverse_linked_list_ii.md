# LeetCode 92: Reverse Linked List II

> **Pattern:** In-place sub-segment reversal with sentinel dummy  
> **Difficulty:** Medium  
> **Access:** Free  
> **Link:** [LeetCode 92](https://leetcode.com/problems/reverse-linked-list-ii/)

## The problem

Given the `head` of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes of the list from position `left` to position `right`, and return the reversed list.

Positions are 1-indexed. Solve it in one pass and $\mathcal{O}(1)$ space.

```text
Input:  head = [ 1, 2, 3, 4, 5 ], left = 2, right = 4
Output: [ 1, 4, 3, 2, 5 ]
```

## The core trick

Use a `dummy` node anchored at `0` before `head`. This cleanly handles the edge case where `left = 1` (the original head itself gets reversed).

1. Walk a pointer `prev` to node `left - 1` (the node immediately before the reversal window).
2. The node currently at `prev.next` is `cur`, which will become the **tail** of the reversed sub-segment.
3. For each of the `right - left` iterations, pluck the node `nxt = cur.next` and splice it directly in front of `cur` right after `prev`:

```text
Initial:
[ dummy ] ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ]
                ▲         ▲         ▲
               prev      cur       nxt

Iteration 1 (Splicing Node 3 after prev):
  nxt = cur.next             (3)
  cur.next = nxt.next        (2 connects to 4)
  nxt.next = prev.next       (3 connects to 2)
  prev.next = nxt            (1 connects to 3)

Result: [ 1 ] ──► [ 3 ] ──► [ 2 ] ──► [ 4 ] ──► [ 5 ]
          ▲                   ▲
         prev                cur
```

Notice that `cur` never moves forward; each iteration pulls the next node forward to sit right after `prev`.

### Algorithm steps:
* **1. Anchor sentinel:** Initialize `dummy = ListNode(0, head)`, set `prev = dummy`.
* **2. Locate boundary:** Advance `prev` by `left - 1` steps so it sits right before the sub-segment. Set `cur = prev.next`.
* **3. Splicing loop:** Repeat `right - left` times:
  * `nxt = cur.next` (Bookmark next node).
  * `cur.next = nxt.next` (Bypass `nxt`).
  * `nxt.next = prev.next` (Point `nxt` to the current front of the sub-segment).
  * `prev.next = nxt` (Wire `prev` to `nxt`).
* **4. Return:** Return `dummy.next`.

## Traps to watch for

* **Reversing without a dummy when `left = 1`:** If `left = 1`, the head itself changes. Without `dummy`, `prev` would have to be `None`, forcing special-case branching. With `dummy = ListNode(0, head)`, the exact same logic works for all values of `left`.
* **Advancing `cur`:** Do not do `cur = cur.next`. `cur` remains glued to the node originally at index `left` as it slides to the back of the reversed window.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def reverseBetween(self, head: ListNode | None, left: int, right: int) -> ListNode | None:
        if not head or left == right:
            return head

        dummy = ListNode(0, head)
        prev = dummy

        # 1. Walk prev to node left - 1
        for _ in range(left - 1):
            prev = prev.next

        cur = prev.next

        # 2. Splicing loop
        for _ in range(right - left):
            nxt = cur.next
            cur.next = nxt.next
            nxt.next = prev.next
            prev.next = nxt

        return dummy.next
```

</details>

## Complexity

* **Time:** $\mathcal{O}(n)$ single pass (advances at most `right` steps).
* **Space:** $\mathcal{O}(1)$ auxiliary memory (only 3 pointer references).
