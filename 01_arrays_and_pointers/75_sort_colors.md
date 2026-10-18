# LeetCode 75: Sort Colors

> **Difficulty:** Medium | **Pattern:** Three Pointers / Dutch National Flag  
> **Source Code:** [`75_sort_colors.py`](./75_sort_colors.py)

## The problem

Given an array `nums` with $n$ objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order 0 (red), 1 (white), and 2 (blue). You must solve it in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ extra space without using the library sort.

## Why the naive way fails

Using a two-pass counting sort (counting occurrences of 0, 1, 2, then overwriting `nums`) works in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space, but requires two passes over the array. Interviewers specifically ask for a single-pass $\mathcal{O}(n)$ in-place partition.

## The core trick

Use Dijkstra's **Dutch National Flag** algorithm with three pointers:
- `low`: Next placement index for `0`. Everything before `low` is guaranteed to be `0`.
- `mid`: Current element being inspected. Everything between `low` and `mid - 1` is `1`.
- `high`: Next placement index for `2`. Everything after `high` is guaranteed to be `2`.

```text
[ 0, 0 ... | 1, 1 ... | ? ? ? | ... 2, 2 ]
           ^          ^       ^
          low        mid     high
```

### Algorithm steps (Dutch National Flag):
* **1. Initialize three pointers:** `low = 0` (boundary for 0s), `mid = 0` (current scanner), and `high = n - 1` (boundary for 2s).
* **2. Scan while mid <= high:**
  * `nums[mid] == 0`: Swap with `nums[low]`, then advance both `low += 1` and `mid += 1`.
  * `nums[mid] == 1`: Already in correct middle section; simply advance `mid += 1`.
  * `nums[mid] == 2`: Swap with `nums[high]`, then decrement `high -= 1` (do NOT advance `mid`, since the swapped element from `high` must still be inspected).
* **3. Termination:** Invariant ensures `[0...low-1]` is 0s, `[low...mid-1]` is 1s, and `[high+1...n-1]` is 2s in a single $\mathcal{O}(n)$ pass.

## Step-by-step trace

Input: `nums = [2, 0, 2, 1, 1, 0]`

| Step | `low` | `mid` | `high` | Array state | Action taken |
|---|---|---|---|---|---|
| 1 | 0 | 0 | 5 | `[2, 0, 2, 1, 1, 0]` | `nums[0] == 2` $\implies$ swap with `high` (idx 5), `high = 4` |
| 2 | 0 | 0 | 4 | `[0, 0, 2, 1, 1, 2]` | `nums[0] == 0` $\implies$ swap with `low` (idx 0), `low = 1, mid = 1` |
| 3 | 1 | 1 | 4 | `[0, 0, 2, 1, 1, 2]` | `nums[1] == 0` $\implies$ swap with `low` (idx 1), `low = 2, mid = 2` |
| 4 | 2 | 2 | 4 | `[0, 0, 2, 1, 1, 2]` | `nums[2] == 2` $\implies$ swap with `high` (idx 4), `high = 3` |
| 5 | 2 | 2 | 3 | `[0, 0, 1, 1, 2, 2]` | `nums[2] == 1` $\implies$ advance `mid = 3` |
| 6 | 2 | 3 | 3 | `[0, 0, 1, 1, 2, 2]` | `nums[3] == 1` $\implies$ advance `mid = 4` |
| 7 | 2 | 4 | 3 | `[0, 0, 1, 1, 2, 2]` | `mid > high` $\implies$ Loop terminates |

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def sortColors(self, nums: list[int]) -> None:
        low, mid, high = 0, 0, len(nums) - 1

        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:
                nums[high], nums[mid] = nums[mid], nums[high]
                high -= 1
```

</details>

## Traps to watch for

- **Incrementing `mid` (or `i`) after swapping with `high` (or `r`):** This is the #1 bug in this problem.
  * When you swap with `low`, the incoming number came from already-inspected territory (it was guaranteed to be a `1`), so advancing `mid += 1` is safe.
  * When you swap with `high`, the incoming number comes from uninspected territory (`?`). It could be a `0`, `1`, or another `2`!
  * **Failure example:** On `nums = [1, 2, 0]`, at `i = 1`, `nums[1] == 2` swaps with `nums[2] == 0`, producing `[1, 0, 2]`. If you increment `i` to 2, the loop terminates (`i <= r` fails) and the incoming `0` at index 1 is never placed into the `0` zone!
  * **Rule:** Only decrement `high -= 1`. Leave `mid` at the same index so the next iteration examines the newly arrived element.

## Complexity

- **Time Complexity:** $\mathcal{O}(n)$ single pass.
- **Space Complexity:** $\mathcal{O}(1)$ in-place mutations.
