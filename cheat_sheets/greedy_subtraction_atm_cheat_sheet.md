# Greedy Subtraction (ATM Pattern) Cheat Sheet

> Problem walkthrough: [LC 12: Integer to Roman](../01_arrays_and_pointers/12_integer_to_roman.md)

When decomposing a number into standard fixed units (Roman numerals, cash bills, time units), store the denominations from largest to smallest and repeatedly peel off the largest denomination that fits.

## 1. When to use it
1. You are converting a quantity into fixed units or symbols.
2. The unit system is **canonical** (taking the largest piece first never blocks the optimal answer).
3. You can list all denominations in descending order upfront.

### Algorithm steps:
* **1. Descending denomination ordering:** Sort or declare all base units and special subtractive compounds from largest to smallest.
* **2. Greedy match and peel:** Inspect each unit `(val, sym)`. While `num >= val`, append `sym` to the result and subtract `val` from `num`.
* **3. Advance until exhausted:** Move to the next smaller denomination when `num < val`, terminating once all denominations are checked or `num == 0` in $\mathcal{O}(1)$ time.


---

## 2. Two Templates

### Flavor A: `while` subtraction loop (best when counts are small, like Roman numerals)
```python
def intToRoman(num: int) -> str:
    # Include subtractive pairs (900, 400, 90, 40, 9, 4) right in the table
    denominations = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"),  (90, "XC"),  (50, "L"),  (40, "XL"),
        (10, "X"),   (9, "IX"),   (5, "V"),   (4, "IV"), (1, "I")
    ]
    res = []
    for val, sym in denominations:
        while num >= val:
            res.append(sym)
            num -= val
    return "".join(res)
```

### Flavor B: `//` and `%` division (best when counts can be huge, like seconds to days)
```python
def decompose_math(num: int, denominations: list[tuple[int, str]]) -> list[tuple[int, str]]:
    res = []
    for unit, label in denominations:
        if num == 0:
            break
        count, num = divmod(num, unit)
        if count > 0:
            res.append((count, label))
    return res
```

---

## 3. Traps to Watch For
1. **When greedy subtraction fails (LC 322 Coin Change):** Greedy only works on canonical systems like US coins `[25, 10, 5, 1]` or Roman numerals. If given arbitrary coins like `[1, 3, 4]` for target `6`, greedy picks `4 + 1 + 1` (3 coins) instead of `3 + 3` (2 coins). Arbitrary coin sets require Dynamic Programming.
2. **Pre-baking Roman subtractive pairs:** Treat `900 ("CM")`, `400 ("CD")`, `90 ("XC")`, `40 ("XL")`, `9 ("IX")`, and `4 ("IV")` as standard denominations in your table so you never need special `if` branches.
3. **Descending order is mandatory:** Always iterate from largest denomination to smallest.
