# LeetCode 54: Spiral Matrix

> **Difficulty:** Medium | **Pattern:** 4-Boundary Wall Shrinking (`top`, `bottom`, `left`, `right`) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/spiral-matrix/](https://leetcode.com/problems/spiral-matrix/)

## The problem

Given an `m x n` `matrix`, return all elements of the matrix in clockwise spiral order.

```text
Input:
[ 1,  2,  3,  4 ]
[ 5,  6,  7,  8 ]
[ 9, 10, 11, 12 ]

Output: [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
```

---

## The core trick: 4 shrinking walls

Maintain four boundary pointers: `top = 0`, `bottom = m - 1`, `left = 0`, `right = n - 1`.
In each cycle, walk one full perimeter and shrink the wall you just finished:
1. **Top row (Left -> Right):** Walk `col` from `left` to `right` on row `top`, then `top += 1`.
2. **Right col (Top -> Bottom):** Walk `row` from `top` to `bottom` on col `right`, then `right -= 1`.
3. **Bottom row (Right -> Left):** If `top <= bottom`, walk `col` from `right` down to `left` on row `bottom`, then `bottom -= 1`.
4. **Left col (Bottom -> Top):** If `left <= right`, walk `row` from `bottom` down to `top` on col `left`, then `left += 1`.

---

## Step-by-step trace (`3 x 4` matrix)

**Initial boundaries:** `top = 0, bottom = 2, left = 0, right = 3`

**Step 1 (Sweep `top = 0` Left -> Right, then `top = 1`):**
```text
[ 1 → 2 → 3 → 4 ]   <- collected: [1, 2, 3, 4]
──────────────────  top moves down to 1
[ 5,  6,  7,  8 ]
[ 9, 10, 11, 12 ]
```

**Step 2 (Sweep `right = 3` Top -> Bottom, then `right = 2`):**
```text
[ 5,  6,  7 |  8 ↓ ]
[ 9, 10, 11 | 12 ↓ ]  <- collected: [1, 2, 3, 4, 8, 12]
            right moves left to 2
```

**Step 3 (`top <= bottom` holds: Sweep `bottom = 2` Right -> Left, then `bottom = 1`):**
```text
[ 5,  6,  7 ]
─────────────  bottom moves up to 1
[ 9 ← 10 ← 11 ]  <- collected: [1, 2, 3, 4, 8, 12, 11, 10, 9]
```

**Step 4 (`left <= right` holds: Sweep `left = 0` Bottom -> Top, then `left = 1`):**
```text
[ 5 ↑ | 6,  7 ]  <- collected: [..., 9, 5]
      left moves right to 1
```

**Step 5 (Next cycle: Sweep `top = 1` from `left = 1` to `right = 2`, then `top = 2`):**
```text
[ 6 → 7 ]        <- collected: [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
Now top (2) > bottom (1) -> Loop ends!
```

---

## Traps to watch for

* **Missing the mid-loop `if top <= bottom` / `if left <= right` check:** On a non-square matrix like `1 x 4` (`[[1, 2, 3, 4]]`), Step 1 increments `top` to `1`, which immediately crosses `bottom = 0`. Without `if top <= bottom:` before Step 3, you would re-read the same row backward.

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        res: list[int] = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            # 1. Traverse top row (left -> right)
            for c in range(left, right + 1):
                res.append(matrix[top][c])
            top += 1

            # 2. Traverse right column (top -> bottom)
            for r in range(top, bottom + 1):
                res.append(matrix[r][right])
            right -= 1

            # 3. Traverse bottom row (right -> left) if rows remain
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    res.append(matrix[bottom][c])
                bottom -= 1

            # 4. Traverse left column (bottom -> top) if cols remain
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    res.append(matrix[r][left])
                left += 1

        return res
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(M \times N)$ because every cell is visited once.
* **Space:** $\mathcal{O}(1)$ auxiliary space (excluding output list).
