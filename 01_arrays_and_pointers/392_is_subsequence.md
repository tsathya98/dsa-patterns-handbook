# 🎯 LeetCode 392: Is Subsequence – Master Study Guide

> **Difficulty:** Easy | **Pattern:** Two Pointers Formation C (Two Conveyor Belts)  
> **Complexity:** Time: $\mathcal{O}(|t|)$ | Auxiliary Space: $\mathcal{O}(1)$ (Beats 99% memory!)  
> **Source Code:** [`392_is_subsequence.py`](./392_is_subsequence.py)

---

## 📌 Problem in Plain English

Given two strings `s` and `t`, return `true` if `s` is a **subsequence** of `t`, or `false` otherwise.

> A **subsequence** means you can delete some (or zero) characters from `t` without changing the relative order of the remaining characters.

```text
Example 1:
Input:  s = "abc", t = "ahbgdc"
Output: True ('a', 'b', 'c' appear in order: a -> b -> c)

Example 2:
Input:  s = "axc", t = "ahbgdc"
Output: False ('x' never appears after 'a')
```

---

## 🧠 Mental Model: Two Conveyor Belts (Formation C)

Imagine two independent conveyor belts:
* **Belt 1 (`p1`):** The shopping checklist `s`. Only advances when an item is found!
* **Belt 2 (`p2`):** The supermarket warehouse stream `t`. Constantly moving forward looking for matches.

```text
Checklist (s):  [a]   b    c
                 ↑ p1

Stream (t):     [a]   h    b    g    d    c
                 ↑ p2
Match! Advance p1 -> 'b', advance p2 -> 'h'.
```

### The Invariants:
1. `p2` **always advances** on every step (`p2 += 1`) because we cannot rewind time in the warehouse stream.
2. `p1` **only advances** when `s[p1] == t[p2]`.
3. If `p1 == len(s)`, all checklist items were matched in order $\to$ **`True`**!

---

## 💻 Production Implementation

```python
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        p1, p2 = 0, 0
        
        while p1 < len(s) and p2 < len(t):
            if s[p1] == t[p2]:
                p1 += 1
            p2 += 1  # p2 moves every single step
            
        return p1 == len(s)
```

---

## ⚡ Complexity & Follow-up
* **Time Complexity:** $\mathcal{O}(|t|)$ – Single pass through `t`.
* **Auxiliary Space:** $\mathcal{O}(1)$ – Zero extra memory allocated.

### 💼 FAANG Follow-up Question:
> *"What if there are lots of incoming `s`, say $s_1, s_2, \dots, s_k$ where $k \ge 10^9$, and you want to check one by one against a fixed `t`?"*

* **Answer:** Preprocess `t` into a **HashMap of indices** (`char -> [idx1, idx2, ...]`). Then for each character in `s`, use **Binary Search (`bisect_right`)** to find the next valid index in $\mathcal{O}(|s| \log |t|)$ time instead of scanning `t` each time!
