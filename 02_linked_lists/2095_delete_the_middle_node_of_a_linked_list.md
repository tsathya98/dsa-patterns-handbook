# LeetCode 2095: Delete the Middle Node of a Linked List

> **Pattern:** Fast & Slow Pointers (Midpoint Predecessor)  
> **Difficulty:** Medium  
> **Link:** [LeetCode 2095](https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/)

## The problem

You are given the `head` of a linked list. Delete the middle node, and return the `head` of the modified linked list.

The middle node of a linked list of size $n$ is the $\lfloor n / 2 \rfloor$-th node from the start (0-indexed).
* For $n = 1$: node 0 is deleted (result: empty list `[]`).
* For $n = 4$: node 2 is deleted (the second middle node for even lengths).
* For $n = 7$: node 3 is deleted.

```text
Input:  head = [1, 3, 4, 7, 1, 2, 6] (n = 7, middle index = 3 -> node 7)
Output: [1, 3, 4, 1, 2, 6]

Input:  head = [1, 2, 3, 4] (n = 4, middle index = 2 -> node 3)
Output: [1, 2, 4]

Input:  head = [1] (n = 1, middle index = 0 -> node 1)
Output: []
```

---

## The core trick

To delete any node in a singly linked list, you cannot stand on the node itself; you must stand on its **predecessor** so you can bypass it with:
```python
predecessor.next = predecessor.next.next
```

In standard Tortoise & Hare (LeetCode 876), `slow` lands directly on the middle node. There are two clean ways to get a handle on the predecessor:

### Approach 1: Track `prev` during traversal (Your approach)
* Check the edge case first: if the list has only 1 node (`not head.next`), deleting the middle leaves an empty list (`return None`).
* Maintain `prev = None` before advancing `slow = slow.next`.
* When the loop ends, `slow` is on the middle node and `prev` is right behind it.
* Snip: `prev.next = slow.next`.

### Approach 2: Dummy sentinel head offset
* Attach `dummy = ListNode(0, head)`.
* Start `slow = dummy` and `fast = head`.
* Because `slow` starts exactly 1 step behind `head`, when `fast` finishes, `slow` naturally stops on the node **before** the middle.
* This automatically handles the 1-node list without any separate `if` check (`slow` is `dummy`, `dummy.next = dummy.next.next` becomes `None`).

---

## Step-by-step trace

Trace on `head = [1, 2, 3, 4]` (even length):

```text
Initial state:
  slow
  fast
   │
   ▼
  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► None

Step 1:
  prev = [ 1 ]
  slow moves to [ 2 ]
  fast moves to [ 3 ]

Step 2:
  prev = [ 2 ]
  slow moves to [ 3 ]  (middle node to delete)
  fast moves to None   (fast.next was None on [4])

Loop ends because fast is None.
Snip: prev.next = prev.next.next (links [2] directly to [4])
Result: [1] ──► [2] ──► [4] ──► None
```

---

## Solutions

### Approach 1: Previous pointer tracker

<details>
<summary>Spoiler: Solution Code (Track Prev)</summary>

```python
class Solution:
    def deleteMiddle(self, head: ListNode | None) -> ListNode | None:
        if not head or not head.next:
            return None

        prev = None
        slow = head
        fast = head

        while fast and fast.next:
            prev = slow
            slow = slow.next
            fast = fast.next.next

        prev.next = slow.next
        return head
```

</details>

### Approach 2: Sentinel dummy node offset

<details>
<summary>Spoiler: Solution Code (Sentinel Dummy)</summary>

```python
class Solution:
    def deleteMiddle(self, head: ListNode | None) -> ListNode | None:
        dummy = ListNode(0, head)
        slow = dummy
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        slow.next = slow.next.next
        return dummy.next
```

</details>

---

## Traps to watch for

* **Single-node list (`head = [1]`):** If you don't handle this edge case (or use a dummy node), `prev` remains `None` and `prev.next` throws `AttributeError: 'NoneType' object has no attribute 'next'`.
* **Even-length definition:** The problem specifies $\lfloor n / 2 \rfloor$ (0-indexed). For $n = 4$, middle is index 2 (`nums[2]`), which matches standard `fast.next.next` progression.

## Complexity

* **Time Complexity:** $\mathcal{O}(n)$ (single pass; fast pointer traverses the list once).
* **Space Complexity:** $\mathcal{O}(1)$ (in-place pointer updates).
