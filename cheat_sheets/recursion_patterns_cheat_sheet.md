# Recursion & Backtracking Patterns Cheat Sheet

> Patterns sourced from: InterviewCoach DSA Python Cohort, FAANG Interview Standards

Recursion is breaking a problem down into smaller self-similar subproblems until reaching a trivial base case. Backtracking is recursion with state restoration (`path.pop()`) when a path leads to a dead end.

---

## 1. Recursion Architecture: Head vs. Tail Recursion

```text
Problem: Print numbers from 1 to N

Tail Recursion (Work on the way DOWN):
def print_1_to_n(i, n):
    if i > n: return
    print(i)                 # Work BEFORE recursive call
    print_1_to_n(i + 1, n)

Head / Backtrack Recursion (Work on the way UP):
def print_1_to_n(n):
    if n == 0: return
    print_1_to_n(n - 1)      # Dive to base case first
    print(n)                 # Work AFTER unwinding call stack
```

### Algorithm steps:
* **1. Recursive descent:** Call `print_1_to_n(n - 1)` before executing any print logic, pushing each frame onto the call stack until hitting `n == 0`.
* **2. Base case guard:** When `n == 0`, immediately return to stop further recursive calls.
* **3. Post-recursion unwinding:** As each stack frame pops in reverse order (from `1` up to `n`), execute `print(n)` to produce ascending output in $\mathcal{O}(n)$ time and $\mathcal{O}(n)$ call stack depth.


---

## 2. Pattern 1: Divide and Conquer on Operators (LC 241)

When an expression contains operators (`+`, `-`, `*`), split at **every operator index**, recursively compute all possible values for the left sub-expression and right sub-expression, and combine them.

### Algorithm steps:
* **1. Operator pivot scan:** Iterate through each character of the string to find every arithmetic operator (`+`, `-`, `*`).
* **2. Independent branch evaluation:** Split the expression into `left = expression[:i]` and `right = expression[i + 1:]`, recursively evaluating all possible outcomes for both sides.
* **3. Cartesian combination:** Combine each result `l` from the left branch with each result `r` from the right branch using the pivot operator, returning raw integer values when no operators exist.


```python
def diffWaysToCompute(expression: str) -> list[int]:
    res = []
    for i, ch in enumerate(expression):
        if ch in "+-*":
            left = diffWaysToCompute(expression[:i])
            right = diffWaysToCompute(expression[i + 1:])
            for l in left:
                for r in right:
                    if ch == '+': res.append(l + r)
                    elif ch == '-': res.append(l - r)
                    elif ch == '*': res.append(l * r)
    return res if res else [int(expression)]
```

---

## 3. Pattern 2: Observation & Symmetry Tree (LC 779)

In problems where rows generate binary sequences by replacing `0 -> 01` and `1 -> 10`:
1. Row $N$ has $2^{N-1}$ numbers.
2. The **first half** of row $N$ is identical to row $N - 1$.
3. The **second half** of row $N$ is the exact bitwise inverse (`1 - val`) of row $N - 1$ shifted by $mid = 2^{N-2}$.

```text
Row 1: 0
Row 2: 0 1
Row 3: 0 1 1 0
Row 4: 0 1 1 0 1 0 0 1
       [-- same as R3 --] [-- flipped R3 --]
```

```python
def kthGrammar(n: int, k: int) -> int:
    if n == 1 and k == 1:
        return 0
    mid = 2 ** (n - 2)
    if k <= mid:
        return kthGrammar(n - 1, k)
    return 1 - kthGrammar(n - 1, k - mid)
```

---

## 4. Pattern 3: O(1) Pruned Backtracking (N-Queens, LC 51)

Instead of scanning the whole $N \times N$ chessboard to check if a square is safe ($\mathcal{O}(N)$ check), use three sets with $\mathcal{O}(1)$ mathematical properties:
1. `cols`: Column index `col`.
2. `diag`: Main diagonal constant `row - col`.
3. `anti_diag`: Anti-diagonal constant `row + col`.

```text
Chessboard diagonals:
Main diagonals (row - col):
  (0,0)=0   (0,1)=-1  (0,2)=-2
  (1,0)=1   (1,1)=0   (1,2)=-1
  (2,0)=2   (2,1)=1   (2,2)=0

Anti-diagonals (row + col):
  (0,0)=0   (0,1)=1   (0,2)=2
  (1,0)=1   (1,1)=2   (1,2)=3
  (2,0)=2   (2,1)=3   (2,2)=4
```

```python
def solveNQueens(n: int) -> list[list[str]]:
    res = []
    board = [["."] * n for _ in range(n)]
    cols, diag, anti_diag = set(), set(), set()

    def backtrack(r: int) -> None:
        if r == n:
            res.append(["".join(row) for row in board])
            return

        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti_diag:
                continue

            board[r][c] = "Q"
            cols.add(c); diag.add(r - c); anti_diag.add(r + c)

            backtrack(r + 1)

            board[r][c] = "."
            cols.remove(c); diag.remove(r - c); anti_diag.remove(r + c)

    backtrack(0)
    return res
```

---

## 5. Pattern 4: Pick vs. Skip Decision Trees (Subsets, LC 78)

For subset generation, there are two standard implementations:

### Method A: Pick vs. Skip (Binary Tree)
At each element, make exactly two recursive branches:
1. Pick `nums[i]`: append, recurse, pop.
2. Skip `nums[i]`: recurse without appending.

### Method B: Loop over remaining choices
Loop `j` from `start` to `len(nums) - 1`, append `nums[j]`, recurse with `j + 1`, and pop. Every state reached is a valid subset.

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res, path = [], []
    def backtrack(start: int) -> None:
        res.append(path[:])  # Copy path
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    backtrack(0)
    return res
```
