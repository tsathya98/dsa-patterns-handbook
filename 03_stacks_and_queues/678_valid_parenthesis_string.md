# 🎯 LeetCode 678: Valid Parenthesis String – Master Study Guide

> **Difficulty:** Medium | **Pattern:** Two Stacks (Indices) / Greedy Range  
> **Complexity:** Time: $\mathcal{O}(n)$ | Auxiliary Space: $\mathcal{O}(n)$  
> **Source Code:** [`678_valid_parenthesis_string.py`](./678_valid_parenthesis_string.py)

---

## 📌 Problem in Plain English

Given a string `s` containing `'('`, `')'`, and `'*'`. Return `true` if valid:
1. `'('` must be closed by `')'`.
2. `'*'` is a **wildcard joker** 🃏:
   * It can be `'('`
   * It can be `')'`
   * It can be empty `""` (disappear!)

---

## ⚠️ Why `s.replace("*", ")")` Fails (The Trap)

When you do `s.replace("*", ")")`, you force **EVERY single star** in the string to make the exact same choice!
* In reality, **each star is independent**:
  * Star 1 might want to be `'('`
  * Star 2 might want to be `')'`
  * Star 3 might want to disappear `""`

---

## 🧠 Mental Model: The Two Stacks (Index Bookkeeping)

Instead of storing characters, **store the index positions** in two stacks:
1. `open_stack`: indices of `'('`
2. `star_stack`: indices of `'*'`

```text
String:   (   *   )
Index:    0   1   2

open_stack: [0]
star_stack: [1]
```

### The 2 Rules:

#### Rule 1: When you see `')'`
* If we have a real `'('`, pop it! (`open_stack.pop()`)
* Otherwise, if we have a `'*'`, use it as a substitute `'('`! (`star_stack.pop()`)
* If neither exists, we have an orphan `')'` $\to$ **Impossible! Return `False`**.

#### Rule 2: At the end, clean up leftover `'('`
Can our leftover stars close our leftover open brackets?
* A `'*'` can ONLY close a `'('` if it appears **AFTER** it!
* If `open_stack[-1] < star_stack[-1]`: pop both! ✅
* If `open_stack[-1] > star_stack[-1]`: e.g. `*(` $\to$ star is behind the bracket, so it can never close it! ❌ **Return `False`**.

Any leftover stars at the end? They just become empty strings `""`.

---

## 💻 Clean Implementation

```python
class Solution:
    def checkValidString(self, s: str) -> bool:
        open_stack = []  # stores indices of '('
        star_stack = []  # stores indices of '*'
        
        for i, ch in enumerate(s):
            if ch == '(':
                open_stack.append(i)
            elif ch == '*':
                star_stack.append(i)
            else:  # ch == ')'
                if open_stack:
                    open_stack.pop()
                elif star_stack:
                    star_stack.pop()
                else:
                    return False
        
        # Match leftover '(' with '*' that come AFTER them
        while open_stack and star_stack:
            if open_stack[-1] < star_stack[-1]:
                open_stack.pop()
                star_stack.pop()
            else:
                return False
                
        return len(open_stack) == 0
```

---

## ⚡ Complexity
* **Time Complexity:** $\mathcal{O}(n)$ – single pass to scan characters, followed by at most $\mathcal{O}(n)$ pops.
* **Space Complexity:** $\mathcal{O}(n)$ – index stacks.
