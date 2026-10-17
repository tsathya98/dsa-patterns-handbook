# LeetCode 125: Valid Palindrome

> **Difficulty:** Easy | **Pattern:** Two Pointers (Inward Squeeze)
> **Source Code:** [`125_valid_palindrome.py`](./125_valid_palindrome.py)

## The problem

A string `s` is a palindrome if, after converting uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forward and backward. Return `True` if `s` is a palindrome, or `False` otherwise.

## Why the naive way fails

Building a filtered string `[c.lower() for c in s if c.isalnum()]` and comparing it to its reverse `cleaned[::-1]` works in $\mathcal{O}(n)$ time, but allocates two new $\mathcal{O}(n)$ copies in memory and scans the entire string even if the first and last characters mismatch.

## The core trick

Place `l = 0` at the start and `r = len(s) - 1` at the end, then squeeze inward in $\mathcal{O}(1)$ extra space:
1. If `s[l]` is not alphanumeric, advance `l += 1`.
2. If `s[r]` is not alphanumeric, retreat `r -= 1`.
3. Otherwise, compare `s[l].lower() == s[r].lower()`. If they match, move both inward (`l += 1`, `r -= 1`); if not, return `False` immediately.

```text
  l ──►                                  ◄── r
 "A   m a n ,   a   p l a n . . .   P a n a m a"
```

### Algorithm steps:
* **1. Initialize two pointers:** Set `l = 0` and `r = len(s) - 1`.
* **2. Squeeze inward while l < r:**
  * If `not s[l].isalnum()`, advance `l += 1`.
  * Else if `not s[r].isalnum()`, retreat `r -= 1`.
  * Else compare characters case-insensitively: if `s[l].lower() == s[r].lower()`, advance both pointers with `l += 1` and `r -= 1`.
  * If characters do not match, return `False` immediately.
* **3. Termination:** If pointers cross without mismatch, return `True`.

## Step-by-step trace

Input: `s = "A man, a"`

| Step | `l` (`s[l]`) | `r` (`s[r]`) | Check | Action |
|---|---|---|---|---|
| 1 | 0 (`'A'`) | 7 (`'a'`) | `'a' == 'a'` | Match: `l = 1`, `r = 6` |
| 2 | 1 (`' '`) | 6 (`' '`) | `not s[l].isalnum()` | Skip non-alnum: `l = 2` |
| 3 | 2 (`'m'`) | 6 (`' '`) | `not s[r].isalnum()` | Skip non-alnum: `r = 5` |
| 4 | 2 (`'m'`) | 5 (`','`) | `not s[r].isalnum()` | Skip non-alnum: `r = 4` |
| 5 | 2 (`'m'`) | 4 (`'n'`) | `'m' != 'n'` | Mismatch: return `False` |

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1

        while l < r:
            if not s[l].isalnum():
                l += 1
            elif not s[r].isalnum():
                r -= 1
            elif s[l].lower() == s[r].lower():
                l += 1
                r -= 1
            else:
                return False

        return True
```

</details>

## Traps to watch for

* **Using `isalpha()` instead of `isalnum()`:** Digits count as valid characters in this problem. Using `isalpha()` skips `'0'` in `"0P"` and wrongly returns `True`.
* **Missing `l < r` inside inner `while` loops:** If you use inner `while` loops to skip punctuation, an all-punctuation string like `".,"` will push `l` past `len(s) - 1` (`IndexError`) unless guarded by `while l < r and not s[l].isalnum()`. Using `if / elif` inside the main `while l < r:` loop avoids that bug entirely.

## Complexity

* **Time:** $\mathcal{O}(n)$ since each pointer visits each character at most once.
* **Space:** $\mathcal{O}(1)$ auxiliary memory.
