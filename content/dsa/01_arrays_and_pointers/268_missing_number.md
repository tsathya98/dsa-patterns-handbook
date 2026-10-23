# LeetCode 268: Missing Number

> **Difficulty:** Easy | **Pattern:** Bitwise XOR / Gauss Arithmetic Sum  
> **Source Code:** [`268_missing_number.py`](./268_missing_number.py) | **Link:** [LeetCode 268](https://leetcode.com/problems/missing-number/)

## The problem

Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

```text
Input: nums = [3, 0, 1]
Output: 2 (Range is [0, 3], length is 3, missing 2)

Input: nums = [0, 1]
Output: 2 (Range is [0, 2], length is 2, missing 2)
```

---

## Approach 1: Brute force (sort and compare)

Sort `nums` in ascending order. Compare `nums[i]` with `i`. The first index where `nums[i] != i` is the missing number. If all match, the missing number is `n`.
* **Time:** $\mathcal{O}(N \log N)$ sorting time.
* **Space:** $\mathcal{O}(1)$ or $\mathcal{O}(N)$ depending on the sort implementation.

---

## Approach 2: Semi-optimized (hash set / counter lookup)

Store all numbers in a hash map or hash set. Loop `i` from $0 \dots n$. The first number not present in the set is the answer.
* **Time:** $\mathcal{O}(N)$ lookup time.
* **Space:** $\mathcal{O}(N)$ auxiliary memory. Works, but wastes $\mathcal{O}(N)$ memory on distinct small integers.

---

## Approach 3: Optimized (Gauss arithmetic sum)

The sum of integers from $0$ to $n$ is given by Gauss's formula:

$$\text{expected\_sum} = \frac{n(n + 1)}{2}$$

The missing number is simply the difference between the expected total and the actual sum:

$$\text{missing} = \text{expected\_sum} - \sum_{x \in \text{nums}} x$$

* **Time:** $\mathcal{O}(N)$ single pass.
* **Space:** $\mathcal{O}(1)$ auxiliary space.
* **Trap in typed languages:** In C++ or Java, if $n = 10^5$, $n(n + 1)$ can cause 32-bit integer overflow. Python handles arbitrarily large integers automatically.

---

## Approach 4: Optimal FAANG standard (bitwise XOR)

XOR ($\oplus$) has two fundamental algebraic properties:
1. Self-cancellation: $x \oplus x = 0$
2. Identity: $x \oplus 0 = x$

If we XOR every index $i \in [0, n]$ together with every value in `nums`, all present numbers appear exactly twice and cancel out to 0. The missing number appears only once and survives!

```text
nums = [3, 0, 1],  n = 3
Expected values:  0 ^ 1 ^ 2 ^ 3
Actual values:    3 ^ 0 ^ 1
Combined XOR:    (0 ^ 0) ^ (1 ^ 1) ^ (3 ^ 3) ^ 2
               = 0 ^ 0 ^ 0 ^ 2 = 2
```

### Algorithm steps:
* **1. Initialize:** `ans = len(nums)` (covers the $n$-th index).
* **2. Sweep:** For each index `i` and value `num` in `enumerate(nums)`:
  * `ans ^= i ^ num`
* **3. Return:** `ans` in $\mathcal{O}(N)$ time and $\mathcal{O}(1)$ space with zero overflow risk.

---

<details>
<summary>Spoiler: Solution Code (All Approaches)</summary>

```python
from collections import Counter
from typing import List


class Solution:
    # Approach 1: Sorting O(N log N) time, O(1) space
    def missingNumber_sort(self, nums: List[int]) -> int:
        nums.sort()
        for i, val in enumerate(nums):
            if i != val:
                return i
        return len(nums)

    # Approach 2: Hash Set / Counter O(N) time, O(N) space
    def missingNumber_counter(self, nums: List[int]) -> int:
        dct = Counter(nums)
        n = len(nums)
        for i in range(n + 1):
            if i not in dct:
                return i
        return -1

    # Approach 3: Gauss Math Sum O(N) time, O(1) space
    def missingNumber_math(self, nums: List[int]) -> int:
        n = len(nums)
        expected_sum = n * (n + 1) // 2
        return expected_sum - sum(nums)

    # Approach 4: Bitwise XOR O(N) time, O(1) space (FAANG Gold Standard)
    def missingNumber(self, nums: List[int]) -> int:
        ans = len(nums)
        for i, num in enumerate(nums):
            ans ^= i ^ num
        return ans
```

</details>

---

## Complexity comparison

| Approach | Time Complexity | Auxiliary Space | Status |
|---|---|---|---|
| **1. Sorting** | $\mathcal{O}(N \log N)$ | $\mathcal{O}(1)$ | Sub-optimal time |
| **2. Hash Set / Counter** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Passes, but memory overhead |
| **3. Gauss Math Sum** | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | Optimal, slight overflow risk in C++ |
| **4. Bitwise XOR** | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ | FAANG gold standard (zero overflow) |
