# 🪣 LeetCode 11: Container With Most Water – Two-Pointer Master Guide

> **Difficulty:** Medium  
> **Study Plan:** Top Interview 150 / NeetCode 150 / Blind 75  
> **Pattern:** Two Pointers (Shrinking Window / Opposite Ends)  
> **LeetCode Link:** [LeetCode 11: Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

---

## 📌 Problem Description

You are given an integer array `height` of length $n$. There are $n$ vertical lines drawn such that the two endpoints of the $i$-th line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return *the maximum amount of water a container can store*.

> **Notice:** You may not slant the container.

```text
Example 1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. 
The max area is between index 1 (height 8) and index 8 (height 7).
Width = 8 - 1 = 7.
Height = min(8, 7) = 7.
Area = 7 * 7 = 49.

Example 2:
Input: height = [1,1]
Output: 1
```

---

## 💡 The "Aha!" Intuition: Why Brute Force is Too Slow

The area between two bars at indices $l$ and $r$ ($l < r$) is governed by:
$$\text{Area} = \text{width} \times \text{height} = (r - l) \times \min(height[l], height[r])$$

A naive brute-force checks all pairs $(l, r)$, which takes $\mathcal{O}(n^2)$ time. With $n \le 10^5$, $\mathcal{O}(n^2) = 10^{10}$ operations, which triggers a **Time Limit Exceeded (TLE)**.

### The Two-Pointer Strategy
To do this in $\mathcal{O}(n)$, we start with the widest possible container:
- `l = 0` (leftmost bar)
- `r = len(height) - 1` (rightmost bar)

At every step, the distance between the lines ($\text{width} = r - l$) **shrinks by 1**.

```text
    Index:   0   1   2   3   4   5   6   7   8
   Height:  [1,  8,  6,  2,  5,  4,  8,  3,  7]
             ▲                               ▲
             │                               │
            left                           right
     Width = 8 - 0 = 8
     Bottleneck = min(1, 7) = 1
     Area = 8 * 1 = 8
```

### 🔑 The Crucial Question: Which pointer do we move?
The water capacity is bottlenecked strictly by the **shorter line**.
- If we move the **taller line inward**:
  - The width **decreases** $(r - l - 1)$.
  - The height can at best be the same shorter line (or even shorter).
  - Therefore, the area **can only decrease or stay worse**. It is mathematically impossible to find a larger area by moving the taller line!
- If we move the **shorter line inward**:
  - The width still decreases.
  - BUT we might encounter a much taller line that compensates for the lost width.
  - This is the **only move that could possibly yield a larger area**.

Hence, the greedy choice is always: **advance the pointer of the shorter line**.

---

## 💻 Standard Optimal Solution (User's Solution)

```python
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        l = 0
        r = len(height) - 1
        max_area = 0
        
        while l < r:
            min_h = min(height[l], height[r])
            width = r - l
            curr_area = width * min_h
            max_area = max(curr_area, max_area)
            
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
            
        return max_area
```

---

## ⏱️ Complexity Analysis

* **Time Complexity:** $\mathcal{O}(n)$ — Every iteration moves either pointer `l` forward or pointer `r` backward by 1. The two pointers meet after at most $n - 1$ steps. Since we must read through the heights to find the maximum, $\mathcal{O}(n)$ is asymptotically optimal.
* **Space Complexity:** $\mathcal{O}(1)$ — Only a few primitive variables (`l`, `r`, `max_area`, `min_h`, `width`) are allocated in memory.

---

## 🔬 Critical Findings & Practical Optimizations

While the above solution is asymptotically optimal ($\mathcal{O}(n)$), here are important findings regarding real-world performance and interview expectations:

### 1. The Fast-Forward Optimization (Skipping Shorter Bars)
Whenever you move a pointer away from a line of height $h$, the next container will have a smaller width. 
If the next bar is **shorter than or equal to** $h$, its area is **guaranteed to be strictly smaller** than the area you just evaluated:
$$\text{new\_area} = (\text{width} - 1) \times \min(h_{\text{new}}, h_{\text{other}}) \le (\text{width} - 1) \times h < \text{width} \times h$$

Therefore, you can safely skip all subsequent bars that are $\le$ the current bottleneck without calculating their area:

```python
while l < r and height[l] <= hl:
    l += 1
```

### 2. Built-in Function Call Overhead in Python
In a tight loop running $10^5$ times:
- `min()` and `max()` are Python function calls that add slight frame overhead.
- Writing `hl < hr` and comparing directly with an `if area > max_area:` eliminates redundant comparisons and avoids calling `min()` followed immediately by another comparison check.

### 3. Fast-Forward Implementation (Beats ~95%+ on LeetCode)

```python
from typing import List

class SolutionOptimized:
    def maxArea(self, height: List[int]) -> int:
        l = 0
        r = len(height) - 1
        max_area = 0

        while l < r:
            hl, hr = height[l], height[r]
            
            if hl < hr:
                area = (r - l) * hl
                if area > max_area:
                    max_area = area
                # Fast-forward past any bars shorter than or equal to hl
                while l < r and height[l] <= hl:
                    l += 1
            else:
                area = (r - l) * hr
                if area > max_area:
                    max_area = area
                # Fast-forward past any bars shorter than or equal to hr
                while l < r and height[r] <= hr:
                    r -= 1

        return max_area
```

---

## 🏢 Mega-Company (Google / FAANG) Interview Playbook

### Do companies like Google expect the faster version?
**No, they do not expect you to code the micro-optimized version first.**

1. **Cleanliness & Maintainability:** The standard solution is clean, readable, and less prone to off-by-one errors or missed boundary checks (`l < r`). Google interviewers prioritize bug-free, readable production code.
2. **Identical Asymptotic Complexity:** Both solutions are $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space. The theoretical worst-case (e.g., strictly monotonically increasing or decreasing heights) executes the exact same number of operations.
3. **The Winning Interview Strategy:**
   - **Step 1:** Write the standard clean solution first and prove correctness with a walk-through.
   - **Step 2:** State the complexity ($\mathcal{O}(n)$ time, $\mathcal{O}(1)$ space) and explain why $\mathcal{O}(n)$ is theoretically optimal.
   - **Step 3 (The Senior Signal):** Offer the fast-forward observation verbally:
     > *"Asymptotically we are at the optimal $\mathcal{O}(n)$, but as a practical constant-factor optimization, whenever we move a pointer because it was the bottleneck, any subsequent line on that side that is $\le$ the bottleneck height cannot possibly beat our max area because width has decreased. We can fast-forward past them with an inner while loop."*
   - This demonstrates deep optimization insight without adding unnecessary code complexity.
