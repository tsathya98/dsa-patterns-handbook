# Binary Search Cheat Sheet

Every check cuts the remaining search space in half, turning an $\mathcal{O}(n)$ scan into $\mathcal{O}(\log n)$ time (at most ~20 steps for $1,000,000$ items).

## 1. When you can use it
Binary search works whenever your search space has a **two-sided split** where one check at `mid` tells you which half to throw away:
1. **Sorted arrays** (exact match, first/last occurrence, floor/ceil).
2. **Partially ordered or structural arrays** (rotated sorted arrays, adjacent slope comparisons for peaks/valleys, even/odd index parity).
3. **Binary search on the answer** (any min/max question where feasibility flips monotonically from `False` to `True`).

### Decision rules:
* **1. Sorted target lookup or boundaries:** Use standard `lo <= hi`. For exact matches, return on equality. For first or last occurrences, cache `ans = mid` and steer `hi = mid - 1` (to find earlier hits) or `lo = mid + 1` (to find later hits).
* **2. Rotated sorted arrays:** Evaluate `nums[lo] <= nums[mid]`. At least one half is always strictly sorted. Check whether the target falls within that sorted half to pick which side to discard.
* **3. Unsorted peak or local extrema:** Compare `nums[mid]` against `nums[mid + 1]`. Step toward the rising slope to guarantee hitting a local maximum.
* **4. Monotonic optimization (Search on Answer):** When finding the minimum feasible capacity or speed, binary search the value space `[lo, hi]` using a greedy helper predicate `can_finish(mid)` in $\mathcal{O}(\log(\text{range}) \times \text{cost})$.


---

## 2. The 7 Binary Search Archetypes

| # | Archetype | Trigger / Setup | How `mid` steers `[lo, hi]` | Guide & Problems |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Exact Lookup** | Standard sorted array | `nums[mid] < target` $\to$ `lo = mid + 1` | [01. Fundamentals](../dsa/05_binary_search/01_binary_search_fundamentals_and_occurrences.md) (LC 704) |
| 2 | **First / Last Boundary** | Sorted array with duplicates | Record `ans = mid`, then push `hi = mid - 1` (first) or `lo = mid + 1` (last) | [01. Occurrences](../dsa/05_binary_search/01_binary_search_fundamentals_and_occurrences.md) (LC 34) |
| 3 | **Slope / Peak / Valley** | Unsorted array, distinct neighbors | Walk toward the rising slope (peak) or falling slope (local min) | [02. Local Minima & Peaks](../dsa/05_binary_search/02_local_minima_and_peak_finding.md) (LC 162) |
| 4 | **Index Parity** | Sorted pairs `[a,a,b,c,c]` with 1 unique | Before single element, pairs start at **even** indices; after it, at **odd** indices | [03. Index Parity](../dsa/05_binary_search/03_index_parity_single_element_in_duplicates.md) (LC 540) |
| 5 | **Rotated Array** | Sorted array rotated at unknown pivot | At least one half (`lo..mid` or `mid..hi`) is always strictly sorted; check if `target` lies inside it | [04. Rotated Search](../dsa/05_binary_search/04_search_in_rotated_sorted_array.md) (LC 33, 153) |
| 6 | **Exponential Search** | Infinite or unknown-length sorted stream | Double `hi` (`1, 2, 4, 8...`) until `arr[hi] >= target`, then binary search `[lo, hi]` | [05. Infinite Arrays](../dsa/05_binary_search/05_exponential_search_infinite_arrays.md) (LC 702) |
| 7 | **Search on Answer** | "Minimize the maximum" or "min speed/capacity" | Test `can_finish(mid)`. If `True`, record `ans = mid` and search for a better value | [06. Search on Answer](../dsa/05_binary_search/06_binary_search_on_answer_greedy_predicates.md) (LC 875, 410) |

---

## 3. Core Templates

### Template A: Standard / Boundary Lookup
Using `while lo <= hi` with `lo = mid + 1` and `hi = mid - 1` prevents infinite loops when `lo` and `hi` are adjacent.

```python
def search_boundary(nums: list[int], target: int, find_first: bool) -> int:
    lo, hi = 0, len(nums) - 1
    ans = -1

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            ans = mid
            if find_first:
                hi = mid - 1  # Keep hunting left
            else:
                lo = mid + 1  # Keep hunting right
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return ans
```

### Template B: Binary Search on the Answer (Monotonic Predicate)
Use when answers look like `[No, No, No, Yes, Yes, Yes]` and you want the first `Yes` (or last `Yes`).

```python
def minEatingSpeed(piles: list[int], h: int) -> int:
    lo, hi = 1, max(piles)
    ans = hi

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if can_finish(piles, mid, h):
            ans = mid
            hi = mid - 1  # Valid speed; try slower
        else:
            lo = mid + 1  # Too slow; must go faster

    return ans
```

---

## 4. Traps to Watch For
1. **Infinite loops on 2 elements:** Because `mid = (lo + hi) // 2` rounds down to `lo` when `hi == lo + 1`, writing `lo = mid` will loop forever. Always advance past `mid` (`lo = mid + 1`, `hi = mid - 1`) and save candidate answers in `ans`.
2. **Rotated array duplicate boundary:** In `nums[lo] <= nums[mid]`, the `<=` is mandatory because `mid` can equal `lo` on a 2-element range.
3. **Overflow in static languages:** `lo + (hi - lo) // 2` avoids 32-bit integer overflow in C++/Java.
