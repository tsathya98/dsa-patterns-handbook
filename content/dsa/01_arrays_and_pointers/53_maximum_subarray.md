# LeetCode 53: Maximum Subarray

> **Difficulty:** Medium | **Pattern:** Kadane's Algorithm (Running Prefix Reset)  
> **Source Code:** [`53_maximum_subarray.py`](53_maximum_subarray.py) | **Link:** [LeetCode 53](https://leetcode.com/problems/maximum-subarray/)

## The problem

Find the contiguous subarray inside `nums` that has the largest sum, and return that sum.

```text
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6  (From subarray [4, -1, 2, 1])
```

---

## Approach 1: Brute force (nested loops)

Check every possible subarray `(i, j)`. Compute running sums and track the maximum.
* **Time:** $\mathcal{O}(N^2)$ nested iterations.
* **Space:** $\mathcal{O}(1)$. Hits TLE for $N = 10^5$.

---

## Approach 2: Semi-optimized (divide and conquer)

Split the array in half at `mid`. The maximum subarray must lie in one of three places:
1. Entirely in the left half.
2. Entirely in the right half.
3. Crossing the midpoint (spanning from `mid` leftward and `mid + 1` rightward).

Solve recursively with recurrence $T(N) = 2T(N/2) + \mathcal{O}(N)$.
* **Time:** $\mathcal{O}(N \log N)$.
* **Auxiliary space:** $\mathcal{O}(\log N)$ recursion stack frames. Follow-up question often asked by interviewers.

---

## Approach 3: Optimized (Kadane's algorithm)

Walk through the array while keeping a running `cur_sum`. At each number `num`, ask:
> *"Does adding `num` to the previous running sum help, or is the previous sum dragging me down?"*

- If `cur_sum < 0`, carrying it forward hurts future sums. Drop the past baggage and start fresh at `num`.
- If `cur_sum >= 0`, keep the positive cushion and add `num`.

```python
cur_sum = max(cur_sum + num, num)
max_sum = max(max_sum, cur_sum)
```

```text
nums:      [ -2,   1,  -3,   4,  -1,   2,   1,  -5,   4 ]
cur_sum:     -2    1   -2    4    3    5    6    1    5
Decision:   start reset reset start keep keep keep keep keep
max_sum:     -2    1    1    4    4    5    6    6    6
```

### Algorithm steps:
* **1. Initialize:** `max_sum = float("-inf")`, `cur_sum = 0`.
* **2. Iterate:** For each `num` in `nums`:
  * `cur_sum = max(cur_sum + num, num)`
  * `max_sum = max(max_sum, cur_sum)`
* **3. Return:** `max_sum` in single pass.

---

<details>
<summary>Spoiler: Solution Code (All 3 Approaches)</summary>

```python
class Solution:
    # Approach 1: Brute Force (O(N^2) time, O(1) space)
    def maxSubArray_brute(self, nums: list[int]) -> int:
        n = len(nums)
        max_sum = float("-inf")
        for i in range(n):
            curr_sum = 0
            for j in range(i, n):
                curr_sum += nums[j]
                max_sum = max(max_sum, curr_sum)
        return int(max_sum)

    # Approach 2: Divide and Conquer (O(N log N) time, O(log N) space)
    def maxSubArray_divide_and_conquer(self, nums: list[int]) -> int:
        def cross_sum(left: int, mid: int, right: int) -> int:
            left_sum = float("-inf")
            curr = 0
            for i in range(mid, left - 1, -1):
                curr += nums[i]
                left_sum = max(left_sum, curr)

            right_sum = float("-inf")
            curr = 0
            for i in range(mid + 1, right + 1):
                curr += nums[i]
                right_sum = max(right_sum, curr)

            return int(left_sum + right_sum)

        def helper(left: int, right: int) -> int:
            if left == right:
                return nums[left]
            mid = (left + right) // 2
            left_best = helper(left, mid)
            right_best = helper(mid + 1, right)
            cross_best = cross_sum(left, mid, right)
            return max(left_best, right_best, cross_best)

        return helper(0, len(nums) - 1)

    # Approach 3: Kadane's Algorithm (O(N) time, O(1) space)
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = float("-inf")
        cur_sum = 0
        for num in nums:
            cur_sum = max(cur_sum + num, num)
            max_sum = max(max_sum, cur_sum)
        return int(max_sum)
```

</details>

---

## Complexity comparison

| Approach | Time Complexity | Auxiliary Space | Status |
|---|---|---|---|
| **1. Brute Force** | $\mathcal{O}(N^2)$ | $\mathcal{O}(1)$ | TLE on $N = 10^5$ |
| **2. Divide & Conquer** | $\mathcal{O}(N \log N)$ | $\mathcal{O}(\log N)$ | Classic interview follow-up |
| **3. Kadane's Algorithm** | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Optimal FAANG benchmark |
