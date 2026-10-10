# 🏧 Greedy Subtraction (The ATM / Cashier Pattern) Master Cheat Sheet

> **Pattern:** Greedy Subtraction / Change-Making Decomposition  
> **Target Audience:** Rapid interview review, mental checklist, and copy-paste templates.  
> **Philosophy:** When converting a total into standard denominations, always greedily take the largest available piece first until you can't, then move down.

---

## 💡 1. What is the Greedy Subtraction (ATM) Pattern?

Instead of converting a number into a string and doing complicated digit-by-digit place-value math (`10 ** len`), we maintain an **ordered list/mapping of standard denominations from largest to smallest**.

We greedily deduct the largest possible denomination repeatedly until the remaining balance is smaller than that denomination, then step down to the next smaller one.

```text
Target: 3749
Available Denominations: [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]

Step 1: 3749 >= 1000? YES -> take 1000 ("M"), remainder = 2749
Step 2: 2749 >= 1000? YES -> take 1000 ("M"), remainder = 1749
Step 3: 1749 >= 1000? YES -> take 1000 ("M"), remainder = 749
Step 4:  749 >= 1000? NO  -> drop to 900
Step 5:  749 >=  900? NO  -> drop to 500
Step 6:  749 >=  500? YES -> take 500  ("D"), remainder = 249
... and so on down to 0!
```

---

## 🎯 2. When to Use It? (The 3-Second Mental Checklist)

Ask yourself these 3 questions:

1. **Am I decomposing a single quantity into standard fixed units or symbols?**  
   *(Roman numerals, cash change, seconds to days/hours/minutes, numbers to English words).*
2. **Is the unit system canonical (Greedy works)?**  
   *(Taking the largest denomination immediately never prevents an optimal solution).*
3. **Can I predefine the denominations in descending order?**  
   *(If yes, you only need one single pass over the denominations list).*

👉 If all three are **YES**, use **Greedy Subtraction**.

---

## 🏧 3. Real-World Mental Models

| Everyday Scenario | Denominations (Largest to Smallest) | Greedy Action |
| :--- | :--- | :--- |
| **ATM Dispenser** | `$100, $50, $20, $10, $5, $1` | Peel off the biggest bill that fits into remaining balance. |
| **Time Formatter** | `86400s (Day), 3600s (Hour), 60s (Min), 1s (Sec)` | Convert big chunks first, what's left is minutes and seconds. |
| **Metric / Storage**| `1 TB, 1 GB, 1 MB, 1 KB, 1 B` | Show highest unit without manual decimal parsing. |
| **Roman Numerals** | `1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1` | Peel off largest Roman value or subtractive combo. |

---

## 🛠️ 4. The Two Implementation Flavors

### Flavor A: Repeated Subtraction (`while` loop) — *Whiteboard Favorite!* 🏆
Best for interviews because it avoids math edge cases (off-by-one division bugs).

```python
def decompose_while(num: int, denominations: dict) -> list:
    result = []
    for unit in denominations:
        while num >= unit:
            result.append(denominations[unit])
            num -= unit
    return result
```

* **When to use:** When each denomination is used only a few times (e.g., Roman numerals where count $\le 3$).
* **Advantage:** Impossible to get wrong under interview stress.

---

### Flavor B: Division & Modulo (`//` and `%`) — *Arithmetic 1-Step* ⚡
Best when the multiplier can be large (e.g., converting $987,654$ seconds into hours).

```python
def decompose_math(num: int, denominations: list) -> list:
    result = []
    for unit, label in denominations:
        if num == 0:
            break
        count = num // unit
        if count > 0:
            result.append((count, label))
            num %= unit
    return result
```

* **When to use:** When `num` can be huge, avoiding thousands of subtraction loops.
* **Advantage:** Direct $\mathcal{O}(1)$ math per denomination.

---

## 📋 5. Classic Problems in this Family

| LeetCode # | Problem Name | Denomination Set | Trick / Nuance |
| :--- | :--- | :--- | :--- |
| **LC 12** | **Integer to Roman** | `[1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]` | Include subtractive pairs (`900: 'CM'`, `4: 'IV'`) as standard bills! |
| **LC 273** | **Integer to English Words** | `[10^9: "Billion", 10^6: "Million", 10^3: "Thousand"]` | Process in 3-digit chunks using division and recursion. |
| **LC 322** | **Coin Change (Warning!)** | Arbitrary coin arrays (e.g., `[1, 3, 4]` for amount `6`) | ⚠️ **Greedy FAILS** here! Must use **Dynamic Programming** ($4+1+1=3$ coins vs optimal $3+3=2$ coins). |

> [!WARNING]
> **When does the ATM Greedy logic FAIL?**  
> Greedy only works on **canonical** coin systems (like US coins `[25, 10, 5, 1]` or Roman numerals). If an interview gives arbitrary coin values like `[1, 3, 4]` and asks for change of `6`:
> * Greedy picks: `4 + 1 + 1` (3 coins)
> * Optimal is: `3 + 3` (2 coins)  
> For arbitrary coin sets, switch to **DP (Unbounded Knapsack)**!

---

## ⚠️ 6. Top 3 Pitfalls to Avoid in Interviews

1. **Forgetting subtractive combinations in Roman numerals:**
   * Do NOT just store `[1000, 500, 100, 50, 10, 5, 1]`.
   * Pre-bake `900 ("CM")`, `400 ("CD")`, `90 ("XC")`, `40 ("XL")`, `9 ("IX")`, `4 ("IV")` directly into your denomination list.
2. **Sorting order mistake:**
   * Denominations **MUST** be processed in descending order. If you check `1` first, a number like `5` would dispense five `1`s instead of one `5`.
3. **Dictionary insertion order in older Python versions:**
   * In Python 3.7+, dictionaries preserve insertion order. In languages like Java or C++, use an `Array` / `List` of pairs (`[(1000, "M"), (900, "CM"), ...]`), not an unordered hash table (`unordered_map` / `HashMap`).

---

## ⏱️ 7. Complexity Blueprint

* **Time Complexity:** $\mathcal{O}(1)$ for Roman numerals (fixed 13 denominations, $\le 15$ total loop iterations). In general, $\mathcal{O}(D)$ where $D$ is the number of denominations.
* **Space Complexity:** $\mathcal{O}(1)$ auxiliary space (fixed denomination table).
