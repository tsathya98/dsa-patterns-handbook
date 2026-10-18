# LeetCode 304: Range Sum Query 2D - Immutable

> **Difficulty:** Medium | **Pattern:** 2D Prefix Sum + Inclusion-Exclusion Principle | **Access:** Free  
> **Link:** [https://leetcode.com/problems/range-sum-query-2d-immutable/](https://leetcode.com/problems/range-sum-query-2d-immutable/)

## The problem

Given a 2D matrix `matrix`, handle multiple queries of the following type in **$\mathcal{O}(1)$ time per query**:
* Calculate the sum of the elements of `matrix` inside the rectangle defined by its upper-left corner `(row1, col1)` and lower-right corner `(row2, col2)`.

---

## Why 1D row prefix sums aren't optimal

If you store a 1D prefix sum for each row, a query across `R` rows still takes $\mathcal{O}(R)$ time. When the problem requires $\mathcal{O}(1)$ per query, we need a **2D prefix sum table**.

---

## The core trick: Padded `(m + 1) x (n + 1)` 2D Prefix Sum

Define `pref[r + 1][c + 1]` as the sum of the rectangle from `(0, 0)` to `(r, c)`.
Adding a `0`-padded top row and left column eliminates every `r == 0` or `c == 0` boundary check!

### 1. Building `pref` in $\mathcal{O}(M \times N)$:
```text
pref[r + 1][c + 1] = matrix[r][c] + pref[r][c + 1] + pref[r + 1][c] - pref[r][c]
                                    (top box)        (left box)       (overlap added twice)
```

### 2. Querying `(r1, c1)` to `(r2, c2)` in $\mathcal{O}(1)$:
```text
+---------------+-------------+
|   Overlap     |   Top Cut   |
|  pref[r1][c1] |pref[r1][c2+1]
+---------------+-------------+
|   Left Cut    |   TARGET    |
|pref[r2+1][c1] |  (r1,c1)..  |
|               |  (r2,c2)    |
+---------------+-------------+
                       ^ pref[r2+1][c2+1]

Sum = pref[r2 + 1][c2 + 1]   (Big box from (0,0) to (r2,c2))
    - pref[r1][c2 + 1]       (Subtract box above row r1)
    - pref[r2 + 1][c1]       (Subtract box left of col c1)
    + pref[r1][c1]           (Add back top-left corner subtracted twice!)
```

---

## Step-by-step trace

**Input `2 x 2` matrix:**
```text
matrix = [ [3, 0],
           [5, 6] ]
```

**Step 1: Build `(3 x 3)` padded `pref` table:**
* `pref[1][1] = 3 + 0 + 0 - 0 = 3`
* `pref[1][2] = 0 + 0 + 3 - 0 = 3`
* `pref[2][1] = 5 + 3 + 0 - 0 = 8`
* `pref[2][2] = 6 + 3 + 8 - 3 = 14`

```text
pref = [ [0,  0,  0],
         [0,  3,  3],
         [0,  8, 14] ]
```

**Step 2: Query `sumRegion(1, 1, 1, 1)` (just cell `(1, 1)` which has value `6`):**
```text
ans = pref[2][2] - pref[1][2] - pref[2][1] + pref[1][1]
    = 14         - 3          - 8          + 3
    = 6
```

<details>
<summary>Spoiler: Solution Code</summary>

```python
class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        m, n = len(matrix), len(matrix[0])
        self.pref = [[0] * (n + 1) for _ in range(m + 1)]

        for r in range(m):
            for c in range(n):
                self.pref[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.pref[r][c + 1]
                    + self.pref[r + 1][c]
                    - self.pref[r][c]
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.pref[row2 + 1][col2 + 1]
            - self.pref[row1][col2 + 1]
            - self.pref[row2 + 1][col1]
            + self.pref[row1][col1]
        )
```

</details>

---

## Complexity

* **Precomputation (`__init__`):** $\mathcal{O}(M \times N)$ time and space.
* **Per Query (`sumRegion`):** $\mathcal{O}(1)$ time.
