# LeetCode 83: Remove Duplicates from Sorted List

> **Pattern:** In-place pointer skipping  
> **Difficulty:** Easy  
> **Link:** [LeetCode 83](https://leetcode.com/problems/remove-duplicates-from-sorted-list/)

## The problem

Given the `head` of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.

```text
Input:  head = [1, 1, 2, 3, 3]
Output: [1, 2, 3]
```

## The core trick

Because the list is already sorted, any duplicates sit right next to each other. You do not need a hash set to track seen values.

Walk a single pointer `cur` from `head` and compare `cur.val` with `cur.next.val`:
- **Values match (`cur.val == cur.next.val`):** Snip out the neighbor by setting `cur.next = cur.next.next`. Stay on `cur` without advancing it yet, because the new `cur.next` might also have the same value (like `[1, 1, 1]`).
- **Values differ (`cur.val != cur.next.val`):** Now it is safe to step forward with `cur = cur.next`.

Do you need a `dummy` node here? No. Even if the head value is duplicated (`[1, 1, 2]`), we always keep the first copy of `head` and delete the duplicates after it. Because `head` is never deleted, you can simply return `head` at the end.

### Algorithm steps:
* **1. Initialize walker:** Set `cur = head`.
* **2. Compare adjacent nodes:** While `cur` is not None and `cur.next` is not None:
  * If `cur.val == cur.next.val`: snip the duplicate neighbor with `cur.next = cur.next.next` (keep `cur` in place to test subsequent duplicates).
  * Else: distinct values confirmed, advance `cur = cur.next`.
* **3. Terminate traversal:** Loop finishes when `cur` or `cur.next` reaches None.
* **4. Return head:** Return original `head`.

## Step-by-step trace

Trace on consecutive duplicates `head = [1, 1, 1]`:

```text
Step 1: cur starts at first 1
  cur
   │
   ▼
  [ 1 ] ──► [ 1 ] ──► [ 1 ] ──► None
  cur.val (1) == cur.next.val (1) -> snip: cur.next = cur.next.next
  Keep cur on the first node.

Step 2: Recheck from the same cur against the new neighbor
  cur
   │
   ▼
  [ 1 ] ────────────► [ 1 ] ──► None
  cur.val (1) == cur.next.val (1) -> snip: cur.next = cur.next.next (None)

Step 3: cur.next is now None, so while cur and cur.next ends
  [ 1 ] ──► None
```

## Traps to watch for

- **Advancing `cur` on the same turn you snip a node:** If you run `cur = cur.next` inside the `if` branch instead of an `else` branch, `[1, 1, 1]` leaves a duplicate `[1, 1]` behind because you skipped checking the middle `1` against the third `1`.
- **Looping on `while cur:` instead of `while cur and cur.next:`:** Inside the loop we check `cur.next.val`. If `cur` is on the final node, `cur.next` is `None`, and `.val` raises an `AttributeError`.
- **Returning `head.next` out of habit:** You only return `.next` when you created a fake `dummy` node. Here `head` is the real first element.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def deleteDuplicates(self, head: ListNode | None) -> ListNode | None:
        cur = head

        while cur and cur.next:
            if cur.val == cur.next.val:
                cur.next = cur.next.next
            else:
                cur = cur.next

        return head
```

</details>

## Complexity

- **Time:** $\mathcal{O}(n)$ since each node is either visited or bypassed once.
- **Space:** $\mathcal{O}(1)$ in-place pointer updates.
