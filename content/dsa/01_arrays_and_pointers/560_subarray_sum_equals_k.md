# LeetCode 560: Subarray Sum Equals K

> **Difficulty:** Medium | **Pattern:** Running Prefix Sum + Hash Map Frequency  
> **Source Code:** [`560_subarray_sum_equals_k.py`](560_subarray_sum_equals_k.py) | **Link:** [LeetCode 560](https://leetcode.com/problems/subarray-sum-equals-k/)

## The problem

Given an integer array `nums` and an integer `k`, return the total number of contiguous subarrays whose sum equals `k`.

```text
Input:  nums = [1, 2, 3],  k = 3
Output: 2   (Subarrays [1, 2] and [3])

Input:  nums = [1, -1, 0], k = 0
Output: 3   (Subarrays [1, -1], [0], and [1, -1, 0])
```

---

## Why sliding window fails here

`nums` can contain **negative numbers** and **zeroes**. A two-pointer sliding window requires monotonicity: expanding right must grow the window sum, and shrinking left must decrease it. With negative numbers, adding an element can decrease the sum, which breaks sliding window completely.

---

## Approach 1: Brute force (nested loops)

Fix every start index `i` from $0 \dots n - 1$, expand `j` from `i \dots n - 1`, maintain running `curr_sum += nums[j]`, and increment `count` whenever `curr_sum == k`.
* **Time:** $\mathcal{O}(N^2)$ nested iterations.
* **Space:** $\mathcal{O}(1)$ auxiliary space. Hits TLE for $N = 2 \times 10^4$.

---

## Approach 2: Semi-optimized (explicit prefix array)

Precompute an $(N + 1)$-length prefix sum array where `prefix[i] = sum(nums[0...i-1])`.
Any subarray sum from index `i` to `j - 1` is given by `prefix[j] - prefix[i]`.
Check all pairs `(i, j)` in $\mathcal{O}(N^2)$ time.
* **Time:** $\mathcal{O}(N^2)$.
* **Space:** $\mathcal{O}(N)$ to store the prefix array. Shows clear prefix sum intuition, but still too slow.

---

## Approach 3: Optimized (running prefix sum + hash map frequency)

### The tape cutting analogy:
Think of `cur_sum` as a measuring tape starting at index 0 that keeps extending (never reset).
If the total tape length from index 0 to `i` is `cur_sum`, and we want a piece at the end that sums to `k`:
$$\text{Front slice to cut off} = \text{cur\_sum} - k$$

Every time that exact `needed_cut` appeared as a previous prefix measurement, chopping it off leaves a valid contiguous subarray ending at `i` that sums to `k`.

```text
[ 3,   4,   2,   5 ]  (cur_sum = 14, k = 7)
├─────────┤├───────┤
  Cut off    Target 
  prefix       k=7
 (14-7=7)
```

### Why cur_sum is never reset:
`cur_sum` is an odometer from the starting line (index 0). If you reset it midway, previous measurements lose their common origin and subtracting readings breaks.

### Algorithm steps:
* **1. Base seed:** `prefix_counts = {0: 1}`, `cur_sum = 0`, `count = 0`. An empty prefix before index 0 has distance 0.
* **2. Step forward:** For each `x` in `nums`:
  * `cur_sum += x`
  * `needed_cut = cur_sum - k`
  * `count += prefix_counts.get(needed_cut, 0)`
  * `prefix_counts[cur_sum] = prefix_counts.get(cur_sum, 0) + 1`
* **3. Return:** `count` in single-pass linear time.

---

<details>
<summary>Spoiler: Solution Code (All 3 Approaches)</summary>

```python
class Solution:
    # Approach 1: Brute Force (O(N^2) time, O(1) space)
    def subarraySum_brute(self, nums: list[int], k: int) -> int:
        count = 0
        n = len(nums)
        for i in range(n):
            curr_sum = 0
            for j in range(i, n):
                curr_sum += nums[j]
                if curr_sum == k:
                    count += 1
        return count

    # Approach 2: Semi-Optimized (O(N^2) time, O(N) space)
    def subarraySum_prefix_array(self, nums: list[int], k: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]
        count = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                if prefix[j] - prefix[i] == k:
                    count += 1
        return count

    # Approach 3: Optimized Running Hash Map (O(N) time, O(N) space)
    def subarraySum(self, nums: list[int], k: int) -> int:
        prefix_counts = {0: 1}
        cur_sum = 0
        count = 0

        for x in nums:
            cur_sum += x
            needed_cut = cur_sum - k
            count += prefix_counts.get(needed_cut, 0)
            prefix_counts[cur_sum] = prefix_counts.get(cur_sum, 0) + 1

        return count
```

</details>

---

## Complexity comparison

| Approach | Time Complexity | Auxiliary Space | Status |
|---|---|---|---|
| **1. Brute Force** | $\mathcal{O}(N^2)$ | $\mathcal{O}(1)$ | TLE on $N = 2 \times 10^4$ |
| **2. Prefix Array** | $\mathcal{O}(N^2)$ | $\mathcal{O}(N)$ | TLE, extra memory |
| **3. Running Hash Map** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Optimal FAANG bar |
