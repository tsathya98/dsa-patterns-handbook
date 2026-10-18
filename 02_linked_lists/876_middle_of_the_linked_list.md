# LeetCode 876: Middle of the Linked List

> **Pattern:** Fast & slow pointers (Tortoise and Hare)  
> **Difficulty:** Easy  
> **Access:** Free  
> **Link:** [LeetCode 876](https://leetcode.com/problems/middle-of-the-linked-list/)

## The problem

Given the `head` of a singly linked list, return the middle node of the linked list.

If there are two middle nodes (even number of nodes), return the **second middle** node.

```text
Example 1 (Odd count):
Input:  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None
Output: Node 3

Example 2 (Even count):
Input:  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► [ 6 ] ──► None
Output: Node 4 (second middle)
```

## The core trick

Instead of counting length $n$ with one full pass and doing a second pass to node $n // 2$, use two pointers moving at different speeds:

* `slow` moves 1 step per turn: `slow = slow.next`.
* `fast` moves 2 steps per turn: `fast = fast.next.next`.

Because `fast` travels at exactly twice the speed of `slow` ($2x$), by the time `fast` reaches the end of the track, `slow` has covered exactly half the distance ($x$) and rests on the middle node.

### Algorithm steps:
* **1. Initialize pointers:** Start both `slow = head` and `fast = head`.
* **2. Advance runners:** While `fast` is not None and `fast.next` is not None:
  * Advance `slow = slow.next`.
  * Advance `fast = fast.next.next`.
* **3. Return:** When the loop exits, return `slow`.

## Step-by-step trace

```text
Odd count: [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None
Start:   slow = 1, fast = 1
Step 1:  slow = 2, fast = 3
Step 2:  slow = 3, fast = 5
Loop terminates because fast.next is None.
Returns slow (Node 3).

Even count: [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► [ 6 ] ──► None
Start:   slow = 1, fast = 1
Step 1:  slow = 2, fast = 3
Step 2:  slow = 3, fast = 5
Step 3:  slow = 4, fast = None
Loop terminates because fast is None.
Returns slow (Node 4, the second middle).
```

## Traps to watch for

* **Checking `while fast.next and fast:`**: In Python, evaluating `fast.next` when `fast` is `None` immediately throws `AttributeError: 'NoneType' object has no attribute 'next'`. Always check `fast` before `fast.next`: `while fast and fast.next:`.
* **First middle vs second middle:** If a problem requires the first middle for even lengths (like splitting a list before reversal in Palindrome or Reorder List), use `while fast.next and fast.next.next:`.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def middleNode(self, head: ListNode | None) -> ListNode | None:
        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow
```

</details>

## Complexity

* **Time:** $\mathcal{O}(n)$ single pass (fast visits $n$ nodes, loop runs $n/2$ times).
* **Space:** $\mathcal{O}(1)$ auxiliary memory (only two reference pointers).
