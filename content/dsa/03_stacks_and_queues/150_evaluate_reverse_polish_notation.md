# LeetCode 150: Evaluate Reverse Polish Notation

> **Difficulty:** Medium | **Pattern:** LIFO Stack (Postfix Expression Evaluation)  
> **Source Code:** [`150_evaluate_reverse_polish_notation.py`](150_evaluate_reverse_polish_notation.py) | **Link:** [LeetCode 150](https://leetcode.com/problems/evaluate-reverse-polish-notation/)

## The problem

Evaluate the value of an arithmetic expression in Reverse Polish Notation (postfix).
Valid operators are `+`, `-`, `*`, and `/`.
Each operand may be an integer or another expression.
Division between two integers must truncate toward zero.

```text
Input:  tokens = ["2", "1", "+", "3", "*"]
Output: 9  ((2 + 1) * 3 = 9)

Input:  tokens = ["4", "13", "5", "/", "+"]
Output: 6  (4 + (13 / 5) = 6)
```

---

## The two interview traps

1. **Operand order upon popping**:
   The stack pops the most recent item first.
   The first popped element is the **right** operand. The second popped element is the **left** operand.
   Writing `a - b` instead of `b - a` will produce the wrong sign on subtraction and incorrect quotient on division.

2. **Division truncation toward zero**:
   Python's floor division operator `//` rounds toward negative infinity (`-3 // 2 == -2`).
   The problem specifies truncation toward zero (`-3 / 2 == -1.5 -> -1`).
   Use `int(left / right)` to ensure proper float-to-int zero-truncation.

---

## Visual walkthrough

Tracing `tokens = ["4", "13", "5", "/", "+"]`:

```text
Token   Action             Stack (bottom -> top)
-------------------------------------------------
"4"     Push operand       [ 4 ]
"13"    Push operand       [ 4, 13 ]
"5"     Push operand       [ 4, 13, 5 ]
"/"     Pop 5 (right)
        Pop 13 (left)
        int(13 / 5) = 2
        Push result        [ 4, 2 ]
"+"     Pop 2 (right)
        Pop 4 (left)
        4 + 2 = 6
        Push result        [ 6 ]

End: return stack[0] -> 6
```

---

### Algorithm steps:

* **1. Initialize stack and operator set:** Create `stack = []` and `ops = {"+", "-", "*", "/"}`.
* **2. Iterate tokens:** For each token:
  * If token is not an operator, convert to `int(token)` and push to `stack`.
  * If token is an operator, pop `right = stack.pop()` and `left = stack.pop()`.
  * Compute the result according to the operator (`left + right`, `left - right`, `left * right`, or `int(left / right)`).
  * Push the computed result back onto `stack`.
* **3. Return final result:** Return `stack[0]`.

---

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack: list[int] = []
        ops = {"+", "-", "*", "/"}

        for token in tokens:
            if token not in ops:
                stack.append(int(token))
            else:
                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "*":
                    stack.append(left * right)
                else:
                    stack.append(int(left / right))

        return stack[0]
```

</details>

---

## Complexity

- **Time:** $\mathcal{O}(N)$ where $N$ is the length of `tokens`. Each token is pushed and popped at most once.
- **Space:** $\mathcal{O}(N)$ auxiliary memory for the stack storing operands.
