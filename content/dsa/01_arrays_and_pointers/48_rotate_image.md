# LeetCode 48: Rotate Image

> **Difficulty:** Medium | **Pattern:** 2D In-Place Matrix Decomposition  
> **Source Code:** [`48_rotate_image.py`](48_rotate_image.py) | **Link:** [LeetCode 48](https://leetcode.com/problems/rotate-image/)

## The problem

You are given an $N \times N$ 2D matrix representing an image. Rotate the image by **90 degrees clockwise** in-place without allocating a second matrix ($\mathcal{O}(1)$ auxiliary space).

```text
Input:
[ 1, 2, 3 ]
[ 4, 5, 6 ]
[ 7, 8, 9 ]

Output:
[ 7, 4, 1 ]
[ 8, 5, 2 ]
[ 9, 6, 3 ]
```

---

## The Core Trick: Geometric Decomposition

A 90° clockwise rotation can be decomposed into two $\mathcal{O}(1)$ space primitive operations. You can execute them in either order:

### Way A (Reverse rows top-to-bottom, then Transpose)
```text
Original          Reverse Rows (Vertical Flip)       Transpose
1  2  3              7  8  9                          7  4  1
4  5  6    --->      4  5  6                --->      8  5  2
7  8  9              1  2  3                          9  6  3
```

### Way B (Transpose, then Reverse each row left-to-right)
```text
Original              Transpose              Reverse Each Row (Horizontal Flip)
1  2  3                1  4  7                           7  4  1
4  5  6      --->      2  5  8                 --->      8  5  2
7  8  9                3  6  9                           9  6  3
```

---

## The Critical Gotcha: Upper-Triangle Transpose

When transposing, **only iterate over the upper triangle** (`j` from `i + 1` to `n - 1`):
```python
for i in range(n):
    for j in range(i + 1, n):  # Start at i + 1, NEVER 0!
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```
If `j` started at `0`, you would swap cell `(i, j)` with `(j, i)`, and then later swap `(j, i)` back with `(i, j)`, canceling out the transpose and leaving the matrix unchanged.

---

### Algorithm steps:

* **1. Vertical flip:** Reverse the outer list `matrix.reverse()` to swap rows top-to-bottom in $\mathcal{O}(N)$ time.
* **2. Transpose across diagonal:** Loop row `i` from `0` to `n - 1` and col `j` from `i + 1` to `n - 1`. Swap `matrix[i][j]` with `matrix[j][i]`.
* **3. In-place completion:** The matrix is now rotated 90° clockwise with zero auxiliary allocations.

---

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        # Step 1: Vertical flip (Reverse rows top-to-bottom)
        matrix.reverse()

        # Step 2: Transpose across main diagonal
        n = len(matrix)
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```

</details>

---

## Complexity

- **Time:** $\mathcal{O}(N^2)$ where $N$ is the matrix dimension. Reversing rows takes $\mathcal{O}(N)$ swaps, and the transpose takes $\frac{N(N - 1)}{2}$ swaps.
- **Space:** $\mathcal{O}(1)$ auxiliary memory (purely in-place swaps).
