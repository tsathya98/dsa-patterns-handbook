# 🧠 Python Memory Model, Pointers & Core Collections

> **Context:** Airtribe DSA Foundations — Python Under the Hood  
> **Goal:** Understand how Python actually stores variables, pointers, lists, tuples, sets, and dicts in RAM so tricky edge cases become obvious.

---

## 1. Variables Are Name Tags (Pointers), Not Boxes

In C/C++, a variable like `int x = 10` is a physical box in memory holding `10`.  
In Python, **everything is an object on the heap**, and a variable is just a **sticky note (reference/pointer)** pointing to a memory address.

```text
name = "Ashish"          name = "Arushi" (Reassignment)
───────────────          ──────────────────────────────
[ name ] ──► 0x100 ("Ashish")     [ name ] ──────┐
                                                 ▼
                         0x100 ("Ashish")      0x200 ("Arushi")
                         (0 refs -> GC 🗑️)     (1 ref -> Alive ✅)
```

* Strings, integers, and tuples are **immutable**: you never overwrite `"Ashish"` in-place.
* Reassigning `name = "Arushi"` allocates a brand-new string at `0x200` and moves the `name` sticky note.
* Once `0x100 ("Ashish")` has **zero references** pointing to it, Python's **Garbage Collector (GC)** reclaims that memory.

---

## 2. Low-Level Arrays vs. Python `list`

| Feature | Low-Level Array (C / `array` module) | Python `list` (`[1, "hi", 3.5]`) |
|---|---|---|
| **Data Types** | **Homogeneous** (all elements must be the exact same type, e.g., 32-bit `int`). | **Heterogeneous** (can mix `int`, `str`, `list`, etc.). |
| **Memory Layout** | **Contiguous raw values** packed back-to-back in RAM. | **Contiguous array of pointers (references)** pointing to scattered objects in RAM. |
| **Index Lookup `a[i]`** | $\mathcal{O}(1)$ (`base_address + i * sizeof(type)`) | $\mathcal{O}(1)$ (`base_address + i * 8 bytes` $\to$ follow pointer) |

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

---

## 3. The #1 Trap: Mutable Objects Inside an Immutable Tuple

> **Why did `t = (1, 2, [3, 4]); t[2].append(5)` work if tuples are immutable?!**

Because **tuple immutability only locks the pointer addresses stored in the tuple's slots**—it does **not** freeze the objects those pointers point to!

```text
t = (1, 2, [100, 200])

Tuple t (Immutable Slots):
┌─────────┬─────────┬─────────┐
│ Slot 0  │ Slot 1  │ Slot 2  │
│  0x001  │  0x002  │  0x999  │  ◄── Slot 2 is locked to address 0x999 forever!
└────┬────┴────┬────┴────┬────┘
     ▼         ▼         ▼
    (1)       (2)     0x999: [ 100, 200 ]  (Mutable List Object)
```

### Case A: `t[2].append(300)` (✅ WORKS)
* You follow pointer `0x999` to the list object and mutate its internal array: `[100, 200, 300]`.
* What is stored inside Tuple `Slot 2`? **Still `0x999`!**
* Since the tuple's slot address never changed, Python allows it.
* Same rule applies to a **Set** or **Dict** inside a tuple:
  * `t = (1, {10, 20}); t[1].add(30)` $\to$ ✅ **Works**
  * `t = (1, {"a": 1}); t[1]["b"] = 2` $\to$ ✅ **Works**

### Case B: `t[2] = [100, 200, 300]` (❌ `TypeError`)
* Writing `[100, 200, 300]` creates a **brand-new list** at a new address (say `0x888`).
* `t[2] = ...` tries to overwrite `Slot 2` from `0x999` to `0x888`.
* Tuple slots are locked $\to$ `TypeError: 'tuple' object does not support item assignment`.

### Bonus Edge Case: `t[2] += [300]` (🤯 Throws `TypeError` AND Mutates!)
* `+=` on a list calls `list.__iadd__` (which mutates `0x999` in-place first!) and then tries to reassign `t[2] = result` (which raises `TypeError`). Result: it throws `TypeError`, **and** the list inside `t[2]` is still modified! Never do this in production.

---

## 4. Slicing & Concatenation Memory Mechanics

```python
list_a = [10, 20, 30]
list_b = [40, 50]
combined = list_a + list_b      # Creates NEW list at 0x500: [10, 20, 30, 40, 50]
combined_slice = combined[1:4]  # Creates NEW list at 0x600: [20, 30, 40]
combined = 0                    # Moves 'combined' tag to int 0
```

* **Does `0x500` stay in memory because `combined_slice` sliced it?** **NO!**
* In Python, slicing a list (`combined[1:4]`) allocates a **brand-new list container** (`0x600`) that copies the **pointers** to `20`, `30`, and `40`.
* `combined_slice` does **not** point to the `combined` list container (`0x500`).
* As soon as `combined = 0` runs, nothing points to `0x500`, so the `0x500` list container is **immediately garbage collected** (while the integers `20, 30, 40` stay alive because both `list_a`/`list_b` and `combined_slice` still point to them).

---

## 5. Sets, Dictionaries & The Hashability Rule

Both `set` and `dict` use a **Hash Table** under the hood ($\mathcal{O}(1)$ average lookup, vs $\mathcal{O}(n)$ linear scan for `list`).

To put an item into a `set` (or use it as a `dict` key), Python runs `hash(item)`.
* **Rule:** An object is **hashable** only if its value can **never change** during its lifetime.
* Immutable primitives (`int`, `float`, `str`, `bool`) $\to$ **Hashable ✅**
* Mutable containers (`list`, `set`, `dict`) $\to$ **Unhashable ❌** (`TypeError: unhashable type`)
* **What about `tuple`?** A tuple is hashable **ONLY IF every single item inside it is also hashable!**

```python
s1 = {1, 2, (3, 4)}        # ✅ Valid! Tuple contains only ints (immutable)
s2 = {1, 2, (3, [4, 5])}   # ❌ TypeError: unhashable type: 'list'!
```

> **Why can't `(3, [4, 5])` go in a set?** Because as we saw in Section 3, you could mutate `[4, 5].append(6)` in-place, which would change the tuple's hash while it's already sitting in a hash bucket—corrupting the hash table!

---

## 6. Classic Python Syntax Gotchas (From Quiz)

| Snippet | Output / Behavior | Why? |
|---|---|---|
| `3 // 2` vs `-3 // 2` | `1` vs `-2` | `//` is **floor division** (rounds down toward $-\infty$, so `-1.5` floors to `-2`). |
| `x = (45)` | `int` (`45`) | Parentheses without a comma are just math grouping! |
| `x = (45,)` or `x = 45,` | `tuple` (`(45,)`) | **The comma makes the tuple**, not the parentheses. |
| `x = {}` vs `y = {1}` | `dict` vs `set` | Empty `{}` is always an empty `dict`. Use `set()` for an empty set. |
| `a, *mid, b = (1, 2, 3, 4)` | `mid` is `[2, 3]` (`list`) | Starred unpacking `*mid` **always returns a `list`**, even when unpacking a tuple or string! |
| `nums.reverse()` vs `nums[::-1]` | `None` (in-place) vs new `list` | `.reverse()` mutates in-place ($\mathcal{O}(1)$ space). `[::-1]` allocates a new reversed copy ($\mathcal{O}(n)$ space). |
| `nums.remove(3)` | Removes **first** `3` only | Scans left-to-right ($\mathcal{O}(n)$), removes the first exact match, raises `ValueError` if missing. |
| `s = {1, (9, 2)}; 9 in s` | `False` (`(9, 2) in s` is `True`) | Set membership checks top-level elements only; it never searches inside nested tuples. |
| `d["c"]` vs `d.get("c")` | `KeyError` vs `None` | `d.get("c", default)` safely returns `None` (or `default`) without crashing. |
| `dict(zip(["a", "b"], [1, 2, 3]))` | `{"a": 1, "b": 2}` | `zip()` stops silently at the **shortest** iterable (`3` is ignored). Use `zip(..., strict=True)` in Python 3.10+ to raise `ValueError`. |
