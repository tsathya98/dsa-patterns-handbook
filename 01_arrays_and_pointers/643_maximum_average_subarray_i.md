# LeetCode 643: Maximum Average Subarray I

> **Difficulty:** Easy | **Pattern:** Fixed-Size Sliding Window (Running Differential)  
> **LeetCode:** [643. Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/)

## The problem

Given an integer array `nums` of length `n` and an integer `k`, find a contiguous subarray of length `k` with the maximum average value and return that average. Answers within $10^{-5}$ of the actual value are accepted.

```text
Input:  nums = [1, 12, -5, -6, 50, 3], k = 4
Output: 12.75
Explanation: Subarray [12, -5, -6, 50] has sum 51, and 51 / 4 = 12.75.
```

## Why the naive way fails

Recomputing `sum(nums[i : i + k])` at every starting index adds $k$ elements $(n - k + 1)$ times, taking $\mathcal{O}(n \cdot k)$ time. For $n = 100,000$ and $k = 50,000$, that is $2.5 \times 10^9$ additions and triggers Time Limit Exceeded.

## The core trick: Subtract the leaving element, add the entering element

When a window of size $k = 4$ slides right by one index, the middle $k - 1$ elements stay unchanged:

```text
Window 1: [ 1,  12,  -5,  -6 ],  50,   3   -> sum = 2
            ^ leaves

Window 2:   1, [ 12,  -5,  -6,   50 ], 3   -> sum = 2 - 1 + 50 = 51
                                 ^ enters
```

Update the running sum in $\mathcal{O}(1)$ time at each step `i` (for `i` from `k` to `n - 1`):

$$\text{tot} = \text{tot} + \text{nums}[i] - \text{nums}[i - k]$$

### Practical optimizations

1. **Loop `for i in range(k, len(nums))`:** Indexing by the entering element `i` makes the leaving element `i - k`, avoiding `i + k - 1` off-by-one bugs.
2. **Divide by `k` once at the end:** Since $k > 0$ is constant, the subarray with the largest sum also has the largest average. Tracking `max_tot` as an integer and returning `max_tot / k` at the end avoids $n - k$ floating-point divisions inside the loop.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        tot = sum(nums[:k])
        max_tot = tot

        for i in range(k, len(nums)):
            tot += nums[i] - nums[i - k]
            if tot > max_tot:
                max_tot = tot

        return max_tot / k
```

</details>

## Complexity

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n)$ | Sums the first $k$ elements once, then takes $n - k$ constant-time steps. |
| **Space** | $\mathcal{O}(1)$ | Only tracks `tot` and `max_tot`. (To avoid allocating the initial `nums[:k]` slice in Python, you can use `sum(nums[i] for i in range(k))`). |
