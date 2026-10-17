# 🏔️ Local Minima & Peak Finding (Binary Search on Unsorted Arrays)

> **Course Reference:** CodeKerdos DSA — Class 8  
> **Core Concept:** Applying Binary Search to **unsorted** arrays using slope / gradient navigation (LeetCode 162).

---

## 1. The Paradox: Binary Search Without a Sorted Array

In beginner computer science, students are told: *"Binary Search only works on sorted arrays."*  
**This is incomplete.**

Binary Search works whenever you can make a **guaranteed directional decision** at `mid` that eliminates half the candidates. You do not need the entire array to be sorted; you only need a **local slope (gradient)**.

---

## 2. Local Minima in an Array of Distinct Elements

An element `arr[i]` is a **Local Minimum** if it is strictly smaller than both its immediate neighbors:
$$\text{arr}[i] < \text{arr}[i - 1] \quad \text{AND} \quad \text{arr}[i] < \text{arr}[i + 1]$$

* **Boundary Rules:**
  * Index $0$ is a local minimum if $arr[0] < arr[1]$.
  * Index $N - 1$ is a local minimum if $arr[N - 1] < arr[N - 2]$.

```text
arr = [ 9 ,  6 ,  3 , 14 ,  5 ,  7 ,  4 ]
             ▲              ▲         ▲
         Local Min      Local Min   Local Min
```

---

## 3. The Slope / Gradient Navigation Principle

Imagine being dropped into a mountain range in total darkness:
* If the ground slopes downward to your left, following the downward slope is **mathematically guaranteed** to hit a valley (local minimum) or terminate at the edge!

```text
At index mid:

Case A: arr[mid] > arr[mid - 1]
         ▲
        /   (Sloping downward to the left)
       /
       -> A local minimum is GUARANTEED to exist in the left half!
       -> Move left: hi = mid - 1

Case B: arr[mid] > arr[mid + 1]
       \
        \   (Sloping downward to the right)
         ▼
       -> A local minimum is GUARANTEED to exist in the right half!
       -> Move right: lo = mid + 1

Case C: arr[mid] < arr[mid - 1] and arr[mid] < arr[mid + 1]
       \   /
        \ /  (You are at the bottom of the valley!)
       -> MATCH! Return mid!
```

---

## 4. Implementation

```python
def find_local_minimum(arr: list[int]) -> int:
    n = len(arr)
    if n == 1:
        return 0

    # 1. Check boundary elements first in O(1)
    if arr[0] < arr[1]:
        return 0
    if arr[n - 1] < arr[n - 2]:
        return n - 1

    # 2. Search interior elements [1, n - 2]
    lo, hi = 1, n - 2
    while lo <= hi:
        mid = lo + (hi - lo) // 2

        # Check if mid is smaller than both neighbors
        if arr[mid] < arr[mid - 1] and arr[mid] < arr[mid + 1]:
            return mid
        # Downward slope to the left
        elif arr[mid] > arr[mid - 1]:
            hi = mid - 1
        # Downward slope to the right
        else:
            lo = mid + 1

    return -1
```

### LeetCode 162: Find Peak Element (The Inverted Twin)
Finding a **Peak Element** ($arr[i] > arr[i-1]$ and $arr[i] > arr[i+1]$) uses the exact inverse logic:
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

* **Time Complexity:** $\mathcal{O}(\log N)$ — Halves search space on every step without ever sorting.
* **Auxiliary Space:** $\mathcal{O}(1)$.
