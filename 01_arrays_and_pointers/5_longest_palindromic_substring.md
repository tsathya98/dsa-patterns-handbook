# LeetCode 5: Longest Palindromic Substring

> **Difficulty:** Medium | **Pattern:** Two Pointers (Expand Around Center)  
> **Source Code:** [`5_longest_palindromic_substring.py`](./5_longest_palindromic_substring.py)

## The problem

Given a string `s`, return the longest palindromic substring in `s`.

```text
Input:  s = "babad" -> Output: "bab" (or "aba")
Input:  s = "cbbd"  -> Output: "bb"
```

## The core trick: Expand outward from every center

Checking whether a known string is a palindrome uses inward pointers (`l = 0, r = n - 1`). Finding a palindrome inside a larger string reverses the direction: start at a center and expand outward (`l -= 1`, `r += 1`) while `s[l] == s[r]`.

Every palindrome has one of two center types ($2n$ centers in total):

```text
1. Odd-length palindrome ("bab") -> Center is on index i:
   Start: l = i, r = i
         <-- l   r -->
       " b  [a]  b "

2. Even-length palindrome ("cbbd") -> Center is between i and i + 1:
   Start: l = i, r = i + 1
         <-- l     r -->
       " c  [b  b]  d "
```

### Algorithm steps (Expand around centers):
* **1. Define expansion helper:** Given starting centers `l` and `r`, expand outward with `l -= 1` and `r += 1` while `l >= 0`, `r < len(s)`, and `s[l] == s[r]`. Return valid boundaries `(l + 1, r)`.
* **2. Track longest palindrome:** Initialize `best_l = 0` and `best_r = 0`.
* **3. Test all centers:** For each index `i` from `0` to `len(s) - 1`:
  * Expand around odd center: `_expand(i, i)`.
  * Expand around even center: `_expand(i, i + 1)`.
  * If either candidate is longer than `best_r - best_l`, update `best_l, best_r`.
* **4. Return:** `s[best_l:best_r]` in $\mathcal{O}(n^2)$ time and $\mathcal{O}(1)$ space.

## Boundary math: Why the valid slice is `s[l + 1 : r]`

Inside the expansion loop:
```python
while l >= 0 and r < len(s) and s[l] == s[r]:
    l -= 1
    r += 1
```
When the `while` loop terminates, `l` and `r` have already stepped one index past the palindrome (either out of bounds or onto mismatched characters):

```text
s = "x  b  a  b  y"
     0  1  2  3  4
     ^           ^
     l           r   (loop stops here because s[0] != s[4])
```

- Last valid left index: `l + 1` (`1`)
- Last valid right index: `r - 1` (`3`)
- Since Python's slice stop index is exclusive, `s[l + 1 : r]` extracts indices `l + 1` through `r - 1`, with length `r - (l + 1) = r - l - 1`.

Returning the index pair `(l + 1, r)` from the helper and slicing `s` once at the very end avoids allocating $2n$ intermediate strings during the loop.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def _expand(l: int, r: int) -> tuple[int, int]:
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return l + 1, r

        best_l, best_r = 0, 0
        for i in range(len(s)):
            for l, r in (_expand(i, i), _expand(i, i + 1)):
                if r - l > best_r - best_l:
                    best_l, best_r = l, r

        return s[best_l:best_r]
```

</details>

## Complexity

| Approach | Time | Auxiliary Space | Notes |
| :--- | :--- | :--- | :--- |
| Brute force (all substrings) | $\mathcal{O}(n^3)$ | $\mathcal{O}(n)$ | Hits TLE for $n = 1000$. |
| 2D Dynamic Programming (`dp[i][j]`) | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | Allocates an $n \times n$ boolean table. |
| Expand Around Center | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Optimal practical interview solution. |
| Manacher's Algorithm | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Linear time, rarely expected in interviews. |
