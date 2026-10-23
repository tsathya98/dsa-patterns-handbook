# LeetCode 27: Remove Element

> **Difficulty:** Easy | **Pattern:** Two Pointers (Scout and Writer)  
> **Constraints:** $\mathcal{O}(n)$ time, $\mathcal{O}(1)$ auxiliary space in-place.

## The problem

Given an integer array `nums` and an integer `val`, remove all occurrences of `val` in `nums` in-place. The order of the remaining elements may be changed. Return `k`, the number of elements not equal to `val`, with the first `k` slots of `nums` holding those kept elements.

## The core trick: Scout and Writer

Use two pointers moving left to right:
- **Scout (`i`):** Scans every element in `nums` and checks `nums[i] != val`.
- **Writer (`k`):** Marks the boundary of the clean prefix (`0 .. k - 1`). Whenever `i` finds a value to keep, copy `nums[k] = nums[i]` and advance `k += 1`.

```text
         Writer (k) marks where the next kept element goes
         v
nums = [ 0 , 1 , 2 , 2 , 3 , 0 , 4 , 2 ],  val = 2
                 ^
                 Scout (i) inspects every element

Invariant: [ Kept elements (0 .. k-1) | Ignored / Unexplored (k .. n-1) ]
```

When the loop finishes, `k` equals the count of kept elements.

### Algorithm steps:
* **1. Initialize writer pointer:** Set `k = 0` to track the boundary where valid non-`val` elements will be placed.
* **2. Scout through elements:** Loop `i` from `0` to `len(nums) - 1`.
* **3. Filter elements:**
  * If `nums[i] != val`, keep the element: write `nums[k] = nums[i]` and advance `k += 1`.
  * If `nums[i] == val`, skip the element and leave `k` unchanged.
* **4. Return:** `k`, the number of elements not equal to `val`.

## Step-by-step trace

Tracing `nums = [3, 2, 2, 3]`, `val = 3`:

| Step (`i`) | `nums[i]` | `nums[i] != 3`? | Action | Array state | `k` after |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `3` | False | Skip | `[3, 2, 2, 3]` | `0` |
| `1` | `2` | True | `nums[0] = 2`, `k += 1` | `[2, 2, 2, 3]` | `1` |
| `2` | `2` | True | `nums[1] = 2`, `k += 1` | `[2, 2, 2, 3]` | `2` |
| `3` | `3` | False | Skip | `[2, 2, 2, 3]` | `2` |

## Follow-up: What if `val` is rare?

If `nums` has $100,000$ elements and only one equals `val`, the Scout and Writer loop still executes `nums[k] = nums[i]` $99,999$ times. Since the problem allows changing the relative order, you can instead swap any matching `nums[i] == val` with the last active element `nums[n - 1]` and shrink `n -= 1`. Avoid advancing `i` after a swap so the newly swapped value from the tail gets inspected on the next iteration.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k


# Follow-up optimization when `val` is rare (does not preserve order):
class SolutionSwapTail:
    def removeElement(self, nums: list[int], val: int) -> int:
        i = 0
        n = len(nums)
        while i < n:
            if nums[i] == val:
                nums[i] = nums[n - 1]
                n -= 1
            else:
                i += 1
        return n
```

</details>

## Pattern connection & complexity

The same Scout and Writer loop solves three related problems by changing one condition:
- **LC 27: Remove Element:** `if nums[i] != val:`
- **[LC 26: Remove Duplicates](26_remove_duplicates_from_sorted_array.md):** `if nums[i] != nums[i - 1]:`
- **[LC 283: Move Zeroes](283_move_zeroes.md):** `if nums[i] != 0:` (swap `nums[k]` and `nums[i]`)

| Variant | Time | Space | Preserves Order? | Best When |
| :--- | :--- | :--- | :--- | :--- |
| Scout and Writer | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Yes | Standard default, clean and order-preserving. |
| Swap with Tail | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | No | Target `val` is rare and writes are expensive. |
