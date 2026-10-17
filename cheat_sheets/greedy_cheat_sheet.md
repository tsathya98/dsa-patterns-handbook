# Greedy Algorithms Cheat Sheet

A greedy algorithm builds a solution step by step by locking in the best immediate choice at each step, without backtracking.

## 1. Greedy vs. Two Pointers
People mix these up constantly:
- **Two Pointers** is a **pointer mechanic** (`left`/`right` or `slow`/`fast`).
- **Greedy** is the **decision rule** that tells you which pointer to move or which item to pick.
- Example ([LC 11: Container With Most Water](../01_arrays_and_pointers/11_container_with_most_water.md)): Two Pointers puts `l` at `0` and `r` at `n-1`. The greedy rule says the shorter wall bottlenecks the water height, so moving the taller wall can never help; therefore, always move the shorter wall inward.

---

## 2. The 4 Greedy Archetypes

### Archetype 1: The Cashier / ATM ([LC 12: Integer to Roman](../01_arrays_and_pointers/12_integer_to_roman.md))
Repeatedly peel off the largest denomination that fits into the remaining target.
- **Works when:** Denominations are canonical (like US coins or Roman numerals).
- **Fails when:** Denominations are arbitrary (like coins `[1, 3, 4]` for target `6`, where greedy picks `4+1+1` instead of `3+3`; use DP there).

### Archetype 2: The Horizon / Max Reach ([LC 55: Jump Game](../01_arrays_and_pointers/55_jump_game.md), LC 45)
You don't care which exact path of jumps you took; you only care about the **furthest index reachable so far** (`max_reach`).
```python
max_reach = 0
for i, jump in enumerate(nums):
    if i > max_reach:
        return False  # Stranded past the horizon
    max_reach = max(max_reach, i + jump)
return True
```

### Archetype 3: Interval Scheduler (LC 435: Non-Overlapping Intervals, LC 452)
To pack the maximum number of non-overlapping meetings into a room, sort intervals by **end time** (`key=lambda x: x[1]`) and always pick the meeting that finishes earliest. Finishing early leaves the most room for future meetings.

### Archetype 4: Micro-Gain Accumulator ([LC 122: Best Time to Buy and Sell Stock II](../01_arrays_and_pointers/122_best_time_to_buy_and_sell_stock_ii.md))
When unlimited trades are allowed, harvesting every upward daily step (`prices[i] - prices[i-1] > 0`) adds up to the exact same profit as buying the bottom and selling the peak ($5 - 1 = (3 - 1) + (5 - 3)$).

---

## 3. Summary Table

| Archetype | Variable Tracked | Rule | Classic Problems |
| :--- | :--- | :--- | :--- |
| Cashier / ATM | `remaining` | Subtract largest unit that fits | LC 12 |
| Horizon | `max_reach` | `max_reach = max(max_reach, i + nums[i])` | LC 55, LC 45 |
| Scheduler | `prev_end` | Sort by end time; pick earliest finish | LC 435, LC 452 |
| Accumulator | `profit` | Add every positive delta `nums[i] - nums[i-1]` | LC 122, LC 134 |
