# ✂️ LeetCode 19: Remove Nth Node From End of List

> **Pattern:** Two Pointers with Fixed Gap (Measuring Stick) + Dummy Node  
> **Difficulty:** Medium

---

## 📌 Problem Description
Given the `head` of a linked list, remove the $n$-th node from the end of the list and return its head.

```text
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5] (Node 4 removed)
```

---

## 💡 The Measuring Stick Technique

How do you find the $N$-th node from the end in **one single pass** without counting the total length first?

### The Ruler Analogy:
Hold a ruler of length $N$.
1. Place the `right` pointer $N$ steps ahead of `left`.
2. Move both `left` and `right` at the **same speed** until `right` hits the end (`None`).
3. Now `left` is pointing **directly before the node to be deleted**!

---

## 🔍 Why the Dummy Node is Lifesaving Here
What if $N$ equals the list length (i.e. deleting the head node `[1]`)?
By starting `left` at `dummy` (which sits at index $-1$ before the head), `left` will naturally stop right before the head, allowing `left.next = left.next.next` to safely delete the head!

```text
Example: [1, 2, 3, 4, 5], n = 2

1. Initialize dummy and pointers:
   [dummy] ────► [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
      ▲            ▲
      │            │
    left         right

2. Advance right by n + 1 steps (3 steps):
   [dummy] ────► [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
      ▲                                    ▲
      │                                    │
    left                                 right (3 steps ahead)

3. Move both pointers together until right is None:
   [dummy] ────► [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
                                           ▲                                    ▲
                                           │                                    │
                                         left                                 right

4. Delete Node 4:
   left.next = left.next.next  (Node 3 skips Node 4 and connects directly to Node 5!)
```

---

## 💻 Python 3 Implementation

```python
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        dummy = ListNode(0, head)
        left = dummy
        right = head
        
        # Advance right pointer n steps
        for _ in range(n):
            right = right.next
            
        # Move both until right reaches None
        while right:
            left = left.next
            right = right.next
            
        # Delete the nth node
        left.next = left.next.next
        
        return dummy.next
```

- **Time Complexity:** $\\mathcal{O}(N)$ single pass
- **Space Complexity:** $\\mathcal{O}(1)$
