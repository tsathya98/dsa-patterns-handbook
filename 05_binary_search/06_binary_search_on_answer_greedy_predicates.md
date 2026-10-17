# 🎯 Binary Search on the Answer (Greedy Predicates)

> **Course Reference:** CodeKerdos DSA — Class 9 & 10  
> **Core Concept:** Optimization problems where direct search is exponential, but verifying feasibility is $\mathcal{O}(N)$ (Aggressive Cows, Painter's Partition, Allocate Books, LC 875, LC 410).

---

## 1. What is "Binary Search on the Answer"?

Instead of searching for an index inside a given array, **the search space IS the answer range $[lo, hi]$**.

### How to Identify It in 3 Seconds:
1. The problem asks for **"Minimum of a Maximum"** (e.g. minimize the maximum work assigned to any painter) or **"Maximum of a Minimum"** (e.g. maximize the minimum distance between cows).
2. The candidate answer space is **monotonic**:
   ```text
   Capacity:    1     2     3     4     5     6     7
   Feasible?  [ No ,  No ,  No ,  YES,  YES,  YES,  YES ]
                                   ▲
                          Turning point = 4!
   ```
3. If a capacity of $4$ works, any capacity $> 4$ is also guaranteed to work.
4. If a capacity of $3$ fails, any capacity $< 3$ is also guaranteed to fail.

---

## 2. The 3-Step Universal Template

1. **Define Search Boundaries $[lo, hi]$:**
   * `lo = max(arr)` (A single worker must at least be able to do the single largest job).
   * `hi = sum(arr)` (One worker does every job).
2. **Write the $\mathcal{O}(N)$ Greedy Validator `is_feasible(capacity)`:**
   * Simulate assigning elements sequentially. When current sum exceeds `capacity`, increment worker count.
3. **Execute Binary Search:**
   * If `is_feasible(mid)` is `True`: this capacity works! Record `ans = mid` and search left (`hi = mid - 1`) to see if we can do it with even less capacity.
   * If `False`: capacity is too small; search right (`lo = mid + 1`).

---

## 3. Classic Master Problem: Painter's Partition / Split Array Largest Sum (LC 410)

Given $N$ boards of length `arr[i]` and $K$ painters, find the minimum time to paint all boards if each painter can only paint contiguous boards.

```python
def splitArray(nums: list[int], k: int) -> int:
    def is_feasible(max_capacity: int) -> bool:
        chunks = 1
        current_sum = 0
        for num in nums:
            if current_sum + num > max_capacity:
                chunks += 1
                current_sum = num
            else:
                current_sum += num
        return chunks <= k

    lo = max(nums)
    hi = sum(nums)
    ans = hi

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if is_feasible(mid):
            ans = mid
            hi = mid - 1  # Try a smaller maximum workload
        else:
            lo = mid + 1  # Need more capacity

    return ans
```

---

## 4. The Maximizing Twin: Aggressive Cows (LC 1552: Magnetic Force Between Two Balls)

> **Goal:** Place $C$ cows in $N$ stalls such that the **minimum distance between any two cows is as large as possible**.

* Monotonic space: If distance $D$ is possible, distances $< D$ are also possible.
* Search space: `lo = 1`, `hi = stalls[-1] - stalls[0]`.

```python
def maxDistance(stalls: list[int], cows: int) -> int:
    stalls.sort()

    def can_place(min_dist: int) -> bool:
        placed = 1
        last_pos = stalls[0]
        for i in range(1, len(stalls)):
            if stalls[i] - last_pos >= min_dist:
                placed += 1
                last_pos = stalls[i]
        return placed >= cows

    lo = 1
    hi = stalls[-1] - stalls[0]
    best_dist = 0

    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if can_place(mid):
            best_dist = mid
            lo = mid + 1  # Try to push for a larger minimum distance!
        else:
            hi = mid - 1

    return best_dist
```

* **Time Complexity:** $\mathcal{O}(N \log(\text{sum} - \max))$ for partitioning, $\mathcal{O}(N \log N + N \log(\text{range}))$ for Aggressive Cows.
* **Auxiliary Space:** $\mathcal{O}(1)$.
