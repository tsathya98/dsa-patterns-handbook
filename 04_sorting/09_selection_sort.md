# 🎯 Selection Sort – Complete Guide & Intuition

> **Source Reference:** [AlgoMaster.io – Selection Sort](https://algomaster.io/learn/dsa/selection-sort)  
> **Category:** Comparison-Based Elementary Sorting  
> **Difficulty:** Easy

---

## 📌 1. What Is Selection Sort?

**Selection Sort** divides the array into two parts:
1. A **sorted sublist** on the left (initially empty).
2. An **unsorted sublist** on the right (initially the whole array).

In each pass, the algorithm finds ("selects") the **minimum element** from the unsorted sublist and swaps it with the leftmost unsorted element, growing the sorted sublist by one.

```text
Pass 1: Find minimum in arr[0...n-1], swap with arr[0].
Pass 2: Find minimum in arr[1...n-1], swap with arr[1].
Pass i: Find minimum in arr[i...n-1], swap with arr[i].
```

---

## 🔍 2. Visual Walkthrough

Array: `[64, 25, 12, 22, 11]`

1. **Pass 1 ($i = 0$):** Search `[64, 25, 12, 22, 11]`. Min is `11` at index 4. Swap `arr[0]` and `arr[4]`.  
   $	o [\mathbf{11}, 25, 12, 22, 64]$
2. **Pass 2 ($i = 1$):** Search `[25, 12, 22, 64]`. Min is `12` at index 2. Swap `arr[1]` and `arr[2]`.  
   $	o [\mathbf{11}, \mathbf{12}, 25, 22, 64]$
3. **Pass 3 ($i = 2$):** Search `[25, 22, 64]`. Min is `22` at index 3. Swap `arr[2]` and `arr[3]`.  
   $	o [\mathbf{11}, \mathbf{12}, \mathbf{22}, 25, 64]$
4. **Pass 4 ($i = 3$):** Search `[25, 64]`. Min is `25` at index 3. Swap with itself.  
   $	o [\mathbf{11}, \mathbf{12}, \mathbf{22}, \mathbf{25}, \mathbf{64}]$ (Sorted!)

---

## 💻 3. Python 3 Implementation

```python
def selection_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    
    for i in range(n - 1):
        # Assume the current position is the minimum
        min_idx = i
        
        # Scan the rest of the array to find the true minimum
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
                
        # Swap the found minimum with the first unsorted position
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            
    return arr
```

---

## 📊 4. Complexity & Key Characteristics

- **Time Complexity:** $\mathcal{O}(n^2)$ in **ALL cases** (Best, Average, Worst).  
  *Why?* Even if the array is sorted, Selection Sort must still scan all remaining elements to confirm the minimum.
- **Space Complexity:** $\mathcal{O}(1)$ (In-place).
- **Total Swaps:** At most $n - 1$ swaps. (Minimizes memory writes!).
- **Stability:** ❌ **NOT Stable.**  
  *Example:* Sorting `[4_a, 4_b, 1]`. The `1` is swapped with `4_a`, resulting in `[1, 4_b, 4_a]`. The relative order of `4_a` and `4_b` was inverted.
