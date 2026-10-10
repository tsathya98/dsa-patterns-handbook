# 🏛️ LeetCode 13: Roman to Integer – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** Top Interview 150 / NeetCode 150 / Blind 75  
> **Pattern:** Hash Map / Linear Scan (Lookahead Comparison)  
> **LeetCode Link:** [LeetCode 13: Roman to Integer](https://leetcode.com/problems/roman-to-integer/)

---

## 📌 Problem in Plain English

Roman numerals are represented by seven different symbols:
* `I = 1`, `V = 5`, `X = 10`, `L = 50`, `C = 100`, `D = 500`, `M = 1000`

Usually, symbols are written from largest to smallest from left to right: `XII = 10 + 1 + 1 = 12`.

However, when a smaller symbol appears **before** a larger symbol, it represents subtraction:
* `IV = 5 - 1 = 4`
* `IX = 10 - 1 = 9`
* `XL = 50 - 10 = 40`, `XC = 100 - 10 = 90`
* `CD = 500 - 100 = 400`, `CM = 1000 - 100 = 900`

Given a roman numeral string `s`, convert it to an integer.

```text
Example 1: s = "III"      -> Output: 3
Example 2: s = "LVIII"    -> Output: 58 (50 + 5 + 3)
Example 3: s = "MCMXCIV"  -> Output: 1994 (1000 + 900 + 90 + 4)
```

---

## 💡 The "Aha!" Moment: The Universal Subtraction Rule

You do **not** need a separate dictionary of subtraction pairs (`{"I": ["V", "X"]}`).

There is a single **universal mathematical rule** for Roman numerals:

> **"Whenever a smaller value appears BEFORE a larger value, SUBTRACT it. Otherwise, ADD it!"**

```text
Look at "MCMXCIV" (1994):
- M (1000) >= C (100)  -> ADD 1000
- C (100)  <  M (1000) -> SUBTRACT 100  (Lookahead sees larger M!)
- M (1000) >= X (10)   -> ADD 1000
- X (10)   <  C (100)  -> SUBTRACT 10   (Lookahead sees larger C!)
- C (100)  >= I (1)    -> ADD 100
- I (1)    <  V (5)    -> SUBTRACT 1    (Lookahead sees larger V!)
- V (5)    is last     -> ADD 5

Total = +1000 - 100 + 1000 - 10 + 100 - 1 + 5 = 1994
```

---

## 🔬 Performance Finding: Why Did the Initial Code Take 10 ms (Beats 16%)?

### Your Initial Approach:
```python
sub = {"I": ["V", "X"], "X": ["L", "C"], "C": ["D", "M"]}
while i < len(s):
    if i < len(s) - 1 and s[i] in sub and s[i + 1] in sub[s[i]]:
        total -= dct[s[i]]
    else:
        total += dct[s[i]]
    i += 1
```

### Why it was slower:
1. **Three lookups per character:**
   * Hash lookup in `sub` (`s[i] in sub`).
   * Hash lookup to extract the list (`sub[s[i]]`).
   * Linear search in the list (`s[i+1] in [...]`).
2. **`while` loop bytecode overhead:** Python's interpreted `while i < len(s): ... i += 1` executes slower in bytecode than a C-optimized `for i in range(...)`.

---

## ⚡ The Optimized Version (2–3 ms, Beats 90%+)

Replace all nested lookups with **one direct integer comparison**:

```python
class Solution:
    def romanToInt(self, s: str) -> int:
        dct = {
            "I": 1, "V": 5, "X": 10, "L": 50,
            "C": 100, "D": 500, "M": 1000
        }
        total = 0
        n = len(s)
        
        for i in range(n):
            # If current numeral is smaller than the next one, subtract it!
            if i < n - 1 and dct[s[i]] < dct[s[i + 1]]:
                total -= dct[s[i]]
            else:
                total += dct[s[i]]
                
        return total
```

---

## ⏱️ Complexity Analysis

* **Time Complexity:** $\mathcal{O}(n)$ — Single pass through string of length $n$. (Since $n \le 15$ by constraints, this takes $\le 15$ operations).
* **Space Complexity:** $\mathcal{O}(1)$ — The dictionary has a fixed size of 7 key-value pairs.

---

## 🎩 Fun Interview Bonus: The `str.replace` 1-ms Trick

In Python, the 6 subtraction cases can be replaced with additive equivalents:
* `"IV"` $\to$ `"IIII"` ($4$)
* `"IX"` $\to$ `"VIIII"` ($9$)
* `"XL"` $\to$ `"XXXX"` ($40$)
* `"XC"` $\to$ `"LXXXX"` ($90$)
* `"CD"` $\to$ `"CCCC"` ($400$)
* `"CM"` $\to$ `"DCCCC"` ($900$)

```python
class SolutionCheat:
    def romanToInt(self, s: str) -> int:
        translations = {
            "I": 1, "V": 5, "X": 10, "L": 50,
            "C": 100, "D": 500, "M": 1000
        }
        s = (s.replace("IV", "IIII")
              .replace("IX", "VIIII")
              .replace("XL", "XXXX")
              .replace("XC", "LXXXX")
              .replace("CD", "CCCC")
              .replace("CM", "DCCCC"))
              
        return sum(translations[c] for c in s)
```
*(Because `str.replace()` runs in compiled C code, this often clocks in at 0–1 ms on LeetCode!)*
