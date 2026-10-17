# 🐍 Python Internals, Memory & Collections Cheat Sheet

> **Scope:** Pointers vs Values, Mutability vs Hashability, Time/Space Costs of Built-in Operations, and Classic Interview Gotchas.

---

## 1. Mutability vs. Hashability Matrix

| Type | Mutable? (Can change in-place?) | Hashable? (Can be `set` item / `dict` key?) | Empty Syntax | Single-Item Syntax |
|---|---|---|---|---|
| `int`, `float`, `bool` | ❌ No (Immutable) | ✅ Yes | `0`, `0.0`, `False` | `45` (Note: `(45)` is still an `int`!) |
| `str` | ❌ No (Immutable) | ✅ Yes | `""` | `"a"` |
| `tuple` | ❌ No (Fixed pointer slots) | ⚠️ **Only if ALL elements inside are hashable!** | `()` | `(45,)` or `45,` (**comma required!**) |
| `list` | ✅ Yes (Dynamic pointer array) | ❌ No (`TypeError`) | `[]` | `[45]` |
| `set` | ✅ Yes (Hash table of keys) | ❌ No (Use `frozenset` if needed) | `set()` (**NOT `{}`!**) | `{45}` |
| `dict` | ✅ Yes (Hash table of `k: v`) | ❌ No (`TypeError`) | `{}` | `{"a": 1}` |

---

## 2. The Tuple Pointer Rule (Why `t[2].append()` Works)

**Mental Model:** A tuple is an **immutable array of memory addresses (pointers)**.
* You **CANNOT** change which memory address a tuple slot points to (`t[2] = new_obj` $\to$ ❌ `TypeError`).
* You **CAN** mutate the object living at that memory address if that object is mutable (`list`, `set`, `dict`)!

```python
t = (1, [10, 20], {100, 200}, {"a": 1})

t[1].append(30)     # ✅ Works! List at slot 1 mutates in-place; pointer in t[1] is unchanged.
t[2].add(300)       # ✅ Works! Set at slot 2 mutates in-place; pointer in t[2] is unchanged.
t[3]["b"] = 2       # ✅ Works! Dict at slot 3 mutates in-place; pointer in t[3] is unchanged.

t[1] = [10, 20, 30] # ❌ TypeError! Trying to overwrite slot 1's memory address.
```

**Hashability Consequence:**
* `{1, 2, (3, 4)}` $\to$ ✅ **Valid set** (tuple holds only immutable ints).
* `{1, 2, (3, [4, 5])}` $\to$ ❌ **`TypeError: unhashable type: 'list'`** (because the inner list could mutate!).

---

## 3. In-Place Mutation vs. New Object Allocation

| Goal | In-Place ($\mathcal{O}(1)$ Extra Space, Returns `None`) | New Object Copy ($\mathcal{O}(n)$ Extra Space, Returns New Object) |
|---|---|---|
| **Reverse a List** | `nums.reverse()` | `nums[::-1]` or ` list(reversed(nums))` |
| **Sort a List** | `nums.sort()` | `sorted(nums)` |
| **Add to List** | `nums.append(x)` / `nums.extend(b)` | `nums + b` (Allocates brand-new list!) |
| **Slice a List** | N/A | `nums[1:4]` (Allocates new list copying element pointers) |

> **GC Rule on Slices & `+`:**  
> `c = a + b` creates a new list `c`, and `s = c[1:4]` creates *another* new list `s` that copies the **element pointers** (not a reference to `c`). If you then set `c = 0`, the list container created by `a + b` has **0 references** and is **immediately Garbage Collected**!

---

## 4. High-Yield Operation Complexities & Traps

| Operation | Code | Time | Space | Critical Gotcha |
|---|---|---|---|---|
| **List vs Set Lookup** | `x in my_list` vs `x in my_set` | $\mathcal{O}(n)$ vs $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Always convert a lookup list to a `set` before looping! |
| **List Remove by Value** | `nums.remove(3)` | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Removes **only the first** exact match of `3`. Raises `ValueError` if not found. |
| **List Pop End vs Front** | `nums.pop()` vs `nums.pop(0)` | $\mathcal{O}(1)$ vs $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Never `pop(0)` in a loop! Use `collections.deque.popleft()` ($\mathcal{O}(1)$). |
| **Dict Bracket vs `.get()`** | `d["c"]` vs `d.get("c", 0)` | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | `d["c"]` raises `KeyError` if missing; `d.get("c")` returns `None` (or default). |
| **Star Unpacking** | `a, *mid, b = (1, 2, 3, 4)` | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | `mid` is **always a `list`** (`[2, 3]`), even when unpacking a `tuple` or `str`! |
| **Zipping Collections** | `dict(zip(keys, vals))` | $\mathcal{O}(\min(N,M))$ | $\mathcal{O}(\min(N,M))$ | Silently **truncates** to the shortest iterable! Does NOT raise `ValueError`. |
| **Negative Slicing** | `"codecurdos"[-4:]` | $\mathcal{O}(k)$ | $\mathcal{O}(k)$ | Starts 4 chars from the end (`'r'`) and slices to the end $\to$ `"rdos"`. |
| **Floor Division** | `3 // 2` vs `-3 // 2` | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Floors toward $-\infty$: `3 // 2 == 1`, but `-3 // 2 == -2` (use `int(-3 / 2)` to truncate toward `0`). |
