# ⚖️ LeetCode 724: Find Pivot Index – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** LeetCode 75 / Top Interview 150  
> **Pattern:** Prefix Sum (The Seesaw Balance Pattern)  
> **LeetCode Link:** [LeetCode 724: Find Pivot Index](https://leetcode.com/problems/find-pivot-index/)

---

## 📌 Problem in Plain English

Given an array of integers `nums`, calculate the **pivot index** of this array.

The **pivot index** is the index where the sum of all the numbers strictly to the **left** of the index is equal to the sum of all the numbers strictly to the **index's right**.

* If no such index exists, return `-1`.
* If there are multiple pivot indexes, you should return the **left-most pivot index**.

### Example 1:
```text
Input: nums = [1, 7, 3, 6, 5, 6]
Output: 3
Explanation:
Left sum = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11
Right sum = nums[4] + nums[5] = 5 + 6 = 11
Pivot is index 3 (value 6).
```

---

## 💡 The "Aha!" Moment: The Seesaw Balance Analogy ⚖️

### Why Brute Force Slicing is Bad:
If you do `sum(nums[:i])` and `sum(nums[i+1:])` at each index:
* Slicing creates sublists in memory: $\mathcal{O}(n)$.
* Summing iterates through the sublists: $\mathcal{O}(n)$.
* Repeating inside an $\mathcal{O}(n)$ loop $\implies \mathbf{\mathcal{O}(n^2)}$ time complexity!

### The Conservation Law:
Notice that the entire array is divided into exactly three parts:
$$\mathbf{\text{Left Sum} + \text{Pivot (nums[i])} + \text{Right Sum} = \text{Total Sum}}$$

You can calculate `total_sum` **once** at the beginning.  
Then, as you walk through the array, the right sum is **free**:
$$\mathbf{\text{Right Sum} = \text{Total Sum} - \text{Left Sum} - \text{nums}[i]}$$

---

## 💻 Clean $\mathcal{O}(n)$ Solution ($\mathcal{O}(1)$ Space)

```python
class Solution:
    def pivotIndex(self, nums: list[int]) -> int:
        total = sum(nums)
        left_sum = 0
        
        for i, num in enumerate(nums):
            # Check balance: does Left equal Right?
            if left_sum == total - left_sum - num:
                return i
            # Accumulate left sum as we step forward
            left_sum += num
            
        return -1
```

---

## 📊 Step-by-Step Trace on `nums = [1, 7, 3, 6, 5, 6]` (`total = 28`)

| Index $i$ | `num` | `left_sum` | `right_sum = total - left_sum - num` | `left_sum == right_sum`? | Action |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | `1` | `0` | $28 - 0 - 1 = \mathbf{27}$ | `0 == 27` ❌ | `left_sum += 1` $\to 1$ |
| **1** | `7` | `1` | $28 - 1 - 7 = \mathbf{20}$ | `1 == 20` ❌ | `left_sum += 7` $\to 8$ |
| **2** | `3` | `8` | $28 - 8 - 3 = \mathbf{17}$ | `8 == 17` ❌ | `left_sum += 3` $\to 11$ |
| **3** | **`6`** | **`11`** | $28 - 11 - 6 = \mathbf{11}$ | **`11 == 11` ✅ MATCH!** | **Return index `3`** |

---

## ⚠️ Key Interview Takeaways

1. **Check BEFORE Adding:**  
   Notice the order: you check `left_sum == right_sum` **before** doing `left_sum += num`. The pivot element itself is strictly excluded from both sides.
2. **Handles Negative Numbers & Zeros Naturally:**  
   Because this is pure algebraic conservation, negative numbers (e.g., `nums = [-1, -1, 0, 1, 1, 0]`) work perfectly without any special-casing.
3. **No Boundary `if/else` Checks:**  
   When $i = 0$, `left_sum = 0` and `right_sum = total - nums[0]`. No need for `if i == 0:` branch.

---

## ⏱️ Complexity Blueprint

* **Time Complexity:** $\mathcal{O}(n)$ — two passes: one to compute `sum(nums)`, one to scan for the pivot.
* **Space Complexity:** $\mathcal{O}(1)$ — only two integer scalar variables (`total`, `left_sum`).
