# 📈 LeetCode 121: Best Time to Buy and Sell Stock

> **Difficulty:** Easy | **Top Interview 150:** Arrays / Strings  
> **Pattern:** Running Minimum Tracking / 1D Greedy State Machine  
> **Complexity:** Time: $\mathcal{O}(n)$ | Space: $\mathcal{O}(1)$  
> **Source Code:** [`121_best_time_to_buy_and_sell_stock.py`](./121_best_time_to_buy_and_sell_stock.py)

---

## 🎯 Is This Problem FAANG-Worthy?

### Verdict: **YES — But as a Warm-Up Filter & Stepping Stone**
Do not underestimate LC 121 because it's labeled "Easy". At **Meta, Google, Amazon, and Bloomberg**, LC 121 serves 3 distinct interview roles:
1. **The 5-Minute Warm-Up / Smoke Screen:** In a 45-minute technical screen, interviewers often throw LC 121 in the first 7 minutes. They are checking:
   * Do you immediately recognize $\mathcal{O}(n^2)$ brute-force vs. $\mathcal{O}(n)$ single pass?
   * Can you write bug-free code in under 3 minutes without stuttering?
   * Do you properly handle the case where prices strictly decrease (can you lose money, or is minimum profit $0$?).
2. **The "Gateway" Problem for Part 2 / 3:**
   * If you nail LC 121 in 5 minutes, they immediately pivot to:
     * **LC 122 (Stock II):** Unlimited transactions (Greedy daily step collection).
     * **LC 123 / 188 (Stock III & IV):** At most 2 or $k$ transactions (2D State Machine DP).
     * **LC 309 / 714 (Stock with Cooldown or Transaction Fee):** Finite state machine DP.
3. **Equivalence to Kadane's Algorithm:**
   * If you transform the prices array into daily differences `diff[i] = prices[i] - prices[i-1]`, finding the maximum profit is **literally Kadane's Maximum Subarray Problem (LC 53)**. Interviewers love asking candidates if they see the equivalence!

---

## 🧠 Mental Model: The "Past Valley & Future Peak"

Imagine you are traveling through time with a suitcase of cash.
At each day `i`, you have two questions:
1. *"Is today the cheapest day I've seen in all of history so far?"*  
   $\rightarrow$ If yes, update `min_price = price`.
2. *"If I bought at the historical record low and sold today, how much profit would I make?"*  
   $\rightarrow$ If `price - min_price > max_profit`, update `max_profit`.

```text
Prices:  [ 7,   1,   5,   3,   6,   4 ]
          ▲     ▲         ▲
          │     │         └─ Sell here (profit = 6 - 1 = 5)
          │     └─ New historical valley (min_price = 1)
          └─ Initial valley (min_price = 7)
```

---

## 🔬 Code Analysis: Comparing Approaches

### Your Submitted Code
```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_prof = float(-inf)
        min_price = float(inf)
        for price in prices:
            min_price = min(min_price, price)
            max_prof = max(max_prof, price - min_price)
        return max_prof
```

### Critical Analysis & Subtle Nuances:

1. **Initial Value of `max_prof`:**
   * In your code, you initialized `max_prof = float(-inf)`.
   * **Why LeetCode accepted it:** For `[7, 6, 4, 3, 1]`, on day 1 `min_price = 7`, so `price - min_price = 7 - 7 = 0`. Thus `max_prof` was bumped to `0`.
   * **Interview Note:** If you cannot make any profit, you simply do not transact, returning `0`. It is much cleaner and avoids edge case misunderstandings to initialize `max_profit = 0` directly.
2. **`min()` / `max()` Function Overhead vs. `if/elif`:**
   * Built-in `min()` and `max()` in Python incur Python function call overhead and tuple unpacking for each loop iteration.
   * Using direct `if price < min_price:` and `elif price - min_price > max_profit:` is significantly faster (~35ms vs ~55ms) and demonstrates hardware-conscious branching intuition.

---

## 💡 Production Solution

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price
                
        return max_profit
```

* **Time Complexity:** $\mathcal{O}(n)$ — Single pass through `prices`.
* **Space Complexity:** $\mathcal{O}(1)$ — Only two scalar trackers (`min_price`, `max_profit`).
