# ⚖️ Prefix Sum (The Seesaw Balance Pattern) Master Cheat Sheet

> **Pattern:** Prefix Sum & Total Conservation (The Seesaw Balance Pattern)  
> **Target Audience:** Complete Beginner / 1st-Year CS Student  
> **The Big Idea:** In an array of fixed elements, the sum is **conserved**. If you know the Total Sum and your Left Sum, the Right Sum is instantly free: $\text{Right} = \text{Total} - \text{Left} - \text{Current}$.  
> **Core Analogy:** A playground seesaw with a pivot in the middle.

---

## 💡 1. What Problem Does It Solve?

In problems asking you to compare the **left side vs. the right side** of an array (e.g., finding a balance point, split point, or pivot):

* **The Brute Force Trap ($\mathcal{O}(n^2)$):**  
  At every index $i$, re-slicing and re-summing `sum(nums[:i])` and `sum(nums[i+1:])` wastes $2.5 \times 10^9$ operations on large arrays.
* **The Seesaw Solution ($\mathcal{O}(n)$ Time, $\mathcal{O}(1)$ Space):**  
  Compute the `total_sum = sum(nums)` **once upfront**. As you walk forward, accumulate `left_sum`. The right side is derived with zero slicing!

---

## 🎯 2. The 3-Second Mental Checklist (How to Spot It)

Ask yourself these **3 trigger questions**:

```text
1. Am I looking for a "split point", "pivot index", or comparing "elements before" vs "elements after"?
                                  +
2. Does the comparison involve SUMS, COUNTS, or CUMULATIVE properties?
                                  +
3. Is the whole array fixed/static (known total)?
                                  │
                                  ▼
             ⚖️ THE SEESAW PREFIX BALANCE PATTERN! ⚖️
```

---

## ⚖️ 3. The Core Intuition: The Playground Seesaw Analogy

Imagine a seesaw with weights placed across it:

```text
              TOTAL SUM = 28
 ┌───────────────────────────────────────┐
 │   1       7       3   │ 6 │   5     6 │
 └───────────────────────┴───┴───────────┘
         ▲                 ▲       ▲
     LEFT SIDE           PIVOT   RIGHT SIDE
 (running accumulator)   num[i]   (Total - Left - num[i])
```

### The Conservation Law:
$$\mathbf{\text{Left Sum} + \text{Pivot Element} + \text{Right Sum} = \text{Total Sum}}$$

Rearranging for the Right side:
$$\mathbf{\text{Right Sum} = \text{Total Sum} - \text{Left Sum} - \text{Pivot Element}}$$

* **You do NOT need two arrays (`lsum` and `rsum`).**
* **You do NOT need list slicing (`nums[:i]` or `nums[i+1:]`).**
* You only need **one scalar integer variable**: `left_sum = 0`!

---

## ⚙️ 4. Universal Code Template

```python
def find_balance_point(nums: list[int]) -> int:
    total = sum(nums)      # Pass 1: O(n) upfront total
    left_sum = 0
    
    for i, num in enumerate(nums):  # Pass 2: O(n) walk
        # Seesaw balance test:
        # Does Left Side == Right Side?
        if left_sum == total - left_sum - num:
            return i
            
        # Add current number to left side as we walk forward
        left_sum += num
        
    return -1
```

---

## 🧩 5. Where Else Does This Pattern Appear?

| LeetCode # | Problem Name | Seesaw Condition |
| :--- | :--- | :--- |
| **LC 724** | **Find Pivot Index** | `left_sum == total - left_sum - num` |
| **LC 1991**| **Find Middle Index in Array** | Identical problem (alias of LC 724). |
| **LC 2270**| **Number of Ways to Split Array** | Split between $i$ and $i+1$: `left_sum >= total - left_sum`. |
| **LC 238** | **Product of Array Except Self** | Multiplicative version: $\text{Prefix Product} \times \text{Suffix Product}$. |
| **LC 1664**| **Ways to Make a Fair Array** | Deleting index $i$ flips parity of subsequent elements: `even_L + odd_R == odd_L + even_R`. |
| **LC 2017**| **Grid Game** | Top row right sum vs. bottom row left sum across two parallel seesaws. |

### ⚡ The Deletion Parity Shift Rule (LC 1664)
When removing index $i$:
* Elements before $i$ keep their original parity.
* Elements after $i$ shift left by 1, swapping their parity (even becomes odd, odd becomes even):
$$\text{new\_even} = \text{even\_sum}[0 \dots i-1] + \text{odd\_sum}[i+1 \dots N-1]$$
$$\text{new\_odd} = \text{odd\_sum}[0 \dots i-1] + \text{even\_sum}[i+1 \dots N-1]$$

---

## ❓ 6. How is This Different from Sliding Window or Kadane?

| Pattern | Mental Model | Window / Range | When to Pick |
| :--- | :--- | :--- | :--- |
| **Seesaw Prefix** | **Balance Scale** | Left of $i$ vs. Right of $i$ (splits entire array) | Splitting array into two sides, pivots, equilibrium points. |
| **Sliding Window** | **Rubber Band** | Subarray of size $K$ or dynamic $[L, R]$ | Finding longest/shortest/max *contiguous slice*. |
| **Kadane's Algorithm** | **Toxic Debt** | Subarray ending at index $i$ | Finding max sum subarray with *negative penalties*. |

---

## ⚠️ 7. Student Traps to Avoid in Interviews

1. **Order of updating `left_sum`:**  
   Always check the balance condition **BEFORE** adding `num` to `left_sum`! (The pivot element itself is strictly excluded from both sides).
2. **First / Last index edge cases:**  
   * For index `0`: `left_sum` starts at `0`. Right sum is `total - num`.
   * For the last index: `left_sum` is `total - last_num`. Right sum is `0`.  
   The formula naturally handles both boundaries without any `if i == 0` special cases!
