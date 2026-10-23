# LeetCode 459: Repeated Substring Pattern

> **Difficulty:** Easy | **Pattern:** String Periodicity / Divisor Chunking
> **Source Code:** [`459_repeated_substring_pattern.py`](459_repeated_substring_pattern.py)

## The problem

Given a string `s`, check if it can be constructed by taking a substring of it and appending multiple copies of the substring together.

## Why the naive way fails

Trying every possible slice index without restrictions leads to $\mathcal{O}(n^3)$ operations and index bugs. You do not need to check arbitrary slices:
1. Any repeating unit must start at index 0.
2. The length of the unit must divide `len(s)` evenly.
3. The unit cannot be longer than `len(s) // 2` because it must repeat at least twice.

## The core trick

There are two clean mental models for this problem:

### Model 1: Divisor Chunking (Direct Logic)

Loop length $L$ from $1$ up to $n // 2$:
1. If $n \% L \neq 0$, skip $L$ immediately (a block of size $L$ cannot pack evenly into $n$).
2. Take the prefix `chunk = s[:L]`.
3. Check if repeating that chunk $(n // L)$ times equals `s`.

### Model 2: The Doubling Trick (String Rotation)

If `s` is made of repeated blocks $P$ ($s = P + P$), then $s + s = P + P + P + P$.
If you remove the first character and the last character:
`(s + s)[1:-1]`
You destroy the original $s$ at the front and the original $s$ at the back. If $s$ still appears anywhere inside that remaining middle string, it proves $s$ has internal periodicity.

```text
s = "abab"
s + s = "abababab"
chop  =  x bababa x   <-- "abab" is inside "bababa"!
```

### Algorithm steps (Divisor check):
* **1. Set bounds:** Let `n = len(s)`. A repeating pattern must have length `L` at most `n // 2`.
* **2. Test candidate lengths:** Loop candidate prefix length `L` from `1` to `n // 2`:
  * If `n % L != 0`, skip `L` (cannot divide string into equal blocks).
  * If `s[:L] * (n // L) == s`, repeating this prefix reconstructs `s`; return `True`.
* **3. Termination:** If no prefix length forms the string, return `False`.

## Step-by-step trace

Input: `s = "abab"`, `n = 4`, max $L = 2$.

| Step | $L$ | `n % L == 0?` | `chunk` | `chunk * (n // L)` | Equals `s`? |
|---|---|---|---|---|---|
| 1 | 1 | `4 % 1 == 0` (Yes) | `"a"` | `"a" * 4 = "aaaa"` | No |
| 2 | 2 | `4 % 2 == 0` (Yes) | `"ab"` | `"ab" * 2 = "abab"` | **Yes, return True** |

<details>
<summary>Spoiler: Solution Code</summary>

### 1-Line Doubling Trick
```python
class Solution:
    def repeatedSubstringPattern(self, s: str) -> bool:
        # Rotating a periodic string lands on itself before shifting length n
        return s in (s + s)[1:-1]
```

### Divisor Chunking
```python
class Solution:
    def repeatedSubstringPattern(self, s: str) -> bool:
        n = len(s)
        for length in range(1, (n // 2) + 1):
            if n % length == 0:
                chunk = s[:length]
                if chunk * (n // length) == s:
                    return True
        return False
```

</details>

## Traps to watch for

1. **Checking past $n // 2$:** A pattern that repeats at least twice can never be longer than half the string.
2. **Missing string slicing boundaries:** Forgetting `[1:-1]` in the doubling trick will always return `True` because `s` is trivially in `s + s` at index 0.

## Complexity

- **Divisor Chunking:** $\mathcal{O}(n \sqrt{n})$ time (number of divisors of $n$ times $\mathcal{O}(n)$ string comparison), $\mathcal{O}(n)$ space.
- **Doubling Trick:** $\mathcal{O}(n)$ time (Boyer-Moore substring search), $\mathcal{O}(n)$ auxiliary space.
