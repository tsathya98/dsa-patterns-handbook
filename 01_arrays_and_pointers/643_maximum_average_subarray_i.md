# 🪟 LeetCode 643: Maximum Average Subarray I – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** LeetCode 75 / Top Interview 150  
> **Pattern:** Fixed-Size Sliding Window (The Running Differential Pattern)  
> **LeetCode Link:** [LeetCode 643: Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/)

---

## 📌 Problem in Plain English

You are given an integer array `nums` consisting of `n` elements, and an integer `k`.

Find a contiguous subarray whose **length is equal to `k`** that has the **maximum average value** and return this value. Any calculation with a precision error $\le 10^{-5}$ will be accepted.

### Example:
```text
Input: nums = [1, 12, -5, -6, 50, 3], k = 4
Output: 12.75
Explanation: Subarray [12, -5, -6, 50] has sum 51, and 51 / 4 = 12.75
```

---

## 💡 The "Aha!" Moment: The Running Differential Pattern 🪟

### Why Brute Force Gets TLE:
If you take a slice `nums[i:i+k]` or use a loop to add $k$ numbers for every starting point:
* You repeat $k$ operations $(n - k + 1)$ times $\implies \mathcal{O}(n \cdot k)$ operations.
* When $n = 100,000$ and $k = 50,000$, that's $\approx 2.5 \times 10^9$ operations $\implies$ **Instant Time Limit Exceeded (TLE)**!

### The Insight:
Notice what happens when a fixed-size window of size $k=4$ moves forward by 1 step:

```text
Step 1: [ 1,  12,  -5,  -6 ],  50,   3    -> Window sum = 1 + 12 - 5 - 6 = 2
          ▲
       (leaves!)

Step 2:   1, [ 12,  -5,  -6,   50 ], 3    -> Window sum = 12 - 5 - 6 + 50 = 51
                               ▲
                            (enters!)
```

The middle numbers `[12, -5, -6]` are shared by **both** windows!  
Instead of recalculating them from scratch, you update the sum in **$\mathcal{O}(1)$**:

$$\text{new\_sum} = \text{old\_sum} - \text{leaving\_element} + \text{entering\_element}$$

---

## 💻 Code Implementations & Progression

### ❌ Step 1: Initial Working Sliding Window (Good, but has micro-bottlenecks)
```python
class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        tot = sum(nums[:k])
        avg = tot / k
        max_avg = avg
        for i in range(1, len(nums) - k + 1):
            tot = tot - nums[i - 1] + nums[i + k - 1]
            avg = tot / k                         # ⚠️ Bottleneck: Float division in each loop!
            max_avg = max(max_avg, avg)           # ⚠️ Function-call overhead
        return max_avg
```

### ✅ Step 2: Fully Optimized Interview Solution (1.6× Faster, Cleaner Indices)

```python
class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        # 1. Establish the baseline sum for the first window of size k
        tot = sum(nums[:k])
        max_tot = tot
        
        # 2. Slide window from index k to len(nums)
        # entering element: nums[i]
        # leaving element:  nums[i - k]
        for i in range(k, len(nums)):
            tot += nums[i] - nums[i - k]
            if tot > max_tot:
                max_tot = tot
                
        # 3. Divide by k once at the very end
        return max_tot / k
```

---

## ⚡ Key Optimizations & Interview Pro Tips

| Technique | Why it Matters |
| :--- | :--- |
| **Index Shift (`range(k, len(nums))` vs `range(1, len-k+1)`)** | Entering element is cleanly `nums[i]`, leaving element is `nums[i - k]`. Eliminates tricky `nums[i + k - 1]` off-by-one errors. |
| **Deferred Division (`max_tot / k` at end)** | Since $k > 0$, maximizing the sum maximizes the average. Floating-point division (`/`) is much slower than integer operations; doing it only once saves $100,000$ float allocations. |
| **`if tot > max_tot` vs `max()`** | Avoids the function-call overhead of Python's built-in `max()` inside tight loops. |

---

## ⏱️ Complexity Blueprint

* **Time Complexity:** $\mathcal{O}(n)$ — exactly one pass over the array of size $n$.
* **Space Complexity:** $\mathcal{O}(1)$ — auxiliary storage for only two scalar variables (`tot`, `max_tot`).
