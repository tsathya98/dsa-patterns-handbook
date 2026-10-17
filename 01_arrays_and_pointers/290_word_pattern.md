# LeetCode 290: Word Pattern

> **Difficulty:** Easy | **Pattern:** Hash Maps (Bijective 1-to-1 Mapping)  
> **LeetCode:** [290. Word Pattern](https://leetcode.com/problems/word-pattern/)

## The problem

Given a `pattern` string and a space-separated string of words `s`, return `True` if there is a bijection (one-to-one mapping) between characters in `pattern` and words in `s`:
- Every character in `pattern` maps to one unique word in `s`.
- Every word in `s` maps to one unique character in `pattern`.

```text
pattern = "abba", s = "dog cat cat dog"  -> True  (a <-> dog, b <-> cat)
pattern = "abba", s = "dog cat cat fish" -> False ('a' cannot map to both dog and fish)
pattern = "abba", s = "dog dog dog dog"  -> False ('a' and 'b' cannot both map to dog)
```

## The trap: `in dict.values()` is $\mathcal{O}(k)$

A common single-dictionary solution checks if a word was already assigned using `if word in dct.values()`:

```python
if pattern[i] not in dct:
    if words[i] in dct.values():  # O(k) linear scan!
        return False
    dct[pattern[i]] = words[i]
```

Hash tables index keys in $\mathcal{O}(1)$, not values. Checking `word in dct.values()` scans every stored value linearly. On LeetCode, `pattern` only contains lowercase English letters, so `len(dct) <= 26` and the code passes. If the key space has $N$ unique items, `in dct.values()` inside a loop turns an $\mathcal{O}(N)$ algorithm into $\mathcal{O}(N^2)$.

## Two $\mathcal{O}(n)$ approaches

### 1. Two hash maps (explicit forward and reverse lookup)
Maintain two dictionaries: `p_to_w` (`char -> word`) and `w_to_p` (`word -> char`). On each pair `(p, w)`, verify that neither map has a conflicting entry in $\mathcal{O}(1)$ time.

### 2. Set cardinality trick
Two equal-length sequences form a bijection if and only if the number of unique characters, the number of unique words, and the number of unique `(char, word)` pairs are all equal:

$$\text{len}(\text{set}(\text{pattern})) == \text{len}(\text{set}(\text{words})) == \text{len}(\text{set}(\text{zip}(\text{pattern}, \text{words})))$$

- `"abba"` and `["dog", "cat", "cat", "dog"]`: `{'a', 'b'}` (2), `{'dog', 'cat'}` (2), `{('a','dog'), ('b','cat')}` (2) $\to$ `2 == 2 == 2` (`True`).
- `"abba"` and `["dog", "dog", "dog", "dog"]`: `{'a', 'b'}` (2) vs `{'dog'}` (1) $\to$ `2 != 1` (`False`).

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(" ")
        if len(pattern) != len(words):
            return False

        p_to_w = {}
        w_to_p = {}

        for p, w in zip(pattern, words):
            if (p in p_to_w and p_to_w[p] != w) or (w in w_to_p and w_to_p[w] != p):
                return False
            p_to_w[p] = w
            w_to_p[w] = p

        return True


# Alternative 1-liner using set cardinality:
class SolutionSet:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(" ")
        if len(pattern) != len(words):
            return False
        return len(set(pattern)) == len(set(words)) == len(set(zip(pattern, words)))
```

</details>

## Complexity

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Time** | $\mathcal{O}(n + m)$ | $n$ is `len(pattern)` and $m$ is `len(s)` (to split `s` into words). |
| **Space** | $\mathcal{O}(m)$ | Stores the list of words from `s.split(" ")` and up to $n$ mappings. |
