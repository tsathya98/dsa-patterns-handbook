# LeetCode 13: Roman to Integer

> **Difficulty:** Easy | **Pattern:** Hash Map + 1-Step Lookahead Scan
> **Link:** [LeetCode 13](https://leetcode.com/problems/roman-to-integer/)

## The problem

Given a Roman numeral string `s` (`I = 1`, `V = 5`, `X = 10`, `L = 50`, `C = 100`, `D = 500`, `M = 1000`), convert it to an integer. When a smaller numeral appears immediately before a larger numeral (such as `IV = 4` or `CM = 900`), the smaller value is subtracted instead of added.

## Why the naive way fails

Hardcoding a nested map of subtraction pairs like `sub = {"I": ["V", "X"], "X": ["L", "C"], "C": ["D", "M"]}` and advancing a manual `while` pointer by 1 or 2 steps works, but does three lookups per character and complicates index bounds.

## The core trick

In any valid Roman numeral, a symbol is subtracted if and only if it is strictly smaller than the symbol immediately to its right:
* If `i < n - 1` and `dct[s[i]] < dct[s[i + 1]]`, subtract `dct[s[i]]`.
* Otherwise, add `dct[s[i]]`.

```text
String:   M      C      M      X      C      I      V
Values:  1000   100   1000    10     100     1      5
Sign:   +1000  -100  +1000   -10    +100    -1     +5  = 1994
```

## Step-by-step trace

Input: `s = "MCMXCIV"`

| Index $i$ | `s[i]` (val) | `s[i + 1]` (val) | Comparison | Operation | `total` |
|---|---|---|---|---|---|
| 0 | `M` (1000) | `C` (100) | $1000 \ge 100$ | $+1000$ | 1000 |
| 1 | `C` (100) | `M` (1000) | $100 < 1000$ | $-100$ | 900 |
| 2 | `M` (1000) | `X` (10) | $1000 \ge 10$ | $+1000$ | 1900 |
| 3 | `X` (10) | `C` (100) | $10 < 100$ | $-10$ | 1890 |
| 4 | `C` (100) | `I` (1) | $100 \ge 1$ | $+100$ | 1990 |
| 5 | `I` (1) | `V` (5) | $1 < 5$ | $-1$ | 1989 |
| 6 | `V` (5) | None | Last char | $+5$ | 1994 |

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def romanToInt(self, s: str) -> int:
        dct = {
            "I": 1, "V": 5, "X": 10, "L": 50,
            "C": 100, "D": 500, "M": 1000,
        }
        total = 0
        n = len(s)

        for i in range(n):
            if i < n - 1 and dct[s[i]] < dct[s[i + 1]]:
                total -= dct[s[i]]
            else:
                total += dct[s[i]]

        return total
```

</details>

## Traps to watch for

* **Out-of-bounds lookahead on the last character:** The last character `s[n - 1]` has no right neighbor and is always added. Guard `dct[s[i + 1]]` with `i < n - 1`, or loop over `range(n - 1)` and add `dct[s[-1]]` at the end.
* **Equal adjacent numerals (`"III"`):** Equal values (`1 == 1`) must be added, so the subtraction condition must be strictly `<` (`dct[s[i]] < dct[s[i + 1]]`), never `<=`.

## Complexity

* **Time:** $\mathcal{O}(n)$ for a single pass over `s` (bounded by $n \le 15$).
* **Space:** $\mathcal{O}(1)$ for the 7-entry dictionary.
