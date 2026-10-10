# 🪢 LeetCode 21: Merge Two Sorted Lists – Master Guide

> **Pattern:** Dummy Node + Zipper Merge Technique  
> **Difficulty:** Easy (Classic Interview Problem)

---

## 📌 Problem Description
You are given the heads of two sorted linked lists `list1` and `list2`.
Merge the two lists into one **sorted** list by splicing together the nodes of the first two lists.
Return the head of the merged linked list.

```text
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
```

---

## 💡 The Zipper Analogy
Think of two rows of people arranged by height.
You stand at the front with a new rope (`dummy`).
You look at the person at the front of Row 1 and Row 2. Whoever is shorter gets called next, grabbed onto your rope (`curr.next`), and you take a step forward (`curr = curr.next`).

---

## 🔍 Visual Step-by-Step Walkthrough

```text
list1: [ 1 ] -> [ 2 ] -> [ 4 ]
list2: [ 1 ] -> [ 3 ] -> [ 4 ]

1. Setup:
   [dummy] 
      ▲
      │
     curr

2. Compare list1.val (1) and list2.val (1):
   Pick list1's 1. 
   curr.next = list1
   curr = curr.next
   list1 = list1.next
   
   [dummy] -> [ 1 (l1) ]
                 ▲
                 │
                curr

3. Compare list1.val (2) and list2.val (1):
   Pick list2's 1.
   curr.next = list2
   curr = curr.next
   list2 = list2.next

   [dummy] -> [ 1 ] -> [ 1 (l2) ]
                          ▲
                          │
                         curr

4. Repeat until one list is exhausted!
5. Attach the remaining tail:
   If list1 is left: curr.next = list1
   If list2 is left: curr.next = list2
```

---

## 💻 Python 3 Implementation

```python
class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        dummy = ListNode()
        curr = dummy
        
        while list1 and list2:
            if list1.val <= list2.val:
                curr.next = list1
                list1 = list1.next
            else:
                curr.next = list2
                list2 = list2.next
            curr = curr.next
            
        # Attach whichever list still has nodes remaining
        curr.next = list1 if list1 else list2
        
        return dummy.next
```

- **Time Complexity:** $\\mathcal{O}(N + M)$
- **Space Complexity:** $\\mathcal{O}(1)$ (reuses existing nodes!)
