# LeetCode 73: Set Matrix Zeroes

> **Difficulty:** Medium | **Pattern:** First Row & First Column as In-Place Marker Flags | **Access:** Free  
> **Link:** [https://leetcode.com/problems/set-matrix-zeroes/](https://leetcode.com/problems/set-matrix-zeroes/)

## The problem

Given an `m x n` integer `matrix`, if an element is `0`, set its entire row and column to `0` **in-place**.

---

## Why zeroing as you scan fails

If you immediately zero out row `r` and column `c` when you see `matrix[r][c] == 0`, the new zeroes you write will trigger chain-reaction zeroing later in your loop and wipe out the whole matrix.

---

## The core trick: Use Row 0 and Col 0 as $\mathcal{O}(1)$ marker arrays

1. **Method 1 ($\mathcal{O}(M + N)$ space):** Record `zero_rows = set()` and `zero_cols = set()` in Pass 1, then zero any cell `(r, c)` where `r in zero_rows or c in zero_cols` in Pass 2.
2. **Method 2 ($\mathcal{O}(1)$ space):** Instead of external sets, use the matrix's own **first row (`matrix[0][c]`)** and **first column (`matrix[r][0]`)** to store the zero flags! Since `matrix[0][0]` overlaps both Row 0 and Col 0, keep a single boolean `first_row_has_zero` to remember whether Row 0 itself started with a zero.

---

## Step-by-step trace (`Method 2: O(1) Space`)

**Initial matrix:**
```text
[ 1,  1,  1 ]
[ 1,  0,  1 ]   <- (1, 1) is 0
[ 1,  1,  1 ]
```

**Pass 1 (Mark Row 0 and Col 0 headers when `matrix[r][c] == 0`):**
At `(r=1, c=1)`, `matrix[1][1] == 0`, so set `matrix[1][0] = 0` (row header) and `matrix[0][1] = 0` (col header):
```text
      v (col 1 marked)
[ 1,  0,  1 ]
[ 0,  0,  1 ]  <- (row 1 marked)
[ 1,  1,  1 ]
```

**Pass 2 (Fill inner cells `(1..m-1, 1..n-1)` from headers):**
Check `if matrix[r][0] == 0 or matrix[0][c] == 0: matrix[r][c] = 0`:
```text
[ 1,  0,  1 ]
[ 0,  0,  0 ]  <- (1, 2) becomes 0 because matrix[1][0] == 0
[ 1,  0,  1 ]  <- (2, 1) becomes 0 because matrix[0][1] == 0
```

**Pass 3 (Zero Col 0 and Row 0 if their own flags were set):**
Neither `first_col_has_zero` nor `first_row_has_zero` was `True`, so we're done!

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def setZeroes(self, matrix: list[list[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        first_row_zero = any(matrix[0][c] == 0 for c in range(n))
        first_col_zero = any(matrix[r][0] == 0 for r in range(m))

        # 1. Mark row and col headers for inner cells
        for r in range(1, m):
            for c in range(1, n):
                if matrix[r][c] == 0:
                    matrix[r][0] = 0
                    matrix[0][c] = 0

        # 2. Zero out inner cells based on headers
        for r in range(1, m):
            for c in range(1, n):
                if matrix[r][0] == 0 or matrix[0][c] == 0:
                    matrix[r][c] = 0

        # 3. Zero out first row and first col if needed
        if first_row_zero:
            for c in range(n):
                matrix[0][c] = 0
        if first_col_zero:
            for r in range(m):
                matrix[r][0] = 0
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(M \times N)$
* **Space:** $\mathcal{O}(1)$ auxiliary space.
