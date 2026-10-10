# 🧱 LeetCode 20: Valid Parentheses – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** NeetCode 150 / Top Interview 150 / Blind 75  
> **Pattern:** Stack (Last-In, First-Out) & The "Push-Expected" Optimization  
> **LeetCode Link:** [LeetCode 20: Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

---

## 📌 Problem in Plain English

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

A string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

```text
Example 1: s = "()"       -> True
Example 2: s = "()[]{}"   -> True
Example 3: s = "(]"       -> False
Example 4: s = "([])"     -> True
Example 5: s = "([)]"     -> False (Order violation!)
```

---

## 🎒 The "Aha!" Mental Model: The Cafeteria Plate Stack

Think of a **spring-loaded cafeteria tray dispenser**:
* When you see an open bracket, you **push a plate onto the stack**.
* The **last plate added** is always the **first plate removed** (**LIFO** - Last In, First Out).
* If you put down a Round plate `(`, then a Square plate `[`, the **very next plate you take off MUST be a Square plate `]`**!
* If someone tries to take off a Round plate while the Square plate is still on top, **the entire stack crashes!**

```text
Input: s = " ( [ ] ) "

Step 1: see '(' -> push '('
        [ ( ]

Step 2: see '[' -> push '['
        [ [ ]  <- TOP OF STACK
        [ ( ]

Step 3: see ']' -> must match TOP OF STACK!
        Matches '['! Pop '['!
        [ ( ]

Step 4: see ')' -> must match TOP OF STACK!
        Matches '('! Pop '('!
        [   ]  <- STACK IS EMPTY!

Valid! Return True!
```

---

## ⚡ The 4 Speed Optimizations (3 ms ➔ 0 ms)

| Issue in Common Solutions | The High-Performance Fix | Performance Impact |
| :--- | :--- | :--- |
| **Odd length processed through full loop** | `if len(s) % 2 != 0: return False` | **Instant $\mathcal{O}(1)$ exit** on odd strings (e.g. `s = "]"`) |
| `for i in range(len(s)): s[i]` | `for ch in s:` | Eliminates index generation and bounds checking |
| `if len(stack) == 0:` | `if not stack:` | Uses direct CPython pointer truthiness |
| Separate `stack[-1]` peek and `stack.pop()` | `if not stack or stack.pop() != ch:` | Combines peek, pop, and comparison in **1 step** |

---

## 📥 The "Push-Expected" Pattern (Top FAANG Optimization)

Instead of pushing opening brackets and constantly looking up a closing-to-opening map:

> **When you see an OPENING bracket, push the CLOSING bracket you EXPECT to see later!**

```text
When you see:       Push this to stack:
     '('        ──►        ')'
     '['        ──►        ']'
     '{'        ──►        '}'
```

### Why this is brilliant:
When you encounter a closing bracket (`')'`), **you don't even need a dictionary lookup!** You just pop and compare directly:
```python
elif not stack or stack.pop() != ch:
    return False
```
This **cuts dictionary lookups by 50%**!

---

## 💻 Complete Production Code (0 ms / Beats 100%)

```python
class Solution:
    def isValid(self, s: str) -> bool:
        # 1. Instant early exit: valid parentheses must come in pairs!
        if len(s) % 2 != 0:
            return False

        # 2. Map open bracket to what we EXPECT to close it
        mapping = {'(': ')', '[': ']', '{': '}'}
        stack = []

        # 3. Direct C iteration (fastest loop in Python)
        for ch in s:
            if ch in mapping:
                stack.append(mapping[ch])  # Push expected closer!
            elif not stack or stack.pop() != ch:
                return False

        # 4. If stack is empty, every bracket was matched cleanly
        return not stack
```

---

## 📊 Complexity Analysis

* **Time Complexity:** $\mathcal{O}(n)$ — We process each character in the string at most twice (one push, one pop).
* **Space Complexity:** $\mathcal{O}(n)$ — In the worst case (e.g., `s = "(((((("`), the stack stores all $n$ characters.

---

## ⚠️ Common Traps & Pitfalls

1. **Closing Bracket First:** `s = "]"`  
   Attempting `stack.pop()` when the stack is empty will crash with `IndexError: pop from empty list`.  
   Always protect with `if not stack:`.
2. **Leftover Opening Brackets:** `s = "(("`  
   The loop finishes with no errors, but the stack still has elements! Always check `return not stack` (not `return True`).
3. **Misnesting:** `s = "([)]"`  
   Open brackets must close in reverse order. Stacks naturally handle this order invariant.
