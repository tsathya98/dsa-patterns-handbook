# 🪟 LeetCode 3: Longest Substring Without Repeating Characters – Master Study Guide

> **Difficulty:** Medium | **Pattern:** Dynamic Sliding Window (The Rubber Band)  
> **Complexity:** Time: $\mathcal{O}(n)$ | Auxiliary Space: $\mathcal{O}(\min(n, m))$ where $m \le 128$ ASCII chars  
> **Source Code:** [`3_longest_substring_without_repeating_characters.py`](./3_longest_substring_without_repeating_characters.py)

---

## 📌 Problem in Plain English

Given a string `s`, find the length of the **longest substring** without repeating characters.

```text
Example 1:
Input:  s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with length 3.

Example 2:
Input:  s = "bbbbb"
Output: 1
Explanation: The answer is "b", with length 1.

Example 3:
Input:  s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with length 3 ("pwke" is a subsequence, not a substring!).
```

---

## ⚠️ Why Brute Force Hits TLE (1028 / 1036 Passed)

If you check substrings from every index and do `len(tmp) == len(set(tmp))` inside a `while` loop:
1. **`set(tmp)` rebuilds a set from scratch on every single character**: That takes $\mathcal{O}(k)$ time per step.
2. **String slicing/appending `tmp += s[j]` creates new string copies** in memory.
3. Total time explodes to $\mathcal{O}(n^3)$, which passes small inputs but hits **Time Limit Exceeded** on inputs with thousands of characters.

---

## 🧠 Mental Model: The Rubber Band (Dynamic Sliding Window)

Instead of restarting the search or re-building sets, use a **Rubber Band window** `[left, right]`:
* `right` stretches the window forward, absorbing new characters.
* `seen` keeps track of characters currently inside the window.

```text
String:   a   b   c   a   b   c   b   b
Window:  [a   b   c]                              seen = {a, b, c}, len = 3
                  ↑ incoming 'a' is a duplicate!

Action:   Snap 'left' forward past the old 'a'!
Window:      [b   c   a]                          seen = {b, c, a}, len = 3
```

### The 2 Invariant Rules:
1. **Stretch (`right`):** Look at incoming character `s[right]`.
2. **Contract (`left`):** If `s[right]` is already in `seen`, contract the window by removing `s[left]` from `seen` and advancing `left += 1` until the duplicate is gone!
3. Add `s[right]` to `seen`, and record `max_len = max(max_len, right - left + 1)`.

---

## 💻 Production Implementation

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left = 0
        max_len = 0
        
        for right in range(len(s)):
            # While the incoming character is a duplicate, shrink from left
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
                
            seen.add(s[right])
            max_len = max(max_len, right - left + 1)
            
        return max_len
```

---

## ⚡ Complexity & FAANG Notes
* **Time Complexity:** $\mathcal{O}(n)$ – Each character enters `seen` once and leaves `seen` at most once (at most $2n$ total pointer moves).
* **Space Complexity:** $\mathcal{O}(\min(n, m))$ – The set never holds more than the character set size ($m \le 128$ for ASCII).
