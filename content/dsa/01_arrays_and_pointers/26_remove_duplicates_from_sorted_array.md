# LeetCode 26: Remove Duplicates from Sorted Array

> **Difficulty:** Easy | **Pattern:** Two Pointers (Scout and Writer)  
> **Constraints:** $\mathcal{O}(n)$ time, $\mathcal{O}(1)$ auxiliary space in-place.

## The problem

Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in-place so each unique element appears only once. Return `k`, the number of unique elements, with the first `k` slots of `nums` holding those unique values in sorted order.

## Why `Counter` fails the interview constraint

```python
counter = Counter(nums)
for k, key in enumerate(counter):
    nums[k] = key
return len(counter)
```

Python 3.7+ dictionaries preserve insertion order, so this passes the online judge, but an interviewer will push back for two reasons:
1. **Breaks $\mathcal{O}(1)$ space:** `Counter(nums)` allocates a hash table holding up to $n$ entries ($\mathcal{O}(n)$ space).
2. **Ignores that `nums` is sorted:** You only need a hash table when the array is unsorted and duplicates are scattered everywhere. In a sorted array, identical numbers sit right next to each other.

## The core trick: Scout and Writer

Use the same two-pointer setup as [LC 27: Remove Element](27_remove_element.md):
- `nums[0]` is always the first unique number, so leave it alone.
- **Writer (`k`):** Starts at index `1`, marking where the next unique number goes.
- **Scout (`i`):** Scans from index `1` to the end. Whenever `nums[i] != nums[i - 1]`, it found a new unique value, so write `nums[k] = nums[i]` and advance `k`.

```text
In LC 27 (Remove Element):     keep if nums[i] != val
In LC 26 (Remove Duplicates):  keep if nums[i] != nums[i - 1]
```

### Algorithm steps:
* **1. Base case and initialization:** If `nums` is empty, return `0`. Otherwise, first element is already unique; set writer pointer `k = 1`.
* **2. Scout through array:** Loop `i` from index `1` to `len(nums) - 1`.
* **3. Write unique elements:**
  * If `nums[i] != nums[i - 1]`, a new unique element is found: write `nums[k] = nums[i]` and advance `k += 1`.
  * Otherwise, ignore duplicate element and leave `k` in place.
* **4. Return:** `k` representing the count of unique elements.

## Step-by-step trace

Tracing `nums = [0, 0, 1, 1, 1, 2, 2, 3]`:

```text
Start: k = 1, i = 1 (nums[0] = 0 is already in place)
[ 0 , 0 , 1 , 1 , 1 , 2 , 2 , 3 ]
      ^
     k,i
```

| `i` | `nums[i]` vs `nums[i-1]` | Action | Array prefix (`0..k-1`) | `k` after |
| :--- | :--- | :--- | :--- | :--- |
| `1` | `0 == 0` (duplicate) | Skip | `[0]` | `1` |
| `2` | `1 != 0` (new unique) | `nums[1] = 1` | `[0, 1]` | `2` |
| `3..4` | `1 == 1` (duplicate) | Skip | `[0, 1]` | `2` |
| `5` | `2 != 1` (new unique) | `nums[2] = 2` | `[0, 1, 2]` | `3` |
| `6` | `2 == 2` (duplicate) | Skip | `[0, 1, 2]` | `3` |
| `7` | `3 != 2` (new unique) | `nums[3] = 3` | `[0, 1, 2, 3]` | `4` |

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        if not nums:
            return 0

        k = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                nums[k] = nums[i]
                k += 1

        return k
```

</details>

## Complexity

| Approach | Time | Auxiliary Space | Notes |
| :--- | :--- | :--- | :--- |
| `Counter` / Hash Set | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Required for unsorted arrays, wastes memory on sorted input. |
| Two Pointers (`i` and `k`) | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Uses adjacent neighbor checks (`nums[i] != nums[i - 1]`). |
