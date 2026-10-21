# LeetCode 1572: Matrix Diagonal Sum

> **Difficulty:** Easy | **Pattern:** Single-Loop Coordinate Formula (`mat[i][i]` and `mat[i][n - 1 - i]`)  
> **Source Code:** [`1572_matrix_diagonal_sum.py`](./1572_matrix_diagonal_sum.py) | **Link:** [LeetCode 1572](https://leetcode.com/problems/matrix-diagonal-sum/)

## The problem

Given a square matrix `mat` ($n \times n$), return the sum of the matrix diagonals. Include all elements on the primary diagonal and secondary diagonal without double-counting the center element when $n$ is odd.

```text
Input: mat = [[1,2,3],
              [4,5,6],
              [7,8,9]]
Output: 25 (Primary: 1 + 5 + 9 = 15; Secondary: 3 + 5 + 7 = 15; Center 5 counted once -> 25)
```

---

## Approach 1: Brute force (nested loops)

Scan every cell `(r, c)` in the $n \times n$ matrix with two loops.
A cell belongs to a diagonal if:
- Primary diagonal: `r == c`
- Secondary diagonal: `r + c == n - 1`

If either condition holds, add `mat[r][c]` to `total`.
* **Time:** $\mathcal{O}(N^2)$ full grid sweep.
* **Space:** $\mathcal{O}(1)$. Unnecessary work since diagonals contain only $2n - 1$ cells.

---

## Approach 2: Semi-optimized (single loop with in-loop branch)

Notice that row `i` only ever touches two diagonal cells: column `i` and column `n - 1 - i`.
Iterate `i` from $0 \dots n - 1$.
Inside the loop, check if `i == n - 1 - i`.
- If true (the center cell), add `mat[i][i]` once and `continue`.
- Otherwise, add both `mat[i][i] + mat[i][n - 1 - i]`.
* **Time:** $\mathcal{O}(N)$ single loop.
* **Space:** $\mathcal{O}(1)$. Solves the problem in optimal time, but runs an `if` check on every iteration.

---

## Approach 3: Optimized (branchless hot loop + single center deduction)

In an $n \times n$ matrix, `i == n - 1 - i` can happen at most once, and only when $n$ is odd (at row `n // 2`).
Instead of checking a condition on all $n$ iterations:
1. Always add `mat[i][i] + mat[i][n - 1 - i]` in the loop.
2. After the loop, if $n$ is odd (`n % 2 == 1`), subtract the center cell `mat[n // 2][n // 2]` once.

```text
Row 0:  mat[0][0] + mat[0][2] = 1 + 3 = 4
Row 1:  mat[1][1] + mat[1][1] = 5 + 5 = 10  (Center added twice)
Row 2:  mat[2][2] + mat[2][0] = 9 + 7 = 16
Running sum: 4 + 10 + 16 = 30
Subtract center once: 30 - 5 = 25
```

### Algorithm steps:
* **1. Initialize:** `n = len(mat)`, `total = 0`.
* **2. Loop:** For each `i` in `range(n)`:
  * `total += mat[i][i] + mat[i][n - 1 - i]`
* **3. Deduct overlap:** If `n % 2 == 1`:
  * `total -= mat[n // 2][n // 2]`
* **4. Return:** `total`.

---

<details>
<summary>Spoiler: Solution Code (All 3 Approaches)</summary>

```python
class Solution:
    # Approach 1: Brute Force (O(N^2) time, O(1) space)
    def diagonalSum_brute(self, mat: list[list[int]]) -> int:
        n = len(mat)
        total = 0
        for r in range(n):
            for c in range(n):
                if r == c or r + c == n - 1:
                    total += mat[r][c]
        return total

    # Approach 2: Semi-Optimized with in-loop check (O(N) time, O(1) space)
    def diagonalSum_semi_optimized(self, mat: list[list[int]]) -> int:
        n = len(mat)
        total = 0
        for i in range(n):
            if i == n - 1 - i:
                total += mat[i][i]
                continue
            total += mat[i][i] + mat[i][n - 1 - i]
        return total

    # Approach 3: Optimized branchless loop (O(N) time, O(1) space)
    def diagonalSum(self, mat: list[list[int]]) -> int:
        n = len(mat)
        total = 0
        for i in range(n):
            total += mat[i][i] + mat[i][n - 1 - i]

        if n % 2 == 1:
            total -= mat[n // 2][n // 2]

        return total
```

</details>

---

## Complexity comparison

| Approach | Time Complexity | Auxiliary Space | Status |
|---|---|---|---|
| **1. Brute Force** | $\mathcal{O}(N^2)$ | $\mathcal{O}(1)$ | Wasteful grid scan |
| **2. Semi-Optimized** | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Optimal time, in-loop branch |
| **3. Branchless Loop** | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Cleanest FAANG production code |
