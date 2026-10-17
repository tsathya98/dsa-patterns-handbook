# LeetCode 19: Remove Nth Node From End of List

> **Pattern:** Two pointers with fixed offset + dummy node  
> **Difficulty:** Medium  
> **Link:** [LeetCode 19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

## The problem

Given the `head` of a linked list, remove the $n$-th node from the end of the list and return its head.

```text
Input:  head = [1, 2, 3, 4, 5], n = 2
Output: [1, 2, 3, 5] (Node 4 is removed)
```

## The core trick

Counting the length of the list in one pass and walking to `length - n` in a second pass works, but you can do it in a single pass using two pointers separated by a fixed gap.

Think of `left` and `right` as the two ends of a rigid ruler of length $n$:
1. Attach a `dummy` node before `head`. Start `left` at `dummy` and `right` at `head`.
2. Advance `right` forward by $n$ steps. Now `left` and `right` have $n$ nodes between them.
3. Slide both `left` and `right` forward one step at a time until `right` walks off the end into `None`.
4. Because the gap stayed fixed, `left` is now sitting right before the target node. Bypass it with `left.next = left.next.next`.

Starting `left` on `dummy` handles the edge case where $n$ equals the length of the list (deleting the original `head`). When `right` hits `None`, `left` is still on `dummy`, so `left.next = left.next.next` cleanly unhooks the first node.

## Step-by-step trace

Trace on `head = [1, 2, 3, 4, 5]`, `n = 2`:

```text
1. Setup (left on dummy, right on head):
   [dummy] ────► [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
      ▲            ▲
     left        right

2. Advance right by n = 2 steps:
   [dummy] ────► [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
      ▲                                    ▲
     left                                right

3. Move both together until right is None:
   [dummy] ────► [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
                                           ▲                                   ▲
                                          left                               right

4. Snip target node (left.next = left.next.next):
   Node 3 skips Node 4 and points straight to Node 5.
```

## Traps to watch for

- **Skipping the dummy node:** Without `dummy`, deleting the head of a 1-node list (`head = [1], n = 1`) requires special `if` branches because there is no previous node to rewire.
- **Stopping at `while right.next:` when `left` starts at `dummy`:** Since `left` starts one step behind `head`, `right` must walk all the way to `None` (`while right:`) for `left` to land on the node before the target.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        dummy = ListNode(0, head)
        left = dummy
        right = head

        for _ in range(n):
            right = right.next

        while right:
            left = left.next
            right = right.next

        left.next = left.next.next
        return dummy.next
```

</details>

## Complexity

- **Time:** $\mathcal{O}(n)$ single pass.
- **Space:** $\mathcal{O}(1)$ auxiliary memory.
