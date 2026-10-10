# 🧱 Arrays, Strings & HashMaps Master Cheat Sheet & Decision Guide

> **Pattern:** Core Linear Data Structures (Arrays, Strings, Sets, and HashMaps)  
> **Audience:** Complete Beginner / 1st-Year CS Student  
> **Analogies:** The Row of Houses (Array) vs. The VIP Bouncer (Set) vs. The Coat Check (HashMap)

---

## 💡 1. The 4 Big Data Structures Compared

| Data Structure | Plain English Analogy | Superpower | Big Weakness |
|---|---|---|---|
| **Array / List** | A row of houses on a street | Instant index access (`arr[4]`) in $\mathcal{O}(1)$ | Inserting/deleting in the middle is slow ($\mathcal{O}(n)$) |
| **String** | An immutable sentence carved in stone | Fast sequential reads | Changing a character creates a whole new string! |
| **Set** | A VIP bouncer's guest list | Instant presence check: *"Have I seen this?"* in $\mathcal{O}(1)$ | No duplicate items, no indexing (`set[0]` doesn't exist) |
| **HashMap / Dict** | A coat-check ticket system | Look up any value by key (`ticket -> coat`) in $\mathcal{O}(1)$ | Uses more memory than an array |

---

## 🛑 2. The #1 Python String Trap: $\mathcal{O}(n^2)$ Concatenation

In Python, strings are **immutable** (cannot be changed in-place).
```python
# ❌ DANGEROUS CODE (O(n^2)):
result = ""
for char in s:
    result += char  # Python builds an ENTIRE NEW STRING copy every single time!
```
If `s` has $100,000$ characters, this does $10^{10}$ operations and **Times Out (TLE)**!

```python
# ✅ OPTIMAL CODE (O(n)):
result = []
for char in s:
    result.append(char)
return "".join(result)  # Fast single-pass string allocation!
```

---

## 🏆 3. The "Two Sum" Complement Trick (The Most Famous Interview Pattern)

When asked to find two numbers that add up to `target`:
* **Brute Force:** Check every pair using nested loops $\to \mathcal{O}(n^2)$.
* **HashMap Trick:** As you walk through the array, remember every number you've seen. For each number, ask the HashMap: *"Have we already seen `target - num`?"* $\to \mathcal{O}(n)$ time!

```python
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}  # number -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
        
    return []
```

---

## 🗂️ 4. The Group Anagrams Pattern (Canonical Keys)

When you need to group items together (like anagrams `"eat"`, `"tea"`, `"ate"`):
1. **Find a signature (canonical key):** Sorting the characters of `"eat"`, `"tea"`, and `"ate"` all produce the exact same key: `"aet"`.
2. Store the words in a dictionary where the key is the sorted signature!

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    
    for word in strs:
        sorted_key = "".join(sorted(word))  # "eat" -> "aet"
        groups[sorted_key].append(word)
        
    return list(groups.values())
```
