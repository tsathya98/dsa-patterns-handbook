# 🔄 LeetCode 1721: Swapping Nodes in a Linked List – Master Guide

> **Difficulty:** Medium  
> **Study Plan:** Top Interview 150 / Linked Lists  
> **Pattern:** Two Pointers (The Measuring Stick / Offset Technique)  
> **LeetCode Link:** [LeetCode 1721: Swapping Nodes in a Linked List](https://leetcode.com/problems/swapping-nodes-in-a-linked-list/)

---

## 📌 Problem in Plain English

You are given the `head` of a linked list, and an integer `k`.

Return the head of the linked list after **swapping the values** of the $k^{\text{th}}$ node from the beginning and the $k^{\text{th}}$ node from the end (the list is 1-indexed).

```text
Example 1:
Input:  head = [ 1, 2, 3, 4, 5 ], k = 2
Output: [ 1, 4, 3, 2, 5 ]
Explanation: The 2nd node from start is 2. The 2nd node from end is 4. Swapped!

Example 2:
Input:  head = [ 7, 9, 6, 6, 7, 8, 3, 0, 9, 5 ], k = 5
Output: [ 7, 9, 6, 6, 8, 7, 3, 0, 9, 5 ]

Example 3:
Input:  head = [ 100, 90 ], k = 2
Output: [ 90, 100 ]
```

---

## 🚨 The Sneaky Bug: Swapping Inside a Rebuild Loop

When storing values in a list and rebuilding the linked list:
```python
# ❌ TRAP: Swapping during reconstruction
for i in range(len(lst)):
    if i == k - 1:
        lst[k-1], lst[len(lst) - k] = lst[len(lst)-k], lst[k-1]
        cur.val = lst[i]
```
### Why did this pass 68 test cases and fail 64?
* **When $k$ is in the front half:** The loop visits index `k - 1` *before* the second node, so the swap happens early and both values are read correctly.
* **When $k$ is in the back half (e.g. `[100, 90], k = 2`):** The loop visits index `0` *before* index `1`. It reads the unswapped value `100`, then later swaps at index `1` and reads `100` again $\implies$ outputting `[100, 100]`!
* **The Rule:** Always complete your list manipulations **before** beginning node creation or assignment!

---

## 🎒 The "Aha!" Mental Model: The Measuring Stick 📏

How do you find the $k^{\text{th}}$ node from the **end** without knowing the list's total length and without allocating an array?

Use two pointers like a **fixed-length wooden ruler**:

```text
head = [ 1,  2,  3,  4,  5 ], k = 2

Step 1: Walk 'first' to the k-th node from start:
        [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ]
                   ▲
                 first (k-th from start)

Step 2: Place 'second' at head, and 'fast' at 'first':
        second    fast
          │        │
          ▼        ▼
        [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None

Step 3: Slide both together until 'fast' hits the last node!
                             second    fast
                               │        │
                               ▼        ▼
        [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None
                               ▲
                      k-th node from END!
```

Because the gap between `fast` and `second` is fixed at $k$ nodes:
When `fast` hits the final node (`fast.next is None`), **`second` is guaranteed to be standing on the $k^{\text{th}}$ node from the end!**

---

## 🖐️ The "Fencepost" Step Rule: Why `range(k - 1)`?

Remember: `first` **already starts on Node 1** (`head`).
* To reach Node 1 ($k = 1$): You need **0 steps** $\implies$ `range(0)`.
* To reach Node 2 ($k = 2$): You need **1 step** $\implies$ `range(1)`.
* To reach Node $k$: You need **$k - 1$ steps** $\implies$ `range(k - 1)`.

> [!WARNING]
> Using `range(k)` takes 1 step too many! On $k = 1$, it lands on Node 2. On $k = 5$ on a 5-node list, it walks into `None` and crashes with `AttributeError`!

---

## 💻 Complete Production Code ($\mathcal{O}(1)$ Space)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def swapNodes(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        first = head
        second = head

        # 1. Walk first to the k-th node from the beginning (k - 1 steps)
        for _ in range(k - 1):
            first = first.next

        # 2. Put fast at first, and slide second from head
        fast = first
        while fast.next:
            fast = fast.next
            second = second.next

        # 3. Swap their values directly in-place!
        first.val, second.val = second.val, first.val

        return head
```

---

## 📊 Complexity Analysis

| Metric | Approach 1 (Store Node References) | Approach 2 (Measuring Stick) |
| :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ single pass |
| **Space Complexity** | $\mathcal{O}(n)$ (array of node pointers) | **$\mathcal{O}(1)$ (Zero extra memory!)** 🏆 |
| **Passes** | 1 pass to store, 1 pass to read | 1 single synchronized pass |

---

## 🎯 Related Benchmark Problems
This exact **Measuring Stick / Offset Technique** solves:
1. **LC 19: Remove Nth Node From End of List** (Deletes the target node using dummy head).
2. **LC 876: Middle of the Linked List** (Ratio variation where fast moves 2x).
3. **LC 141: Linked List Cycle Detection** (Detecting closed loops).
