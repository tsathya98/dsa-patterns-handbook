# 🔦 LeetCode 5: Longest Palindromic Substring – Master Study Guide

> **Difficulty:** Medium | **Pattern:** Two Pointers Formation F (Outward Expand Around Center / The Flashlight Beam)  
> **Complexity:** Time: $\mathcal{O}(n^2)$ | Auxiliary Space: $\mathcal{O}(1)$ (Beats 92.04% memory!)  
> **Source Code:** [`5_longest_palindromic_substring.py`](./5_longest_palindromic_substring.py)

---

## 📌 Problem in Plain English

Given a string `s`, return the **longest palindromic substring** in `s` (a contiguous slice that reads the exact same forward and backward).

```text
Example 1:
Input:  s = "babad"
Output: "bab" (or "aba")

Example 2:
Input:  s = "cbbd"
Output: "bb"
```

---

## 🧠 Mental Model: The Flashlight Beam (Expand Around Center)

* **Validating** if a known string is a palindrome (*LC 125*) uses **Inward Squeeze** (`l = 0, r = n - 1`).
* **Finding** a palindrome hidden inside a string (*LC 5, LC 647*) flips the pointers inside-out: **Outward Expansion**!

Think of a **Flashlight Beam** starting at a center index `i` and shining outward (`l -= 1`, `r += 1`) as long as the left and right characters mirror each other (`s[l] == s[r]`).

### Why Are There 2 Types of Centers? ($2N$ Centers Total)
Every palindrome has either an **Odd** length or an **Even** length:

```text
1. ODD-LENGTH PALINDROME ("b a b") -> Center is ON character i:
   Start: l = i, r = i
         ◄── l   r ──►
       " b   [a]   b "

2. EVEN-LENGTH PALINDROME ("c b b d") -> Center is BETWEEN i and i + 1:
   Start: l = i, r = i + 1
         ◄── l       r ──►
       " c   [b   b]   d "
```

---

## 🔍 The Boundary Rule: Why `return s[l + 1 : r]`?

Inside the `while` loop:
```python
while l >= 0 and r < len(s) and s[l] == s[r]:
    l -= 1
    r += 1
```
When the `while` loop finally stops, `l` and `r` have **already stepped 1 index too far outward** (either out of bounds or onto mismatched characters)!

```text
s = "x  b  a  b  y"
     0  1  2  3  4
     ▲           ▲
     l           r    <-- Loop stops here because s[0] ('x') != s[4] ('y')!
```
* Last **valid** left index = `l + 1` (`1`)
* Last **valid** right index = `r - 1` (`3`)
* In Python slicing `s[start:stop]`, `stop` is exclusive, so `(r - 1) + 1 = r`.
* Therefore: **`s[l + 1 : r]`** (and its length is `(r - 1) - (l + 1) + 1 = r - l - 1`).

---

## 💻 Production Implementation (Your Accepted Solution)

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def _expand(l: int, r: int) -> str:
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l + 1 : r]

        max_len = 0
        max_pal = ""
        for i in range(len(s)):
            pal = _expand(i, i)
            if len(pal) > max_len:
                max_len = len(pal)
                max_pal = pal
            pal = _expand(i, i + 1)
            if len(pal) > max_len:
                max_len = len(pal)
                max_pal = pal
        return max_pal
```

---

## ⚡ Micro-Optimization: Slice Once at the End ($\mathcal{O}(1)$ Pure Space)

In `_expand`, returning `s[l+1:r]` allocates $2N$ string slices across the loop. If you instead return just the length or indices `(l + 1, r)` and slice `s` **only once** at the very end, you avoid $2N$ heap allocations:

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def _expand(l: int, r: int) -> tuple[int, int]:
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return l + 1, r  # Just 2 integers, zero string copying!

        best_l, best_r = 0, 0
        for i in range(len(s)):
            for l, r in (_expand(i, i), _expand(i, i + 1)):
                if r - l > best_r - best_l:
                    best_l, best_r = l, r

        return s[best_l:best_r]
```

---

## 🏆 Complexity & FAANG Trade-offs

| Approach | Time | Auxiliary Space | Interview Verdict |
|---|---|---|---|
| **Brute Force (All substrings + reverse)** | $\mathcal{O}(n^3)$ | $\mathcal{O}(n)$ | ❌ TLE ($1000^3 = 10^9$ ops). |
| **2D Dynamic Programming (`dp[i][j]`)** | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | ⚠️ Wastes $N^2$ matrix memory and slower than Two Pointers. |
| **Expand Around Center (Yours!)** | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | 🏆 **FAANG Gold Standard** — Intuitive, zero DP table overhead, beats 92% memory. |
| **Manacher's Algorithm** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | 🤓 Overkill trivia; interviewers never expect you to code Manacher's from memory. |
