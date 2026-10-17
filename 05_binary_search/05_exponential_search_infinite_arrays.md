# ♾️ Exponential Search in Infinite / Unbounded Arrays

> **Course Reference:** CodeKerdos DSA — Class 10  
> **Core Concept:** Solving LeetCode 702 in $\mathcal{O}(\log P)$ time using exponential boundary expansion.

---

## 📌 Problem Statement

Given an **infinite sorted array** (or a data stream where `len(arr)` cannot be called, or out-of-bounds access returns $\infty$), find the index of target $K$.

```text
arr = [ 1 , 3 , 5 , 7 , 9 , 11 , 13 , 15 , 17 , 19 , ... ∞ ]
Constraint: You CANNOT use len(arr) — the size is conceptually infinite.
Target: 13
```

---

## 🧠 The 2-Phase Algorithm: Exponential Doubling + Binary Search

### Why Linear Search Fails:
Scanning element-by-element (`while arr[i] <= k: i += 1`) takes $\mathcal{O}(P)$ time, where $P$ is the position of $K$. If $P = 10^9$, it times out.

### Phase 1: Exponential Doubling ($\mathcal{O}(\log P)$)
Since you cannot set `hi = len(arr) - 1`, **grow your own upper bound exponentially**:
1. Start at `lo = 0, hi = 1`.
2. While `arr[hi] < k`:
   * Leapfrog `lo = hi`.
   * Double `hi = hi * 2`.

```text
Target k = 13:

Step 0: lo = 0, hi = 1   -> arr[1] = 3   < 13 -> Double!
Step 1: lo = 1, hi = 2   -> arr[2] = 5   < 13 -> Double!
Step 2: lo = 2, hi = 4   -> arr[4] = 9   < 13 -> Double!
Step 3: lo = 4, hi = 8   -> arr[8] = 17  > 13 -> BOUNDARY CAPTURED!
        Search range [lo, hi] = [4, 8]
```

### Phase 2: Classical Binary Search ($\mathcal{O}(\log P)$)
Once you capture a finite interval $[lo, hi]$ where $arr[lo] \le k \le arr[hi]$, execute standard binary search inside $[lo, hi]$.

---

## 💻 Implementation (LeetCode 702)

```python
class ArrayReader:
    def get(self, index: int) -> int:
        """Returns arr[index], or 2**31 - 1 if index is out of bounds."""
        pass

def search_infinite(reader: 'ArrayReader', target: int) -> int:
    # Phase 1: Exponential Doubling to find boundaries
    lo = 0
    hi = 1
    while reader.get(hi) < target:
        lo = hi
        hi *= 2

    # Phase 2: Binary Search in [lo, hi]
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        val = reader.get(mid)
        if val == target:
            return mid
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1
```

---

## ⚡ Complexity Derivation

Let $P$ be the actual index of the target:
1. **Doubling Steps:** $1, 2, 4, 8, \dots, 2^m$.  
   The loop terminates when $2^m \ge P \implies m = \lceil\log_2 P\rceil$ steps.
2. **Binary Search Window:** The interval length is $hi - lo \le 2P - P = P$.  
   Binary search takes $\log_2 P$ comparisons.

$$\text{Total Time} = \mathcal{O}(\log P) + \mathcal{O}(\log P) = \mathcal{O}(\log P)$$
* **Auxiliary Space:** $\mathcal{O}(1)$.
