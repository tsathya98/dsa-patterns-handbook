# Quick sort

> **Source reference:** [AlgoMaster.io, Quick Sort](https://algomaster.io/learn/dsa/quick-sort)  
> **Category:** Divide and conquer (partitioning)  
> **Difficulty:** Medium

## 1. How quick sort works

Quick sort is an in-place divide-and-conquer sorting algorithm:
1. **Pick a pivot:** Choose an element from the subarray (for example, the last element, a random element, or the median of three).
2. **Partition:** Rearrange the subarray so that:
   * Elements $\le$ the pivot sit to its left.
   * Elements $>$ the pivot sit to its right.
   * The pivot lands at its final sorted index `pi`.
3. **Recurse:** Run quick sort on the left subarray `low...pi-1` and the right subarray `pi+1...high`.

### Algorithm steps:
* **1. Base case:** If `low >= high`, the subarray has $\le 1$ element; return immediately.
* **2. Partition around pivot:** Select pivot element (e.g. `arr[high]`). Pointer $i = low - 1$.
* **3. Scan elements ($j$):** Scan $j$ from $low$ to $high - 1$. If `arr[j] <= pivot`, increment $i += 1$ and swap `arr[i]` with `arr[j]`.
* **4. Lock pivot:** Swap `arr[i + 1]` with `arr[high]`. The pivot lands at its final sorted index `pi = i + 1`.
* **5. Recurse:** Recursively sort `quick_sort(arr, low, pi - 1)` and `quick_sort(arr, pi + 1, high)`.

## 2. Lomuto partition trace

Array: `[10, 80, 30, 90, 40, 50, 70]`, pivot = `70` (last element)

```text
Start (i = -1, j = 0, pivot = 70):
      [ 10 , 80 , 30 , 90 , 40 , 50 , 70 ]
   ▲     ▲                             ▲
   i     j                           pivot

Iteration 1 (j = 0): arr[0] = 10 <= 70 -> i += 1 (0), swap(arr[0], arr[0])
      [ 10 , 80 , 30 , 90 , 40 , 50 , 70 ]
         ▲    ▲                        ▲
         i    j                      pivot

Iteration 2 (j = 1): arr[1] = 80 > 70 -> skip! i stays at 0
      [ 10 , 80 , 30 , 90 , 40 , 50 , 70 ]
         ▲         ▲                   ▲
         i         j                 pivot

Iteration 3 (j = 2): arr[2] = 30 <= 70 -> i += 1 (1), swap(80, 30)
      [ 10 , 30 , 80 , 90 , 40 , 50 , 70 ]
              ▲         ▲              ▲
              i         j            pivot

Iterations 4-6 (j = 3..5): 90 skipped; 40 and 50 swapped into i = 2, 3
      [ 10 , 30 , 40 , 50 , 80 , 90 , 70 ]
                        ▲              ▲
                        i            pivot

Final Step: Swap pivot (70) with arr[i + 1] (80):
      [ 10 , 30 , 40 , 50 , 70 , 90 , 80 ]
                             ▲
                      Locked Pivot (pi = 4)
```

## 3. Python 3 implementation

```python
def quick_sort(arr: list[int], low: int, high: int) -> None:
    if low < high:
        pi = partition(arr, low, high)
        
        quick_sort(arr, low, pi - 1)   # Sort left of pivot
        quick_sort(arr, pi + 1, high)  # Sort right of pivot

def partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

## 4. Complexity and characteristics

* **Average-case time:** $\mathcal{O}(n \log n)$ with low constant overhead and good cache locality.
* **Worst-case time:** $\mathcal{O}(n^2)$, which happens when the chosen pivot is repeatedly the smallest or largest element (such as picking the last element on an already-sorted array). Randomized pivot selection or median-of-three avoids this on sorted inputs.
* **Space complexity:** $\mathcal{O}(\log n)$ expected recursion stack depth ($\mathcal{O}(n)$ in the skewed worst case).
* **Stability:** Unstable, because partitioning swaps non-adjacent elements across the array.
