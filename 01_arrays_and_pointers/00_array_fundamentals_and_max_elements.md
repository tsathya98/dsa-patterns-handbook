# 🧱 Array Fundamentals, Max Elements & Leaders

> **Course Reference:** CodeKerdos DSA — Class 4 & Class 6  
> **Core Concepts:** Python lists vs low-level arrays, single-pass max tracking, right-to-left traversal, and leaders in an array.

---

## 1. Python List vs `array.array`

In Python coding interviews and competitive programming:
* **`list`:** Built-in dynamic array of pointers to heap objects. Highly optimized in CPython, handles mixed types, and grows automatically.
* **`array.array`:** Requires `import array`, enforces homogeneous C data types, lacks LeetCode method support, and provides no meaningful algorithmic speedup in Python.
* **Rule:** Always use standard Python `list` for all DSA problems.

---

## 2. Count Elements With at Least One Greater Element

Given an integer array `arr`, count how many elements have **at least one strictly greater element** in the array.

```text
Example:
Input:  arr = [2, 5, 1, 4, 8, 0, 8, 1, 3, 8]
Length: 10
The maximum element is 8.
Every element strictly smaller than 8 has at least one element greater than it (namely 8!).
Elements equal to 8 have NO greater element in the array.
Result: 10 - (count of 8s) = 10 - 3 = 7 elements.
```

### The $\mathcal{O}(N)$ Optimal Observation
* **Brute Force:** Compare every element with all other elements $\to \mathcal{O}(N^2)$.
* **Optimal:** Find the maximum value in `arr`. Any element strictly smaller than `max_val` has at least one greater element (the maximum itself). Elements equal to `max_val` have zero greater elements.
* **Formula:** $\text{Result} = N - \text{count}(\text{max\_val})$.

```python
def count_elements_with_greater(arr: list[int]) -> int:
    if not arr:
        return 0
    max_val = max(arr)
    max_count = arr.count(max_val)
    return len(arr) - max_count
```
* **Time Complexity:** $\mathcal{O}(N)$ (Two linear passes: one for `max`, one for `count`).
* **Auxiliary Space:** $\mathcal{O}(1)$.

---

## 3. Leaders in an Array

An element is a **Leader** if it is strictly greater than **all elements to its right**.
* The rightmost element is always a leader (there are no elements to its right).

```text
Input:  arr = [16, 17, 4, 3, 5, 2]

Inspect from right to left:
- 2:  Rightmost element -> LEADER (max_so_far = 2)
- 5:  5 > 2 -> LEADER (max_so_far = 5)
- 3:  3 < 5 -> Not a leader
- 4:  4 < 5 -> Not a leader
- 17: 17 > 5 -> LEADER (max_so_far = 17)
- 16: 16 < 17 -> Not a leader

Leaders: [17, 5, 2] (or [2, 5, 17] in reverse)
```

### The Right-to-Left Scanning Pattern
* **Brute Force:** For each index $i$, scan from $i+1$ to $N-1$ to see if any element is $\ge arr[i]$ $\to \mathcal{O}(N^2)$.
* **Optimal:** Scan from **right to left** ($N-1$ down to $0$), maintaining a running scalar `max_so_far`. An element is a leader if and only if `arr[i] > max_so_far`.

```python
def find_leaders(arr: list[int]) -> list[int]:
    n = len(arr)
    if n == 0:
        return []
    
    leaders = [arr[-1]]
    max_so_far = arr[-1]
    
    for i in range(n - 2, -1, -1):
        if arr[i] > max_so_far:
            leaders.append(arr[i])
            max_so_far = arr[i]
            
    leaders.reverse()  # Return in original left-to-right order
    return leaders
```
* **Time Complexity:** $\mathcal{O}(N)$.
* **Auxiliary Space:** $\mathcal{O}(1)$ (excluding output array).
