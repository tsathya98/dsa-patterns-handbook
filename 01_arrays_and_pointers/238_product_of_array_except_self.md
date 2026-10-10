# 🍞 LeetCode 238: Product of Array Except Self – Master Study Guide

> **Difficulty:** Medium | **Pattern:** Prefix & Suffix Accumulator (The Sandwich Pattern)  
> **Complexity:** Time: $\mathcal{O}(n)$ | Auxiliary Space: $\mathcal{O}(1)$ (Output array excluded)  
> **Source Code:** [`238_product_of_array_except_self.py`](./238_product_of_array_except_self.py)

---

## 📌 Problem in Plain English

Given an integer array `nums`, return an array `res` such that `res[i]` is equal to the product of all elements of `nums` **except `nums[i]`**.

* **Constraint 1:** You must write an algorithm that runs in $\mathcal{O}(n)$ time.
* **Constraint 2:** You **cannot use the division operation `/`**.

```text
Example 1:
Input:  nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]

Explanation:
- res[0] = 2 * 3 * 4 = 24
- res[1] = 1 * 3 * 4 = 12
- res[2] = 1 * 2 * 4 = 8
- res[3] = 1 * 2 * 3 = 6

Example 2:
Input:  nums = [-1, 1, 0, -3, 3]
Output: [0, 0, 9, 0, 0]
```

---

## 🧠 Mental Model: The Sandwich (Left × Right)

Without division, the product of everything except index `i` is simply:
$$\text{res}[i] = (\text{product of everything to the LEFT of } i) \times (\text{product of everything to the RIGHT of } i)$$

```text
Array:               [ 1,      2,      3,      4 ]

Prefix (Left):       [ 1,      1,      2,      6 ]   (what's before each element)
Suffix (Right):      [ 24,     12,     4,      1 ]   (what's after each element)
--------------------------------------------------------------------------------
Result (Left × Right): [ 24,    12,     8,      6 ]
```

---

## 🚀 The $\mathcal{O}(1)$ Extra Space Optimization (FAANG Follow-Up)

Instead of allocating two separate lists `prefix = []` and `suffix = []`, we reuse `res`!

1. **Forward Pass:** Store all left products directly into `res`.
2. **Backward Pass:** Use a single scalar variable `suffix = 1` moving backward, multiplying directly into `res[i]` on the fly.

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [1] * n
        
        # 1. Forward Pass: Collect products to the left
        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]
            
        # 2. Backward Pass: Multiply products to the right on the fly
        suffix = 1
        for i in range(n - 1, -1, -1):
            res[i] *= suffix
            suffix *= nums[i]
            
        return res
```

---

## ⚡ Complexity & Trade-offs

| Approach | Time | Aux Space | Notes |
|---|---|---|---|
| Brute Force (Nested loops) | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | TLE for $n = 10^5$. |
| Total Product with Division `/` | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Breaks on `0` (ZeroDivisionError) and banned by problem. |
| Separate `prefix[]` & `suffix[]` | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | ✅ Great intuitive baseline (what you coded!). |
| **Running In-Place `res[]` (Optimal)** | $\mathcal{O}(n)$ | **$\mathcal{O}(1)$** | 🏆 FAANG Standard. Beats memory percentiles. |
