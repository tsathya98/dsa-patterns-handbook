# Backtracking Cheat Sheet

Backtracking is recursion with an undo step: make a choice, recurse deeper, and then pop that choice (`path.pop()`) on the way back up so you can try the next branch cleanly.

```text
Decision Tree for Subsets of [1, 2]:
               []
            /      \
      pick 1        skip 1
        /              \
      [1]              []
     /   \            /  \
  [1,2]  [1]        [2]  []
```

## 1. The 3-Step Universal Template

Every backtracking problem follows the same loop:
1. **Choose:** `path.append(choice)`
2. **Explore:** `backtrack(next_state)`
3. **Un-choose (Undo):** `path.pop()`

```python
def backtrack(state):
    if is_solution(state):
        result.append(path[:])  # Always append a copy!
        return

    for choice in choices(state):
        if is_valid(choice):
            path.append(choice)   # 1. Choose
            backtrack(next_state) # 2. Explore
            path.pop()            # 3. Undo
```

---

## 2. The 3 Classic Problem Types

### Type 1: Subsets (LC 78, $2^n$ total)
Order does not matter, so pass `start_idx = i + 1` to avoid picking earlier elements again. Every node in the tree is a valid subset.

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res, path = [], []

    def backtrack(start: int) -> None:
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return res
```

### Type 2: Combinations of Size $K$ (LC 77, $\binom{n}{k}$ total)
Same as Subsets, except you only record `path[:]` when `len(path) == k`.

### Type 3: Permutations (LC 46, $n!$ total)
Order matters (`[1, 2]` and `[2, 1]` are different), so iterate over all `nums` each time and use a `used` set or boolean array to skip elements already in `path`.

```python
def permute(nums: list[int]) -> list[list[int]]:
    res, path = [], []
    used = [False] * len(nums)

    def backtrack() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

    backtrack()
    return res
```

---

## 3. The #1 Python Bug: `res.append(path)`
In Python, lists are mutable references. Writing `res.append(path)` appends a pointer to the same `path` list, which gets emptied by `path.pop()` by the time recursion finishes, leaving `res` full of empty lists `[[], [], []]`. Always copy with `res.append(path[:])` or `list(path)`.
