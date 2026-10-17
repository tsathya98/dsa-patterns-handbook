# 🔍 Binary Search Fundamentals & Occurrence Boundaries

> **Course Reference:** CodeKerdos DSA — Class 8  
> **Core Concepts:** Search space halving, middle landing, first & last occurrence boundaries, occurrence count, floor and ceil.

---

## 1. Why Binary Search Works (The Search Space Invariant)

Every search problem needs two components:
1. **Target ($K$):** The item or condition you seek.
2. **Search Space $[lo, hi]$:** The range of possible positions.

When an array is **ordered (sorted)**, testing the midpoint `mid = (lo + hi) // 2` splits the remaining candidates into two equal halves. With **a single comparison**, you permanently eliminate $50\%$ of all remaining elements:

$$\text{Search space after } k \text{ steps} = \frac{N}{2^k}$$
Setting $\frac{N}{2^k} = 1 \implies k = \log_2 N$.
For $N = 1,000,000$, binary search takes at most **$20$ comparisons**!

```text
Indices:  0    1    2    3    4    5    6
Array:  [ 2 ,  5 ,  8 , 12 , 16 , 23 , 38 ]   Target = 23
          ▲              ▲              ▲
         lo             mid            hi
1. arr[mid] = 12 < 23 -> Target must be to the right -> lo = mid + 1
```

```python
def binary_search(arr: list[int], k: int) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == k:
            return mid
        elif arr[mid] < k:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

---

## 2. First & Last Occurrence in Arrays with Duplicates (LC 34)

When `arr` contains duplicate values, normal binary search halts at **any arbitrary match**, not necessarily the first or last:

```text
arr = [ 2 , 4 , 10 , 10 , 10 , 18 , 20 ],  k = 10
              ▲    ▲    ▲
            First       Last
```

### The Invariant for First Occurrence:
* When `arr[mid] == k`: You found a match, but **do not stop**! A duplicate might exist earlier to the left.
* Record `ans = mid`, and force the search space leftward: **`hi = mid - 1`**.

### The Invariant for Last Occurrence:
* When `arr[mid] == k`: Record `ans = mid`, and force the search space rightward: **`lo = mid + 1`**.

```python
def find_first_occurrence(arr: list[int], k: int) -> int:
    lo, hi = 0, len(arr) - 1
    ans = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == k:
            ans = mid
            hi = mid - 1  # Keep searching left for earlier occurrence
        elif arr[mid] < k:
            lo = mid + 1
        else:
            hi = mid - 1
    return ans

def find_last_occurrence(arr: list[int], k: int) -> int:
    lo, hi = 0, len(arr) - 1
    ans = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == k:
            ans = mid
            lo = mid + 1  # Keep searching right for later occurrence
        elif arr[mid] < k:
            lo = mid + 1
        else:
            hi = mid - 1
    return ans
```

### Total Occurrences of $K$:
$$\text{Count}(K) = \begin{cases} \text{last} - \text{first} + 1 & \text{if } \text{first} \ne -1 \\ 0 & \text{if } \text{first} == -1 \end{cases}$$
Runs in **$\mathcal{O}(\log N)$ time** without linear scanning.

---

## 3. Floor and Ceil of $K$

Given a sorted array and target $K$:
* **Floor of $K$:** Largest element $\le K$.
* **Ceil of $K$:** Smallest element $\ge K$.

```python
def find_floor(arr: list[int], k: int) -> int:
    lo, hi = 0, len(arr) - 1
    ans = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= k:
            ans = arr[mid]  # Candidate floor; try to find a larger one on the right
            lo = mid + 1
        else:
            hi = mid - 1
    return ans

def find_ceil(arr: list[int], k: int) -> int:
    lo, hi = 0, len(arr) - 1
    ans = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] >= k:
            ans = arr[mid]  # Candidate ceil; try to find a smaller one on the left
            hi = mid - 1
        else:
            lo = mid + 1
    return ans
```
