# Local minima and peak finding (binary search on unsorted arrays)

> **Course reference:** CodeKerdos DSA, Class 8  
> **Core concept:** Applying binary search to unsorted arrays using local slope navigation (LeetCode 162).

## 1. Binary search without a sorted array

Binary search does not require the entire array to be sorted. It works whenever a check at `mid` gives you a guaranteed directional decision that eliminates half of the remaining candidates. For peak and valley problems, a local slope between adjacent elements is enough.

## 2. Local minimum in an array of distinct elements

An element `arr[i]` is a **local minimum** if it is strictly smaller than its immediate neighbors:
$$\text{arr}[i] < \text{arr}[i - 1] \quad \text{AND} \quad \text{arr}[i] < \text{arr}[i + 1]$$

* **Boundary rules:**
  * Index $0$ is a local minimum if $\text{arr}[0] < \text{arr}[1]$.
  * Index $N - 1$ is a local minimum if $\text{arr}[N - 1] < \text{arr}[N - 2]$.

```text
arr = [ 9 ,  6 ,  3 , 14 ,  5 ,  7 ,  4 ]
             ▲              ▲         ▲
         Local Min      Local Min   Local Min
```

## 3. Following the downward slope

Suppose you already checked the two ends (`arr[0]` and `arr[N - 1]`) and neither is a local minimum. That means the array slopes down going inward from both ends (`arr[0] > arr[1]` and `arr[N - 1] > arr[N - 2]`).

If you inspect `mid` and see which neighbor is smaller, following the downward slope is guaranteed to hit at least one local minimum in that half:

```text
At index mid:

Case A: arr[mid] > arr[mid - 1]
         ▲
        /   (Sloping downward to the left)
       /
       -> A local minimum is guaranteed to exist in the left half.
       -> Move left: hi = mid - 1

Case B: arr[mid] > arr[mid + 1]
       \
        \   (Sloping downward to the right)
         ▼
       -> A local minimum is guaranteed to exist in the right half.
       -> Move right: lo = mid + 1

Case C: arr[mid] < arr[mid - 1] and arr[mid] < arr[mid + 1]
       \   /
        \ /  (Bottom of the valley)
       -> Return mid.
```

### Algorithm steps:
* **1. Boundary edge cases:** If $N = 1$, return index 0. Check boundary endpoints `arr[0]` and `arr[n - 1]`.
* **2. Initialize inner bounds:** Set `lo = 1` and `hi = n - 2`.
* **3. Compare mid with neighbors:** Compute `mid = lo + (hi - lo) // 2`:
  * If `arr[mid]` is smaller than both neighbors (`arr[mid - 1]` and `arr[mid + 1]`), valley found! Return `mid`.
  * If `arr[mid] > arr[mid - 1]`, downward slope to the left guarantees a local minimum exists on the left; steer `hi = mid - 1`.
  * Otherwise, downward slope to the right guarantees a local minimum on the right; steer `lo = mid + 1`.

```playthrough
{
  "algorithm": "peak_finding",
  "initial": [1, 2, 1, 3, 5, 6, 4]
}
```


## 4. Implementation

```python
def find_local_minimum(arr: list[int]) -> int:
    n = len(arr)
    if n == 1:
        return 0

    # 1. Check boundary elements in O(1)
    if arr[0] < arr[1]:
        return 0
    if arr[n - 1] < arr[n - 2]:
        return n - 1

    # 2. Search interior elements [1, n - 2]
    lo, hi = 1, n - 2
    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if arr[mid] < arr[mid - 1] and arr[mid] < arr[mid + 1]:
            return mid
        elif arr[mid] > arr[mid - 1]:
            hi = mid - 1
        else:
            lo = mid + 1

    return -1
```

### LeetCode 162: Find Peak Element
Finding a **peak element** ($\text{arr}[i] > \text{arr}[i-1]$ and $\text{arr}[i] > \text{arr}[i+1]$) follows the upward slope instead:
```python
def findPeakElement(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1  # Peak lies to the right (upward slope)
        else:
            hi = mid      # Peak lies at mid or to the left
    return lo
```

* **Time complexity:** $\mathcal{O}(\log N)$, halving the search space on every step without sorting.
* **Auxiliary space:** $\mathcal{O}(1)$.
