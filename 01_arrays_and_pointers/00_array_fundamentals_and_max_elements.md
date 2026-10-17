# Array fundamentals, max elements, and leaders

> **Course reference:** CodeKerdos DSA, Class 4 and Class 6
> **Core concepts:** Python lists vs low-level arrays, single-pass max tracking, right-to-left traversal, and array leaders.

## Python `list` vs `array.array`

In Python coding interviews, always use the built-in `list`. It is a dynamic array of pointers to heap objects, heavily optimized in CPython, and grows automatically. The `array.array` module enforces homogeneous C types, lacks standard interview helper methods, and offers no meaningful algorithmic speedup in Python.

## Count elements with at least one greater element

Given an integer array `arr`, count how many elements have at least one strictly greater element in the array.

Comparing every element against every other element takes $\mathcal{O}(N^2)$ time. Instead, find the maximum value in `arr`. Every element strictly smaller than `max_val` has at least one greater element (the maximum itself). Only elements equal to `max_val` have nothing greater than them.

$$\text{Result} = N - \text{count}(\text{max\_val})$$

```text
Input:  arr = [2, 5, 1, 4, 8, 0, 8, 1, 3, 8]
Length: 10, Max: 8, Count of 8s: 3
Result: 10 - 3 = 7
```

<details>
<summary>Spoiler: Solution Code</summary>

```python
def count_elements_with_greater(arr: list[int]) -> int:
    if not arr:
        return 0
    max_val = max(arr)
    return len(arr) - arr.count(max_val)
```

</details>

* **Time complexity:** $\mathcal{O}(N)$ across two linear passes (`max` and `count`).
* **Space complexity:** $\mathcal{O}(1)$.

## Leaders in an array

An element is a leader if it is strictly greater than all elements to its right. The rightmost element is always a leader because nothing sits to its right.

Scanning right from every index $i$ takes $\mathcal{O}(N^2)$ time. Instead, scan from right to left ($N-1$ down to $0$) while tracking `max_so_far`. An element `arr[i]` is a leader if and only if `arr[i] > max_so_far`.

### Algorithm steps:
* **1. Initialize rightmost leader:** Set `leaders = [arr[-1]]` and `max_so_far = arr[-1]`. The rightmost element has no elements to its right, so it is always a leader.
* **2. Scan right to left:** Iterate `i` from `n - 2` down to `0`.
* **3. Compare with running max:**
  * If `arr[i] > max_so_far`, append `arr[i]` to `leaders` and update `max_so_far = arr[i]`.
  * Otherwise, ignore `arr[i]` because a larger element exists to its right.
* **4. Return leaders:** Reverse `leaders` if original left-to-right order is required, completing in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ auxiliary space.

| Index $i$ | `arr[i]` | `max_so_far` (before) | `arr[i] > max_so_far`? | Leader? | `max_so_far` (after) |
|---|---|---|---|---|---|
| 5 | 2 | None | Base case (rightmost) | Yes | 2 |
| 4 | 5 | 2 | $5 > 2$ | Yes | 5 |
| 3 | 3 | 5 | $3 < 5$ | No | 5 |
| 2 | 4 | 5 | $4 < 5$ | No | 5 |
| 1 | 17 | 5 | $17 > 5$ | Yes | 17 |
| 0 | 16 | 17 | $16 < 17$ | No | 17 |

<details>
<summary>Spoiler: Solution Code</summary>

```python
def find_leaders(arr: list[int]) -> list[int]:
    n = len(arr)
    if n == 0:
        return []

    leaders = [arr[-1]]
    max_so_far = arr[-1]

    for i in range(n - 2, -1, -1):
        if arr[i] > max_so_far:
            leaders.append(arr[i])
            max_so_far = arr[i]

    leaders.reverse()
    return leaders
```

</details>

* **Time complexity:** $\mathcal{O}(N)$.
* **Space complexity:** $\mathcal{O}(1)$ auxiliary (excluding the output list).
