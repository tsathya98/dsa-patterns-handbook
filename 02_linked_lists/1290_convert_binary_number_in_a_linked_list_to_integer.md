# ⚡ LeetCode 1290: Convert Binary Number in a Linked List to Integer – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** Top Interview 150 / Linked Lists & Bit Manipulation  
> **Pattern:** Positional Stream Accumulation (Horner's Rule & Bit Shift)  
> **LeetCode Link:** [LeetCode 1290: Convert Binary Number in a Linked List to Integer](https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/)

---

## 📌 Problem in Plain English

Given `head` which is a reference node to a singly-linked list. The value of each node in the linked list is either `0` or `1`. The linked list holds the binary representation of a number.

Return the decimal value of the number in the linked list. The most significant bit is at the head of the linked list.

```text
Example 1:
Input:  head = [ 1 ] ──► [ 0 ] ──► [ 1 ] ──► None
Output: 5
Explanation: (101) in base-2 is (1 * 4) + (0 * 2) + (1 * 1) = 5.

Example 2:
Input:  head = [ 0 ] ──► None
Output: 0

Example 3:
Input:  head = [ 1, 1, 1, 1 ] ──► None
Output: 15
```

---

## ⚖️ Why String Concatenation is an Anti-Pattern

A common initial instinct:
```python
num = ""
while head:
    num += str(head.val)   # ⚠️ O(n^2) trap!
    head = head.next
binary = 0
for i in range(len(num)):
    binary += int(num[i]) * (2 ** (len(num) - 1 - i))
return binary
```

### Why interviewers ask you to optimize this:
1. **Python String Immutability ($\mathcal{O}(n^2)$ copying):**  
   Every time you execute `num += str(...)`, Python allocates a new string in RAM and copies all existing characters.
2. **Two Passes & Exponentiation:**  
   First pass builds the string; second pass calculates powers of 2 using `2 ** (power)`.
3. **Hardware Realities:**  
   In hardware and systems programming (e.g. Nvidia, embedded microcontrollers), data arrives as a **stream of bits** across a wire. You process bits on the fly in $\mathcal{O}(1)$ space!

---

## 🎒 The "Aha!" Mental Model: Base-10 vs Base-2 Streams

How do you read a standard base-10 number from a stream of incoming digits?

```text
Digits arrive:  '1'  ──►  '2'  ──►  '3'

Start:  ans = 0
See 1:  ans = (0 * 10) + 1  = 1
See 2:  ans = (1 * 10) + 2  = 12
See 3:  ans = (12 * 10) + 3 = 123
```
Each step **multiplies the current total by 10 and adds the new digit**!

---

### ⚡ The Exact Same Logic in Base-2 (Binary):
Instead of multiplying by 10, **multiply by 2**:

```text
Bits arrive:  [ 1 ]  ──►  [ 0 ]  ──►  [ 1 ]   (Binary 101)

Start:  ans = 0
See 1:  ans = (0 * 2) + 1 = 1
See 0:  ans = (1 * 2) + 0 = 2
See 1:  ans = (2 * 2) + 1 = 5  (Exact Answer!)
```

This is known as **Horner's Rule** for polynomial evaluation.

---

## 💻 Production Code Options

### Option A: Clean Arithmetic (Horner's Rule)
```python
class Solution:
    def getDecimalValue(self, head: ListNode | None) -> int:
        ans = 0
        while head:
            ans = ans * 2 + head.val  # Shift left by 1 place, add new bit
            head = head.next
        return ans
```

### Option B: Low-Level Bitwise (Hardware Shift Register - Nvidia Favorite)
Multiplying by 2 is equivalent to a **bit shift left (`<< 1`)**, and adding a single bit is a **bitwise OR (`|`)**:

```python
class Solution:
    def getDecimalValue(self, head: ListNode | None) -> int:
        ans = 0
        while head:
            ans = (ans << 1) | head.val
            head = head.next
        return ans
```

---

## 📊 Complexity Analysis

| Metric | String Concatenation | Horner's Rule / Bit Shift |
| :--- | :--- | :--- |
| **Time Complexity** | $\mathcal{O}(n^2)$ (string re-allocation) | **$\mathcal{O}(n)$ single pass** 🏆 |
| **Space Complexity** | $\mathcal{O}(n)$ (stores string) | **$\mathcal{O}(1)$ auxiliary space** 🏆 |
| **Passes** | 2 passes | **1 single pass** |
