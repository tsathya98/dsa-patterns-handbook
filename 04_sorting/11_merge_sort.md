# 🌲 Merge Sort – Complete Guide & Intuition

> **Source Reference:** [AlgoMaster.io – Merge Sort](https://algomaster.io/learn/dsa/merge-sort)  
> **Category:** Divide and Conquer  
> **Difficulty:** Medium (Guaranteed $\mathcal{O}(n \log n)$)

---

## 📌 1. What Is Merge Sort?

Merge Sort is a classic **Divide and Conquer** algorithm:
1. **Divide:** Recursively split the array in half until each subarray has only 1 element (a 1-element array is always sorted).
2. **Conquer & Combine:** Merge the two sorted halves back together in linear time using the two-pointer merge technique.

```text
                  [38, 27, 43, 3, 9, 82, 10]
                  /                        \
          [38, 27, 43, 3]              [9, 82, 10]
          /             \              /         \
      [38, 27]       [43, 3]        [9, 82]      [10]
      /      \       /     \        /     \        |
    [38]    [27]   [43]    [3]     [9]    [82]   [10]
      \      /       \     /        \     /        |
      [27, 38]       [3, 43]        [9, 82]      [10]
          \             /              \         /
          [3, 27, 38, 43]              [9, 10, 82]
                  \                        /
                  [3, 9, 10, 27, 38, 43, 82]
```

---

## 💻 2. Python 3 Implementation

```python
def merge_sort(arr: list[int]) -> list[int]:
    # Base case: 0 or 1 elements are already sorted
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    return merge(left_half, right_half)

def merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= guarantees stability!
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    # Append any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

---

## 📊 3. Complexity & Key Characteristics

- **Time Complexity:** $\mathcal{O}(n \log n)$ in **ALL cases** (Best, Average, Worst).
  - Tree depth is $\log_2 n$.
  - Work per level is $\mathcal{O}(n)$ to merge.
- **Space Complexity:** $\mathcal{O}(n)$ auxiliary memory for merging subarrays.
- **Stability:** ✅ **STABLE.**
- **Best for:** Sorting Linked Lists (where random access is not available, and extra space is $\mathcal{O}(1)$ with pointers) and external sorting of large files on disk.
