# 🃏 Insertion Sort – Complete Guide & Intuition

> **Source Reference:** [AlgoMaster.io – Insertion Sort](https://algomaster.io/learn/dsa/insertion-sort)  
> **Category:** Comparison-Based Adaptive Sorting  
> **Difficulty:** Easy (Extremely Practical)

---

## 📌 1. What Is Insertion Sort?

**Insertion Sort** works the exact same way most people sort a hand of playing cards:
1. Start with one card in your hand (trivially sorted).
2. Pick up the next card from the table.
3. Compare it backward against the cards already in your hand and **slide/shift** larger cards to the right.
4. **Insert** the new card into its correct open slot.

---

## 🔍 2. Visual Walkthrough

Array: `[12, 11, 13, 5, 6]`

1. **Step 1:** Key = `11`. Compare with `12`. Shift `12` right. Insert `11`.  
   $	o [\mathbf{11, 12}, 13, 5, 6]$
2. **Step 2:** Key = `13`. Compare with `12`. $13 > 12$, no shift needed.  
   $	o [\mathbf{11, 12, 13}, 5, 6]$
3. **Step 3:** Key = `5`. Compare with `13, 12, 11`. Shift all right. Insert `5`.  
   $	o [\mathbf{5, 11, 12, 13}, 6]$
4. **Step 4:** Key = `6`. Shift `13, 12, 11` right. Insert `6`.  
   $	o [\mathbf{5, 6, 11, 12, 13}]$ (Sorted!)

---

## 💻 3. Python 3 Implementation

```python
def insertion_sort(arr: list[int]) -> list[int]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Shift elements of arr[0...i-1] that are greater than key to one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            
        # Place key into its correct position
        arr[j + 1] = key
        
    return arr
```

---

## 📊 4. Complexity & Key Characteristics

- **Best Case Time:** $\mathcal{O}(n)$ – When array is already sorted (the `while` condition immediately fails).
- **Worst / Average Case Time:** $\mathcal{O}(n^2)$ – Reverse sorted array.
- **Space Complexity:** $\mathcal{O}(1)$ in-place.
- **Stability:** ✅ **STABLE.**
- **Why it matters in real systems:** Hybrid sorting algorithms like **Timsort** (used in Python's `sort()` and Java's `Arrays.sort()`) use Insertion Sort for small blocks ($N \le 32$ or $64$) because of low constant factor overhead and great CPU cache locality.
