# Single element in duplicates (index parity pattern)

> **Course reference:** CodeKerdos DSA, Class 9  
> **Core concept:** Solving LeetCode 540 in $\mathcal{O}(\log N)$ time by checking the index parity of adjacent duplicate pairs.

## 1. Problem statement

Given a sorted array of size $2K + 1$ where every element appears twice except for one element that appears once, find that single element in $\mathcal{O}(\log N)$ time and $\mathcal{O}(1)$ space.

```text
Input:  arr = [ 3 , 3 ,  1 , 1 ,  8 , 8 ,  10 , 10 ,  19 ,  6 , 6 ,  2 , 2 ,  4 , 4 ]
Index:          0   1    2   3    4   5     6    7     8    9  10   11  12   13  14
Output: 19
```

## 2. The parity shift across the single element

Look at the `(first, second)` indices of each duplicate pair before and after the single element:

```text
BEFORE THE SINGLE ELEMENT (Left side):
Pair [3, 3]   -> Indices (0, 1) -> (EVEN, ODD)
Pair [1, 1]   -> Indices (2, 3) -> (EVEN, ODD)
Pair [8, 8]   -> Indices (4, 5) -> (EVEN, ODD)
Pair [10, 10] -> Indices (6, 7) -> (EVEN, ODD)
Invariant: Each pair starts at an EVEN index.

THE SINGLE ELEMENT:
Element [19]  -> Index 8 (EVEN)

AFTER THE SINGLE ELEMENT (Right side):
Pair [6, 6]   -> Indices (9, 10)  -> (ODD, EVEN)
Pair [2, 2]   -> Indices (11, 12) -> (ODD, EVEN)
Pair [4, 4]   -> Indices (13, 14) -> (ODD, EVEN)
Invariant: Each pair now starts at an ODD index.
```

## 3. Binary search steps

At each midpoint `mid`:
1. **Check if `arr[mid]` is the single element:**  
   If `arr[mid] != arr[mid - 1]` and `arr[mid] != arr[mid + 1]`, return `arr[mid]`.
2. **Find the start index of the current pair (`first_idx`):**
   * If `arr[mid] == arr[mid - 1]`, the pair starts at `first_idx = mid - 1`.
   * Otherwise (`arr[mid] == arr[mid + 1]`), the pair starts at `first_idx = mid`.
3. **Steer using the parity of `first_idx`:**
   * If `first_idx % 2 == 0`, we are still in the `(even, odd)` left region, so the single element is further right: `lo = first_idx + 2`.
   * If `first_idx % 2 == 1`, the parity has already shifted to `(odd, even)`, so the single element is to the left: `hi = first_idx - 1`.

## 4. Implementation (LeetCode 540)

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

        # 1. Check if mid is unpaired
        if arr[mid] != arr[mid - 1] and arr[mid] != arr[mid + 1]:
            return arr[mid]

        # 2. Align to the first occurrence of the pair
        if arr[mid] == arr[mid - 1]:
            first_idx = mid - 1
        else:
            first_idx = mid

        # 3. Steer based on parity of first_idx
        if first_idx % 2 == 0:
            lo = first_idx + 2  # Single element is on the right
        else:
            hi = first_idx - 1  # Single element is on the left

    return -1
```

* **Time complexity:** $\mathcal{O}(\log N)$.
* **Auxiliary space:** $\mathcal{O}(1)$.
