# LeetCode 560: Subarray Sum Equals K

> **Difficulty:** Medium | **Pattern:** Running Prefix Sum + Hash Map Frequency (`prefix_sum - k`) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/subarray-sum-equals-k/](https://leetcode.com/problems/subarray-sum-equals-k/)

## The problem

Given an array of integers `nums` and an integer `k`, return the total number of contiguous subarrays whose sum equals `k`.

```text
Input:  nums = [1, 2, 3],  k = 3
Output: 2   (subarrays [1, 2] and [3])
```

---

## Why sliding window fails here

`nums` can contain **negative numbers** and **zeroes** (e.g., `nums = [1, -1, 1], k = 1`). When elements can be negative, expanding the window does not monotonically increase the sum, and shrinking does not monotonically decrease it.

---

## The core trick: Prefix sum complement lookup (`cur_sum - k`)

If the running sum from index `0` to `i` is `cur_sum`, and some earlier prefix from `0` to `j` had sum `cur_sum - k`, then the subarray between `j + 1` and `i` must sum to exactly `k`:
$$\text{sum}(j+1 \dots i) = \text{cur\_sum} - (\text{cur\_sum} - k) = k$$

Store a hash map `prefix_counts = {0: 1}` mapping each prefix sum to how many times it has occurred so far.
* Why `{0: 1}`? An empty prefix before index `0` has sum `0`. If `cur_sum == k` right from index `0`, `cur_sum - k = 0` matches that base case!

---

## Step-by-step trace (`nums = [1, 2, 1, -1, 2]`, `k = 3`)

**Initial state:**
```text
cur_sum = 0,  ans = 0,  prefix_counts = {0: 1}
```

**Iteration 1 (`x = 1`):**
`cur_sum = 1`. Need `cur_sum - k = 1 - 3 = -2` (count `0`).
Record `cur_sum = 1`:
```text
ans = 0,  prefix_counts = {0: 1, 1: 1}
```

**Iteration 2 (`x = 2`):**
`cur_sum = 3`. Need `3 - 3 = 0`. `prefix_counts[0]` is `1`! (`[1, 2]` sums to 3).
```text
ans = 0 + 1 = 1,  prefix_counts = {0: 1, 1: 1, 3: 1}
```

**Iteration 3 (`x = 1`):**
`cur_sum = 4`. Need `4 - 3 = 1`. `prefix_counts[1]` is `1`! (`[2, 1]` sums to 3).
```text
ans = 1 + 1 = 2,  prefix_counts = {0: 1, 1: 1, 3: 1, 4: 1}
```

**Iteration 4 (`x = -1`):**
`cur_sum = 3`. Need `3 - 3 = 0`. `prefix_counts[0]` is `1`! (`[1, 2, 1, -1]` sums to 3).
Now `3` appears a **second** time in `prefix_counts`:
```text
ans = 2 + 1 = 3,  prefix_counts = {0: 1, 1: 1, 3: 2, 4: 1}
```

**Iteration 5 (`x = 2`):**
`cur_sum = 5`. Need `5 - 3 = 2` (count `0`).
```text
ans = 3,  prefix_counts = {0: 1, 1: 1, 3: 2, 4: 1, 5: 1}
```

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        prefix_counts = {0: 1}
        cur_sum = 0
        ans = 0

        for x in nums:
            cur_sum += x
            ans += prefix_counts.get(cur_sum - k, 0)
            prefix_counts[cur_sum] = prefix_counts.get(cur_sum, 0) + 1

        return ans
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(N)$ single pass.
* **Space:** $\mathcal{O}(N)$ for the `prefix_counts` hash map.
