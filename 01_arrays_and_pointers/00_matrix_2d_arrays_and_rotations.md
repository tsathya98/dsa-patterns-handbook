# 🧊 2D Matrices, Diagonals & In-Place Rotations

> **Course Reference:** CodeKerdos DSA — Class 7  
> **Core Concepts:** Diagonal coordinate invariants ($i+j$, $i-j$), in-place matrix transpose, 90° clockwise/anticlockwise rotation, and 4-pointer spiral traversal.

---

## 1. 2D Arrays in Python Memory

In Python, a 2D array is a **list of lists**:
```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```
* `rows = len(matrix)`
* `cols = len(matrix[0])`
* `matrix[r][c]` accesses row `r`, column `c`.

---

## 2. Diagonals & The Coordinate Sum Invariant

For an $N \times N$ square matrix:

```text
Indices (i, j):
  (0,0)   (0,1)   (0,2)
  (1,0)   (1,1)   (1,2)
  (2,0)   (2,1)   (2,2)
```

### The Invariants:
1. **Principal Diagonal (Top-Left to Bottom-Right):**
   * Row index equals column index: **$i == j$**.
2. **Anti-Diagonal (Top-Right to Bottom-Left):**
   * Sum of row and column index is constant: **$i + j == N - 1$**.
3. **All Right-to-Left Diagonals:**
   * Total diagonals = $2N - 1$.
   * Every element on the same diagonal shares the exact same sum $s = i + j$ ($0 \le s \le 2N - 2$).

```python
def print_all_anti_diagonals(matrix: list[list[int]]) -> list[list[int]]:
    n = len(matrix)
    result = []
    for s in range(2 * n - 1):
        diagonal = []
        for i in range(n):
            j = s - i
            if 0 <= j < n:
                diagonal.append(matrix[i][j])
        result.append(diagonal)
    return result
```

---

## 3. In-Place Matrix Transpose

**Transposing** a matrix swaps rows and columns: `matrix[i][j] <-> matrix[j][i]`.

> ⚠️ **The Double-Swap Trap:**  
> If your loop visits every cell $(i, j)$, you will swap `(0, 1)` with `(1, 0)`, and later swap `(1, 0)` with `(0, 1)` back to the original!  
> **Rule:** Only loop for **$j > i$** (the upper triangle above the main diagonal).

```python
def transpose_in_place(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```
* **Time Complexity:** $\mathcal{O}(N^2)$
* **Auxiliary Space:** $\mathcal{O}(1)$ (pure in-place).

---

## 4. Rotate Matrix 90° In-Place (LeetCode 48)

How do you rotate an $N \times N$ matrix 90 degrees clockwise without allocating an $N \times N$ new matrix?

### The Two-Step Formula:
$$\text{90° Clockwise Rotation} = \text{Transpose} + \text{Reverse Each Row}$$

```text
Original:
[ 1 , 2 , 3 ]
[ 4 , 5 , 6 ]
[ 7 , 8 , 9 ]

Step 1: Transpose (Swap across main diagonal):
[ 1 , 4 , 7 ]
[ 2 , 5 , 8 ]
[ 3 , 6 , 9 ]

Step 2: Reverse every row (Inward squeeze):
[ 7 , 4 , 1 ]
[ 8 , 5 , 2 ]
[ 9 , 6 , 3 ]  <-- Rotated 90° Clockwise!
```

```python
def rotate_90_clockwise(matrix: list[list[int]]) -> None:
    n = len(matrix)
    # 1. Transpose in-place
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            
    # 2. Reverse each row
    for row in matrix:
        row.reverse()
```

### What About 90° Anti-Clockwise?
$$\text{90° Anti-Clockwise Rotation} = \text{Transpose} + \text{Reverse Row Order (Flip Upside Down)}$$

```python
def rotate_90_anticlockwise(matrix: list[list[int]]) -> None:
    n = len(matrix)
    # 1. Transpose in-place
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            
    # 2. Reverse row order (flip vertically)
    matrix.reverse()
```

---

## 5. Spiral Matrix Traversal (LeetCode 54)

Traverse an $M \times N$ matrix in clockwise spiral order.

```text
top ───►  [ 1 ,  2 ,  3 ,  4 ]
          [ 5 ,  6 ,  7 ,  8 ]
bottom ─► [ 9 , 10 , 11 , 12 ]
            ▲              ▲
           left          right
```

### The 4 Boundary Pointers Pattern
Maintain 4 bounds: `top = 0`, `bottom = m - 1`, `left = 0`, `right = n - 1`.  
On each loop, perform 4 directional sweeps and shrink the boundaries:

1. **Left $\to$ Right** along `top` row $\to$ `top += 1`.
2. **Top $\to$ Bottom** along `right` column $\to$ `right -= 1`.
3. **Right $\to$ Left** along `bottom` row (only if `top <= bottom`!) $\to$ `bottom -= 1`.
4. **Bottom $\to$ Top** along `left` column (only if `left <= right`!) $\to$ `left += 1`.

```python
def spiralOrder(matrix: list[list[int]]) -> list[int]:
    if not matrix or not matrix[0]:
        return []

    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    result = []

    while top <= bottom and left <= right:
        # 1. Traverse top row
        for c in range(left, right + 1):
            result.append(matrix[top][c])
        top += 1

        # 2. Traverse right column
        for r in range(top, bottom + 1):
            result.append(matrix[r][right])
        right -= 1

        # 3. Traverse bottom row (guard against single remaining row)
        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1

        # 4. Traverse left column (guard against single remaining col)
        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1

    return result
```
* **Time Complexity:** $\mathcal{O}(M \times N)$ (Visits every cell exactly once).
* **Auxiliary Space:** $\mathcal{O}(1)$ (excluding output array).
