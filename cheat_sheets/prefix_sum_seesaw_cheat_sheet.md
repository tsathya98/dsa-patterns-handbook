# Prefix Sum & Seesaw Balance Cheat Sheet

> Guides: [Prefix Sums & Special Index Queries](../01_arrays_and_pointers/00_prefix_sums_and_special_index_queries.md) | [LC 724: Find Pivot Index](../01_arrays_and_pointers/724_find_pivot_index.md)

## 1. Range Sum Queries in $\mathcal{O}(1)$
Build a prefix array where `pref[i]` stores the sum of `nums[0..i]`. Any range sum `sum(L, R)` is then a single subtraction:
$$\text{sum}(L, R) = \begin{cases} \text{pref}[R] & \text{if } L = 0 \\ \text{pref}[R] - \text{pref}[L - 1] & \text{if } L > 0 \end{cases}$$

---

## 2. The Seesaw Balance Pattern ($\mathcal{O}(1)$ Space Pivot Search)
When comparing the sum to the left of index `i` with the sum to the right of `i`, you don't even need a prefix array. Because the total sum of the array is fixed:
$$\text{left\_sum} + \text{nums}[i] + \text{right\_sum} = \text{total\_sum}$$
$$\implies \text{right\_sum} = \text{total\_sum} - \text{left\_sum} - \text{nums}[i]$$

```text
          total_sum = 28
[  1,   7,   3  |  6  |  5,   6  ]
   └─── 11 ───┘  pivot   └─ 11 ─┘
     left_sum    nums[i]  total - left_sum - nums[i]
```

### Algorithm steps:
* **1. Total sum initialization:** Calculate `total = sum(nums)` in an initial pass and initialize running accumulator `left_sum = 0`.
* **2. Pivot equality test:** At each index `i`, derive `right_sum = total - left_sum - num` and check whether `left_sum == right_sum`. If they match, return `i` immediately.
* **3. Invariant maintenance:** Add `num` to `left_sum` only after performing the pivot comparison, guaranteeing $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ extra space.


### Template ([LC 724: Find Pivot Index](../01_arrays_and_pointers/724_find_pivot_index.md))
```python
def pivotIndex(nums: list[int]) -> int:
    total = sum(nums)
    left_sum = 0

    for i, num in enumerate(nums):
        if left_sum == total - left_sum - num:
            return i
        left_sum += num

    return -1
```
*(Trap: Always check `left_sum == right_sum` **before** adding `num` to `left_sum`, because the pivot element `nums[i]` belongs to neither side.)*

---

## 3. Even/Odd Parity Shift on Deletion (LC 1664: Fair Array)
When you delete index `i` from an array:
- Elements **before** `i` (`0 .. i-1`) keep their original indices and even/odd parity.
- Elements **after** `i` (`i+1 .. n-1`) shift left by 1, flipping their parity (old even indices become odd; old odd indices become even).

$$\text{new\_even\_sum} = \text{even\_left}[0..i-1] + \text{odd\_right}[i+1..n-1]$$
$$\text{new\_odd\_sum} = \text{odd\_left}[0..i-1] + \text{even\_right}[i+1..n-1]$$

---

## 4. Related Problems

| Problem | Formula / Trick |
| :--- | :--- |
| [LC 724: Find Pivot Index](../01_arrays_and_pointers/724_find_pivot_index.md) | `left_sum == total - left_sum - num` |
| LC 2270: Ways to Split Array | Split between `i` and `i+1`: `left_sum >= total - left_sum` |
| [LC 238: Product Except Self](../01_arrays_and_pointers/238_product_of_array_except_self.md) | Multiplicative prefix pass followed by suffix pass |
| LC 1664: Ways to Make a Fair Array | `even_L + odd_R == odd_L + even_R` |
| LC 560: Subarray Sum Equals K | Hash map counting occurrences of `cur_prefix - k` |
