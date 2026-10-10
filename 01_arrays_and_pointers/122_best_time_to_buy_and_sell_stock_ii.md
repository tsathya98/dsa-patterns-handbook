# 📈 LeetCode 122: Best Time to Buy and Sell Stock II – Master Guide

> **Difficulty:** Medium  
> **Study Plan:** Top Interview 150 / NeetCode 150 / Blind 75  
> **Pattern:** Greedy (Valley-to-Peak / Daily Step Accumulation)  
> **LeetCode Link:** [LeetCode 122: Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)

---

## 📌 Problem in Plain English

You are given an integer array `prices` where `prices[i]` is the stock price on the $i$-th day.

On each day, you may decide to buy and/or sell the stock. You can only hold **at most one** share of the stock at any time. However, you can buy it and then immediately sell it on the same day.

Find and return **the maximum profit** you can achieve with **unlimited transactions**.

```text
Example 1:
Input: prices = [7, 1, 5, 3, 6, 4]
Output: 7
Explanation: 
- Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5 - 1 = 4.
- Buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6 - 3 = 3.
Total profit is 4 + 3 = 7.

Example 2:
Input: prices = [1, 2, 3, 4, 5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5 - 1 = 4.

Example 3:
Input: prices = [7, 6, 4, 3, 1]
Output: 0
Explanation: Prices strictly drop. We make zero transactions -> profit = 0.
```

---

## 💡 The "Aha!" Moment: Stock I vs. Stock II

* **Stock I (LC 121):** You can only buy **once** and sell **once**. You must search for the single global minimum followed by the maximum profit.
* **Stock II (LC 122):** You have **unlimited transactions**. You can jump in and out of the market as many times as you like!

> ⚠️ **Is this Kadane's Algorithm?**  
> **No!** Kadane finds a *single contiguous subarray*. In Stock II, you can take multiple disconnected gains and skip all drops. It is **pure Greedy**.

---

## 🔍 Two Ways to Think About the Solution

### Approach 1: The "Valley-to-Peak" Method (Your Intuition)
You wait for a local minimum (a "valley" `x`), buy there, hold while prices rise, and cash out the moment prices drop (or when you reach the end).

```python
class SolutionValleyToPeak:
    def maxProfit(self, prices: list[int]) -> int:
        prof = 0
        x = 0
        temp_prof = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i - 1]:
                temp_prof = prices[i] - prices[x]
                if i == len(prices) - 1:
                    prof += temp_prof
            else:
                prof += temp_prof
                temp_prof = 0
                x = i
        return prof
```
* **Why this works:** It correctly identifies every local bottom and top.
* **The drawback:** Requires managing state variables (`x`, `temp_prof`) and an extra check for the end of the array (`if i == len(prices) - 1`).

---

### Approach 2: The "Telescoping Sum" Math Trick (The 3-Line Upgrade)

Look at what happens when prices rise continuously: `[1, 2, 5]`
* Buying at `1` and selling at `5` gives:
  $$5 - 1 = \mathbf{4}$$
* Notice that collecting every single daily increase gives the exact same answer:
  $$(2 - 1) + (5 - 2) = 1 + 3 = \mathbf{4}$$

In general, across any multi-day upward slope $A \le B \le C$:
$$(C - A) = (B - A) + (C - B)$$

Because intermediate days cancel out, **you don't need to remember where the valley started (`x`), and you don't need temporary profit (`temp_prof`)!**

Whenever tomorrow's price is higher than today's, **just pocket the difference immediately**:

```text
Prices:       [ 7 ,    1 ,    5 ,    3 ,    6 ,    4 ]
Daily Steps:     Drop   +4    Drop   +3    Drop

Total Profit = 4 + 3 = 7
```

---

## 💻 Clean Python 3 Solution

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        profit = 0
        
        for i in range(1, len(prices)):
            # If today's price is higher than yesterday's, take the profit!
            if prices[i] > prices[i - 1]:
                profit += prices[i] - prices[i - 1]
                
        return profit
```

---

## ⏱️ Complexity Analysis

* **Time Complexity:** $\mathcal{O}(n)$ — Single linear pass over the array of length $n$.
* **Space Complexity:** $\mathcal{O}(1)$ — Only one accumulator variable (`profit`).

---

## 🏢 Interview Perspective (Google / Meta)

1. **Why interviewers like this problem:** It tests whether a candidate can recognize that a seemingly complex "buying schedule" optimization collapses into a dead-simple greedy check.
2. **Can you really buy and sell on the same day?**  
   Yes! The problem allows buying and selling on the same day. Even if an interviewer says "you can't buy and sell on the exact same day", buying at $1$ and selling at $5$ yields identical profit to the daily increments, so the formula is mathematically equivalent.
