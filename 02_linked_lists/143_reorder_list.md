# 🔄 LeetCode 143: Reorder List – The "Triple Crown" Master Guide

> **Difficulty:** Medium (LinkedIn, Amazon, Microsoft Interview Favorite)  
> **Source Reference:** [NeetCode - Reorder List (LeetCode 143)](https://www.youtube.com/watch?v=S5bfdUTrKLM)  
> **Pattern:** 3-in-1 Combination (Fast/Slow Pointers + In-Place Reversal + Zipper Merge)

---

## 📌 Problem Description

You are given the head of a singly linked-list:
$$L_0 \to L_1 \to L_2 \to \dots \to L_{n-1} \to L_n$$

Reorder the list to be on the following form:
$$L_0 \to L_n \to L_1 \to L_{n-1} \to L_2 \to L_{n-2} \to \dots$$

> **Constraint:** You must do this **in-place** without modifying the node values (only changing the pointers/links).

```text
Example 1 (Even Length):
Input:  1 -> 2 -> 3 -> 4 -> None
Output: 1 -> 4 -> 2 -> 3 -> None

Example 2 (Odd Length):
Input:  1 -> 2 -> 3 -> 4 -> 5 -> None
Output: 1 -> 5 -> 2 -> 4 -> 3 -> None
```

---

## 💡 The "Aha!" Intuition: Why this is 3 Problems in One

If this were a regular array `[1, 2, 3, 4, 5]`, it would be trivial using two pointers from opposite ends:
- Take from front (`1`), take from back (`5`)
- Take from front (`2`), take from back (`4`)
- Take remaining (`3`)

**The Challenge with a Singly Linked List:**  
You **cannot go backwards** from the tail! You can only go forward (`.next`).

### How to overcome this in $\mathcal{O}(1)$ Extra Space?
We divide the problem into **3 simple phases** that you already know:

```text
Original List:  1 -> 2 -> 3 -> 4 -> 5 -> None

Phase 1 (Split in Half):
First Half:     1 -> 2 -> 3 -> None
Second Half:    4 -> 5 -> None

Phase 2 (Reverse Second Half):
First Half:     1 -> 2 -> 3 -> None
Reversed 2nd:   5 -> 4 -> None

Phase 3 (Zipper Merge / Interleave):
1 ────► 5 ────► 2 ────► 4 ────► 3 -> None
```

---

## 🔍 Phase-by-Phase Deep Dive & Pointer Diagrams

---

### 🟢 Phase 1: Find the Middle & Split the List

We use the **Fast & Slow Pointer** technique:
- `slow` moves 1 step at a time.
- `fast` moves 2 steps at a time.
- Start `fast` at `head.next` so `slow` lands on the exact end of the first half.

```text
Initial State:
[ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
  ▲           ▲
  │           │
 slow        fast

Step 1:
[ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
              ▲                       ▲
              │                       │
             slow                    fast

Step 2:
[ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
                          ▲                                   ▲
                          │                                   │
                         slow                                fast (hits end)
```

Now:
1. The **second half** starts at `slow.next` (Node 4).
2. ⚠️ **CRITICAL MOVE:** Cut the connection between the two halves by setting `slow.next = None`! If you forget this, your list will have a loop/cycle.

```python
slow, fast = head, head.next
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next

second = slow.next   # Head of second half (Node 4)
slow.next = None     # Disconnect! First half ends at Node 3
```

---

### 🟢 Phase 2: Reverse the Second Half

Now take the second half (`4 -> 5 -> None`) and reverse its arrows using the standard **3-pointer technique**:

```text
Before:  None       [ 4 ] ────► [ 5 ] ────► None
          ▲           ▲
          │           │
         prev        curr

Step 1:  None ◄──── [ 4 ]        [ 5 ] ────► None
                      ▲            ▲
                      │            │
                     prev         curr

Step 2:  None ◄──── [ 4 ] ◄──── [ 5 ]        None
                                   ▲            ▲
                                   │            │
                                  prev         curr (None)
```

At the end of the loop, `prev` is pointing to **Node 5**.
```python
prev = None
curr = second
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt

second = prev  # 'second' now points to 5 -> 4 -> None
```

---

### 🟢 Phase 3: The Zipper Merge (Interleave)

Now we have two distinct lists:
- `first`:  `1 -> 2 -> 3 -> None`
- `second`: `5 -> 4 -> None`

We want to stitch them together like teeth on a zipper: `1 -> 5 -> 2 -> 4 -> 3`.

#### ⚠️ The Bookmark Trap: Why we need `tmp1` and `tmp2`
If you do `first.next = second`, you immediately overwrite Node 1's arrow to Node 2! You would lose Node 2 and Node 3 forever!

So before modifying any pointers, **bookmark the next steps**:
```python
tmp1 = first.next   # Bookmark Node 2
tmp2 = second.next  # Bookmark Node 4

first.next = second # 1 points to 5
second.next = tmp1  # 5 points to 2

# Move pointers forward to our bookmarks:
first = tmp1        # Move to 2
second = tmp2       # Move to 4
```

```text
Visualizing the Stitch:

Step 1:
[ 1 ] ──────► [ 5 ]
                │
                ▼
              [ 2 ] ────► [ 3 ] ────► None
                │
              [ 4 ] ────► None

Step 2:
[ 1 ] ──► [ 5 ] ──► [ 2 ] ──► [ 4 ] ──► [ 3 ] ──► None
```

The `while second:` loop naturally terminates when `second` becomes `None`!

---

## 💻 Complete Python 3 Code

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next:
            return
        
        # ----------------------------------------------------
        # Phase 1: Find Middle (Fast & Slow Pointers)
        # ----------------------------------------------------
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
        second = slow.next  # Start of second half
        slow.next = None    # Cut list into two separate halves!
        
        # ----------------------------------------------------
        # Phase 2: Reverse Second Half (In-place 3 Pointers)
        # ----------------------------------------------------
        prev = None
        curr = second
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
            
        second = prev  # 'second' is now head of reversed second half
        
        # ----------------------------------------------------
        # Phase 3: Zipper Merge First & Second Halves
        # ----------------------------------------------------
        first = head
        while second:
            tmp1, tmp2 = first.next, second.next
            
            first.next = second
            second.next = tmp1
            
            first = tmp1
            second = tmp2
```

---

## ⏱️ Complexity Analysis

- **Time Complexity:** $\mathcal{O}(N)$
  - Phase 1 (Find middle): $\mathcal{O}(N/2)$
  - Phase 2 (Reverse second half): $\mathcal{O}(N/2)$
  - Phase 3 (Zipper merge): $\mathcal{O}(N/2)$
  - Total Time: $\mathcal{O}(N)$
- **Space Complexity:** $\mathcal{O}(1)$
  - All operations are done in-place by simply rewiring existing pointer connections. Zero extra nodes or arrays created!

---

## 🧠 Common Interview Traps & Pitfalls

1. **Cycle creation (Forgetting `slow.next = None`):**  
   If you don't cut the link between the two halves, the tail of the first half will still point to the old second half, creating an infinite cycle.
2. **Losing references during the Zipper Merge:**  
   Always bookmark `tmp1 = first.next` and `tmp2 = second.next` *before* changing `.next` pointers.
3. **Loop condition for Zipper:**  
   `while second:` is sufficient because the second half is either equal in length or 1 node shorter than the first half.
