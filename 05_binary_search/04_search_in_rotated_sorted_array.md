# 🔄 Search in Rotated Sorted Array (Half-Identification Pattern)

> **Course Reference:** CodeKerdos DSA — Class 9 & 10  
> **Core Concept:** Solving LeetCode 33 & 153 in $\mathcal{O}(\log N)$ time by determining which half is monotonic.

---

## 📌 Problem Statement

An integer array `nums` sorted in ascending order is rotated at an unknown pivot index:
```text
Original: [ 0 , 1 , 2 , 4 , 5 , 6 , 7 ]
Rotated:  [ 4 , 5 , 6 , 7 , 0 , 1 , 2 ]
Target: 0 -> Returns index 4
```

---

## 🧠 The Half-Identification Invariant

When an array is rotated, a single comparison with `arr[lo]` reveals which half is unbroken:
$$\text{At any midpoint } mid\text{, AT LEAST ONE HALF is GUARANTEED to be normally sorted!}$$

```text
nums = [ 4 , 5 , 6 , 7 , 0 , 1 , 2 ]
         ▲           ▲           ▲
        lo          mid         hi

Compare nums[lo] (4) and nums[mid] (7):
Since nums[lo] <= nums[mid] (4 <= 7) -> The LEFT half [4, 5, 6, 7] is 100% SORTED!
```

### The Steering Rule:
1. **If Left Half is Sorted (`nums[lo] <= nums[mid]`):**
   * Check if target falls strictly within the sorted left boundaries:
     $$\text{nums}[lo] \le \text{target} < \text{nums}[mid]$$
   * If **Yes** $\implies$ search left: `hi = mid - 1`.
   * If **No** $\implies$ target must be in the right half: `lo = mid + 1`.

2. **If Right Half is Sorted (`nums[mid] < nums[hi]`):**
   * Check if target falls strictly within the sorted right boundaries:
     $$\text{nums}[mid] < \text{target} \le \text{nums}[hi]$$
   * If **Yes** $\implies$ search right: `lo = mid + 1`.
   * If **No** $\implies$ search left: `hi = mid - 1`.

---

## 💻 Implementation (LeetCode 33)

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2

        if nums[mid] == target:
            return mid

        # Check if left half is sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1  # Target is in sorted left half
            else:
                lo = mid + 1  # Target is in right half
        # Otherwise, right half must be sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1  # Target is in sorted right half
            else:
                hi = mid - 1  # Target is in left half

    return -1
```

---

## ⚡ Finding the Minimum in Rotated Sorted Array (LeetCode 153)

To find the inflection point / minimum element, compare `nums[mid]` against `nums[hi]`:

```python
def findMin(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = lo + (hi - lo) // 2

        if nums[mid] > nums[hi]:
            # Minimum must be to the right of mid (in the disrupted valley)
            lo = mid + 1
        else:
            # mid could be the minimum itself, so keep mid
            hi = mid

    return nums[lo]
```

* **Time Complexity:** $\mathcal{O}(\log N)$.
* **Auxiliary Space:** $\mathcal{O}(1)$.
