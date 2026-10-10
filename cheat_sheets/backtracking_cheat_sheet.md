# 🔄 Backtracking Master Cheat Sheet & Decision Guide

> **Pattern:** Backtracking (Exhaustive Search with Undo / Pruning)  
> **Audience:** Complete Beginner / 1st-Year CS Student  
> **Analogy:** Exploring a Maze with an "Undo" (Ctrl+Z) Button

---

## 💡 1. What is Backtracking?

Imagine walking through a maze. You reach a fork in the road:
1. You **choose** to go Left.
2. You walk until you hit a dead end.
3. You don't give up! You **backtrack** (walk backward to the fork).
4. Now you **choose** to go Right!

Backtracking is simply **brute-force recursion**, but with a superpower:
Whenever you reach an invalid state or finish recording a combination, you **undo your last move** and try the next alternative.

```text
Decision Tree for [1, 2]:
                    [] (Start)
                 /      \
            Include 1   Don't Include 1
              /             \
            [1]              []
           /   \            /   \
        [1,2]  [1]        [2]   []
```

---

## ⚙️ 2. The 3-Step Universal Template

Every single backtracking problem in computer science follows the exact same 3-step rhythm:

```python
def backtrack(state):
    if base_case_reached:
        results.append(list(path))  # Record answer snapshot
        return
        
    for choice in available_choices:
        if is_valid(choice):
            path.append(choice)      # 1. CHOOSE (Make a move)
            backtrack(next_state)    # 2. EXPLORE (Recurse deeper)
            path.pop()               # 3. UN-CHOOSE (Undo / Backtrack!)
```

> ⚠️ **The Critical Line: `path.pop()`**  
> If you forget `path.pop()`, the choices from earlier branches pollute the next branches!

---

## 🏆 3. The 3 Classic Types of Backtracking Problems

---

### 🔹 Type 1: Subsets (Include vs. Exclude)
* **Goal:** Generate all possible subsets (power set) of an array `[1, 2, 3]`.
* **Formula:** An array of length $N$ has $2^N$ subsets.
* **LeetCode Problem:** *Subsets* (LC 78).

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result = []
    
    def backtrack(start_idx: int, path: list[int]):
        # Every path along the way is a valid subset!
        result.append(list(path))  # Must use list(path) to make a copy!
        
        for i in range(start_idx, len(nums)):
            path.append(nums[i])        # 1. Choose
            backtrack(i + 1, path)      # 2. Explore
            path.pop()                  # 3. Un-choose
            
    backtrack(0, [])
    return result
```

---

### 🔹 Type 2: Permutations (Order Matters!)
* **Goal:** Rearrange numbers in all possible orders (e.g. `[1, 2, 3]` $\to$ `[1,2,3]`, `[1,3,2]`, `[2,1,3]`...).
* **Formula:** An array of length $N$ has $N!$ permutations.
* **LeetCode Problem:** *Permutations* (LC 46).

```python
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    
    def backtrack(path: list[int]):
        if len(path) == len(nums):
            result.append(list(path))
            return
            
        for num in nums:
            if num not in path:          # Only choose numbers not yet picked!
                path.append(num)         # 1. Choose
                backtrack(path)          # 2. Explore
                path.pop()               # 3. Un-choose
                
    backtrack([])
    return result
```

---

### 🔹 Type 3: Combinations (Choose $K$ items)
* **Goal:** Pick $K$ items out of $N$ candidates (e.g., choose 2 items from `[1, 2, 3, 4]`).
* **LeetCode Problem:** *Combinations* (LC 77).

---

## ⚠️ 4. The #1 Python Trap in Backtracking

Look at this common bug:
```python
result.append(path)  # ❌ FATAL BUG!
```
In Python, lists are passed **by reference**! If you do `result.append(path)`, every element in `result` will point to the exact same list in memory. When the recursion finishes and `path` is popped empty, your `result` will be `[[], [], []]`!

**The Fix:** Always append a **copy** of the list:
```python
result.append(list(path))  # ✅ Or path[:]
```
