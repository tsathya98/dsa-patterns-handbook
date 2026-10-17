# LeetCode 238: Product of Array Except Self

> **Difficulty:** Medium | **Pattern:** Prefix and Suffix Accumulator  
> **Source Code:** [`238_product_of_array_except_self.py`](./238_product_of_array_except_self.py)

## The problem

Given an integer array `nums`, return an array `res` where `res[i]` is the product of all elements in `nums` except `nums[i]`.
- Must run in $\mathcal{O}(n)$ time.
- Cannot use the division operator `/`.

```text
Input:  nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]

Input:  nums = [-1, 1, 0, -3, 3]
Output: [0, 0, 9, 0, 0]
```

## Why division fails

Even if division were allowed, taking the total product and dividing by `nums[i]` breaks as soon as the array contains a `0` (`ZeroDivisionError`). You would have to write separate branches for zero count $= 0$, $= 1$, and $\ge 2$.

## The core trick: Left product times right product

Without division, the product of everything except index `i` is the product of everything to its left multiplied by everything to its right:

$$\text{res}[i] = \left(\prod_{j=0}^{i-1} \text{nums}[j]\right) \times \left(\prod_{j=i+1}^{n-1} \text{nums}[j]\right)$$

```text
nums:                [  1,   2,   3,   4 ]
Prefix (left of i):  [  1,   1,   2,   6 ]
Suffix (right of i): [ 24,  12,   4,   1 ]
------------------------------------------
res (Left * Right):  [ 24,  12,   8,   6 ]
```

### Algorithm steps:
* **1. Initialize result array:** Create `res = [1] * n` and track running `prefix = 1`.
* **2. Forward pass (left products):** For each index `i` from `0` to `n - 1`:
  * Store current prefix product: `res[i] = prefix`.
  * Update prefix product: `prefix *= nums[i]`.
* **3. Backward pass (right products):** Initialize running `suffix = 1`. For each index `i` from `n - 1` down to `0`:
  * Multiply stored prefix with suffix: `res[i] *= suffix`.
  * Update suffix product: `suffix *= nums[i]`.
* **4. Return:** `res` in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ auxiliary space.

## Cutting space from $\mathcal{O}(n)$ to $\mathcal{O}(1)$

Allocating separate `prefix` and `suffix` arrays works in $\mathcal{O}(n)$ space, but you can do both passes directly inside the output array `res`:
1. **Forward pass:** Sweep left to right with a running `prefix = 1`. Write `prefix` into `res[i]`, then multiply `prefix` by `nums[i]`.
2. **Backward pass:** Sweep right to left with a running `suffix = 1`. Multiply `res[i]` by `suffix`, then multiply `suffix` by `nums[i]`.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [1] * n

        # Forward pass: store product of elements to the left of i
        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]

        # Backward pass: multiply by product of elements to the right of i
        suffix = 1
        for i in range(n - 1, -1, -1):
            res[i] *= suffix
            suffix *= nums[i]

        return res
```

</details>

## Complexity

| Approach | Time | Auxiliary Space | Notes |
| :--- | :--- | :--- | :--- |
| Brute force (nested loops) | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Hits TLE for $n = 10^5$. |
| Total product with `/` | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Disallowed by prompt and breaks on zeros. |
| Separate `prefix` and `suffix` lists | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Good starting point, allocates two extra arrays. |
| Two passes inside `res` | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Optimal (output array excluded from extra space). |
