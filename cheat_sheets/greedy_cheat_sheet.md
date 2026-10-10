# 🦅 The Master Guide to Greedy Algorithms: Intuition, Archetypes & The Two-Pointers Distinction

> **Target Audience:** Intuitive, pattern-first problem solvers.  
> **Rule #1:** Zero Dynamic Programming jargon. No abstract math proofs.  
> **Rule #2:** If you can understand making change at a cash register, you understand Greedy.

---

## 🧭 1. What is "Greedy" in Plain English?

Imagine you are at an all-you-can-eat buffet with a 10-minute timer.
* You don't sit down with a notebook mapping out all 50 possible dish combinations.
* You walk up to each station and ask one selfish question: **"What is the single best, tastiest item right in front of me right now?"**
* You put it on your plate, move forward, and **never put anything back**.

> ### 🧠 The Definition:
> A **Greedy Algorithm** builds an optimal solution step-by-step by **always making the choice that looks best at that exact moment**, without ever second-guessing or backtracking.

---

## ⚖️ 2. The Big Confusion: Greedy vs. Two Pointers

Candidates constantly confuse these two in interviews. Here is the clear distinction:

| Dimension | 🎯 Two Pointers | 🦅 Greedy |
|---|---|---|
| **What is it?** | A **Mechanical Technique** (Data Structure pointer traversal). | A **Strategic Philosophy** (How you make decisions). |
| **Pointers on Screen** | Always explicit pointers: `left`, `right`, or `slow`, `fast`. | Can be pointers, a single `for` loop variable, or sorting + priority queue. |
| **Core Question** | *"Which end of the array should I squeeze or advance next?"* | *"What is the best immediate choice right here, and can I lock it in forever?"* |
| **Overlap Alert!** | Many Two-Pointer problems use **Greedy Decision Rules**! (e.g., Container With Most Water). | Two Pointers is just *one way* to implement a greedy choice! |

### The Container With Most Water (LC 11) Example:
* **Two Pointers:** `left = 0`, `right = len(height) - 1`.
* **Greedy Decision:** *"The container's height is bottlenecked by the shorter wall. Moving the taller wall can NEVER increase water volume. Therefore, I greedily advance the shorter wall inward."*
* 👉 **Two Pointers is the car; Greedy is the driver deciding which turn to make.**

---

## 🗂️ 3. The 4 Universal Archetypes of Greedy Problems

Almost 95% of all Greedy interview problems fall into one of these 4 practical buckets:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   THE 4 GREEDY ARCHETYPES                               │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ 1. The Cashier     │ 2. The Horizon     │ 3. The Interval Scheduler    │
│    (Atm / Change)  │    (Laser Reach)   │    (Meeting Rooms)           │
├────────────────────┴────────────────────┴──────────────────────────────┤
│ 4. The Accumulator (Telescoping / Micro-Gains)                         │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Archetype 1: The Cashier / ATM Pattern (Largest Unit First)
* **The Real-Life Analogy:** A customer asks for \$87 in change. You don't give them 87 one-dollar bills. You greedily grab the biggest bill possible: one \$50, one \$20, one \$10, one \$5, and two \$1s.
* **The Rule:** Decompose descending from largest denomination to smallest.
* **Classic Problems:**
  * **LC 12: Integer to Roman** (Greedily subtract 1000, 900, 500, etc.)
  * **Coin Change (Canonical Coins)**

---

### Archetype 2: The Horizon / Laser Reach Pattern (Expand the Boundary)
* **The Real-Life Analogy:** You are hiking across stepping stones in the dark with a flashlight. As you step onto each stone, you sweep your beam forward. You don't care *which* exact step you took; you only care: **"What is the furthest stone illuminated so far?"**
* **The Rule:** Track a single scalar `max_reach`. If you ever reach a stone where `i > max_reach`, you ran out of light and are stranded.
* **Classic Problems:**
  * **LC 55: Jump Game** (`max_reach = max(max_reach, i + nums[i])`)
  * **LC 45: Jump Game II** (Count how many times your horizon must expand to reach the end)
  * **LC 1024: Video Stitching**

---

### Archetype 3: The Interval Scheduler / Activity Chooser (Earliest Finish Time)
* **The Real-Life Analogy:** A conference room can only host one meeting at a time. To fit the maximum number of meetings in one day, which meeting do you pick first?  
  * *Trap:* Pick the shortest meeting? No.
  * *Greedy Truth:* **Pick the meeting that ends earliest!** The sooner a meeting finishes, the more room you leave open for future meetings.
* **The Rule:** Sort intervals by **end time** (`key=lambda x: x[1]`). Greedily pick the next interval whose start time $\ge$ current finish time.
* **Classic Problems:**
  * **LC 435: Non-overlapping Intervals**
  * **LC 452: Minimum Number of Arrows to Burst Balloons**
  * **LC 252 / 253: Meeting Rooms**

---

### Archetype 4: The Micro-Gain Accumulator (Telescoping Sums)
* **The Real-Life Analogy:** In a stock market with unlimited zero-fee trades, if the price goes from \$1 $\to$ \$5 $\to$ \$10, you don't need to predict the future peak. Harvesting every upward tick (\$5 - \$1 = \$4, and \$10 - \$5 = \$5) naturally sums to the total valley-to-peak run (\$9).
* **The Rule:** If today's step is positive (`prices[i] > prices[i-1]`), greedily add it. If it's negative, ignore it.
* **Classic Problems:**
  * **LC 122: Best Time to Buy and Sell Stock II**
  * **LC 134: Gas Station** (Greedily track surplus vs. deficit)

---

## 🔍 4. The 3-Second "Is It Greedy?" Checklist (Interview Mental Triggers)

When an interviewer hands you a problem, how do you know if Greedy works? Run this 3-question filter:

### 1. Does "Bigger / Further / Earliest" strictly dominate?
* If reaching stone 10 is *always* strictly better than or equal to reaching stone 5 with zero penalty, **try Greedy**.

### 2. Is there an "Undo" penalty?
* Does picking an option right now prevent a completely different, secretly superior combination down the road?
* *If NO (choices don't trap you):* **Greedy works.**
* *If YES (taking 3 coins now prevents an optimal 2-coin answer later, like with arbitrary coin denominations [1, 3, 4] for 6):* **Greedy fails**, you need exhaustive search.

### 3. Can sorting simplify the world?
* If sorting the input by size, start time, end time, or weight makes the best immediate choice obvious, it is almost certainly a Greedy problem.

---

## 📋 Summary Table for Quick Reference

| Greedy Archetype | What You Track | Golden Rule |
|---|---|---|
| **The Cashier / ATM** | `remaining_target` | Pick the largest denomination that fits. |
| **The Horizon** | `max_reach` | Update furthest reachable boundary; fail if `i > max_reach`. |
| **The Scheduler** | `last_end_time` | Sort by end time; pick what finishes earliest. |
| **The Accumulator** | `total_profit` | Grab every positive adjacent delta `curr - prev > 0`. |
| **The Squeeze Driver** | `left`, `right` | Bottleneck rule: Move whichever pointer restricts max potential. |
