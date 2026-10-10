# 🎯 LeetCode 125: Valid Palindrome – Master Study Guide

> **Difficulty:** Easy | **Pattern:** Two Pointers Formation A (Inward Squeeze)  
> **Complexity:** Time: $\mathcal{O}(n)$ | Auxiliary Space: $\mathcal{O}(1)$ (In-place, beats 95% memory!)  
> **Source Code:** [`125_valid_palindrome.py`](./125_valid_palindrome.py)

---

## 📌 Problem in Plain English

A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.
* Letters and numbers count.
* Spaces, commas, colons, punctuation do not count.

```text
Example 1:
Input:  s = "A man, a plan, a canal: Panama"
Cleaned: "amanaplanacanalpanama"
Result: True (reads identical in reverse)

Example 2:
Input:  s = "race a car"
Result: False ('e' != 'a')

Example 3:
Input:  s = "0P"
Result: False ('0' != 'p')
```

---

## 🧠 Mental Model: The Inward Squeeze

Instead of allocating a whole new string with regex or list comprehensions ($\mathcal{O}(n)$ space trap), use two pointers squeezing inward:
* Pointer `l` starts at the front (`0`).
* Pointer `r` starts at the back (`len(s) - 1`).

```text
  l ->                                      <- r
 "A   m a n ,   a   p l a n . . .   P a n a m a"
```

### The Squeeze Logic:
1. If `s[l]` is punctuation/space $\to$ skip it forward (`l += 1`).
2. If `s[r]` is punctuation/space $\to$ skip it backward (`r -= 1`).
3. If both are alphanumeric:
   * Compare lowercased: `s[l].lower() == s[r].lower()`.
   * Match? Advance both inward (`l += 1`, `r -= 1`).
   * Mismatch? **Immediately return `False`**.
4. If pointers cross without mismatch $\to$ **Return `True`**.

---

## 💻 Production Implementation

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

---

## ⚡ Complexity & FAANG Trade-offs

| Approach | Time | Space | Verdict in FAANG Interview |
|---|---|---|---|
| Filter string + Reverse `s[::-1]` | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Works, but creates 2 new string copies. Rejected for $\mathcal{O}(1)$ follow-up. |
| **Two Pointers Squeeze (Yours!)** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | 🏆 **Optimal**. Zero memory allocated, early termination on first mismatch. |
