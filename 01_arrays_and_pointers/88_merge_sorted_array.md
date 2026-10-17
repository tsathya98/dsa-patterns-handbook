# 🪢 88. Merge Sorted Array

> **Difficulty:** Easy (LeetCode Label) / **Medium** (Under FAANG $\mathcal{O}(1)$ space constraints)  
> **Pattern:** Two Pointers — **Formation E: The Tail-Buffer / Reverse Placement Pattern**  
> **Constraints:** $\mathcal{O}(m + n)$ Time, $\mathcal{O}(1)$ Auxiliary Space in-place.

---

## 💡 1. The Core Dilemma: Why is this NOT a Normal "Easy"?

On LeetCode, this is labeled "Easy" because anyone can write:
```python
nums1[m:] = nums2
nums1.sort()  # O((m + n) log(m + n)) — REJECTED AT FAANG!
```

In a real interview, the prompt requires:
> *"Do it in $\mathcal{O}(m + n)$ linear time and strictly $\mathcal{O}(1)$ extra memory by modifying `nums1` in place."*

### 💥 The "Bulldozer Collision" Trap:
When you merge two sorted lists from the front (Left $\to$ Right), comparing `nums1[0]` and `nums2[0]`:
```text
nums1 = [ 2 , 5 , 6 , 0 , 0 , 0 ],  m = 3
nums2 = [ 1 , 3 , 4 ],              n = 3

Compare nums1[0] (2) vs nums2[0] (1).
1 is smaller! Write 1 into nums1[0]...

nums1 = [ 1 , 5 , 6 , 0 , 0 , 0 ]
          ▲
💥 DISASTER! The '2' is overwritten and lost forever!
```

To avoid losing `2`, you would have to shift the rest of `nums1` rightward ($\mathcal{O}(m \cdot n)$ slow) or make an extra copy of `nums1` ($\mathcal{O}(m)$ memory). Both violate interview constraints!

---

## 🔍 2. How to Think of Going Backwards (The 3-Question Deductive Train)

Candidates often ask: *"How could anyone ever think of going backwards on their own?"*

Here is the exact deductive dialogue:

```text
Question 1: "What went wrong when I tried the obvious way?"
Answer:     "I started from the front, and I destroyed unread data by overwriting it."
                  │
                  ▼
Question 2: "WHERE in this array can I write right now without destroying anything?"
Answer:     "Only where the zeros are! At the very end of nums1 (the tail)!"
                  │
                  ▼
Question 3: "If I must write to the back first, WHAT belongs at the back?"
Answer:     "In a sorted list, the LARGEST numbers belong at the back.
             So instead of finding the smallest, I must compare from the back
             and place the LARGEST number first!"
```

> 🏷️ **The Tail-Buffer Mental Trigger:**  
> **Symptom:** You must modify Array $A$ in place, and Array $A$ has **extra buffer capacity / padding at the end**.  
> **Prescription:** **NEVER GO LEFT-TO-RIGHT. ALWAYS WORK FROM THE TAIL BACKWARD.**

---

## 🎬 3. Visual Step-by-Step Trace

### Initial State:
* `p1 = m - 1 = 2` (points to `6`)
* `p2 = n - 1 = 2` (points to `4`)
* `p = m + n - 1 = 5` (points to the last safe buffer zero)

```text
nums1 = [ 2 , 5 , 6 ,  0 , 0 , 0 ]
                  ▲            ▲
                  p1           p

nums2 = [ 1 , 3 , 4 ]
                  ▲
                  p2
```

### Round 1:
* Compare `nums1[p1] (6)` vs `nums2[p2] (4)`.
* **6 is greater!** Place `6` at `nums1[p]`. Decrement `p1` and `p`.
```text
nums1 = [ 2 , 5 , 6 ,  0 , 0 , 6 ]
              ▲            ▲
              p1           p
nums2 = [ 1 , 3 , 4 ]
                  ▲
                  p2
```

### Round 2:
* Compare `nums1[p1] (5)` vs `nums2[p2] (4)`.
* **5 is greater!** Place `5` at `nums1[p]`. Decrement `p1` and `p`.
```text
nums1 = [ 2 , 5 , 6 ,  0 , 5 , 6 ]
          ▲            ▲
          p1           p
nums2 = [ 1 , 3 , 4 ]
                  ▲
                  p2
```

### Round 3:
* Compare `nums1[p1] (2)` vs `nums2[p2] (4)`.
* **4 is greater!** Place `4` at `nums1[p]`. Decrement `p2` and `p`.
```text
nums1 = [ 2 , 5 , 6 ,  4 , 5 , 6 ]
          ▲        ▲
          p1       p
nums2 = [ 1 , 3 , 4 ]
              ▲
              p2
```

### Round 4:
* Compare `nums1[p1] (2)` vs `nums2[p2] (3)`.
* **3 is greater!** Place `3` at `nums1[p]`. Decrement `p2` and `p`.
```text
nums1 = [ 2 , 5 , 3 ,  4 , 5 , 6 ]
          ▲   ▲
          p1  p
nums2 = [ 1 , 3 , 4 ]
          ▲
          p2
```

### Round 5:
* Compare `nums1[p1] (2)` vs `nums2[p2] (1)`.
* **2 is greater!** Place `2` at `nums1[p]`. Decrement `p1` and `p`.
```text
nums1 = [ 2 , 2 , 3 ,  4 , 5 , 6 ]
      ▲   ▲
      p1  p
nums2 = [ 1 , 3 , 4 ]
          ▲
          p2
```
*(Now `p1 = -1`. The first while loop terminates).*

### Final Cleanup:
* `nums2` still has `[ 1 ]` at `p2 = 0`. Copy `nums2[0]` into `nums1[p]`:
```text
nums1 = [ 1 , 2 , 2 ,  4 , 5 , 6 ]  ✅ PERFECTLY SORTED IN-PLACE!
```

---

## 💻 4. Python Implementation

```python
class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        p1 = m - 1          # Last valid item in nums1
        p2 = n - 1          # Last item in nums2
        p = m + n - 1       # Write pointer at safe buffer tail

        # Compare from back, place largest element at p
        while p1 >= 0 and p2 >= 0:
            if nums1[p1] > nums2[p2]:
                nums1[p] = nums1[p1]
                p1 -= 1
            else:
                nums1[p] = nums2[p2]
                p2 -= 1
            p -= 1

        # Follow-up: If nums2 still has leftovers, copy them into nums1
        while p2 >= 0:
            nums1[p] = nums2[p2]
            p2 -= 1
            p -= 1

        # What if nums1 has leftovers?
        # NOTHING TO DO! They are ALREADY in their correct sorted positions!
```

---

## 🧠 5. The Top Interview Follow-Up Question

Interviewers almost always ask:
> *"Why did you only write `while p2 >= 0:` at the end? Why isn't there a `while p1 >= 0:` loop?"*

### 💡 The Senior Answer:
*"Because `nums1` is the destination array. If `p2` finishes first, any remaining elements in `nums1` are already sitting at indices `0 ... p1` in their correct, relative sorted order. Copying them onto themselves would be a redundant no-op."*

---

## 📊 6. Complexity Analysis

| Metric | Complexity | Explanation |
| :--- | :---: | :--- |
| **Time Complexity** | $\mathcal{O}(m + n)$ | Each iteration places exactly one element at pointer `p`. We make at most $m + n$ total steps. |
| **Auxiliary Space** | $\mathcal{O}(1)$ | We only use three integer pointers (`p1`, `p2`, `p`). Zero extra memory allocated. |

---

## 🔄 7. Similar Problems (The "Reverse In-Place" Family)

Once you recognize this **Tail-Buffer** trick, these classic problems use the exact same mental model:

1. **[LC 977: Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/)**
   * *The Problem:* Array has negative and positive numbers (`[-4, -1, 0, 3, 10]`). Squaring them puts the **largest** squares at the two outer extremes!
   * *The Pattern:* Squeeze from both ends, fill output array **from the back to the front**!
2. **[LC 844: Backspace String Compare](https://leetcode.com/problems/backspace-string-compare/)**
   * *The Problem:* Characters followed by `#` are deleted.
   * *The Pattern:* Going forward requires a stack ($\mathcal{O}(n)$ space). Going **backwards from the tail** counts backspaces in $\mathcal{O}(1)$ space!
3. **URLify (Cracking the Coding Interview):**
   * *The Problem:* Replace spaces with `"%20"` in a string that has trailing buffer space.
   * *The Pattern:* Fill from right-to-left to prevent overwriting unshifted letters.
4. **[LC 66: Plus One](file:///Users/sathyat/Developer/projects/dsa/66_plus_one.md)**
   * *The Pattern:* Process the addition from the last digit backward to handle carry cleanly.
