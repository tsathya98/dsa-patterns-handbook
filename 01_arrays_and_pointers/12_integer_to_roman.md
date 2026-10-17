# LeetCode 12: Integer to Roman

> **Difficulty:** Medium | **Pattern:** Greedy Subtraction (Cashier / ATM Pattern)
> **Link:** [LeetCode 12](https://leetcode.com/problems/integer-to-roman/)

## The problem

Given an integer `num` ($1 \le \text{num} \le 3999$), convert it to a Roman numeral string using the standard 7 symbols (`I`, `V`, `X`, `L`, `C`, `D`, `M`) and the 6 subtractive combinations (`IV`, `IX`, `XL`, `XC`, `CD`, `CM`).

## Why the naive way fails

Converting `num` to a string and writing custom branching rules for 4s, 9s, and place values (`10 ** pos`) produces brittle code full of special cases.

## The core trick

Treat the conversion like an ATM dispensing cash with the fewest bills possible. List all 13 valid values (including the 6 subtractive pairs) in strictly descending order:

```text
Value:   1000   900   500   400   100    90    50    40    10     9     5     4     1
Symbol:   "M"  "CM"   "D"  "CD"   "C"  "XC"   "L"  "XL"   "X"  "IX"   "V"  "IV"   "I"
```

Iterate through the table from largest to smallest. For each `(val, sym)`, subtract `val` and append `sym` for as long as `num >= val` (or compute `count = num // val` and `num %= val`).

### Algorithm steps:
* **1. Define value-symbol mapping:** List roman values and symbols in descending order, including subtractive combinations (`1000: "M"`, `900: "CM"`, `500: "D"`, `400: "CD"`, ..., `1: "I"`).
* **2. Greedily subtract largest values:** For each `(val, sym)` pair:
  * While `num >= val`, append `sym` to the output list and subtract `num -= val`.
* **3. Termination:** Join and return the accumulated symbols once `num == 0`.

## Step-by-step trace

Input: `num = 3749`

| Denomination | `num` (before) | Fits (`num // val`) | Appended | `num` (after) | Output so far |
|---|---|---|---|---|---|
| `1000 ("M")` | 3749 | 3 | `"MMM"` | 749 | `"MMM"` |
| `500 ("D")` | 749 | 1 | `"D"` | 249 | `"MMMD"` |
| `100 ("C")` | 249 | 2 | `"CC"` | 49 | `"MMMDCC"` |
| `40 ("XL")` | 49 | 1 | `"XL"` | 9 | `"MMMDCCXL"` |
| `9 ("IX")` | 9 | 1 | `"IX"` | 0 | `"MMMDCCXLIX"` |

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def intToRoman(self, num: int) -> str:
        dct = {
            1000: "M", 900: "CM", 500: "D", 400: "CD",
            100: "C",  90: "XC",  50: "L",  40: "XL",
            10: "X",   9: "IX",   5: "V",   4: "IV",
            1: "I",
        }

        res = []
        for val, sym in dct.items():
            while num >= val:
                res.append(sym)
                num -= val

        return "".join(res)
```

</details>

## Traps to watch for

* **Ascending order bug:** The table must go from `1000` down to `1`. Starting at `1` will turn `3749` into 3,749 `"I"` characters.
* **Forgetting subtractive pairs:** The 6 two-character symbols (`CM`, `CD`, `XC`, `XL`, `IX`, `IV`) must be included directly in the lookup table so the greedy loop picks `"CM"` for `900` instead of `"DCCCC"`.

## Complexity

* **Time:** $\mathcal{O}(1)$ because `num <= 3999` and no symbol repeats more than 3 times, bounding the total loop iterations to at most 15.
* **Space:** $\mathcal{O}(1)$ for the fixed 13-entry table and output buffer.
