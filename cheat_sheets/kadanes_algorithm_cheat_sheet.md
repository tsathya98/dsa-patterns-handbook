# 📈 Kadane's Algorithm Master Cheat Sheet & Decision Guide

> **Pattern:** Dynamic Programming / Greedy Prefix Reset (Kadane's Algorithm)  
> **Target Audience:** Complete Beginner / 1st-Year CS Student  
> **The Big Idea:** Contiguous subarray optimization in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.  
> **Core Analogy:** Declaring bankruptcy on "Toxic Debt".

---

## 💡 1. What Problem Does It Solve?

> **The Problem:** Given an array of numbers containing both positive and negative values, find the **contiguous subarray** (an unbroken slice) that yields the **largest possible sum**.
> 
> * **LeetCode 53: Maximum Subarray**  
> * Example: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` $\implies$ Max sum is **6** (from subarray `[4, -1, 2, 1]`).

* **Brute Force:** Checking all pairs `(i, j)` and calculating their sums takes **$\mathcal{O}(n^2)$** time.
* **Kadane's Algorithm:** Solves it in a **single pass** in **$\mathcal{O}(n)$ time** and **$\mathcal{O}(1)$ space**.

---

## 💸 2. The Core Intuition: The "Toxic Debt" Analogy

Imagine you are walking down a street collecting cash bags (positive numbers) and bills/debt (negative numbers):
* **Positive numbers (`+$`):** Valuable assets. Keep them!
* **Negative numbers (`-$`):** Debts/losses. They hurt your total.

As you walk, you track your running wallet balance (`current_sum`):
* If your past streak has a **positive balance** (e.g., `+5`), it can help boost future numbers. Keep carrying it forward!
* But if your past streak drops **below 0** (e.g., `-3`), it has become **toxic debt**:
  * If you carry a debt of `-3` into a new number `+4`, your total becomes $4 - 3 = 1$.
  * If you had simply **thrown away the past debt**, you would have **$4$**!

> 💡 **The Golden Rule of Kadane:**  
> **"Never carry negative debt forward. The moment your running sum drops below 0, declare bankruptcy, discard the past, and start a fresh streak right here!"**

---

## 🎯 3. When to Use Kadane? (The 3-Second Mental Radar)

Look for these **3 unmistakable clues** in the problem prompt:

```text
Clue 1: "Contiguous Subarray"  (Elements must be unbroken neighbors)
            +
Clue 2: Array has NEGATIVE numbers (Penalties / Losses)
            +
Clue 3: Asking for "Maximum Sum", "Maximum Score", or "Best Profit"
            │
            ▼
   🚨 100% KADANE'S ALGORITHM! 🚨
```

> 💡 **The Dead Giveaway:**  
> If an array had **only positive numbers**, the maximum subarray would trivially be the **entire array**!  
> The only reason this problem exists is because **negative numbers act as penalties**.

---

## ❓ 4. Why Kadane? (Why Other Patterns Fail Here)

| Pattern | Why It Doesn't Work Here |
|---|---|
| **Two Pointers (The Squeeze)** | Requires a **sorted array** so pointers know whether moving `left` or `right` increases or decreases the sum. But here, the array is unsorted and sorting it scrambles the contiguous order! |
| **Sliding Window** | Sliding window shrinks `left` **one element at a time** (`left += 1`). But in Kadane, once a sum is negative, you don't shrink by 1 — **you instantly dump the entire past window!** |
| **Prefix Sums** | Works, but requires building an auxiliary array and tracking minimums. Kadane accomplishes the same thing on the fly with **$\mathcal{O}(1)$ memory**. |

---

## 🎛️ 5. The 1-Line Question Kadane Asks at Every Element

At every single number, you make an easy choice:
> *"Should I **add this number to my past streak**, OR **ditch the past and start a brand new streak** with just this number?"*

$$\text{current\_sum} = \max(\text{num}, \text{current\_sum} + \text{num})$$
$$\text{max\_sum} = \max(\text{max\_sum}, \text{current\_sum})$$

---

## 🔍 6. Step-by-Step Frame Trace (Visual Proof)

Array: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| Step | Num | Past Streak + Num | Or Start Fresh (Num)? | `current_sum` | `max_so_far` | Action Taken |
|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| 0 | `-2` | — | `-2` | **`-2`** | **`-2`** | Start at first element |
| 1 | `1` | $-2 + 1 = -1$ | `1` | **`1`** | **`1`** | Ditched `-2` debt! Started fresh with `1` |
| 2 | `-3` | $1 + (-3) = -2$ | `-3` | **`-2`** | **`1`** | Running sum dipped negative |
| 3 | `4` | $-2 + 4 = 2$ | `4` | **`4`** | **`4`** | Ditched `-2` debt! Started fresh with `4` |
| 4 | `-1` | $4 + (-1) = 3$ | `-1` | **`3`** | **`4`** | Kept streak (still positive) |
| 5 | `2` | $3 + 2 = 5$ | `2` | **`5`** | **`5`** | New record high! 🎉 |
| 6 | `1` | $5 + 1 = 6$ | `1` | **`6`** | **`6`** | New record high! 🏆 |
| 7 | `-5` | $6 + (-5) = 1$ | `-5` | **`1`** | **`6`** | Kept streak (still positive) |
| 8 | `4` | $1 + 4 = 5$ | `4` | **`5`** | **`6`** | Finished! Max answer is **6** |

---

## 💻 7. The Standard Clean Python 3 Code

```python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        current_sum = nums[0]
        max_sum = nums[0]
        
        for num in nums[1:]:
            # Choice: Extend previous streak, or start fresh from 'num'
            current_sum = max(num, current_sum + num)
            # Update the best answer seen so far
            max_sum = max(max_sum, current_sum)
            
        return max_sum
```

---

## ⚠️ 8. The Classic Interview Trap: All Negative Numbers

What if the input is all negative numbers, like `nums = [-5, -2, -8]`?
* The correct answer is **`-2`** (the single least-negative number).
* **❌ The Common Bug:** Initializing `max_sum = 0`.  
  If you do that, your code will return `0`, which is **wrong** because `0` is not even in the array!
* **✅ The Fix:** Always initialize both `current_sum` and `max_sum` to `nums[0]` (or `float('-inf')`).

---

## 🗂️ 9. The 4 Problem Archetypes That Use Kadane

| Archetype | Problem | Kadane Application |
|---|---|---|
| **1. Classic Max Subarray** | LC 53: Maximum Subarray | Pure standard template. |
| **2. Daily Differences / Stock Profit** | LC 121: Best Time to Buy & Sell Stock | Convert prices to daily differences (`prices[i] - prices[i-1]`), then run Kadane! |
| **3. Circular Subarray** | LC 918: Maximum Sum Circular Subarray | `max(Kadane(Max Subarray), Total_Sum - Kadane(Min Subarray))`. |
| **4. Maximum Product Subarray** | LC 152: Maximum Product Subarray | Track both `max_prod` and `min_prod` because negative $\times$ negative = positive. |

---

## 🧠 10. The Golden Rule to Remember Forever
> **"When looking for an optimal contiguous subarray among negative penalties: never carry debt. Accumulate positive gains, and drop the past the second your streak falls below zero."**
