# ✂️ LeetCode 83: Remove Duplicates from Sorted List – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** Top Interview 150 / LeetCode 75  
> **Pattern:** Linked List In-Place Pointer Skipping  
> **LeetCode Link:** [LeetCode 83: Remove Duplicates from Sorted List](https://leetcode.com/problems/remove-duplicates-from-sorted-list/)

---

## 📌 Problem in Plain English

Given the `head` of a **sorted** linked list, delete all duplicates such that each element appears only once. Return the linked list **sorted** as well.

### Example:
```text
Input:  head = [1, 1, 2, 3, 3]
Output: [1, 2, 3]
```

---

## 💡 The "Aha!" Moment: The Snip-and-Recheck Rule

Look at two adjacent nodes in the chain:

```text
cur
 │
 ▼
[ 1 ] ──► [ 1 ] ──► [ 2 ] ──► None
```

* If `cur.val == cur.next.val` (duplicate found!):
  * **Snip the duplicate:** Point `cur.next` to skip the neighbor: `cur.next = cur.next.next`.
  * **CRUCIAL RULE:** **DO NOT move `cur` yet!**  
    Why? Because the *new* neighbor might ALSO be a duplicate (e.g. `[1, 1, 1]`)!
* If `cur.val != cur.next.val` (different numbers):
  * Now it is safe to step forward: `cur = cur.next`.

---

## 🎬 Visual Trace on Consecutive Duplicates: `[1, 1, 1]`

#### 📍 Step 1: `cur` at first `1`
```text
cur
 │
 ▼
[ 1 ] ──► [ 1 ] ──► [ 1 ] ──► None
```
* `cur.val (1) == cur.next.val (1)` $\implies$ Duplicate!
* `cur.next = cur.next.next`
* **`cur` STAYS AT INDEX 0!**

#### 📍 Step 2: Re-check new neighbor!
```text
cur
 │
 ▼
[ 1 ] ─────────────► [ 1 ] ──► None
```
* Look! The new neighbor is ALSO `1`!
* `cur.val (1) == cur.next.val (1)` $\implies$ Duplicate!
* `cur.next = cur.next.next` (points to `None`)

#### 📍 Step 3: Loop terminates
```text
head
 │
 ▼
[ 1 ] ──► None
```
All duplicates are cleanly snipped out!

---

## ❓ The Critical Question: Why `return head` and NOT `return head.next`?

* In `mergeTwoLists`, you created a fake anchor: `dummy = ListNode(0)`. Returning `dummy.next` was necessary to throw away the fake `[0]`.
* In `deleteDuplicates`, **`head` is the REAL first node** of the input!  
  Even if there are duplicates (`1 -> 1`), you keep the first `1`!
* Returning `head.next` would accidentally chop off that first legitimate number.
* 👉 **Rule:** If `head` is a real starting node that belongs in the answer, write **`return head`**!

---

## 💻 The Clean Code

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def deleteDuplicates(self, head: ListNode | None) -> ListNode | None:
        cur = head
        
        while cur and cur.next:
            if cur.val == cur.next.val:
                cur.next = cur.next.next  # Snip duplicate! Do NOT advance cur.
            else:
                cur = cur.next            # Different values: safe to advance cur.
                
        return head                       # Keep original head!
```

---

## ⏱️ Complexity Blueprint

* **Time Complexity:** $\mathcal{O}(n)$ — each node is visited at most once.
* **Space Complexity:** $\mathcal{O}(1)$ — modified strictly in-place with zero extra memory.
