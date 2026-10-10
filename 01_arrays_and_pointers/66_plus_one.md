# 🚗 LeetCode 66: Plus One – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** Top Interview 150 / Arrays & Math  
> **Pattern:** Schoolbook Addition & The Car Odometer Pattern  
> **LeetCode Link:** [LeetCode 66: Plus One](https://leetcode.com/problems/plus-one/)

---

## 📌 Problem in Plain English

You are given a **large integer** represented as an integer array `digits`, where each `digits[i]` is the $i^{\text{th}}$ digit of the number. The digits are ordered from most significant to least significant (left-to-right). 

Increment the large integer by one and return the resulting array of digits.

```text
Example 1:
Input:  digits = [ 1, 2, 3 ]
Output: [ 1, 2, 4 ]   (123 + 1 = 124)

Example 2:
Input:  digits = [ 1, 2, 9 ]
Output: [ 1, 3, 0 ]   (129 + 1 = 130)

Example 3:
Input:  digits = [ 9, 9, 9 ]
Output: [ 1, 0, 0, 0 ] (999 + 1 = 1000)
```

---

## ⚖️ Why Interviewers Reject `int("".join(...)) + 1`

Your first instinct was likely this:
```python
return [int(x) for x in str(int("".join(map(str, digits))) + 1)]
```
### Why is this rejected in interviews if it works?
1. **Integer Overflow in Statically Typed Languages:**  
   In C++, Java, or Go, a 64-bit integer (`long long`) caps out at $\approx 9 \times 10^{18}$ ($\approx 19$ digits). If `digits` contains 100 numbers, `int(...)` crashes with a buffer/arithmetic overflow.
2. **Memory Overhead:**  
   Converting to strings creates multiple intermediate string and list objects in RAM ($\mathcal{O}(n)$ extra space).
3. **The Core Interview Goal:**  
   The interviewer is testing if you understand **Schoolbook Carry Addition** directly on an array without relying on built-in language parsers.

---

## 🎒 The "Aha!" Mental Model: The Car Odometer 🚗

Think of an analog car odometer or a suitcase combination lock rolling forward by 1:

```text
Case 1: Normal number [ 1, 2, 3 ]
  You just bump 3 -> 4!
  Result: [ 1, 2, 4 ]  ──► (STOP immediately!)

Case 2: Ending in 9 [ 1, 2, 9 ]
  The 9 rolls over to 0!
  Carry moves left to 2: bumps 2 -> 3!
  Result: [ 1, 3, 0 ]  ──► (STOP immediately!)

Case 3: All 9s [ 9, 9, 9 ]
  The 9 rolls over to 0!
  The 9 rolls over to 0!
  The 9 rolls over to 0!
  Loop finishes! You are left with [ 0, 0, 0 ]!
  What's missing? Just slap a '1' at the very front:
  Result: [ 1, 0, 0, 0 ]
```

---

## 💻 Complete Production Code

```python
class Solution:
    def plusOne(self, digits: list[int]) -> list[int]:
        # Walk from right to left (least significant digit to most significant)
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits  # 🛑 Done! Early exit, no further carry!
            
            # If the digit was 9, it rolls over to 0
            digits[i] = 0

        # If the loop finished without returning, ALL digits were 9!
        # (e.g. [9, 9, 9] rolled over to [0, 0, 0])
        # Simply prepend a 1 at the front:
        return [1] + digits
```

---

## ⚡ 2 Micro-Optimizations to Notice

1. **`if digits[i] < 9` instead of `if digits[i] + 1 != 10`:**  
   Cleaner, reads like plain English, and avoids extra addition.
2. **`return [1] + digits` instead of `digits.insert(0, 1)`:**  
   In Python, `list.insert(0, ...)` is an **$\mathcal{O}(n)$** operation that shifts every single element in memory to the right. Writing `[1] + digits` creates the new list in one swift allocation and is much cleaner to read.

---

## 📊 Complexity Analysis

* **Time Complexity:** 
  * **Best Case:** $\mathcal{O}(1)$ — If the last digit is not `9` (e.g. `[1, 2, 3]`), it increments and returns on the very first step!
  * **Worst Case:** $\mathcal{O}(n)$ — If all digits are `9` (e.g. `[9, 9, 9]`), it visits all $n$ digits and prepends `1`.
* **Space Complexity:** 
  * $\mathcal{O}(1)$ in-place auxiliary memory (modifies `digits` in-place).
  * $\mathcal{O}(n)$ only in the worst-case scenario when creating `[1] + digits`.
