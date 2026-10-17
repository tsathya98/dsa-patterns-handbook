# Sliding Window Cheat Sheet

Instead of recomputing sums or character counts for every slice in $\mathcal{O}(n^2)$ time, maintain a moving window over the array and update only the two edges (`entering` on the right, `leaving` on the left) in $\mathcal{O}(n)$ time.

## 1. How to spot it
Look for two things together:
1. **Contiguous** subarray or substring (elements sit next to each other, no skipping).
2. Asking for the **maximum**, **minimum**, **longest**, or **shortest** valid range.

---

## 2. Flavor 1: Fixed-Size Window ($K$)
The window width stays locked at $K$. Consecutive windows share $K - 1$ elements, so you update the running state in $\mathcal{O}(1)$ per step:
$$\text{window} = \text{window} + \text{entering} - \text{leaving}$$

### Template A: Numeric sum or average ([LC 643](../01_arrays_and_pointers/643_maximum_average_subarray_i.md))
```python
def max_sum_fixed_window(nums: list[int], k: int) -> int:
    window_sum = sum(nums[:k])
    max_sum = window_sum

    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        if window_sum > max_sum:
            max_sum = window_sum

    return max_sum
```
*(Tip: When a problem asks for the maximum average, don't divide by `k` inside the loop. Find the maximum integer sum first and divide by `k` once at the return statement.)*

### Template B: String or condition counter ([LC 1456](../01_arrays_and_pointers/1456_maximum_number_of_vowels_in_a_substring_of_given_length.md))
```python
def max_vowels(s: str, k: int) -> int:
    vowels = {'a', 'e', 'i', 'o', 'u'}
    count = sum(1 for ch in s[:k] if ch in vowels)
    max_count = count

    for i in range(k, len(s)):
        if s[i] in vowels:
            count += 1
        if s[i - k] in vowels:
            count -= 1
        if count > max_count:
            max_count = count

    return max_count
```

---

## 3. Flavor 2: Dynamic Window (Rubber Band)
The window grows and shrinks as needed:
1. Advance `right` to pull in a new element.
2. While the window violates the rule (like having a duplicate character or exceeding a sum), advance `left` to kick elements out until the window is valid again.
3. Update the best length (`right - left + 1`).

### Template ([LC 3: Longest Substring Without Repeating Characters](../01_arrays_and_pointers/3_longest_substring_without_repeating_characters.md))
```python
def lengthOfLongestSubstring(s: str) -> int:
    left = 0
    seen = set()
    max_len = 0

    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## 4. Quick Decision Table

| Goal | Window Type | When to shrink `left` | Classic Problem |
| :--- | :--- | :--- | :--- |
| Max sum / count of length $K$ | Fixed ($K$) | Every step once `i >= k` | LC 643, LC 1456 |
| Longest substring without repeats | Dynamic | `while s[right] in seen` | LC 3 |
| Shortest subarray with sum $\ge S$ | Dynamic | `while cur_sum >= target` | LC 209 |
| Longest ones with at most $K$ flips | Dynamic | `while zero_count > k` | LC 1004 |

---

## 5. Common Traps
1. **Window length off-by-one:** Inclusive length from `left` to `right` is `right - left + 1`, not `right - left`.
2. **Using `if` instead of `while` when shrinking:** `left` often needs to step forward multiple times before the window becomes valid again.
3. **Writing `s[k]` instead of `s[i]`:** Inside `for i in range(k, len(s))`, the entering item is `s[i]` and the leaving item is `s[i - k]`.
4. **Can `count` drop below zero?** No. Every element leaving at `i - k` entered earlier at `i`, so you never subtract a match you didn't already add.
