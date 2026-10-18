# LeetCode 1572: Matrix Diagonal Sum

> **Difficulty:** Easy | **Pattern:** Single-Loop Index Coordinate Formula (`mat[i][i]` and `mat[i][n - 1 - i]`) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/matrix-diagonal-sum/](https://leetcode.com/problems/matrix-diagonal-sum/)

## The problem

Given a square matrix `mat` (`n x n`), return the sum of the matrix diagonals. Only include the sum of all the elements on the primary diagonal and all the elements on the secondary diagonal that are not part of the primary diagonal.

---

## Why an $\mathcal{O}(N^2)$ nested loop is unnecessary

In a square matrix of size `n x n`, every row `i` (from `0` to `n - 1`) contributes at most two diagonal cells:
* **Primary diagonal (top-left to bottom-right):** column is `c = i` -> `mat[i][i]`
* **Secondary diagonal (top-right to bottom-left):** column is `c = n - 1 - i` -> `mat[i][n - 1 - i]`

So you only need a single loop over `i in range(n)` in $\mathcal{O}(N)$ time!

---

## The core trick: Subtract the center cell if `n` is odd

When `n` is **odd** (e.g. `3 x 3`), the two diagonals cross at the exact center cell `(n // 2, n // 2)` where `i == n - 1 - i`.
Subtract `mat[n // 2][n // 2]` once at the end (or only add `mat[i][n - 1 - i]` when `i != n - 1 - i`).

---

## Step-by-step trace (`3 x 3` matrix)

```text
[ [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9] ]
```

**Iteration 1 (`i = 0`):**
Primary: `mat[0][0] = 1`. Secondary: `mat[0][2] = 3`.
```text
total = 1 + 3 = 4
```

**Iteration 2 (`i = 1`):**
Primary: `mat[1][1] = 5`. Secondary: `mat[1][1]` is the same cell (`i == 3 - 1 - 1`), so don't double-add!
```text
total = 4 + 5 = 9
```

**Iteration 3 (`i = 2`):**
Primary: `mat[2][2] = 9`. Secondary: `mat[2][0] = 7`.
```text
total = 9 + 9 + 7 = 25
```

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def diagonalSum(self, mat: list[list[int]]) -> int:
        n = len(mat)
        total = 0

        for i in range(n):
            total += mat[i][i]              # Primary diagonal
            total += mat[i][n - 1 - i]      # Secondary diagonal

        if n % 2 == 1:
            total -= mat[n // 2][n // 2]    # Remove center overlap when n is odd

        return total
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(N)$ where $N$ is the number of rows (faster than $\mathcal{O}(N^2)$).
* **Space:** $\mathcal{O}(1)$.
