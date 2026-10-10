# 🔢 LeetCode 2: Add Two Numbers – DSA Pattern & Solution Guide

> **Pattern:** Linked List Traversal with Carry State  
> **Difficulty:** Medium  
> **Source Reference:** [NeetCode - Add Two Numbers (LeetCode 2)](https://www.youtube.com/watch?v=wgFPrzTjm7s)

---

## 📌 Problem Description
You are given two **non-empty** linked lists representing two non-negative integers. The digits are stored in **reverse order**, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

```text
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
```

---

## 💡 Key Intuitions & Why Reverse Order Helps

### Elementary School Addition
When adding multi-digit numbers by hand, you always start from the **least significant digit (ones place)** and move towards the left, carrying over any value $\\ge 10$:

```text
    1  (carry)
    3  4  2
  + 4  6  5
  ---------
    8  0  7
```

Because the linked lists are **already reversed**, the head node of each list is the **ones place**:
- $L_1$: `2 -> 4 -> 3` (corresponds to $342$)
- $L_2$: `5 -> 6 -> 4` (corresponds to $465$)

We can traverse from `l1` and `l2` head directly without needing to reverse the lists first!

---

## 🔍 Visual Step-by-Step Walkthrough

### Example 1: Standard Addition (`[2,4,3] + [5,6,4]`)
1. **Ones place:** `2 + 5 + 0 = 7` $\\implies$ Digit `7`, Carry `0`. Create node `[7]`
2. **Tens place:** `4 + 6 + 0 = 10` $\\implies$ Digit `0`, Carry `1`. Create node `[0]`
3. **Hundreds place:** `3 + 4 + 1 = 8` $\\implies$ Digit `8`, Carry `0`. Create node `[8]`
- **Result List:** `7 -> 0 -> 8` (Represents $807$)

---

### Example 2: Lists of Different Lengths (`[2,4,3] + [5,6,4,9]`)
- $L_1$: `2 -> 4 -> 3` ($342$)
- $L_2$: `5 -> 6 -> 4 -> 9` ($9465$)

When `l1` runs out of nodes, we treat its missing digits as `0`:
1. `2 + 5 + 0 = 7` $\\implies$ Digit `7`, Carry `0`
2. `4 + 6 + 0 = 10` $\\implies$ Digit `0`, Carry `1`
3. `3 + 4 + 1 = 8` $\\implies$ Digit `8`, Carry `0`
4. `0 (missing l1) + 9 + 0 = 9` $\\implies$ Digit `9`, Carry `0`
- **Result List:** `7 -> 0 -> 8 -> 9` ($9807$)

---

### Example 3: The Trailing Carry Edge Case (`[7] + [8]`)
- $L_1$: `7`
- $L_2$: `8`
- $7 + 8 = 15 \\implies$ Digit `5`, Carry `1`.
- Both `l1` and `l2` become `None` (exhausted).
- **Crucial check:** Since `carry = 1`, loop condition `while l1 or l2 or carry:` runs one last time, appending final node `[1]`!
- **Result List:** `5 -> 1` ($15$)

---

## ❓ Deep Dive: Why do we need `cur = dummy`? Isn't `dummy` alone enough?

### 🚂 The Train & The Stake Analogy

Imagine you are building a toy train on a track. 

Each train car has only **one hitch on its back** to connect to the next car (`.next`). There is **no reverse gear** and **no rear-view mirror**—you can only move forward.

#### The Two Roles:
1. 📌 **`dummy` (The Wooden Stake):** A heavy wooden stake hammered into the ground at the very beginning of the track. It **never moves**. Its only job is to remember where the train started.
2. 👷‍♂️ **`cur` (The Builder/Worker):** You, walking down the track with tools in your hand.

---

### Step-by-Step Visual Walkthrough:

#### Step 0: Setup
```python
dummy = ListNode()  # Hammer stake into the ground
cur = dummy         # Worker stands at the stake
```
```text
[ STAKE (dummy) ] 
       ▲
       │
   👷‍♂️ (cur stands here)
```

#### Step 1: Add digit 7
```python
cur.next = ListNode(7)  # Attach Car 7 to whatever you are touching
cur = cur.next          # Step forward onto Car 7
```
```text
[ STAKE (dummy) ] ────► [ CAR 7 ]
                            ▲
                            │
                        👷‍♂️ (cur walked here)
```
*Notice: `dummy` did NOT move. But `dummy.next` is now Car 7!*

#### Step 2: Add digit 0
```python
cur.next = ListNode(0)  # Attach Car 0 to Car 7
cur = cur.next          # Step forward onto Car 0
```
```text
[ STAKE (dummy) ] ────► [ CAR 7 ] ────► [ CAR 0 ]
                                            ▲
                                            │
                                        👷‍♂️ (cur walked here)
```

#### Step 3: Add digit 8
```python
cur.next = ListNode(8)  # Attach Car 8 to Car 0
cur = cur.next          # Step forward onto Car 8
```
```text
[ STAKE (dummy) ] ────► [ CAR 7 ] ────► [ CAR 0 ] ────► [ CAR 8 ]
                                                            ▲
                                                            │
                                                        👷‍♂️ (cur walked here)
```

#### 🏁 Returning the Result
When the function finishes:
- `cur` is standing way at the back on `[ CAR 8 ]`. If you returned `cur`, you would only return the tail!
- `dummy` is still sitting at the very front of the track!
- `dummy.next` points directly to the real first car `[ CAR 7 ]`!

```python
return dummy.next  # Returns 7 -> 0 -> 8
```

---

### 💥 What happens if you try to use `dummy` alone?

#### ❌ Flaw 1: If you advance `dummy`
```python
dummy = ListNode()
# In loop:
dummy.next = ListNode(7)
dummy = dummy.next  # You move the stake forward!
```
At the end, `dummy` is on Car 8. `dummy.next` is `None`. You lost the beginning of the list forever!

#### ❌ Flaw 2: If you DO NOT advance `dummy`
```python
dummy = ListNode()
# In loop:
dummy.next = ListNode(7)  # Stake -> 7
dummy.next = ListNode(0)  # Overwrite! Stake -> 0 (Car 7 is lost!)
dummy.next = ListNode(8)  # Overwrite! Stake -> 8 (Car 0 is lost!)
```
`dummy.next` will only point to the final single digit `[8]`.

---

## 💻 Complete Python 3 Solution

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        # 1. Create a dummy node as an anchor, and a moving pointer 'cur'
        dummy = ListNode()
        cur = dummy
        
        carry = 0
        
        # 2. Continue while any list has digits left OR there is a trailing carry
        while l1 or l2 or carry:
            # Extract digits (default to 0 if list is exhausted)
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            
            # 3. New digit and carry calculation
            val = v1 + v2 + carry
            carry = val // 10
            val = val % 10
            
            # 4. Insert new node at current position and advance cursor
            cur.next = ListNode(val)
            cur = cur.next
            
            # 5. Advance list pointers if available
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
            
        # 6. Return the head of the newly created list
        return dummy.next
```

---

## ⏱️ Complexity Analysis
- **Time Complexity:** $\\mathcal{O}(\\max(N, M))$
- **Space Complexity:** $\\mathcal{O}(\\max(N, M))$
