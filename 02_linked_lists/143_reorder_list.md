# LeetCode 143: Reorder List

> **Pattern:** Fast/slow midpoint + in-place reversal + zipper merge  
> **Difficulty:** Medium  
> **Link:** [LeetCode 143](https://leetcode.com/problems/reorder-list/)

## The problem

Given the head of a singly linked list $L_0 \to L_1 \to \dots \to L_{n-1} \to L_n$, reorder it in-place to:
$$L_0 \to L_n \to L_1 \to L_{n-1} \to L_2 \to L_{n-2} \to \dots$$

You may not modify node values; you must rewire the nodes themselves.

```text
Input:  1 -> 2 -> 3 -> 4 -> 5 -> None
Output: 1 -> 5 -> 2 -> 4 -> 3 -> None
```

## The core trick

On an array, you would just walk two pointers inward from both ends. On a singly linked list, you cannot walk backward from the tail unless you reverse the arrows in the back half first.

Break the problem into three standard steps:
1. **Find the middle and split (LC 876):** Walk `slow` (1 step) and `fast` (2 steps) so `slow` stops at the end of the first half. Cut the list in two by saving `second = slow.next` and setting `slow.next = None`.
2. **Reverse the second half in-place (LC 206):** Flip the arrows of `second` so you can walk inward from the original tail.
3. **Zipper merge both halves (LC 21):** Alternate taking one node from `first` and one node from `second`.

### Algorithm steps:
* **1. Split list at midpoint:** Walk `slow = head` and `fast = head.next` until `fast` and `fast.next` terminate. Set `second = slow.next` and cut the first half with `slow.next = None`.
* **2. Reverse the second half:** Reverse `second` in-place using a 3-pointer flip (`prev = None`, `cur = second`) so the tail becomes the new head of the second half.
* **3. Zipper merge both halves:** While `second` is not None:
  * Cache forward pointers: `tmp1 = first.next`, `tmp2 = second.next`.
  * Interleave nodes: `first.next = second`, `second.next = tmp1`.
  * Advance pointers: `first = tmp1`, `second = tmp2`.
* **4. Complete in-place:** The input list is reordered in-place; no return statement required.

## Step-by-step trace

Trace on `1 -> 2 -> 3 -> 4 -> 5 -> None`:

```text
Phase 1: Split at midpoint (slow = head, fast = head.next)
  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None
                        ▲                   ▲
                       slow                fast (fast.next is None)
  second = slow.next (Node 4)
  slow.next = None (cuts link after Node 3)
  First half:  1 -> 2 -> 3 -> None
  Second half: 4 -> 5 -> None

Phase 2: Reverse second half using 3 pointers (prev, curr, nxt)
  Reversed second half: 5 -> 4 -> None

Phase 3: Zipper merge first (1 -> 2 -> 3) and second (5 -> 4)
  Before rewiring, bookmark next nodes:
    tmp1 = first.next   (Node 2)
    tmp2 = second.next  (Node 4)
  Stitch:
    first.next = second (1 -> 5)
    second.next = tmp1  (5 -> 2)
  Advance:
    first = tmp1, second = tmp2
  Result after loop: 1 -> 5 -> 2 -> 4 -> 3 -> None
```

## Traps to watch for

- **Forgetting `slow.next = None`:** If you do not sever the tail of the first half from the start of the second half, Node 3 still points to Node 4 while Node 4 also points to Node 3, creating an infinite cycle.
- **Overwriting `.next` before bookmarking during the merge:** Writing `first.next = second` immediately loses the rest of the first half unless you saved `tmp1 = first.next` beforehand.
- **Wrong loop condition in Phase 3:** Because the second half is always equal to or 1 node shorter than the first half, `while second:` cleanly stops when all pairs are woven.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def reorderList(self, head: ListNode | None) -> None:
        if not head or not head.next:
            return

        # Phase 1: Find end of first half and split
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        second = slow.next
        slow.next = None

        # Phase 2: Reverse the second half in-place
        prev = None
        curr = second
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        second = prev

        # Phase 3: Interleave first and second halves
        first = head
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first, second = tmp1, tmp2
```

</details>

## Complexity

- **Time:** $\mathcal{O}(n)$ across three linear passes ($\mathcal{O}(n/2)$ each).
- **Space:** $\mathcal{O}(1)$ auxiliary memory since all pointers are rewired in-place.
