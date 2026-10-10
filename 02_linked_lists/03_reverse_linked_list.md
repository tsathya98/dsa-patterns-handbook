# 🔄 LeetCode 206: Reverse Linked List – Master Guide

> **Pattern:** In-Place Pointer Flipping (3-Pointer Technique)  
> **Difficulty:** Easy (Must-Know Foundation)

---

## 📌 Problem Description
Given the `head` of a singly linked list, reverse the list, and return the reversed list.

```text
Input:  1 -> 2 -> 3 -> 4 -> 5 -> None
Output: 5 -> 4 -> 3 -> 2 -> 1 -> None
```

---

## 💡 The Core Intuition: The 3-Pointer Technique

To flip an arrow `A -> B` into `A <- B`, you need 3 variables:
1. `prev`: The node behind us (where our arrow should point to). Initially `None`.
2. `curr`: The node we are currently standing on. Initially `head`.
3. `nxt` (or `temp`): A temporary bookmark to remember where the rest of the list is *before* we break the forward arrow!

---

## 🔍 Step-by-Step Frame-by-Frame Walkthrough

Let's reverse `1 -> 2 -> 3 -> None`:

### Initial State:
```text
None       [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► None
 ▲           ▲
 │           │
prev        curr
```

---

### Iteration 1 (at Node 1):
1. **Save next node:** `nxt = curr.next` (Bookmark Node 2)
2. **Reverse arrow:** `curr.next = prev` (Node 1 now points to `None`)
3. **Advance prev:** `prev = curr` (`prev` steps onto Node 1)
4. **Advance curr:** `curr = nxt` (`curr` steps onto Node 2)

```text
None ◄──── [ 1 ]        [ 2 ] ────► [ 3 ] ────► None
             ▲            ▲
             │            │
            prev         curr
```

---

### Iteration 2 (at Node 2):
1. `nxt = curr.next` (Bookmark Node 3)
2. `curr.next = prev` (Node 2 now points back to Node 1)
3. `prev = curr` (`prev` steps onto Node 2)
4. `curr = nxt` (`curr` steps onto Node 3)

```text
None ◄──── [ 1 ] ◄──── [ 2 ]        [ 3 ] ────► None
                         ▲            ▲
                         │            │
                        prev         curr
```

---

### Iteration 3 (at Node 3):
1. `nxt = curr.next` (Bookmark `None`)
2. `curr.next = prev` (Node 3 now points back to Node 2)
3. `prev = curr` (`prev` steps onto Node 3)
4. `curr = nxt` (`curr` steps onto `None`)

```text
None ◄──── [ 1 ] ◄──── [ 2 ] ◄──── [ 3 ]        None
                                     ▲            ▲
                                     │            │
                                    prev         curr
```

### 🏁 Loop Terminates (`curr == None`):
Look where `prev` is standing: it is on **Node 3** (the new head of the reversed list)!

```python
return prev  # Returns 3 -> 2 -> 1 -> None
```

---

## 💻 Python 3 Implementation

```python
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        curr = head
        
        while curr:
            nxt = curr.next   # 1. Bookmark the next node
            curr.next = prev  # 2. Reverse the pointer
            prev = curr       # 3. Step prev forward
            curr = nxt        # 4. Step curr forward
            
        return prev  # prev is the new head!
```

- **Time Complexity:** $\\mathcal{O}(N)$
- **Space Complexity:** $\\mathcal{O}(1)$ in-place.
