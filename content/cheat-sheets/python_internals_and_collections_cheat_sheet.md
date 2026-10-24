# Python Internals, Memory & Collections Cheat Sheet

> Guide: [03. Python Memory Model, Pointers & Core Collections](../dsa/00_foundations/03_python_memory_model_and_collections.md)

## 1. Mutability vs. Hashability

| Type | Mutable? | Hashable (Can be `set` item or `dict` key)? | Empty Syntax | 1-Item Syntax |
| :--- | :--- | :--- | :--- | :--- |
| `int`, `float`, `bool` | No | Yes | `0`, `0.0`, `False` | `45` (`(45)` is still an `int`) |
| `str` | No | Yes | `""` | `"a"` |
| `tuple` | No (fixed slots) | Only if every item inside is also hashable | `()` | `(45,)` (comma required) |
| `list` | Yes | No (`TypeError`) | `[]` | `[45]` |
| `set` | Yes | No (use `frozenset` if needed) | `set()` (`{}` is an empty dict) | `{45}` |
| `dict` | Yes | No (`TypeError`) | `{}` | `{"a": 1}` |

### Decision rules:
* **1. Top-level mutability check:** If the object is a mutable container (like `list`, `set`, or `dict`), it cannot be hashed directly and raises `TypeError`. Convert lists to tuples or sets to frozensets.
* **2. Primitive immutable types:** If the object is a primitive immutable value (`int`, `float`, `bool`, `str`), it is directly hashable and safe to use as a dictionary key or set element.
* **3. Recursive tuple inspection:** If the object is a `tuple`, verify that every nested item inside is also immutable. A tuple containing even one mutable element (such as a list) fails hashability and raises `TypeError`.


---

## 2. Why `t[1].append()` Works Inside a Tuple
A tuple is an immutable array of **memory addresses (pointers)**.
- You **cannot** overwrite which memory address a slot points to (`t[1] = [99]` raises `TypeError`).
- You **can** mutate the object living at that address if the object itself is mutable (`list`, `set`, `dict`).

```python
t = (1, [10, 20], {100, 200})

t[1].append(30)   # Works: list at slot 1 mutates in place; pointer in t[1] never changed
t[2].add(300)     # Works: set at slot 2 mutates in place
t[1] = [10, 20]   # TypeError: cannot replace the pointer stored in slot 1
```

Because `t` contains a mutable list, `{t}` raises `TypeError: unhashable type: 'list'`. A tuple is only hashable when every element inside it is immutable (`(1, (2, 3))`).

---

## 3. The House and Keys Rule (Mutation vs. Reassignment vs. Slicing)

```python
listb = [1, 2, 3]
lista = listb  # Both keys unlock the SAME house (address 0x100)
```

| Action | Code | What Actually Happens | Effect on `lista` |
| :--- | :--- | :--- | :--- |
| **Mutation (inside the house)** | `listb.append(99)`<br>`listb[0] = 42` | Walks inside 123 Main St and rearranges furniture. Memory address stays `0x100`. | **Affected!** `lista` sees `[42, 2, 3, 99]`. |
| **Reassignment (moving houses)** | `listb = [7, 8, 9]` | Moves key `listb` to a brand new house (`0x200`). `lista` remains at 123 Main St. | **Untouched!** `lista` stays `[1, 2, 3]`. |
| **Slice Copy (making a twin house)** | `lista = listb[:]` | Slicing on the right creates a separate shallow copy at `0x300`. | **Untouched!** Modifying `listb` will not touch `lista`. |
| **Slice Assignment (gutting the house)** | `listb[:] = [7, 8, 9]` | Slicing on the left replaces all contents inside 123 Main St in-place without changing address `0x100`. | **Affected!** `lista` sees `[7, 8, 9]`. |

---

## 4. The 2D Grid Allocation Gotcha (`[[0] * C] * R`)

* **1D list of ints (`[0] * 5`):** Safe. Integers are immutable primitives. Changing `arr[0] = 99` rebinds slot 0 to integer `99`.
* **2D list of lists (`[[0] * C] * R`):** Trap! Lists are mutable. `* R` creates $R$ duplicate pointers to the **exact same row list in RAM**. Updating `grid[0][0] = 99` mutates all $R$ rows.
* **The Fix:** Always use list comprehension: `grid = [[0 for _ in range(C)] for _ in range(R)]`.

---

## 5. In-Place Mutation vs. New Copy

| Goal | In-Place ($\mathcal{O}(1)$ Extra Space, Returns `None`) | New Object Copy ($\mathcal{O}(n)$ Extra Space) |
| :--- | :--- | :--- |
| Reverse a list | `nums.reverse()` | `nums[::-1]` or `list(reversed(nums))` |
| Sort a list | `nums.sort()` | `sorted(nums)` |
| Add elements | `nums.append(x)` / `nums.extend(b)` | `nums + b` (allocates a new list) |
| Slice a list | N/A | `nums[1:4]` (allocates a new list of pointers) |

---

## 6. Common Operation Costs & Gotchas

| Operation | Code | Time | Gotcha |
| :--- | :--- | :--- | :--- |
| List vs. Set lookup | `x in lst` vs `x in st` | $\mathcal{O}(n)$ vs $\mathcal{O}(1)$ | Convert lookup lists to a `set` before looping. |
| Remove by value | `nums.remove(3)` | $\mathcal{O}(n)$ | Removes only the **first** match; raises `ValueError` if missing. |
| Pop end vs. front | `nums.pop()` vs `nums.pop(0)` | $\mathcal{O}(1)$ vs $\mathcal{O}(n)$ | Use `collections.deque.popleft()` ($\mathcal{O}(1)$) for queues. |
| Dict lookup | `d["k"]` vs `d.get("k", 0)` | $\mathcal{O}(1)$ | `d["k"]` raises `KeyError` if missing; `.get()` returns default. |
| Star unpacking | `a, *mid, b = (1, 2, 3, 4)` | $\mathcal{O}(n)$ | `mid` is always a `list` (`[2, 3]`), even when unpacking a tuple or string. |
| `zip()` truncation | `dict(zip(keys, vals))` | $\mathcal{O}(\min(n, m))$ | Silently stops at the shorter iterable without raising an error. |
| Negative slicing | `"codekerdos"[-4:]` | $\mathcal{O}(k)$ | Starts 4 chars from the end and slices to the end (`"rdos"`). |
| Floor division | `3 // 2` vs `-3 // 2` | $\mathcal{O}(1)$ | Floors toward $-\infty$: `-3 // 2 == -2`. Use `int(-3 / 2) == -1` to truncate toward `0`. |
