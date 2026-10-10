# ⚡ Quick Sort – Complete Guide & Intuition

> **Source Reference:** [AlgoMaster.io – Quick Sort](https://algomaster.io/learn/dsa/quick-sort)  
> **Category:** Divide and Conquer (Partitioning)  
> **Difficulty:** Medium (Fastest in Practice)

---

## 📌 1. What Is Quick Sort?

Quick Sort is an in-place divide-and-conquer algorithm:
1. **Choose a Pivot:** Pick an element from the array (e.g. last element, random element, or median of three).
2. **Partition:** Rearrange the array so that:
   - All elements **less than or equal to the pivot** are placed to its left.
   - All elements **greater than the pivot** are placed to its right.
   - The pivot lands in its **final sorted position**.
3. **Recursively Sort:** Apply Quick Sort to the left and right subarrays.

---

## 🔍 2. Lomuto Partition Scheme Trace

Array: `[10, 80, 30, 90, 40, 50, 70]`, Pivot = `70`
- Pointer `i` marks the boundary of elements $\le 70$.
- Pointer `j` scans from `0` to `n-2`:
  - `10 <= 70` $\to$ swap with itself, $i$ advances.
  - `80 > 70` $\to$ skip.
  - `30 <= 70` $\to$ swap `80` and `30`.
  - At the end, swap pivot `70` into index $i + 1$.

---

## 💻 3. Python 3 Implementation

```python
def quick_sort(arr: list[int], low: int, high: int) -> None:
    if low < high:
        # pi is partitioning index, arr[pi] is at right place
        pi = partition(arr, low, high)
        
        quick_sort(arr, low, pi - 1)   # Sort left of pivot
        quick_sort(arr, pi + 1, high)  # Sort right of pivot

def partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]  # Choosing last element as pivot
    i = low - 1        # Index of smaller element
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    # Swap pivot to its correct final place
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

---

## 📊 4. Complexity & Key Characteristics

- **Average Time:** $\mathcal{O}(n \log n)$ with very small constant factors (cache-friendly).
- **Worst Case Time:** $\mathcal{O}(n^2)$ (occurs when pivot is always smallest/largest, e.g. already sorted with naive pivot choice).
- **Space Complexity:** $\mathcal{O}(\log n)$ recursion stack space.
- **Stability:** ❌ **NOT Stable.**
