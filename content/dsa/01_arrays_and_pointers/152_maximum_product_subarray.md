# LeetCode 152: Maximum Product Subarray

> **Difficulty:** Medium | **Pattern:** Dual-State Kadane (`cur_max`, `cur_min`) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/maximum-product-subarray/](https://leetcode.com/problems/maximum-product-subarray/)

## The problem

Given an integer array `nums`, find a contiguous non-empty subarray that has the largest product, and return the product.

```text
Input:  nums = [2, 3, -2, 4]    -> Output: 6  (subarray [2, 3])
Input:  nums = [-2, 3, -4]      -> Output: 24 (subarray [-2, 3, -4])
```

---

## Why standard Kadane's algorithm fails

In Maximum Sum Subarray (LC 53), a negative running sum is always dead weight and gets discarded.
In **multiplication**, a huge negative product like `-12` is one negative number away from becoming `+48`!
* Multiplying by a **negative** number flips your **maximum** into your **minimum**, and your **minimum** into your **maximum**.
* Multiplying by **`0`** resets both the running max and running min to `0`.

---

## The core trick: Track both `cur_max` and `cur_min`

At each number `x`:
1. If `x < 0`, **swap `cur_max` and `cur_min`** because multiplying by a negative reverses signs.
2. Update:
   * `cur_max = max(x, cur_max * x)`
   * `cur_min = min(x, cur_min * x)`
3. Update `ans = max(ans, cur_max)`.

---

## Step-by-step trace (`nums = [-2, 3, -4]`)

**Initialization (`i = 0`, `x = -2`):**
```text
cur_max = -2
cur_min = -2
ans     = -2
```

**Iteration 1 (`i = 1`, `x = 3`):**
`x > 0` (no swap).
```text
cur_max = max(3, -2 * 3) = 3
cur_min = min(3, -2 * 3) = -6   <- remembers [-2, 3] = -6!
ans     = max(-2, 3)     = 3
```

**Iteration 2 (`i = 2`, `x = -4`):**
`x < 0` -> **Swap `cur_max` and `cur_min` first!** (`cur_max = -6, cur_min = 3`).
Now multiply by `-4`:
```text
cur_max = max(-4, -6 * -4) = 24  <- (-6) * (-4) = +24!
cur_min = min(-4,  3 * -4) = -12
ans     = max(3, 24)       = 24
```

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        ans = cur_max = cur_min = nums[0]

        for x in nums[1:]:
            if x < 0:
                cur_max, cur_min = cur_min, cur_max

            cur_max = max(x, cur_max * x)
            cur_min = min(x, cur_min * x)
            ans = max(ans, cur_max)

        return ans
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(N)$ single pass.
* **Space:** $\mathcal{O}(1)$ auxiliary space.
