# 🔄 LeetCode 206: Reverse Linked List – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** LeetCode 75 / Top Interview 150 / NeetCode 150  
> **Pattern:** Linked List In-Place Arrow Reversal (The Conga Line 4-Beat Dance)  
> **LeetCode Link:** [LeetCode 206: Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)

---

## 📌 Problem in Plain English

Given the `head` of a singly linked list, reverse the list, and return the reversed list's head.

```text
Input:  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None
Output: [ 5 ] ──► [ 4 ] ──► [ 3 ] ──► [ 2 ] ──► [ 1 ] ──► None
```

---

## 🎒 The "Aha!" Mental Model: The Preschool Conga Line

Imagine 3 children walking in a line holding onto each other's backpacks:
* Alice (1) holds Bob (2)'s backpack.
* Bob (2) holds Charlie (3)'s backpack.
* Charlie (3) holds nothing (`None` / empty air).

```text
               (holds)                   (holds)
  [ Alice ] ─────────────► [ Bob ] ─────────────► [ Charlie ] ──► None
```

**Teacher's Command:**  
> *"Turn around! Charlie at the front, Alice at the back!"*

### ⚠️ The Disaster Trap:
If Bob turns around and lets go of Charlie without someone holding Charlie:  
**Charlie will walk away and get lost forever!** (The rest of the list is lost in memory).

---

## 🛡️ The 3 Roles & The 4-Beat Dance

1. **`prev` (Person Behind You):** Starts at `None` (empty air behind Alice).
2. **`cur` (Person Currently Turning Around):** Starts at `head` (Alice).
3. **`nxt` (Teacher's Spotter Hand):** Holds the child in front so they don't run off before `cur` turns around!

```text
ROUND 1 (Alice turns around):
  prev     cur         nxt
   │        │           │
   ▼        ▼           ▼
  None   [ Alice ] ──► [ Bob ] ──► [ Charlie ] ──► None

Beat 1: nxt = cur.next    -> Teacher holds Bob!
Beat 2: cur.next = prev   -> Alice lets go of Bob and grabs None (behind her).
Beat 3: prev = cur        -> Alice is now the person "behind" for next round.
Beat 4: cur = nxt         -> Next child's turn to turn around (cur moves to Bob).

None ◄── [ Alice ]   [ Bob ] ──► [ Charlie ] ──► None
           ▲           ▲
          prev        cur
```

Repeat this exact 4-beat rhythm for every single child!

---

## ❓ The Big Questions Answered

### 1. "Why `while cur:` and NOT `while cur and cur.next:`?"
* If you write `while cur and cur.next:`, the moment `cur` reaches Charlie (the last child), `cur.next` is `None`!
* The loop stops early! **Charlie never turns around!**
* Using `while cur:` ensures **every child** turns around, and the loop stops only when `cur` steps off the end into `None`.

### 2. "Why `return prev`? Why can't we return `cur` or `cur.next`?"
* **Why NOT `return cur`?**  
  The loop terminates precisely when `cur` becomes **`None`**! Returning `cur` returns an empty list `[]`!
* **Why NOT `return cur.next`?**  
  Since `cur` is `None`, calling `cur.next` crashes with:  
  `AttributeError: 'NoneType' object has no attribute 'next'` 💥
* **Why `return prev`?**  
  Look at where `prev` is standing when `cur` steps into `None`:  
  **`prev` is standing right on Charlie (Node 3)** — the **new front of the line**!

```text
                                        prev            cur
                                         │               │
                                         ▼               ▼
None ◄── [ Alice ] ◄── [ Bob ] ◄── [ Charlie ]        [ None ]
                                         ▲
                                 THIS IS YOUR NEW HEAD!
```

---

## 💻 The Clean Code (Every Line Explained)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        prev = None
        cur = head
        
        while cur:
            nxt = cur.next     # Beat 1 (Spotter): Hold child in front
            cur.next = prev    # Beat 2 (Turn Around): Grab person behind
            prev = cur         # Beat 3 (Slide Prev): You are now the person behind
            cur = nxt          # Beat 4 (Slide Cur): Next child's turn
            
        return prev            # prev is standing on the new front node!
```

---

## ⏱️ Complexity Blueprint

* **Time Complexity:** $\mathcal{O}(n)$ — exactly one pass through the $n$ nodes.
* **Space Complexity:** $\mathcal{O}(1)$ — modified strictly in-place; zero new memory allocated.
