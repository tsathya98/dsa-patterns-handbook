# 🔍 Binary Search Master Cheat Sheet & Decision Guide

> **Pattern:** Binary Search (Divide and Conquer on Monotonic Spaces)  
> **Audience:** Complete Beginner / 1st-Year CS Student  
> **Analogy:** The "Higher or Lower" Number Guessing Game

---

## 💡 1. What is Binary Search?

Imagine playing a guessing game: *"I am thinking of a number between 1 and 100."*
* If you guess 1, then 2, then 3... that is **Linear Search** ($\mathcal{O}(n)$). In the worst case, you ask 100 questions.
* The smart way: You guess **50**.
  * If the host says *"Higher!"*, you just eliminated all numbers from 1 to 50 in **one single second**!
  * Next you guess **75**, eliminating half of what's left.

Every single question cuts the remaining search space **in half**.
* Searching through $1,000,000$ items takes at most **20 checks** ($\log_2(1,000,000) \approx 20$)!
* Time Complexity: **$\mathcal{O}(\log n)$** instead of $\mathcal{O}(n)$.

---

## 🎯 2. When Can You Use It?

You can use Binary Search whenever the data has **monotonic behavior**:
1. **Explicitly Sorted Array:** Numbers are in increasing or decreasing order (`[1, 3, 5, 8, 12, 19]`).
2. **Binary Search on the Answer (Monotonic Predicate):**  
   The array might not be given, but the answer space transitions from `False` to `True` at some point:
   `[Impossible, Impossible, Impossible, POSSIBLE, POSSIBLE, POSSIBLE]`  
   Binary search finds that exact turning point!

---

## ⚙️ 3. The Classical Template (Bug-Free & Easy to Remember)

Most students get infinite loops in Binary Search because they mess up `low <= high` or `mid + 1`. Memorize this standard template:

```python
def binary_search(nums: list[int], target: int) -> int:
    low = 0
    high = len(nums) - 1
    
    while low <= high:
        # 1. Find the exact middle
        mid = (low + high) // 2
        
        # 2. Target found
        if nums[mid] == target:
            return mid
        
        # 3. Target is in the right half -> discard left half
        elif nums[mid] < target:
            low = mid + 1
            
        # 4. Target is in the left half -> discard right half
        else:
            high = mid - 1
            
    return -1  # Not found
```

```text
Visualizing low, mid, high:
Indices:  0    1    2    3    4    5    6
Nums:   [ 2 ,  5 ,  8 , 12 , 16 , 23 , 38 ]    Target = 23
          ▲              ▲              ▲
         low            mid            high

1. nums[mid] = 12 < 23 (Target is higher!)
2. Discard indices 0 to 3 -> move low to mid + 1 (index 4)

Indices:  0    1    2    3    4    5    6
Nums:   [ . ,  . ,  . ,  . , 16 , 23 , 38 ]
                              ▲    ▲    ▲
                             low  mid  high
3. nums[mid] = 23 == Target! FOUND at index 5!
```

---

## 🌟 4. Binary Search on the Answer (Monotonic Predicate)

### The Problem Style:
The problem does **not** give you a sorted list to search through. Instead, it asks:
> *"Find the **minimum speed** to finish a task in $H$ hours"* or *"Find the **maximum capacity** to ship packages in $D$ days."*

### How to recognize it:
1. If a speed of 10 works, will a speed of 11 also work? **Yes.**
2. If a speed of 4 is too slow, will a speed of 3 also be too slow? **Yes.**

The answers look like this:
```text
Speed:     1      2      3      4      5      6      7
Feasible: [No  , No  , No  ,  YES ,  YES ,  YES ,  YES ]
                               ▲
                      We want to find this boundary!
```

#### ⚙️ Binary Search on Answer Template (e.g. *Koko Eating Bananas* - LC 875)
```python
def minEatingSpeed(piles: list[int], h: int) -> int:
    low = 1              # Minimum possible speed
    high = max(piles)    # Maximum possible speed needed
    ans = high
    
    while low <= high:
        mid_speed = (low + high) // 2
        
        if can_finish(piles, mid_speed, h):
            ans = mid_speed        # Record this valid speed
            high = mid_speed - 1   # Can we go even slower? Search left!
        else:
            low = mid_speed + 1    # Too slow! Must speed up! Search right!
            
    return ans
```

---

## 🗺️ 5. The 7 Universal Binary Search Archetypes

| # | Archetype | Invariant / Trigger | Directional Steering Rule | Classic Problems |
|---|---|---|---|---|
| **1** | **Classical Lookup** | Monotonic sorted array | `nums[mid] < target => lo = mid + 1` | Binary Search (LC 704) |
| **2** | **Boundary / Occurrence** | Duplicates in sorted array | On match: `hi = mid - 1` (First) or `lo = mid + 1` (Last) | First & Last Occurrence (LC 34), Floor/Ceil |
| **3** | **Slope / Local Minima** | Unsorted array, distinct neighbors | Downward slope `arr[mid] > arr[mid-1] => hi = mid - 1` | Peak Element (LC 162), Local Minima |
| **4** | **Rotated Half-ID** | Rotated sorted array | Check `nums[lo] <= nums[mid]` to find sorted half | Search Rotated Array (LC 33, LC 153) |
| **5** | **Index Parity** | Sorted pairs with 1 unique | Normalize to 1st occurrence: `even => lo = mid + 2`, `odd => hi = mid - 1` | Single Element in Duplicates (LC 540) |
| **6** | **Exponential Doubling** | Unbounded / infinite stream | Expand `hi = 1 -> 2 -> 4 -> ...` until `arr[hi] >= k` | Search in Infinite Array (LC 702) |
| **7** | **Search on Answer** | Min-max or capacity bounds | Monotonic `is_feasible(mid)` helper steers $[lo, hi]$ | Painter's Partition, Koko (LC 875), Split Array (LC 410) |

---

## ⚠️ 6. Student Traps & Edge Cases

1. **Integer Overflow in other languages:**  
   In Java/C++, `(low + high) // 2` can overflow if numbers are huge ($2 \times 10^9$). In Python, integers have arbitrary precision, but interviewers prefer:  
   `mid = low + (high - low) // 2`
2. **Never do `low = mid` or `high = mid` without loop guard:**  
   Always include the `+ 1` or `- 1` (`low = mid + 1` or `high = mid - 1`). If you don't, when `low` and `high` are adjacent, your loop will run infinitely!
3. **Empty / Single Element Arrays:**  
   Always check $N = 1$ early or ensure `lo <= hi` handles single-element arrays cleanly.
