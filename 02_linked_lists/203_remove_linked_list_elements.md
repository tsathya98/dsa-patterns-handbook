# LeetCode 203: Remove Linked List Elements

> **Pattern:** Sentinel dummy + pointer bypass  
> **Difficulty:** Easy  
> **Access:** Free  
> **Link:** [LeetCode 203](https://leetcode.com/problems/remove-linked-list-elements/)

## The problem

Given the `head` of a linked list and an integer `val`, remove all the nodes of the linked list that have `Node.val == val`, and return the new head.

```text
Input:  head = [ 1, 2, 6, 3, 4, 5, 6 ], val = 6
Output: [ 1, 2, 3, 4, 5 ]

Input:  head = [ 7, 7, 7, 7 ], val = 7
Output: []
```

## The core trick

Deleting nodes from a singly linked list requires holding a pointer to the **preceding node** (`cur`), because a node cannot delete itself: you must rewire `cur.next = cur.next.next`.

If the node to be deleted is the `head` itself (e.g. `[ 7, 7, 7, 7 ]` where `val = 7`), there is no predecessor node. Creating a sentinel node `dummy = ListNode(0, head)` guarantees that **every real node always has a predecessor**.

### Algorithm steps:
* **1. Sentinel setup:** Create `dummy = ListNode(0, head)`, initialize `cur = dummy`.
* **2. Inspect next node:** While `cur.next` is not None:
  * If `cur.next.val == val`: bypass it by updating `cur.next = cur.next.next` (**do not advance cur**, because the newly connected node might also equal `val`).
  * Else: advance `cur = cur.next`.
* **3. Return:** Return `dummy.next`.

## Step-by-step trace

```text
Target val = 6:
[ dummy ] ──► [ 1 ] ──► [ 6 ] ──► [ 6 ] ──► [ 3 ] ──► None

1. cur at dummy: cur.next.val is 1 != 6. Advance cur to [1].
2. cur at [1]:   cur.next.val is 6 == 6.
   Bypass: cur.next = cur.next.next (now points to second [6]).
   Do NOT advance cur!
3. cur still at [1]: cur.next.val is 6 == 6.
   Bypass: cur.next = cur.next.next (now points to [3]).
   Do NOT advance cur!
4. cur still at [1]: cur.next.val is 3 != 6. Advance cur to [3].
5. cur at [3]: cur.next is None. Loop exits.
Return dummy.next -> [1] -> [3] -> None.
```

## Traps to watch for

* **Advancing `cur` on deletion:** If you write `cur = cur.next` after `cur.next = cur.next.next`, you skip consecutive matching values (e.g. `[6, 6]` only deletes the first 6). Only advance `cur` in the `else` branch.
* **Deleting head nodes without a dummy:** Requires a while loop at the top to advance `head`, plus handling empty lists. Sentinel dummy eliminates all special cases.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def removeElements(self, head: ListNode | None, val: int) -> ListNode | None:
        dummy = ListNode(0, head)
        cur = dummy

        while cur.next:
            if cur.next.val == val:
                cur.next = cur.next.next
            else:
                cur = cur.next

        return dummy.next
```

</details>

## Complexity

* **Time:** $\mathcal{O}(n)$ single pass visiting each node once.
* **Space:** $\mathcal{O}(1)$ auxiliary memory (only 1 sentinel node and 1 pointer).
