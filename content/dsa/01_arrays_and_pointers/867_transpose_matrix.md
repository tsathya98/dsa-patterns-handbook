# LeetCode 867: Transpose Matrix

> **Difficulty:** Easy | **Pattern:** 2D Coordinate Transformation  
> **Source Code:** [`867_transpose_matrix.py`](867_transpose_matrix.py) | **Link:** [LeetCode 867](https://leetcode.com/problems/transpose-matrix/)

## The problem

Given a 2D integer array `matrix`, return the transpose of `matrix`.
The transpose of a matrix is the matrix flipped over its main diagonal, switching the matrix's row and column indices (`matrix[r][c] -> mat[c][r]`).

```text
Input:  matrix = [[1, 2, 3], [4, 5, 6]]
Output: [[1, 4], [2, 5], [3, 6]]

Original (2 rows x 3 cols):
[ 1, 2, 3 ]
[ 4, 5, 6 ]

Transposed (3 rows x 2 cols):
[ 1, 4 ]
[ 2, 5 ]
[ 3, 6 ]
```

---

## Core gotchas to watch for

### 1. Dimension reversal on non-square grids
If the input has `R = len(matrix)` rows and `C = len(matrix[0])` columns, the transposed matrix **must have `C` rows and `R` columns**. Writing `mat[i][j] = matrix[j][i]` without swapping the dimension loop bounds triggers an `IndexError`.

### 2. The list multiplication pointer trap
Never initialize 2D grids using `[[0] * R] * C`.
Lists are mutable objects in Python. The outer `* C` duplicates pointers to the exact same inner list. Always allocate independent rows using list comprehension:
```python
mat = [[0 for _ in range(R)] for _ in range(C)]
```

### 3. Slicing does not extract columns
In standard Python, `matrix[:][i]` does not grab column `i`. It slices the outer list and returns row `i`. You must access elements individually or use `zip(*matrix)`.

---

## Visual walkthrough

```text
Cell-by-cell mapping:
matrix[0][0] = 1  --->  mat[0][0] = 1
matrix[0][1] = 2  --->  mat[1][0] = 2
matrix[0][2] = 3  --->  mat[2][0] = 3
matrix[1][0] = 4  --->  mat[0][1] = 4
matrix[1][1] = 5  --->  mat[1][1] = 5
matrix[1][2] = 6  --->  mat[2][1] = 6
```

---

### Algorithm steps:

* **1. Measure dimensions:** Let `R = len(matrix)` and `C = len(matrix[0])`.
* **2. Allocate output canvas:** Build `mat` with `C` rows and `R` columns using list comprehension.
* **3. Map coordinates:** For each row `i` from `0` to `R - 1` and col `j` from `0` to `C - 1`, set `mat[j][i] = matrix[i][j]`.
* **4. Return result:** Return `mat`.

---

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def transpose(self, matrix: list[list[int]]) -> list[list[int]]:
        R = len(matrix)
        C = len(matrix[0])

        # Allocate new matrix of size C rows x R cols
        mat = [[0 for _ in range(R)] for _ in range(C)]

        for i in range(R):
            for j in range(C):
                mat[j][i] = matrix[i][j]

        return mat
```

### The 1-Line Python Alternative (`zip` trick):
```python
class Solution:
    def transpose(self, matrix: list[list[int]]) -> list[list[int]]:
        return [list(col) for col in zip(*matrix)]
```

</details>

---

## Complexity

- **Time:** $\mathcal{O}(R \cdot C)$ (or $\Omega(N)$ where $N$ is total elements). Every element must be read and written once.
- **Space:** $\mathcal{O}(R \cdot C)$ auxiliary memory to store the newly shaped output matrix.
