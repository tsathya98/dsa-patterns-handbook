# 🪟 LeetCode 1456: Maximum Number of Vowels in a Substring of Given Length

> **Difficulty:** Medium  
> **Study Plan:** LeetCode 75  
> **Pattern:** Fixed-Size Sliding Window (Running Differential on Frequencies)  
> **LeetCode Link:** [LeetCode 1456: Maximum Number of Vowels](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/)

---

## 📌 Problem in Plain English

Given a string `s` and an integer `k`, return the maximum number of vowel letters (`'a'`, `'e'`, `'i'`, `'o'`, `'u'`) in any substring of `s` with length `k`.

### Example:
```text
Input: s = "abciiidef", k = 3
Output: 3
Explanation: The substring "iii" contains 3 vowel letters.
```

---

## 💡 The "Aha!" Moment: Running Differential on Counters

### Why Brute Force Fails (TLE on testcase 104/107):
* Slicing `s[i:i+k]` and checking every letter with an inner loop takes $\mathcal{O}(k)$ time per position.
* When `len(s) = 100,000` and `k = 50,436`:
  $$\text{Operations} \approx 50,000 \times 50,000 = \mathbf{2,500,000,000} \text{ (2.5 billion) } \implies \text{TLE!}$$

### The Sliding Window Insight (The VIP Room Analogy):
You cannot do arithmetic (`+`, `-`) directly on letters, but you **can** do arithmetic on your **integer vowel score**:
1. When a new character enters the window on the right (`s[i]`):
   * Is it a vowel? $\implies \text{count} += 1$
2. When an old character leaves the window on the left (`s[i - k]`):
   * Was it a vowel? $\implies \text{count} -= 1$

---

## 💻 Clean $\mathcal{O}(n)$ Solution

```python
class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = {'a', 'e', 'i', 'o', 'u'}
        
        # 1. Base window: count vowels in the first k characters
        count = 0
        for i in range(k):
            if s[i] in vowels:
                count += 1
                
        max_count = count
        if max_count == k:  # Early exit: can't beat k vowels!
            return k
            
        # 2. Slide window from index k to the end
        for i in range(k, len(s)):
            # Add new character entering on right (use i!)
            if s[i] in vowels:
                count += 1
            # Subtract old character leaving on left (use i - k!)
            if s[i - k] in vowels:
                count -= 1
                
            if count > max_count:
                max_count = count
                if max_count == k:
                    return k
                    
        return max_count
```

---

## ⚠️ The Two Big Interview Traps for this Problem

### 1. The `s[k]` vs `s[i]` Indexing Typo:
* **The bug:** Writing `if s[k] in vowels: count += 1` inside the loop.
* **What happens:** As `i` moves forward, `s[k]` keeps checking the exact same index $k$ over and over again instead of the new entering character!
* **The rule:** The entering element is always **`s[i]`**, and the leaving element is always **`s[i - k]`**.

### 2. The "Can `count` drop below 0?" Myth:
* Beginners often write:
  ```python
  if count < 0:
      count = 0  # ❌ Unnecessary defensive code!
  ```
* **Why it's mathematically impossible for `count` to be negative:**
  * Every character that leaves (`s[i - k]`) was **previously added** when it entered!
  * You only subtract if `s[i - k] in vowels` is `True`.
  * If it is a vowel, `count` was already $\ge 1$.
  * Therefore: **$0 \le \text{count} \le k$ at all times.**
