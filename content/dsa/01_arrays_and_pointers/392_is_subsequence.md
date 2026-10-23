# LeetCode 392: Is Subsequence

> **Difficulty:** Easy | **Pattern:** Two Pointers (Two Conveyor Belts)  
> **Source Code:** [`392_is_subsequence.py`](392_is_subsequence.py)

## The problem

Given two strings `s` and `t`, return `True` if `s` is a subsequence of `t`, or `False` otherwise. A subsequence is formed by deleting zero or more characters from `t` without changing the order of the remaining characters.

```text
Input:  s = "abc", t = "ahbgdc" -> True  ('a', 'b', 'c' appear in order)
Input:  s = "axc", t = "ahbgdc" -> False ('x' never appears)
```

## The core trick: Two conveyor belts

Place one pointer on each string:
- **`p1` on `s` (the checklist):** Only steps forward when `s[p1]` matches the current character in `t`.
- **`p2` on `t` (the stream):** Steps forward on every iteration (`p2 += 1`).

```text
Checklist (s):  [a]   b    c
                 ^ p1

Stream (t):     [a]   h    b    g    d    c
                 ^ p2
Match: advance both p1 and p2. On mismatch: advance only p2.
```

If `p1` reaches `len(s)`, every character in `s` was matched in order.

### Algorithm steps:
* **1. Initialize pointers:** Set `p1 = 0` (targeting `s`) and `p2 = 0` (scanning `t`).
* **2. Scan stream while both pointers are in bounds:** While `p1 < len(s)` and `p2 < len(t)`:
  * If `s[p1] == t[p2]`, advance target pointer `p1 += 1`.
  * Always advance stream pointer `p2 += 1`.
* **3. Termination:** Return `p1 == len(s)` to verify all characters of `s` were matched in order.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        p1, p2 = 0, 0

        while p1 < len(s) and p2 < len(t):
            if s[p1] == t[p2]:
                p1 += 1
            p2 += 1

        return p1 == len(s)
```

</details>

## Follow-up: Billions of incoming `s` queries against a fixed `t`

If `t` is fixed and you receive $k \ge 10^9$ query strings $s_1, s_2, \dots, s_k$, scanning all of `t` for every query takes $\mathcal{O}(k \cdot |t|)$ time.

Instead, preprocess `t` once into a hash map mapping each character to its sorted list of indices in `t`:
- Example for `t = "ahbgdc"`: `{'a': [0], 'h': [1], 'b': [2], 'g': [3], 'd': [4], 'c': [5]}`.
- For each character in a query `s`, use binary search (`bisect_right`) on that character's index list to find the smallest index strictly greater than the previous matched index.
- Each query then runs in $\mathcal{O}(|s| \log |t|)$ time instead of $\mathcal{O}(|t|)$.

## Complexity

| Scenario | Time | Auxiliary Space |
| :--- | :--- | :--- |
| Single query (Two Pointers) | $\mathcal{O}(\|t\|)$ | $\mathcal{O}(1)$ |
| $k$ queries with binary search preprocessing | $\mathcal{O}(\|t\| + k \cdot \|s\| \log \|t\|)$ | $\mathcal{O}(\|t\|)$ |
