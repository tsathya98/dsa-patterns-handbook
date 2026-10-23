# Two Sum: Return All Unique Pairs

> **Course reference:** CodeKerdos Homework | **Difficulty:** Medium  
> **Source Code:** [`01_two_sum_all_unique_pairs.py`](01_two_sum_all_unique_pairs.py) | **Pattern:** Canonical Tuple Deduplication

## The problem

Given an integer array `arr` and a target `k`, return all unique pairs of values `(a, b)` such that `a + b == k`.
- Avoid reverse duplicates: if `(1, 5)` is included, `(5, 1)` must not be included.
- Avoid duplicate value pairs even if values repeat in `arr`.
- Expected complexity: $\mathcal{O}(N)$ time using $\mathcal{O}(N)$ extra space.

```text
Input:  arr = [1, 5, 7, -1, 5],  k = 6
Output: [(1, 5), (-1, 7)]
```

---

## Approach 1: Brute force (nested loops)

Examine every pair `(arr[i], arr[j])` for all $i < j$. If the sum equals `k`, insert the normalized pair `(min(arr[i], arr[j]), max(arr[i], arr[j]))` into a set.
* **Time:** $\mathcal{O}(N^2)$ nested iterations.
* **Space:** $\mathcal{O}(U)$ to store unique pairs. Hits TLE when $N \ge 10^5$.

---

## Approach 2: Semi-optimized (sort + two-pointer squeeze)

Sort the array in $\mathcal{O}(N \log N)$ time, then squeeze from both ends with `left` and `right`:
* If `arr[left] + arr[right] == k`: record `(arr[left], arr[right])`, increment `left`, decrement `right`, and skip adjacent duplicates with while loops.
* If sum is smaller, advance `left`. If larger, decrement `right`.
* **Time:** $\mathcal{O}(N \log N)$ dominated by sorting.
* **Auxiliary space:** $\mathcal{O}(1)$ beyond the sort.

---

## Approach 3: Optimized (hash set with canonical tuples)

Scan `arr` in a single pass. For each element `x`:
1. Check if complement `comp = k - x` is in `seen`.
2. If yes, form canonical tuple `pair = (min(x, comp), max(x, comp))`.
3. If `pair` has not been emitted yet, record it.
4. Add `x` to `seen`.

```text
Canonical Tuple Normalization:
(min(1, 5), max(1, 5))  ==>  (1, 5)
(min(5, 1), max(5, 1))  ==>  (1, 5)   <- Automatic duplicate prevention
```

### Algorithm steps:
* **1. Initialize sets:** `seen = set()`, `used_pairs = set()`, `result = []`.
* **2. Compute complement:** For each `x` in `arr`, set `comp = k - x`.
* **3. Match and record:** If `comp in seen`:
  * Form `pair = (min(x, comp), max(x, comp))`.
  * If `pair not in used_pairs`: add to `used_pairs` and append to `result`.
* **4. Mark visited:** Add `x` to `seen` after checking the complement (prevents pairing an element with itself unless duplicated in input).

---

<details>
<summary>Spoiler: Solution Code (All 3 Approaches)</summary>

```python
# Approach 1: Brute Force O(N^2)
def two_sum_unique_pairs_brute(arr: list[int], k: int) -> list[tuple[int, int]]:
    unique_pairs = set()
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == k:
                unique_pairs.add((min(arr[i], arr[j]), max(arr[i], arr[j])))
    return list(unique_pairs)


# Approach 2: Sort + Two Pointers O(N log N)
def two_sum_unique_pairs_two_pointers(arr: list[int], k: int) -> list[tuple[int, int]]:
    arr.sort()
    left, right = 0, len(arr) - 1
    result = []
    while left < right:
        curr_sum = arr[left] + arr[right]
        if curr_sum == k:
            result.append((arr[left], arr[right]))
            left += 1
            right -= 1
            while left < right and arr[left] == arr[left - 1]:
                left += 1
            while left < right and arr[right] == arr[right + 1]:
                right -= 1
        elif curr_sum < k:
            left += 1
        else:
            right -= 1
    return result


# Approach 3: Hash Set with Canonical Tuples O(N)
def two_sum_unique_pairs(arr: list[int], k: int) -> list[tuple[int, int]]:
    seen = set()
    used_pairs = set()
    result = []
    for x in arr:
        comp = k - x
        if comp in seen:
            pair = (min(x, comp), max(x, comp))
            if pair not in used_pairs:
                used_pairs.add(pair)
                result.append(pair)
        seen.add(x)
    return result
```

</details>

---

## Complexity comparison

| Approach | Time Complexity | Auxiliary Space | Status |
|---|---|---|---|
| **1. Brute Force** | $\mathcal{O}(N^2)$ | $\mathcal{O}(U)$ | TLE on large arrays |
| **2. Sort + Two Pointers** | $\mathcal{O}(N \log N)$ | $\mathcal{O}(1)$ | Good when extra space is disallowed |
| **3. Hash Set (Canonical)** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | Optimal target for this problem |
