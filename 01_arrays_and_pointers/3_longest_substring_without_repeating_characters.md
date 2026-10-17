# LeetCode 3: Longest Substring Without Repeating Characters

> **Difficulty:** Medium | **Pattern:** Dynamic Sliding Window  
> **Source Code:** [`3_longest_substring_without_repeating_characters.py`](./3_longest_substring_without_repeating_characters.py)

## The problem

Given a string `s`, return the length of the longest contiguous substring that contains no duplicate characters.

```text
Input:  s = "abcabcbb" -> Output: 3 ("abc")
Input:  s = "bbbbb"    -> Output: 1 ("b")
Input:  s = "pwwkew"   -> Output: 3 ("wke", note that "pwke" is a subsequence, not a substring)
```

## Why the naive way fails

Checking every starting index and testing `len(tmp) == len(set(tmp))` inside a nested loop runs in $\mathcal{O}(n^3)$ time:
1. String concatenation `tmp += s[j]` copies the substring on every step.
2. `set(tmp)` rebuilds a hash set from scratch in $\mathcal{O}(k)$ time per character.

## The core trick: Dynamic sliding window

Maintain a window `[left, right]` and a hash set `seen` holding the characters currently inside that window:

```text
String:   a   b   c   a   b   c   b   b
Window:  [a   b   c]                      seen = {'a', 'b', 'c'}, len = 3
                      ^ incoming 'a' is already in seen

Shrink from left until the old 'a' is removed:
Window:      [b   c   a]                  seen = {'b', 'c', 'a'}, len = 3
```

1. **Expand (`right`):** Inspect the incoming character `c = s[right]`.
2. **Shrink (`left`):** While `c` is already in `seen`, remove `s[left]` from `seen` and increment `left += 1` until the duplicate is evicted.
3. **Record:** Add `c` to `seen` and update `max_cnt = max(max_cnt, right - left + 1)` (or `len(seen)`).

## Step-by-step trace

Tracing `s = "pwwkew"`:

| `right` | `c` | `c in seen`? | Shrink (`left` moves) | Window `[left..right]` | `len(seen)` | `max_cnt` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `'p'` | False | None (`left = 0`) | `"p"` | `1` | `1` |
| `1` | `'w'` | False | None (`left = 0`) | `"pw"` | `2` | `2` |
| `2` | `'w'` | True | Remove `'p'`, `'w'` (`left -> 2`) | `"w"` | `1` | `2` |
| `3` | `'k'` | False | None (`left = 2`) | `"wk"` | `2` | `2` |
| `4` | `'e'` | False | None (`left = 2`) | `"wke"` | `3` | `3` |
| `5` | `'w'` | True | Remove `'w'` (`left -> 3`) | `"kew"` | `3` | `3` |

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        max_cnt = 0
        left = 0

        for c in s:
            while c in seen:
                seen.discard(s[left])
                left += 1

            seen.add(c)
            max_cnt = max(max_cnt, len(seen))

        return max_cnt
```

</details>

## Complexity

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n)$ | Each character enters `seen` once and is removed from `seen` at most once (at most $2n$ pointer operations). |
| **Space** | $\mathcal{O}(\min(n, m))$ | `seen` holds at most $m$ unique characters ($m \le 128$ for ASCII). |
