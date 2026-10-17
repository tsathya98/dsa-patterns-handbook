# Python memory model, pointers, and core collections

> **Context:** Airtribe DSA Foundations, Python internals  
> **Goal:** Understand how Python stores variables, pointers, lists, tuples, sets, and dicts in memory so mutation and aliasing bugs make sense.

## 1. Variables are references, not boxes

In C or C++, a variable like `int x = 10` is a typed slot in memory holding `10`.  
In Python, every value is an object on the heap, and a variable name is a reference (pointer) to that object's memory address.

```text
name = "Ashish"          name = "Arushi" (Reassignment)
───────────────          ──────────────────────────────
[ name ] ──► 0x100 ("Ashish")     [ name ] ──────┐
                                                 ▼
                         0x100 ("Ashish")      0x200 ("Arushi")
                         (0 refs -> GC)        (1 ref -> Alive)
```

* Strings, integers, and tuples are **immutable**. You cannot overwrite `"Ashish"` in place.
* Reassigning `name = "Arushi"` allocates a new string object at `0x200` and points `name` to it.
* Once `0x100 ("Ashish")` drops to zero references, Python's garbage collector reclaims that memory.

## 2. Low-level arrays vs. Python `list`

| Feature | Low-level array (C / `array` module) | Python `list` (`[1, "hi", 3.5]`) |
|---|---|---|
| **Data types** | Homogeneous (all elements share the same type, e.g., 32-bit `int`). | Heterogeneous (can mix `int`, `str`, `list`, etc.). |
| **Memory layout** | Contiguous raw values packed back-to-back in RAM. | Contiguous array of pointers pointing to scattered heap objects. |
| **Index lookup `a[i]`** | $\mathcal{O}(1)$ (`base_address + i * sizeof(type)`) | $\mathcal{O}(1)$ (`base_address + i * 8 bytes`, then dereference pointer) |

```text
LOW-LEVEL ARRAY (Raw Values):
┌─────┬─────┬─────┐
│  10 │  20 │  30 │   (Contiguous raw integers in memory)
└─────┴─────┴─────┘

PYTHON LIST (Array of Pointers):
┌───────┬───────┬───────┐
│ 0xA01 │ 0xB04 │ 0xC09 │   (Contiguous 64-bit memory addresses)
└───┬───┴───┬───┴───┬───┘
    │       │       └──────────► "hello" (str object at 0xC09)
    │       └──────────► [1, 2] (list object at 0xB04)
    └──────────► 10 (int object at 0xA01)
```

## 3. Mutable objects inside an immutable tuple

Consider this snippet:
```python
t = (1, 2, [3, 4])
t[2].append(5)
```
Why does `t[2].append(5)` succeed if tuples are immutable?

Tuple immutability locks the pointer addresses stored in the tuple's slots. It does not freeze the heap objects those pointers reference.

```text
t = (1, 2, [100, 200])

Tuple t (Immutable Slots):
┌─────────┬─────────┬─────────┐
│ Slot 0  │ Slot 1  │ Slot 2  │
│  0x001  │  0x002  │  0x999  │  ◄── Slot 2 is locked to address 0x999
└────┬────┴────┬────┴────┬────┘
     ▼         ▼         ▼
    (1)       (2)     0x999: [ 100, 200 ]  (Mutable List Object)
```

### Case A: `t[2].append(300)` (succeeds)
* Python follows pointer `0x999` to the list object and appends `300` inside that list.
* Tuple slot 2 still holds `0x999`. Because the slot address never changed, no error is raised.
* The same applies to a `set` or `dict` inside a tuple:
  * `t = (1, {10, 20}); t[1].add(30)` works.
  * `t = (1, {"a": 1}); t[1]["b"] = 2` works.

### Case B: `t[2] = [100, 200, 300]` (raises `TypeError`)
* `[100, 200, 300]` creates a new list at a new address (say `0x888`).
* `t[2] = ...` tries to overwrite slot 2 from `0x999` to `0x888`.
* Tuple slots cannot be reassigned, raising `TypeError: 'tuple' object does not support item assignment`.

### Edge case: `t[2] += [300]` (mutates the list and raises `TypeError`)
* `+=` on a list calls `list.__iadd__`, which mutates the list at `0x999` in place first, and then attempts to assign the returned reference back to `t[2]`.
* The assignment step raises `TypeError`, even though the list inside `t[2]` was already modified.

## 4. Slicing and concatenation memory mechanics

```python
list_a = [10, 20, 30]
list_b = [40, 50]
combined = list_a + list_b      # Creates new list at 0x500: [10, 20, 30, 40, 50]
combined_slice = combined[1:4]  # Creates new list at 0x600: [20, 30, 40]
combined = 0                    # Rebinds 'combined' to int 0
```

Does `0x500` stay in memory because `combined_slice` was sliced from it? No.
* Slicing a list (`combined[1:4]`) allocates a new list container (`0x600`) and copies the element references (`20`, `30`, `40`) into it.
* `combined_slice` does not reference the `0x500` list container.
* When `combined = 0` runs, the reference count on `0x500` hits zero and the container is garbage collected. The integer objects `20`, `30`, and `40` remain alive because `list_a`, `list_b`, and `combined_slice` still reference them.

## 5. Sets, dictionaries, and hashability

Both `set` and `dict` are backed by hash tables, giving $\mathcal{O}(1)$ average lookup compared to $\mathcal{O}(n)$ linear scan for a `list`.

To store an item in a `set` or use it as a `dict` key, Python computes `hash(item)`:
* An object is **hashable** if its value cannot change during its lifetime.
* Immutable types (`int`, `float`, `str`, `bool`) are hashable.
* Mutable containers (`list`, `set`, `dict`) are unhashable and raise `TypeError: unhashable type`.
* A `tuple` is hashable **only if every element inside it is also hashable**.

```python
s1 = {1, 2, (3, 4)}        # Valid: tuple contains only immutable ints
s2 = {1, 2, (3, [4, 5])}   # TypeError: unhashable type: 'list'
```

If `(3, [4, 5])` were allowed in a set, mutating the inner list would change the tuple's contents after insertion and leave it in the wrong hash bucket.

## 6. Common Python syntax traps

| Snippet | Output / behavior | Explanation |
|---|---|---|
| `3 // 2` vs `-3 // 2` | `1` vs `-2` | `//` is floor division (rounds toward $-\infty$, so `-1.5` floors to `-2`). |
| `x = (45)` | `int` (`45`) | Parentheses without a trailing comma are mathematical grouping. |
| `x = (45,)` or `x = 45,` | `tuple` (`(45,)`) | The comma creates the tuple, not the parentheses. |
| `x = {}` vs `y = {1}` | `dict` vs `set` | `{}` creates an empty `dict`. Use `set()` for an empty set. |
| `a, *mid, b = (1, 2, 3, 4)` | `mid` is `[2, 3]` (`list`) | Starred unpacking `*mid` always produces a `list`, even when unpacking a tuple or string. |
| `nums.reverse()` vs `nums[::-1]` | `None` (in-place) vs new `list` | `.reverse()` mutates in place ($\mathcal{O}(1)$ space) and returns `None`. `[::-1]` allocates a reversed copy ($\mathcal{O}(n)$ space). |
| `nums.remove(3)` | Removes first `3` only | Scans left-to-right ($\mathcal{O}(n)$), removes the first match, and raises `ValueError` if not found. |
| `s = {1, (9, 2)}; 9 in s` | `False` (`(9, 2) in s` is `True`) | Set membership checks top-level elements only and does not recurse into nested tuples. |
| `d["c"]` vs `d.get("c")` | `KeyError` vs `None` | `d.get("c", default)` returns `None` (or `default`) when the key is missing. |
| `dict(zip(["a", "b"], [1, 2, 3]))` | `{"a": 1, "b": 2}` | `zip()` stops at the shortest iterable (`3` is ignored). Pass `strict=True` in Python 3.10+ to raise `ValueError` on length mismatch. |
