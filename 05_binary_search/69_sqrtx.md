# LeetCode 69: Sqrt(x)

> **Difficulty:** Easy | **Pattern:** Binary Search on Answer (`mid * mid <= x`) | **Access:** Free  
> **Link:** [https://leetcode.com/problems/sqrtx/](https://leetcode.com/problems/sqrtx/)

## The problem

Given a non-negative integer `x`, return the square root of `x` rounded down to the nearest integer ($\lfloor\sqrt{x}\rfloor$) without using any built-in exponent function or operator.

---

## The core trick: Find the largest integer `mid` where `mid * mid <= x`

The condition `mid * mid <= x` is monotonic:
```text
For x = 8:
Candidate m:      0    1    2    3    4
m * m <= 8?       T    T    T    F    F
                            ^
                   Last True = 2
```
Search `[1, x // 2]` (for `x >= 2`):
* If `mid * mid <= x`: `mid` is valid! Record `ans = mid` and try larger candidates (`lo = mid + 1`).
* If `mid * mid > x`: `mid` is too big! Eliminate right half (`hi = mid - 1`).

---

## Step-by-step trace (`x = 8`)

**Initial:** `lo = 1, hi = 4, ans = 0`

**Iteration 1 (`lo = 1`, `hi = 4`):**
`mid = 2`. `2 * 2 = 4 <= 8` (True).
Record `ans = 2`, try bigger: `lo = mid + 1 = 3`.
```text
Candidates: [ 1,   2,   3,   4 ]
             lo   mid       hi   -> 2^2 <= 8: ans = 2, lo = 3
```

**Iteration 2 (`lo = 3`, `hi = 4`):**
`mid = 3`. `3 * 3 = 9 > 8` (False).
Too big: `hi = mid - 1 = 2`.
```text
Candidates: [ x,   x,   3,   4 ]
                     lo,mid  hi  -> 3^2 > 8: hi = 2
```

**Loop ends (`lo = 3 > hi = 2`):** Return `ans = 2`.

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x

        lo, hi = 1, x // 2
        ans = 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if mid * mid <= x:
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        return ans
```

</details>

---

## Complexity

* **Time:** $\mathcal{O}(\log x)$
* **Space:** $\mathcal{O}(1)$
