# LeetCode 560: Subarray Sum Equals K

> **Difficulty:** Medium | **Pattern:** Running Prefix Sum + Hash Map Frequency  
> **Source Code:** [`560_subarray_sum_equals_k.py`](./560_subarray_sum_equals_k.py) | **Link:** [LeetCode 560](https://leetcode.com/problems/subarray-sum-equals-k/)

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

If the running prefix sum from index $0 \dots i$ is `cur_sum`, and some earlier prefix from index $0 \dots j$ had sum `cur_sum - k`, then the subarray between $j + 1$ and $i$ must sum to exactly $k$:

$$\text{sum}(j + 1 \dots i) = \text{cur\_sum} - (\text{cur\_sum} - k) = k$$

Store a hash map `prefix_counts` tracking the frequency of every prefix sum seen so far:
- **Base seed:** Initialize `prefix_counts = {0: 1}`. An empty prefix before index 0 has sum 0. If `cur_sum == k` starting directly from index 0, `cur_sum - k = 0` matches this seed!
- For each number:
  1. `cur_sum += x`
  2. `count += prefix_counts.get(cur_sum - k, 0)`
  3. `prefix_counts[cur_sum] = prefix_counts.get(cur_sum, 0) + 1`

```text
Target k = 3
Array:          [  1,    2,    1,   -1,    2 ]
cur_sum:           1     3     4     3     5
cur_sum - k:      -2     0     1     0     2
Found in map?     No   Yes(0) Yes(1) Yes(0) No
Cumulative ans:    0     1     2     3     3
```

### Algorithm steps:
* **1. Seed prefix map:** `prefix_counts = {0: 1}`, `cur_sum = 0`, `count = 0`.
* **2. Iterate:** For each `x` in `nums`:
  * Accumulate: `cur_sum += x`.
  * Query complement: `count += prefix_counts.get(cur_sum - k, 0)`.
  * Record frequency: `prefix_counts[cur_sum] = prefix_counts.get(cur_sum, 0) + 1`.
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
            count += prefix_counts.get(cur_sum - k, 0)
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
