# 🎯 LeetCode 167: Two Sum II - Input Array Is Sorted – Master Study Guide

> **Difficulty:** Medium | **Pattern:** Two Pointers Formation A (Inward Squeeze)  
> **Complexity:** Time: $\mathcal{O}(n)$ | Auxiliary Space: $\mathcal{O}(1)$ (Strictly constant memory)  
> **Source Code:** [`167_two_sum_ii_input_array_is_sorted.py`](./167_two_sum_ii_input_array_is_sorted.py)

---

## 📌 Problem in Plain English

Given a **1-indexed** array of integers `numbers` that is **already sorted in non-decreasing order**, find two numbers such that they add up to a specific `target` number.
* Return indices as `[index1, index2]` (1-based, so add `+1`).
* **Critical Constraint:** *"Your solution must use only constant extra space $\mathcal{O}(1)$."*

```text
Example 1:
Input: numbers = [2, 7, 11, 15], target = 9
Output: [1, 2] (2 + 7 = 9)

Example 2:
Input: numbers = [2, 3, 4], target = 6
Output: [1, 3] (2 + 4 = 6)
```

---

## ⚠️ The HashMap Trap (Why LC 167 Exists)

In LeetCode 1, the array was **unsorted**, so we had to use a `HashMap` ($\mathcal{O}(n)$ space).

If you submit a HashMap on LC 167, LeetCode accepts it, but your memory score plummets (Beats ~25%). In an interview, the interviewer will say:
> *"Good, but why did I tell you the array was ALREADY SORTED? Can you eliminate the HashMap to achieve $\mathcal{O}(1)$ auxiliary space?"*

---

## 🧠 Mental Model: The Inward Squeeze (Formation A)

Since the array is sorted, we can steer our sum with two pointers squeezing inward:
* Pointer `l` starts at smallest number (`index 0`).
* Pointer `r` starts at largest number (`index len - 1`).

```text
l ->                                <- r
[ 2,    7,    11,    15 ],   target = 9
```

### The Steering Wheel Rules:
Calculate `cur_sum = numbers[l] + numbers[r]`:
1. **If `cur_sum == target`:** Match found! Return `[l + 1, r + 1]`.
2. **If `cur_sum < target`:** The sum is too small. Squeeze the left pointer forward (`l += 1`) to pick a larger number!
3. **If `cur_sum > target`:** The sum is too large. Squeeze the right pointer backward (`r -= 1`) to pick a smaller number!

```text
Step 1: numbers[0] + numbers[3] = 2 + 15 = 17 (> 9). Too big! r -= 1.
Step 2: numbers[0] + numbers[2] = 2 + 11 = 13 (> 9). Too big! r -= 1.
Step 3: numbers[0] + numbers[1] = 2 + 7  =  9 (== 9). Match! Return [1, 2].
```

---

## 💻 Production Implementation

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l, r = 0, len(numbers) - 1
        
        while l < r:
            cur_sum = numbers[l] + numbers[r]
            
            if cur_sum == target:
                return [l + 1, r + 1]
            elif cur_sum < target:
                l += 1  # Need a larger sum
            else:
                r -= 1  # Need a smaller sum
                
        return []
```

---

## ⚡ Complexity Comparison

| Method | Time | Space | Meets Constraint? | Interview Grade |
|---|---|---|---|---|
| HashMap (Dict) | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | ❌ No | Pass (with follow-up prompt) |
| **Two Pointers Squeeze** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | ✅ **Yes** | 🏆 **FAANG Gold Standard** |
