# 🏛️ LeetCode 12: Integer to Roman – Master Guide

> **Difficulty:** Medium  
> **Study Plan:** Top Interview 150 / NeetCode 150  
> **Pattern:** Greedy Subtraction (The ATM / Cashier Pattern)  
> **LeetCode Link:** [LeetCode 12: Integer to Roman](https://leetcode.com/problems/integer-to-roman/)

---

## 📌 Problem in Plain English

Roman numerals are formed by appending the conversions of decimal place values from highest to lowest. Converting $3749$ means:
* $3000 \to \text{"MMM"}$
* $700 \to 500 + 200 \to \text{"DCC"}$
* $40 \to \text{"XL"}$
* $9 \to \text{"IX"}$
* Result = `"MMMDCCXLIX"`

Given an integer `num` ($1 \le num \le 3999$), convert it to a Roman numeral.

---

## 💡 The "Aha!" Moment: The ATM / Cashier Analogy 🏧

Instead of converting `num` to a string (`str(num)`) and doing complicated digit-by-digit place-value math (`10 ** cur_l`), treat this like **an ATM dispensing cash with the fewest bills possible**.

There are 13 fixed bill denominations, arranged from **LARGEST to SMALLEST**:
```text
Value:   1000   900   500   400   100   90    50    40    10     9     5     4     1
Symbol:   "M"  "CM"   "D"  "CD"   "C"  "XC"  "L"  "XL"   "X"  "IX"   "V"  "IV"   "I"
```

To withdraw `num`:
1. Check the largest bill ($1000$).
2. While `num >= 1000`, peel off $1000$ and dispense `"M"`.
3. Move to the next largest bill ($900$), and repeat until the remaining balance is $0$!

---

## 🔍 Two Ways to Implement This

### Approach 1: The Foolproof Whiteboard Version (Your Solution! 🏆)
*Uses repeated subtraction with a `while` loop.*

```python
class Solution:
    def intToRoman(self, num: int) -> str:
        # Denominations MUST be in descending order!
        dct = {
            1000: 'M', 900: 'CM', 500: 'D', 400: 'CD',
            100: 'C',  90: 'XC',  50: 'L',  40: 'XL',
            10: 'X',   9: 'IX',   5: 'V',   4: 'IV',
            1: 'I'
        }
        
        tot = []
        for number in dct:
            while num >= number:
                tot.append(dct[number])
                num -= number
                
        return "".join(tot)
```

#### Why this is the best choice for an interview:
* **Zero math bugs:** No risk of mixing up integer division `//` and modulo `%`.
* **Safe $\mathcal{O}(1)$ execution:** In Roman numerals, no symbol repeats more than 3 times (`MMM`, `CCC`, `XXX`, `III`). The inner `while` loop runs **at most 3 times per denomination**! Total iterations across the entire program $\le 15$.

---

### Approach 2: The Math Shortcut (Division & Modulo)
*Eliminates the inner `while` loop by calculating the count directly.*

```python
class SolutionMath:
    def intToRoman(self, num: int) -> str:
        values = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"),  (90, "XC"),  (50, "L"),  (40, "XL"),
            (10, "X"),   (9, "IX"),   (5, "V"),   (4, "IV"),
            (1, "I")
        ]
        
        res = []
        for val, sym in values:
            if num == 0:
                break
            count = num // val       # How many bills fit?
            res.append(sym * count)  # Append "M" * 3 = "MMM"
            num %= val               # Remaining balance
            
        return "".join(res)
```

---

## ⚖️ Comparison: Which One is Better?

| Metric | Approach 1 (Repeated Subtraction) | Approach 2 (Division & Modulo) |
|---|---|---|
| **Code Style** | `while num >= number: num -= number` | `count = num // val; num %= val` |
| **Interview Safety** | ⭐⭐⭐⭐⭐ **Highest** (Intuitive, zero math errors) | ⭐⭐⭐⭐ (Slight chance of mixing up `//` and `%`) |
| **LeetCode Runtime** | 1–3 ms (Beats 90%+) | 1–3 ms (Beats 90%+) |
| **Inner Loop Iterations** | $\le 3$ times per symbol | 0 (Replaced by math) |

---

## ⏱️ Complexity Analysis

* **Time Complexity:** $\mathcal{O}(1)$ — The loop runs over a fixed set of 13 denominations. Because $num \le 3999$, the total steps are strictly bounded ($\le 15$ operations).
* **Space Complexity:** $\mathcal{O}(1)$ — Fixed dictionary of 13 entries.

---

## ⚠️ Common Student Pitfalls to Avoid

1. **Ascending Order Trap:**  
   If you write the dictionary from `1: "I"` up to `1000: "M"`, the code will try to pay off $3749$ using 3,749 `"I"`s! Always order from **largest to smallest**.
2. **Missing Subtractive Forms:**  
   You must include the 6 subtractive forms (`900: 'CM'`, `400: 'CD'`, `90: 'XC'`, `40: 'XL'`, `9: 'IX'`, `4: 'IV'`) as first-class denominations in your table.
