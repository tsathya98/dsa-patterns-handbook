# Arrays, Strings & HashMaps Cheat Sheet

## 1. Core Operations & Costs

| Type | Read by Index / Key | Search (`x in c`) | Append | Insert/Pop at Index 0 | Mutable? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`list` (Dynamic Array)** | $\mathcal{O}(1)$ | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | $\mathcal{O}(n)$ (shifts everything) | Yes |
| **`str` (String)** | $\mathcal{O}(1)$ | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ copy | $\mathcal{O}(n)$ copy | No |
| **`set` (Hash Set)** | N/A | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | N/A | Yes |
| **`dict` (Hash Map)** | $\mathcal{O}(1)$ by key | $\mathcal{O}(1)$ by key | $\mathcal{O}(1)$ | N/A | Yes |

---

## 2. Three Python Traps That Cause TLE

### Trap 1: String concatenation in a loop (`res += ch`)
Strings are immutable. Writing `res += ch` inside a loop allocates and copies a brand-new string on every step, turning an $\mathcal{O}(n)$ loop into $\mathcal{O}(n^2)$.
```python
# Do this instead (O(n)):
chars = []
for ch in s:
    chars.append(ch)
return "".join(chars)
```

### Trap 2: Checking `val in my_dict.values()` ([LC 290: Word Pattern](../01_arrays_and_pointers/290_word_pattern.md))
`key in my_dict` is $\mathcal{O}(1)$ because keys are hashed. `val in my_dict.values()` scans every entry linearly in $\mathcal{O}(n)$ time. For 1-to-1 (bijective) mappings, use two dicts or a `seen_values` set.

### Trap 3: `list.pop(0)` or `list.insert(0, x)`
Inserting or removing at index `0` shifts all $n - 1$ elements in memory ($\mathcal{O}(n)$). Use `collections.deque` (`popleft()` / `appendleft()` in $\mathcal{O}(1)$) or build the list backward and `.reverse()` it at the end.

---

## 3. Core HashMap Patterns

### Pattern 1: One-Pass Complement Lookup (LC 1: Two Sum)
Instead of checking all pairs in $\mathcal{O}(n^2)$, ask the dict if `target - num` has already been seen:
```python
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        comp = target - num
        if comp in seen:
            return [seen[comp], i]
        seen[num] = i
    return []
```

### Algorithm steps:
* **1. Complement calculation:** For each element `num` at index `i`, compute required complement `comp = target - num`.
* **2. Hash lookup branch:** Check if `comp` exists in `seen`. If present, immediately return pair indices `[seen[comp], i]`.
* **3. State memoization:** If absent, save `seen[num] = i` and proceed to the next element, maintaining $\mathcal{O}(n)$ time and $\mathcal{O}(n)$ auxiliary space.


### Pattern 2: Canonical Signature Grouping (LC 49: Group Anagrams)
Group items that share an underlying property by converting each item into a canonical immutable key (a sorted string or a 26-element character count `tuple`):
```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for word in strs:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())
```
*(Remember: `list` and `set` cannot be dictionary keys because they are mutable; convert them to `tuple` or `str` first.)*
