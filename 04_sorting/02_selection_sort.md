# Selection sort

> **Source reference:** [AlgoMaster.io, Selection Sort](https://algomaster.io/learn/dsa/selection-sort)  
> **Category:** Comparison-based elementary sorting  
> **Difficulty:** Easy

## 1. How selection sort works

Selection sort splits the array into two regions:
1. A sorted prefix on the left (starts empty).
2. An unsorted suffix on the right (starts as the whole array).

On pass $i$, the algorithm scans `arr[i...n-1]` to find the index of the minimum element, then swaps that element into `arr[i]`.

```text
Pass 1: Find minimum in arr[0...n-1], swap with arr[0].
Pass 2: Find minimum in arr[1...n-1], swap with arr[1].
Pass i: Find minimum in arr[i...n-1], swap with arr[i].
```

### Algorithm steps:
* **1. Partition array:** Run pass $i$ from $0$ up to $n - 2$. The prefix before $i$ is sorted; $arr[i...n-1]$ is the unsorted suffix.
* **2. Track minimum index:** Set `min_idx = i`.
* **3. Scan suffix ($j$):** Iterate $j$ from $i + 1$ to $n - 1$. If `arr[j] < arr[min_idx]`, update `min_idx = j`.
* **4. Swap into place:** If `min_idx != i`, swap `arr[i]` and `arr[min_idx]`.
* **5. Grow prefix:** Advance $i$. The smallest unsorted element is now locked at index $i$.

## 2. Walkthrough

Array: `[64, 25, 12, 22, 11]`

1. **Pass 1 ($i = 0$):** Scan `[64, 25, 12, 22, 11]`. Minimum is `11` at index 4. Swap `arr[0]` and `arr[4]`.  
   $\to [\mathbf{11}, 25, 12, 22, 64]$
2. **Pass 2 ($i = 1$):** Scan `[25, 12, 22, 64]`. Minimum is `12` at index 2. Swap `arr[1]` and `arr[2]`.  
   $\to [\mathbf{11}, \mathbf{12}, 25, 22, 64]$
3. **Pass 3 ($i = 2$):** Scan `[25, 22, 64]`. Minimum is `22` at index 3. Swap `arr[2]` and `arr[3]`.  
   $\to [\mathbf{11}, \mathbf{12}, \mathbf{22}, 25, 64]$
4. **Pass 4 ($i = 3$):** Scan `[25, 64]`. Minimum is `25` at index 3. Already at index 3.  
   $\to [\mathbf{11}, \mathbf{12}, \mathbf{22}, \mathbf{25}, \mathbf{64}]$

## 3. Python 3 implementation

```python
def selection_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    
    for i in range(n - 1):
        min_idx = i
        
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
                
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            
    return arr
```

## 4. Complexity and characteristics

* **Time complexity:** $\mathcal{O}(n^2)$ in best, average, and worst cases.  
  Total comparisons: $(n-1) + (n-2) + \dots + 1 = \frac{n(n-1)}{2} \implies \mathcal{O}(n^2)$.
* **Space complexity:** $\mathcal{O}(1)$ in place.
* **Total swaps:** At most $n - 1$ swaps ($\mathcal{O}(n)$ memory writes).
* **Stability:** Unstable.  
  For example, on `[4_a, 4_b, 1]`, pass 1 swaps `4_a` with `1` to produce `[1, 4_b, 4_a]`, reversing the order of `4_a` and `4_b`.

## 5. Bubble sort vs. selection sort

| Feature | Bubble sort | Selection sort |
| :--- | :--- | :--- |
| **Mechanism** | Moves largest element to the end via adjacent swaps | Finds minimum element and swaps it to the front |
| **Best-case time** | $\mathcal{O}(n)$ (with `swapped` early exit) | $\mathcal{O}(n^2)$ (no early exit) |
| **Worst-case time** | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ |
| **Total swaps** | $\mathcal{O}(n^2)$ worst case | $\mathcal{O}(n)$ (at most $n - 1$ swaps) |
| **Stability** | Stable | Unstable |
| **When to prefer** | Nearly sorted data | When memory writes are expensive |

### Why selection sort cannot exit early
In bubble sort, completing a pass with zero adjacent swaps proves by transitivity that the entire array is sorted. In selection sort, verifying that `arr[i]` is the minimum of `arr[i...n-1]` tells you nothing about whether `arr[i+1...n-1]` are in order relative to each other. Even on `[1, 2, 3, 4, 5]`, selection sort has to run all $\frac{n(n-1)}{2}$ comparisons.
