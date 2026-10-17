# Bubble sort

> **Source reference:** [AlgoMaster.io, Bubble Sort](https://algomaster.io/learn/dsa/bubble-sort)  
> **Category:** Comparison-based elementary sorting  
> **Difficulty:** Easy

## 1. How bubble sort works

Bubble sort steps through the array, compares adjacent elements, and swaps them whenever `arr[j] > arr[j + 1]`.

With each pass, the largest remaining unsorted value gets swapped forward until it settles at the end of the unsorted range:
```text
Pass 1: The largest number moves to the last index (n - 1).
Pass 2: The 2nd largest number moves to index (n - 2).
Pass i: The i-th largest number moves to index (n - i).
```
After at most $n - 1$ passes, the array is sorted.

## 2. Step-by-step walkthrough

Sort `[5, 1, 4, 2, 8]` ($n = 5$):

### Pass 1 ($i = 0$)
Compare adjacent pairs up to index $n - 1 - 0 = 4$:
1. Compare `[5, 1]`: $5 > 1 \implies$ swap $\to [1, 5, 4, 2, 8]$
2. Compare `[5, 4]`: $5 > 4 \implies$ swap $\to [1, 4, 5, 2, 8]$
3. Compare `[5, 2]`: $5 > 2 \implies$ swap $\to [1, 4, 2, 5, 8]$
4. Compare `[5, 8]`: $5 < 8 \implies$ no swap $\to [1, 4, 2, 5, \mathbf{8}]$

$\mathbf{8}$ is now in its final position at index 4.

### Pass 2 ($i = 1$)
Compare adjacent pairs up to index $n - 1 - 1 = 3$:
1. Compare `[1, 4]`: $1 < 4 \implies$ no swap $\to [1, 4, 2, 5, 8]$
2. Compare `[4, 2]`: $4 > 2 \implies$ swap $\to [1, 2, 4, 5, 8]$
3. Compare `[4, 5]`: $4 < 5 \implies$ no swap $\to [1, 2, 4, \mathbf{5}, \mathbf{8}]$

$\mathbf{5}$ is now locked in place at index 3.

### Pass 3 ($i = 2$)
Compare adjacent pairs up to index $n - 1 - 2 = 2$:
1. Compare `[1, 2]`: $1 < 2 \implies$ no swap
2. Compare `[2, 4]`: $2 < 4 \implies$ no swap

Zero swaps occurred during Pass 3, which means the array is sorted.

## 3. Early termination (`swapped` flag)

Without an early exit check, bubble sort runs all $n - 1$ passes even when the input is already sorted, taking $\mathcal{O}(n^2)$ time on `[1, 2, 3, 4, 5]`.

Adding `swapped = False` at the start of each pass fixes this. If a full pass finishes with zero swaps, every adjacent pair satisfies `arr[j] <= arr[j + 1]`, so we `break` immediately.

```text
Sorted array of 10,000 elements:
- Without early termination: ~50,000,000 comparisons (O(n^2))
- With early termination:         9,999 comparisons (O(n))
```

## 4. Python 3 implementation

```python
def bubble_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    
    # Outer loop: counts passes (from 0 to n-1)
    for i in range(n - 1):
        swapped = False
        
        # Inner loop: compare adjacent pairs.
        # Shrink the range by i because the last i elements are already placed.
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                
        if not swapped:
            break
            
    return arr
```

## 5. Complexity analysis

| Case | Time complexity | Condition / explanation |
| :--- | :--- | :--- |
| **Best case** | $\mathcal{O}(n)$ | Array is already sorted. The `swapped` flag triggers early exit on Pass 1 ($n - 1$ comparisons, 0 swaps). |
| **Average case** | $\mathcal{O}(n^2)$ | Elements in random order. |
| **Worst case** | $\mathcal{O}(n^2)$ | Reverse sorted order (e.g., `[5, 4, 3, 2, 1]`). Runs $\frac{n(n-1)}{2}$ comparisons and swaps. |
| **Space complexity** | $\mathcal{O}(1)$ | Sorts in place using constant auxiliary memory. |

## 6. Stability

Bubble sort is **stable**.

A sort is stable if equal elements (`5_a` and `5_b`) keep their original relative order in the output. Because bubble sort swaps only on strict inequality (`arr[j] > arr[j + 1]`), equal neighbors never cross over each other.

## 7. Trade-offs

### When it works well
* **Nearly sorted data:** When only 1 or 2 elements are out of place, early termination finishes in near $\mathcal{O}(n)$ time.
* **Checking sortedness:** One pass verifies whether an array is sorted in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.
* **Tiny arrays ($N < 30$):** No recursion or allocation overhead.

### When to avoid it
* **Large datasets ($N > 1,000$):** $\mathcal{O}(n^2)$ time is far slower than $\mathcal{O}(n \log n)$ algorithms like merge sort or quick sort.
* **Random or reverse-sorted data:** Insertion sort beats bubble sort in practice because it performs shifts instead of full swaps.
