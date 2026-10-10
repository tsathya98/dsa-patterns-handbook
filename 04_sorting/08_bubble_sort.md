# 🫧 Bubble Sort – Complete Guide & Intuition

> **Source Reference:** [AlgoMaster.io – Bubble Sort](https://algomaster.io/learn/dsa/bubble-sort)  
> **Category:** Comparison-Based Elementary Sorting  
> **Difficulty:** Easy (Fundamental)

---

## 📌 1. What Is Bubble Sort?

**Bubble Sort** is a comparison-based sorting algorithm that repeatedly steps through the array, compares adjacent elements, and swaps them if they are in the wrong order (i.e. `arr[j] > arr[j + 1]`).

### 🥤 Why is it called "Bubble" Sort?
In a carbonated drink (like soda), larger bubbles rise to the surface faster than smaller ones. 
In Bubble Sort, **larger values "bubble up" to the end of the array** with every pass because they keep getting swapped forward at each comparison.

```text
Pass 1: The absolute largest number bubbles to the last index (n - 1).
Pass 2: The 2nd largest number bubbles to the 2nd-to-last index (n - 2).
Pass i: The i-th largest number bubbles to index (n - i).
```
After at most $n - 1$ passes, the entire array is guaranteed to be sorted.

---

## 🔍 2. Step-by-Step Visual Walkthrough

Let's sort the array: `[5, 1, 4, 2, 8]` (Length $n = 5$)

### 🔵 Pass 1 ($i = 0$):
Compare adjacent pairs up to index $n - 1 - 0 = 4$:
1. Compare `[5, 1]`: $5 > 1 \implies$ **Swap** $	o [1, 5, 4, 2, 8]$
2. Compare `[5, 4]`: $5 > 4 \implies$ **Swap** $	o [1, 4, 5, 2, 8]$
3. Compare `[5, 2]`: $5 > 2 \implies$ **Swap** $	o [1, 4, 2, 5, 8]$
4. Compare `[5, 8]`: $5 < 8 \implies$ No swap $	o [1, 4, 2, 5, \mathbf{8}]$

👉 **Result of Pass 1:** $\mathbf{8}$ (the largest element) is locked in its permanent final position!

---

### 🔵 Pass 2 ($i = 1$):
Compare adjacent pairs up to index $n - 1 - 1 = 3$:
1. Compare `[1, 4]`: $1 < 4 \implies$ No swap $	o [1, 4, 2, 5, 8]$
2. Compare `[4, 2]`: $4 > 2 \implies$ **Swap** $	o [1, 2, 4, 5, 8]$
3. Compare `[4, 5]`: $4 < 5 \implies$ No swap $	o [1, 2, 4, \mathbf{5}, \mathbf{8}]$

👉 **Result of Pass 2:** $\mathbf{5}$ is locked in place!

---

### 🔵 Pass 3 ($i = 2$):
Compare adjacent pairs up to index $n - 1 - 2 = 2$:
1. Compare `[1, 2]`: $1 < 2 \implies$ No swap
2. Compare `[2, 4]`: $2 < 4 \implies$ No swap

👉 **Result of Pass 3:** Zero swaps occurred! The array is already fully sorted.

---

## ⚡ 3. The Critical Optimization: Early Termination (`swapped` Flag)

Without optimization, standard Bubble Sort blindly runs all $n - 1$ passes, even if the array is already sorted on Pass 1. That takes $\mathcal{O}(n^2)$ time even for `[1, 2, 3, 4, 5]`.

### The Fix:
Add a boolean flag `swapped = False` at the start of each pass.
- If we complete an entire pass without making **a single swap**, the array is already 100% sorted!
- We `break` early immediately.

```text
Impact on Sorted Array of 10,000 Elements:
- Without Early Termination: ~50,000,000 comparisons (O(n^2))
- With Early Termination:        10,000 comparisons (O(n))
🚀 A 5,000x speedup!
```

---

## 💻 4. Python 3 Implementation

```python
def bubble_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    
    # Outer loop: counts passes (from 0 to n-1)
    for i in range(n - 1):
        swapped = False
        
        # Inner loop: compare adjacent pairs.
        # Notice range(n - 1 - i): we shrink the range because 
        # the last 'i' elements are already sorted!
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                # Swap adjacent elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                
        # If no two elements were swapped in this pass, array is sorted!
        if not swapped:
            break
            
    return arr
```

---

## 📊 5. Complexity Analysis

| Case | Time Complexity | Condition / Explanation |
| :--- | :--- | :--- |
| **Best Case** | $\mathcal{O}(n)$ | Array is already sorted. The `swapped` flag triggers early exit on Pass 1 ($n - 1$ comparisons, 0 swaps). |
| **Average Case** | $\mathcal{O}(n^2)$ | Elements in random order. Nested loop comparisons. |
| **Worst Case** | $\mathcal{O}(n^2)$ | Array is in reverse sorted order (e.g. `[5, 4, 3, 2, 1]`). Exactly $\frac{n(n-1)}{2}$ comparisons and swaps. |
| **Space Complexity** | $\mathcal{O}(1)$ | In-place sorting. Uses only a constant amount of memory for variables. |

---

## 🔒 6. Stability Analysis: Is Bubble Sort Stable?

**YES, Bubble Sort is Stable.**

### What does "Stable" mean?
If two elements have equal values (e.g. `5_a` and `5_b`), a stable sort guarantees that their original relative order is preserved (`5_a` remains before `5_b` in the sorted output).

### Why is Bubble Sort Stable?
The swap condition uses a strict inequality: `if arr[j] > arr[j + 1]:`.
If `arr[j] == arr[j + 1]`, no swap happens. Thus, duplicate values never leapfrog each other.

---

## ⚖️ 7. When to Use & When NOT to Use

### ✅ Good Use Cases:
1. **Nearly Sorted Data:** If only 1 or 2 elements are misplaced, early termination makes Bubble Sort run in near $\mathcal{O}(n)$ time.
2. **Small Datasets ($N < 30$):** Simple with zero recursion or heap overhead.
3. **Detecting if an Array is Sorted:** One pass of Bubble Sort determines if an array is sorted in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.
4. **Teaching Intuition:** The clearest illustration of adjacent swaps and loop invariants.

### ❌ Poor Use Cases:
1. **Large Datasets ($N > 1000$):** Quadratic $\mathcal{O}(n^2)$ is unacceptably slow compared to Merge Sort or Quick Sort ($\\mathcal{O}(n \log n)$).
2. **Reverse Sorted / Random Data:** Insertion Sort typically outperforms Bubble Sort because it does fewer actual writes/swaps.
