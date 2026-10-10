# 🪢 LeetCode 21: Merge Two Sorted Lists – The "No-Jargon" Guide

> **Target Audience:** Complete beginner / 1st-year CS student  
> **Difficulty:** Easy  
> **LeetCode Link:** [LeetCode 21: Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

---

## 💡 The Big Picture: What Are We Actually Doing?

Imagine two lines of students waiting to enter a cafeteria, both already standing in order of height:

```text
Line 1: [ 1 ] ──► [ 2 ] ──► [ 4 ] ──► None
Line 2: [ 1 ] ──► [ 3 ] ──► [ 4 ] ──► None
```

Your job is to **zipper them together into ONE single line**, from shortest to tallest:

```text
Merged: [ 1 ] ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 4 ] ──► None
```

> **The Golden Rule:**  
> You do **NOT** create new students (no `ListNode(val)` calls).  
> You simply untie the ropes (`.next`) and re-tie them in sorted order!

---

## 🧠 The "Aha!" Moment: Why Do We Need `dummy` AND `cur`?

This is where almost every beginner gets stuck. Let's break it down with a physical analogy.

### 🧥 Analogy: The Coat Rack and Your Hand

Imagine you are hanging coats on a wall:

1. **`dummy` is the Coat Rack on the wall:**
   * It is bolted to the wall. **It NEVER moves.**
   * Why do you need it? Because at the very start, you don't know whose coat is first! The coat rack holds the whole chain so it doesn't fall onto the floor.

2. **`cur` is YOUR HAND:**
   * Your hand grabs the shortest coat and hooks it on.
   * Then your hand **steps forward** to the bottom of that coat, ready to attach the next one!

---

## 🎬 Step-by-Step Visual Comic: Watching `dummy` and `cur` in Action

Let's merge `list1 = [1, 4]` and `list2 = [2, 3]`:

---

### 📍 START: Place the Coat Rack (`dummy`) and put your hand on it (`cur`)

```text
dummy
  │
  ▼
[ 0 ] ──► None
  ▲
 cur (Your hand starts on dummy)
```

---

### 📍 ROUND 1: Compare `list1` (1) vs `list2` (2)
* Who is smaller? `1` is smaller!
* **Action 1:** `cur.next = list1`  *(Your hand hooks [1] onto the rack)*
* **Action 2:** `list1 = list1.next` *(Line 1 advances to [4])*
* **Action 3:** `cur = cur.next` *(Your hand moves to [1])*

```text
dummy
  │
  ▼
[ 0 ] ──────► [ 1 ] ──► None
                ▲
               cur (Your hand is now here!)

Line 1 is now at: [ 4 ]
Line 2 is now at: [ 2 ] ──► [ 3 ]
```

---

### 📍 ROUND 2: Compare `list1` (4) vs `list2` (2)
* Who is smaller? `2` is smaller!
* **Action 1:** `cur.next = list2`  *(Hook [2] onto [1])*
* **Action 2:** `list2 = list2.next` *(Line 2 advances to [3])*
* **Action 3:** `cur = cur.next` *(Your hand moves to [2])*

```text
dummy
  │
  ▼
[ 0 ] ──────► [ 1 ] ──────► [ 2 ] ──► None
                              ▲
                             cur (Hand moves to the tail!)

Line 1 is now at: [ 4 ]
Line 2 is now at: [ 3 ]
```

---

### 📍 ROUND 3: Compare `list1` (4) vs `list2` (3)
* Who is smaller? `3` is smaller!
* **Action 1:** `cur.next = list2`  *(Hook [3] onto [2])*
* **Action 2:** `list2 = list2.next` *(Line 2 is now empty: `None`!)*
* **Action 3:** `cur = cur.next` *(Your hand moves to [3])*

```text
dummy
  │
  ▼
[ 0 ] ──────► [ 1 ] ──────► [ 2 ] ──────► [ 3 ] ──► None
                                            ▲
                                           cur (Hand at the tail)

Line 1 is now at: [ 4 ]
Line 2 is now:    EMPTY (None)
```

---

### 📍 FINISH: One line is empty! Attach the rest in 1 step!
The `while` loop stops because `list2` ran out of people.  
Who is left? Node `[ 4 ]` in `list1`!

* **Action:** `cur.next = list1`  *(Hook the rest of Line 1 directly onto [3])*

```text
dummy
  │
  ▼
[ 0 ] ──────► [ 1 ] ──────► [ 2 ] ──────► [ 3 ] ──────► [ 4 ] ──► None
  ▲             ▲
dummy       dummy.next
(Fake hook)  (REAL START OF YOUR CHAIN!)
```

---

## ❓ The Million Dollar Question: Why `return dummy.next`?

Look at the drawing above one more time:

* If you return `dummy`, you are handing the teacher the **coat rack `[ 0 ]`**!  
  Your answer will be: `[0, 1, 2, 3, 4]`. ❌ *(WRONG! Where did that 0 come from?)*
* If you return `dummy.next`, you skip the coat rack and hand the teacher the **first real student `[ 1 ]`**!  
  Your answer will be: `[1, 2, 3, 4]`. ✅ *(PERFECT!)*

---

## 💻 The Clean Code (Every Line Explained)

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
        # 1. The coat rack (dummy) and your hand (cur)
        dummy = ListNode()
        cur = dummy
        
        # 2. While BOTH lines have students waiting:
        while list1 and list2:
            if list1.val <= list2.val:
                cur.next = list1       # Stitch student from Line 1
                list1 = list1.next     # Advance Line 1
            else:
                cur.next = list2       # Stitch student from Line 2
                list2 = list2.next     # Advance Line 2
                
            cur = cur.next             # Move your hand to the new end of the line!
            
        # 3. One line ran out! Stitch whoever is left over in ONE move:
        if list1:
            cur.next = list1
        else:
            cur.next = list2
            
        # 4. Skip the fake coat rack and return the first real student!
        return dummy.next
```

---

## ⚠️ The 3 Traps That Confuse Beginners

| Trap | What Happens | The Simple Fix |
| :--- | :--- | :--- |
| **`cur.next = list1.val`** | `.val` is just a number (like `4`), but `.next` expects a whole Node box! Next time you do `cur.next`, it crashes. | **Write `cur.next = list1`** (grab the whole student, not their badge number). |
| **`while list1 or list2:`** | If one list finishes early, trying to check `list1.val` on an empty list crashes with `AttributeError`. | **Write `while list1 and list2:`** (only compare when both lines are alive). |
| **`return dummy`** | Adds a random `0` at the very front of your merged answer. | **Write `return dummy.next`** (skips the fake hook). |

---

## ⏱️ How Fast Is This?

* **Time:** $\mathcal{O}(n + m)$ — You only look at each student once. Lightning fast!
* **Space:** $\mathcal{O}(1)$ — You didn't buy any new boxes; you just reconnected the existing arrows.
