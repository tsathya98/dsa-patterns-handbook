# Two Sum: Return All Unique Pairs

> **Course reference:** CodeKerdos Homework | **Difficulty:** Easy-Medium | **Pattern:** Hash Set + Canonical Pair Deduplication

## The problem

Given an integer array `arr` and a target `k`, return all **unique pairs of values** `(a, b)` such that `a + b == k`.

* A pair must not be repeated in reverse order: if `(1, 5)` is included, `(5, 1)` must not be included.
* Duplicate pairs must be avoided even if values appear multiple times in `arr`.
* **Expected complexity:** $\mathcal{O}(N)$ time using $\mathcal{O}(N)$ extra space.

```text
Input:  arr = [1, 5, 7, -1, 5],  k = 6
Output: [(1, 5), (-1, 7)]
```

---

## Why naive hash-map Two Sum fails here

In standard LeetCode 1 (Two Sum), you stop as soon as you find the first pair. Here, you have to scan the entire array, and duplicates create two traps:
1. **Duplicate elements:** The second `5` in `[1, 5, 7, -1, 5]` sees `1` in `seen` again and tries to emit `(1, 5)` a second time.
2. **Reverse-order pairs:** Depending on order, you might record `(1, 5)` and later `(5, 1)`.

---

## The core trick: Canonical tuple `(min, max)` in a `pairs` set

Always store a matched pair in **canonical sorted order**:
```python
pair = (min(x, target_comp), max(x, target_comp))
```
Because `(min(1, 5), max(1, 5))` and `(min(5, 1), max(5, 1))` both evaluate to `(1, 5)`, storing `pair` in a `pairs` set (or checking `if pair not in pairs_set`) automatically kills both reverse-order duplicates and repeated-value duplicates in $\mathcal{O}(1)$ time.

### Algorithm steps:
* **1. Initialize sets:** Create `seen = set()` to track numbers visited so far, and `pairs = set()` (or a `result` list backed by a set) to store unique canonical pairs.
* **2. Check complement:** For each `x` in `arr`, compute `comp = k - x`.
* **3. Record canonical pair:** If `comp in seen`, form `pair = (min(x, comp), max(x, comp))`. If `pair` is not in `pairs`, add it.
* **4. Mark current value visited:** Add `x` to `seen` and move to the next element.

---

## Step-by-step trace (`arr = [1, 5, 7, -1, 5]`, `k = 6`)

**Initial state:**
```text
seen  = {}
pairs = []
```

**Iteration 1 (`i = 0`, `x = 1`):**
`comp = 6 - 1 = 5`. Is `5` in `seen`? No. Add `1` to `seen`.
```text
arr:   [ 1,   5,   7,  -1,   5 ]
         ^
seen  = {1}
pairs = []
```

**Iteration 2 (`i = 1`, `x = 5`):**
`comp = 6 - 5 = 1`. Is `1` in `seen`? **Yes!**
Form canonical pair `(min(5, 1), max(5, 1)) = (1, 5)`. Add `(1, 5)` to `pairs`, and add `5` to `seen`.
```text
arr:   [ 1,   5,   7,  -1,   5 ]
              ^
seen  = {1, 5}
pairs = [(1, 5)]
```

**Iteration 3 (`i = 2`, `x = 7`):**
`comp = 6 - 7 = -1`. Is `-1` in `seen`? No. Add `7` to `seen`.
```text
arr:   [ 1,   5,   7,  -1,   5 ]
                   ^
seen  = {1, 5, 7}
pairs = [(1, 5)]
```

**Iteration 4 (`i = 3`, `x = -1`):**
`comp = 6 - (-1) = 7`. Is `7` in `seen`? **Yes!**
Form canonical pair `(min(-1, 7), max(-1, 7)) = (-1, 7)`. Add `(-1, 7)` to `pairs`, and add `-1` to `seen`.
```text
arr:   [ 1,   5,   7,  -1,   5 ]
                        ^
seen  = {1, 5, 7, -1}
pairs = [(1, 5), (-1, 7)]
```

**Iteration 5 (`i = 4`, `x = 5`):**
`comp = 6 - 5 = 1`. Is `1` in `seen`? **Yes!**
Form canonical pair `(min(5, 1), max(5, 1)) = (1, 5)`.
Is `(1, 5)` already in `pairs_set`? **Yes, skip!**
```text
arr:   [ 1,   5,   7,  -1,   5 ]
                             ^
seen  = {1, 5, 7, -1}
pairs = [(1, 5), (-1, 7)]   <- Duplicate (1, 5) ignored!
```

---

## Traps to watch for

* **Checking `x == comp` (half-target trap):** If `k = 6` and `arr = [3, 4]`, you must check `comp in seen` **before** adding `x` to `seen`. Otherwise a single `3` will pair with itself to form `(3, 3)`. If `arr = [3, 3]`, the first `3` goes into `seen`, and the second `3` legitimately finds `3 in seen` and forms `(3, 3)`.
* **Why `(min, max)` matters:** Without `(min(x, comp), max(x, comp))`, an input like `arr = [1, 5, 1]`, `k = 6` would see `1` at index 0, form `(1, 5)` at index 1, and then at index 2 (`x = 1`, `comp = 5`) form `(5, 1)` if you didn't normalize tuple order.

<details>
<summary>Spoiler: Solution Code</summary>

```python
def two_sum_unique_pairs(arr: list[int], k: int) -> list[tuple[int, int]]:
    seen: set[int] = set()
    used_pairs: set[tuple[int, int]] = set()
    result: list[tuple[int, int]] = []

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

## Complexity

* **Time:** $\mathcal{O}(N)$ single pass over `arr` with $\mathcal{O}(1)$ average hash set lookups.
* **Space:** $\mathcal{O}(N)$ to store `seen` and `used_pairs`.
