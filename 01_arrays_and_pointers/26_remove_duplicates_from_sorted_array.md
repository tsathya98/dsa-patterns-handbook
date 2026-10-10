# ✂️ 26. Remove Duplicates from Sorted Array

> **Difficulty:** Easy  
> **Pattern:** Two Pointers — **Formation B: Scout & Writer (Fast & Slow Pointers)**  
> **Constraints:** $\mathcal{O}(n)$ Time, strictly $\mathcal{O}(1)$ Auxiliary Space in-place.

---

## ⚠️ 1. Honest Review of Your `Counter` Solution

Your solution:
```python
from collections import Counter

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        counter = Counter(nums)
        k = 0
        for key in counter:
            nums[k] = key
            k += 1
        return k
```

### Does it work on LeetCode?
**Yes!** In Python 3.7+, dictionaries preserve insertion order. `Counter` extracts unique keys in the order they first appeared, and you overwrite `nums` with those keys. LeetCode accepts it!

### Is it good in a FAANG interview?
**NO — this is an immediate interview trap!**

Here is why an interviewer will stop you:
1. **Violates the $\mathcal{O}(1)$ Space Constraint:**  
   `Counter(nums)` allocates a brand new hash table in memory holding up to $n$ key-value pairs $\implies \mathcal{O}(n)$ extra space! The problem explicitly states:
   > *"Do not allocate extra space for another array. You must do this by modifying the input array in-place with O(1) extra memory."*
2. **Ignores the Biggest Clue in the Title:**  
   Notice the word: **"SORTED"**.
   * If an array is **UNSORTED** $\implies$ You **MUST** use a Hash Table ($\mathcal{O}(n)$ space) because duplicates could be anywhere.
   * If an array is **SORTED** $\implies$ **All duplicates are glued together side-by-side as adjacent neighbors!** You do **NOT** need a Hash Table!

---

## 💡 2. The $\mathcal{O}(1)$ Solution: Reuse What You Just Learned!

Look at how identical this is to the **Scout & Writer** code you just wrote for [LC 27: Remove Element](file:///Users/sathyat/Developer/projects/dsa/27_remove_element.md):

```text
In LC 27 (Remove Element):
"Keep the number if it is NOT equal to val"
    if nums[i] != val:
        nums[k] = nums[i]
        k += 1

In LC 26 (Remove Duplicates):
"Keep the number if it is NOT equal to its previous neighbor"
    if nums[i] != nums[i - 1]:
        nums[k] = nums[i]
        k += 1
```

### The Setup:
* The very first number `nums[0]` is **always unique** and already sitting in place.
* **Writer (`k`):** Starts at index **`1`** (the destination for the 2nd unique number).
* **Scout (`i`):** Starts at index **`1`** and inspects every number.

---

## 🎬 3. Visual Step-by-Step Trace

Let `nums = [ 0 , 0 , 1 , 1 , 1 , 2 , 2 , 3 ]`:

```text
Initial:
k = 1, nums[0] is already settled as 0.
nums = [ 0 ,  0 ,  1 ,  1 ,  1 ,  2 ,  2 ,  3 ]
              ▲
             k, i

Step 1:
i = 1: nums[1] (0) == nums[0] (0). Duplicate neighbor! Skip!
nums = [ 0 ,  0 ,  1 ,  1 ,  1 ,  2 ,  2 ,  3 ]
              ▲    ▲
              k    i

Step 2:
i = 2: nums[2] (1) != nums[1] (0). NEW UNIQUE NUMBER FOUND!
Write nums[k] = nums[i] -> nums[1] = 1, bump k -> 2.
nums = [ 0 ,  1 ,  1 ,  1 ,  1 ,  2 ,  2 ,  3 ]
                   ▲    ▲
                   k    i

Step 3:
i = 3: nums[3] (1) == nums[2] (1). Duplicate neighbor! Skip!
Step 4:
i = 4: nums[4] (1) == nums[3] (1). Duplicate neighbor! Skip!

Step 5:
i = 5: nums[5] (2) != nums[4] (1). NEW UNIQUE NUMBER FOUND!
Write nums[k] = nums[i] -> nums[2] = 2, bump k -> 3.
nums = [ 0 ,  1 ,  2 ,  1 ,  1 ,  2 ,  2 ,  3 ]
                        ▲              ▲
                        k              i

Step 6:
i = 6: nums[6] (2) == nums[5] (2). Duplicate neighbor! Skip!

Step 7:
i = 7: nums[7] (3) != nums[6] (2). NEW UNIQUE NUMBER FOUND!
Write nums[k] = nums[i] -> nums[3] = 3, bump k -> 4.
nums = [ 0 ,  1 ,  2 ,  3 ,  1 ,  2 ,  2 ,  3 ]
                             ▲
                             k = 4 (Done!)
```

The first `4` numbers are `[ 0 , 1 , 2 , 3 ]` — **$\mathcal{O}(1)$ space, zero hash tables allocated!**

---

## 💻 4. The Clean FAANG Python Solution

```python
class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        if not nums:
            return 0

        # Writer starts at 1 because nums[0] is guaranteed unique
        k = 1

        # Scout scans from 1 to the end
        for i in range(1, len(nums)):
            # If current element differs from previous neighbor, it's a new unique number!
            if nums[i] != nums[i - 1]:
                nums[k] = nums[i]
                k += 1

        return k
```

---

## 📊 5. Comparison: `Counter` vs. Two Pointers

| Metric | Your `Counter` Approach | Optimal Two Pointers (Scout & Writer) |
| :--- | :---: | :---: |
| **Time Complexity** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ |
| **Auxiliary Space** | **$\mathcal{O}(n)$ (Violates constraint ❌)** | **$\mathcal{O}(1)$ (Passes FAANG ✅)** |
| **Memory Overhead** | Allocates hash table + dict nodes in heap | Uses only 2 integer pointers |
| **Interview Verdict** | **Warning / Pushback from interviewer** | **100% Pass** |

---

## 🔑 The Golden Interview Rule: Sorted vs. Unsorted Duplicates

Memorize this forever:

> * **If the problem says "SORTED":**  
>   Duplicates are guaranteed to be adjacent neighbors (`nums[i] == nums[i - 1]`).  
>   👉 **Use Two Pointers ($\mathcal{O}(1)$ space). Never use a Hash Table!**
>
> * **If the problem says "UNSORTED":**  
>   Duplicates can appear anywhere (`[4, 1, 2, 4]`).  
>   👉 **You MUST use a Hash Table / Counter ($\mathcal{O}(n)$ space).**
