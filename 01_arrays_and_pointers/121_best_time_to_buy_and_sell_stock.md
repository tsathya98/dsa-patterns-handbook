# LeetCode 121: Best Time to Buy and Sell Stock

> **Difficulty:** Easy | **Pattern:** Running Minimum Tracking / 1D Greedy
> **Source Code:** [`121_best_time_to_buy_and_sell_stock.py`](./121_best_time_to_buy_and_sell_stock.py)

## The problem

Given an array `prices` where `prices[i]` is the price of a stock on day $i$, maximize your profit by choosing a single day to buy one stock and a later day to sell that stock. Return `0` if no profit is possible.

## Why the naive way fails

Checking every `(buy_day, sell_day)` pair with $0 \le i < j < n$ takes $\mathcal{O}(n^2)$ time, which times out for $n = 10^5$.

## The core trick

You want the largest gap `prices[j] - prices[i]` with $j > i$. As you scan left to right, maintain two numbers:
1. `min_price`: the lowest stock price seen so far.
2. `max_profit`: the best profit achievable by selling today against `min_price`.

```text
Prices:  [ 7,   1,   5,   3,   6,   4 ]
           ▲    ▲              ▲
           │    │              └─ Best sell (profit = 6 - 1 = 5)
           │    └─ New historical low (min_price = 1)
           └─ Initial low (min_price = 7)
```

If you convert `prices` into daily price changes `diff[i] = prices[i] - prices[i - 1]`, finding the maximum single-transaction profit is equivalent to Kadane's Maximum Subarray (LeetCode 53) on `diff`.

## Step-by-step trace

Input: `prices = [7, 1, 5, 3, 6, 4]`

| Day $i$ | `price` | `min_price` | `price - min_price` | `max_profit` |
|---|---|---|---|---|
| 0 | 7 | 7 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 |
| 2 | 5 | 1 | 4 | 4 |
| 3 | 3 | 1 | 2 | 4 |
| 4 | 6 | 1 | 5 | 5 |
| 5 | 4 | 1 | 3 | 5 |

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_price = float("inf")
        max_profit = 0

        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price

        return max_profit
```

</details>

## Traps to watch for

* **Strictly decreasing prices:** For `[7, 6, 4, 3, 1]`, you make zero transactions and return `0`. Initializing `max_profit = 0` handles this directly without risking a negative return value.
* **`if / elif` vs `min()` / `max()`:** If today's price sets a new `min_price`, selling on the same day yields `0` profit, so the `elif` branch safely skips the profit check and avoids Python `min()`/`max()` call overhead.

## Complexity

* **Time:** $\mathcal{O}(n)$ for a single pass over `prices`.
* **Space:** $\mathcal{O}(1)$ using two scalar variables.
