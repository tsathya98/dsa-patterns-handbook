# 🧊 2D Matrix Manipulation Cheat Sheet

> **Scope:** Coordinate invariants, in-place transpositions, 90° rotations, and 4-pointer boundary traversal.

---

## 1. Diagonal Coordinate Invariants ($N \times N$ Matrix)

| Diagonal Type | Condition / Invariant | Number of Diagonals | Example |
|---|---|---|---|
| **Principal Diagonal** (Top-L $\to$ Bottom-R) | $i == j$ | $1$ | $(0,0), (1,1), (2,2)$ |
| **Anti-Diagonal** (Top-R $\to$ Bottom-L) | $i + j == N - 1$ | $1$ | $(0,2), (1,1), (2,0)$ |
| **All Right-to-Left Diagonals** | $s = i + j$ | $2N - 1$ ($s \in [0, 2N - 2]$) | Group by sum $s$ |
| **All Left-to-Right Diagonals** | $d = i - j$ | $2N - 1$ ($d \in [-(N-1), N - 1]$) | Group by difference $d$ |

---

## 2. In-Place Transformations (Zero Extra Memory)

### In-Place Transpose (Upper Triangle Loop)
Only loop for **$j > i$** to avoid double-swapping back:
```python
for i in range(n):
    for j in range(i + 1, n):
        matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```

### The 90° Rotation Formulas

$$\text{90° Clockwise Rotation} = \text{Transpose} + \text{Reverse Each Row}$$
```python
# 1. Transpose in-place (j > i)
# 2. Reverse each row
for row in matrix:
    row.reverse()
```

$$\text{90° Anti-Clockwise Rotation} = \text{Transpose} + \text{Reverse Row Order}$$
```python
# 1. Transpose in-place (j > i)
# 2. Reverse list of rows
matrix.reverse()
```

---

## 3. The 4-Pointer Spiral Matrix Box Pattern

```text
top ───►  [ 1 ,  2 ,  3 ,  4 ]
          [ 5 ,  6 ,  7 ,  8 ]
bottom ─► [ 9 , 10 , 11 , 12 ]
            ▲              ▲
           left          right
```

```python
top, bottom = 0, len(matrix) - 1
left, right = 0, len(matrix[0]) - 1
result = []

while top <= bottom and left <= right:
    # 1. Left to Right across top
    for c in range(left, right + 1):
        result.append(matrix[top][c])
    top += 1

    # 2. Top to Bottom down right
    for r in range(top, bottom + 1):
        result.append(matrix[r][right])
    right -= 1

    # 3. Right to Left across bottom (guard: top <= bottom)
    if top <= bottom:
        for c in range(right, left - 1, -1):
            result.append(matrix[bottom][c])
        bottom -= 1

    # 4. Bottom to Top up left (guard: left <= right)
    if left <= right:
        for r in range(bottom, top - 1, -1):
            result.append(matrix[r][left])
        left += 1
```
* **Time:** $\mathcal{O}(M \times N)$ | **Auxiliary Space:** $\mathcal{O}(1)$.
