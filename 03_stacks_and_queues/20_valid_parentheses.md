# LeetCode 20: Valid Parentheses

> **Pattern:** LIFO stack + push-expected closer  
> **Difficulty:** Easy  
> **Link:** [LeetCode 20](https://leetcode.com/problems/valid-parentheses/)

## The problem

Given a string `s` containing only `'('`, `')'`, `'{'`, `'}'`, `'['`, and `']'`, return `True` if every opening bracket is closed by the same type of bracket in the proper nested order, and `False` otherwise.

```text
s = "()[]{}"  -> True
s = "([])"    -> True
s = "(]"      -> False
s = "([)]"    -> False (inner '[' must close before outer '(')
```

## The core trick

Brackets follow Last-In, First-Out (LIFO) order: the most recently opened bracket must be the very first one closed. That maps directly to a stack.

A clean way to avoid dictionary lookups on closing brackets is the push-expected trick:
- Whenever you see an opening bracket (`'('`, `'['`, `'{'`), push the **closing bracket you expect to see later** (`')'`, `']'`, `'}'`) onto the stack.
- Whenever you see a closing bracket, check that the stack is non-empty and that `stack.pop()` equals the current character. If the stack is empty or the popped closer does not match, return `False` immediately.
- Also check `if len(s) % 2 != 0: return False` right at the start, since any odd-length string cannot pair up evenly.

## Step-by-step trace

Trace on `s = "([])"`:

```text
Step 1: ch = '(' (open)  -> push expected closer ')'
        stack: [ ')' ]

Step 2: ch = '[' (open)  -> push expected closer ']'
        stack: [ ')', ']' ]  <- top of stack

Step 3: ch = ']' (close) -> pop top (']') == ']' (match)
        stack: [ ')' ]

Step 4: ch = ')' (close) -> pop top (')') == ')' (match)
        stack: []

End of string: stack is empty -> return True
```

## Traps to watch for

- **Closing bracket on an empty stack (`s = "]"`):** Calling `stack.pop()` on an empty list raises an `IndexError`. Always guard with `if not stack or stack.pop() != ch:`.
- **Returning `True` unconditionally after the loop (`s = "(("`):** If the string only has opening brackets, the loop finishes without a mismatch, but unmatched items remain on the stack. Always `return not stack`.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2 != 0:
            return False

        expected = {'(': ')', '[': ']', '{': '}'}
        stack = []

        for ch in s:
            if ch in expected:
                stack.append(expected[ch])
            elif not stack or stack.pop() != ch:
                return False

        return not stack
```

</details>

## Complexity

- **Time:** $\mathcal{O}(n)$ single pass (each character is pushed and popped at most once).
- **Space:** $\mathcal{O}(n)$ in the worst case when the input is all opening brackets.
