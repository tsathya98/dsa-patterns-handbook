# 🎯 Single Element in Duplicates (Index Parity Pattern)

> **Course Reference:** CodeKerdos DSA — Class 9  
> **Core Concept:** Solving LeetCode 540 in $\mathcal{O}(\log N)$ time by detecting parity phase shift in adjacent pairs.

---

## 📌 Problem Statement

Given a sorted array of size $2K + 1$ where every element appears exactly twice except for **one unique element** which appears once, find the unique element in $\mathcal{O}(\log N)$ time and $\mathcal{O}(1)$ space.

```text
Input:  arr = [ 3 , 3 ,  1 , 1 ,  8 , 8 ,  10 , 10 ,  19 ,  6 , 6 ,  2 , 2 ,  4 , 4 ]
Index:          0   1    2   3    4   5     6    7     8    9  10  11  12  13  14
Output: 19
```

---

## 🧠 The Mental Model: The Parity Phase Shift

Observe the index positions of adjacent duplicate pairs:

```text
BEFORE UNIQUE ELEMENT (Left Side):
Pair [3, 3]   -> Indices (0, 1) -> (EVEN, ODD)
Pair [1, 1]   -> Indices (2, 3) -> (EVEN, ODD)
Pair [8, 8]   -> Indices (4, 5) -> (EVEN, ODD)
Pair [10, 10] -> Indices (6, 7) -> (EVEN, ODD)
👉 Invariant: First occurrence is always at an EVEN index!

THE UNIQUE ELEMENT:
Element [19]  -> Index 8 (EVEN)

AFTER UNIQUE ELEMENT (Right Side):
Pair [6, 6]   -> Indices (9, 10)  -> (ODD, EVEN)  <- Shifted!
Pair [2, 2]   -> Indices (11, 12) -> (ODD, EVEN)  <- Shifted!
Pair [4, 4]   -> Indices (13, 14) -> (ODD, EVEN)  <- Shifted!
👉 Invariant: First occurrence flipped to an ODD index!
```

---

## ⚙️ The 2-Step Binary Search Algorithm

1. **Find which half contains the single element:**
   * Look at `mid`. Does `arr[mid]` equal its partner?
   * If `arr[mid] != arr[mid - 1]` and `arr[mid] != arr[mid + 1]`: **Match! `arr[mid]` is the unique element.**
2. **Normalize to First Occurrence:**
   * If `arr[mid] == arr[mid - 1]`: the pair began at `mid - 1`. Set `first_idx = mid - 1`.
   * Else (`arr[mid] == arr[mid + 1]`): the pair begins at `mid`. Set `first_idx = mid`.
3. **Check Parity of `first_idx`:**
   * If `first_idx % 2 == 0`: We are still in the normal `(even, odd)` left region. The disruption is to the **RIGHT** $\to$ `lo = first_idx + 2`.
   * If `first_idx % 2 != 0`: We are in the shifted `(odd, even)` right region. The disruption is to the **LEFT** $\to$ `hi = first_idx - 1`.

---

## 💻 Implementation (LeetCode 540)

```python
def singleNonDuplicate(arr: list[int]) -> int:
    n = len(arr)
    if n == 1:
        return arr[0]

    # Boundary checks
    if arr[0] != arr[1]:
        return arr[0]
    if arr[n - 1] != arr[n - 2]:
        return arr[n - 1]

    lo, hi = 1, n - 2
    while lo <= hi:
        mid = lo + (hi - lo) // 2

        # 1. Unpaired check
        if arr[mid] != arr[mid - 1] and arr[mid] != arr[mid + 1]:
            return arr[mid]

        # 2. Normalize to first occurrence
        if arr[mid] == arr[mid - 1]:
            first_idx = mid - 1
        else:
            first_idx = mid

        # 3. Parity steering
        if first_idx % 2 == 0:
            lo = first_idx + 2  # Unique element is on the right
        else:
            hi = first_idx - 1  # Unique element is on the left

    return -1
```

* **Time Complexity:** $\mathcal{O}(\log N)$ — Skips entire pairs on every iteration.
* **Auxiliary Space:** $\mathcal{O}(1)$.
