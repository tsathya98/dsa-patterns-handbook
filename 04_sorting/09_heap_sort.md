# Heap sort

> **Source reference:** [AlgoMaster.io, Heap Sort](https://algomaster.io/learn/dsa/heap-sort)  
> **LeetCode targets:** [LC 912. Sort an Array](https://leetcode.com/problems/sort-an-array/), [LC 215. Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/)  
> **Category:** Tree selection sort  
> **Difficulty:** Medium

## 1. Why MAANG asks heap sort

Heap Sort is the only comparison-based sorting algorithm that simultaneously achieves:
1. **Guaranteed $\mathcal{O}(n \log n)$ time** across best, average, and worst cases (unlike Quick Sort, which degrades to $\mathcal{O}(n^2)$ on bad pivots).
2. **Strictly $\mathcal{O}(1)$ auxiliary space** (unlike Merge Sort, which requires an auxiliary array of size $\mathcal{O}(n)$).

In FAANG interviews (especially at Google, Amazon, and Bloomberg), interviewers often ask candidates to implement `heapify` or `sift_down` manually rather than relying on Python's built-in `heapq` module to test:
* Binary heap array indexing mechanics.
* In-place tree re-balancing without creating node objects.
* Mathematical derivation of why building a heap takes $\mathcal{O}(n)$ time rather than $\mathcal{O}(n \log n)$.

### Binary heap array representation:
For any zero-indexed element at index $i$:
* **Left child:** $2i + 1$
* **Right child:** $2i + 2$
* **Parent:** $(i - 1) // 2$
* **Last internal (non-leaf) node:** $n // 2 - 1$

---

## 2. Algorithm steps

* **1. Build max-heap (Bottom-up):** Start from the last non-leaf parent index $i = n // 2 - 1$ down to root $0$. Run `sift_down(i)` on each. This transforms the raw array into a valid max-heap where `arr[0]` is the maximum element. This phase runs in $\mathcal{O}(n)$ time.
* **2. Extract and sort:** Loop $i$ from $n - 1$ down to $1$:
  * Swap the maximum root `arr[0]` with the current boundary element `arr[i]`.
  * The maximum element is now locked into its final sorted position at the end.
  * Reduce heap size to $i$ and call `sift_down(0)` on the root to restore the max-heap property.
* **3. Termination:** When the heap size shrinks to 1, the entire array is sorted in ascending order.

---

## 3. Python 3 implementation

<details>
<summary>Spoiler: Solution Code</summary>

```python
def heap_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    
    # Step 1: Build max heap in-place - O(n)
    # Leaves are already valid 1-element heaps, so start at last parent
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)
        
    # Step 2: Repeatedly extract max root to the back - O(n log n)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Move current root to end
        sift_down(arr, i, 0)             # Restore heap on reduced size i
        
    return arr

def sift_down(arr: list[int], heap_size: int, root: int) -> None:
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2
    
    if left < heap_size and arr[left] > arr[largest]:
        largest = left
    if right < heap_size and arr[right] > arr[largest]:
        largest = right
        
    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        sift_down(arr, heap_size, largest)
```

</details>

---

## 4. Complexity and characteristics

* **Time complexity:** $\mathcal{O}(n \log n)$ best, average, and worst case.
  * Building the heap takes $\mathcal{O}(n)$ time because the majority of nodes sit near the bottom with small tree heights: $\sum_{h=0}^{\log n} \frac{n}{2^{h+1}} \cdot \mathcal{O}(h) = \mathcal{O}(n)$.
  * Extracting $n$ elements each taking $\mathcal{O}(\log n)$ sift-down steps takes $\mathcal{O}(n \log n)$ time.
* **Space complexity:** $\mathcal{O}(1)$ auxiliary space. The sorting occurs completely in-place.
* **Stability:** Unstable, because long-range swaps between the root and the end of the heap disrupt the relative ordering of equal elements.
* **Heap Sort vs Quick Sort:** Quick Sort has significantly better cache locality because partition accesses adjacent memory blocks sequentially, whereas Heap Sort jumps between indices $i$, $2i$, and $4i$. In practice, Quick Sort is faster on modern CPU architectures, but Heap Sort guarantees no worst-case quadratic degradation.
