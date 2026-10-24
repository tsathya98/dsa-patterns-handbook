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

---

## 2. The House and Keys Mental Model (Mutation vs. Reassignment)

When two variables point to the same list (`lista = listb`), beginners often ask: *"If they share memory, why didn't `lista` change when I wrote `listb = [7, 8, 9]`?"*

The confusion comes from the English word "change". In Python, **modifying what is inside a container** is completely different from **reassigning a variable name to a new container**.

### The Analogy

Imagine a physical house at **123 Main Street**.
Inside the house is furniture: `[1, 2, 3]`.
* Key A is labeled `lista`.
* Key B is labeled `listb`.
Both keys unlock the **exact same house** at 123 Main Street.

```text
Key lista ────┐
              ▼
Key listb ───► [ 123 Main Street: [1, 2, 3] ]
```

### Scenario 1: Changing the furniture (Mutation)
You use key `listb` to walk inside 123 Main Street and add a chair:
```python
listb.append(99)
# or: listb[0] = 42
```
When your roommate unlocks 123 Main Street using key `lista`, do they see the change?
**Yes.** Because you both share the exact same house.
```python
print(lista)  # [42, 2, 3, 99]
```

### Scenario 2: Moving to a new house (Reassignment)
Now you buy a brand new house at **456 Elm Street** and get a new key for it:
```python
listb = [7, 8, 9]  # Reassignment (NO [:] used)
```
Did anything happen to the old house at 123 Main Street? **No.**
Did your roommate move? **No.**
Key `lista` is still in the lock at 123 Main Street.
```text
Key lista ───► [ 123 Main Street: [1, 2, 3] ]
Key listb ───► [ 456 Elm Street:  [7, 8, 9] ]
```
```python
print(listb)  # [7, 8, 9] (your new house)
print(lista)  # [1, 2, 3] (roommate is still at the old house)
```

---

## 3. The 2D List Multiplication Trap (`[[0] * C] * R`)

Why is `[0] * 5` completely safe, but `[[0] * 3] * 3` corrupts your matrix?

### Integers are immutable, lists are mutable
* In `[0] * 5`, the elements are numbers (`0`). You cannot mutate the number `0` in place. Writing `arr[0] = 99` unplugs index 0 from `0` and points it to `99`. The other slots remain untouched.
* In `[[0] * 3] * 3`, the outer `* 3` duplicates the **pointer** to the exact same inner list 3 times:

```text
Row 0 ────┐
Row 1 ────┼───► Address 0x900: [ 0, 0, 0 ]  (Single shared list in RAM)
Row 2 ────┘
```

When you write `grid[0][0] = 99`, you dereference Row 0 and mutate that shared list. All 3 rows immediately reflect the change because `grid[0] is grid[1]` is `True`.

### The Fix: List Comprehension
```python
# Creates R distinct lists in RAM with unique memory addresses:
grid = [[0 for _ in range(C)] for _ in range(R)]
```

---

## 4. Low-level arrays vs. Python `list`

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

## 5. Mutable objects inside an immutable tuple

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

### Decision rules:
* **1. In-place mutation check:** If an operation modifies the mutable object in place (e.g. `t[2].append(300)`), the pointer address stored in the tuple slot remains identical (`0x999`), allowing the change to succeed.
* **2. Reassignment check:** If an operation assigns a new object to a tuple index (e.g. `t[2] = [100, 200, 300]`), Python attempts to rebind the slot address to a new pointer (`0x888`), which immediately raises `TypeError`.
* **3. Augmented assignment gotcha:** When running augmented assignment like `t[2] += [300]`, the mutable object mutates in place first, but the subsequent reference rebinding back to the tuple slot fails with `TypeError`.


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

## 6. Slicing (`copy`) vs. Slice Assignment (`in-place`)

Which side of the equals sign (`=`) the slice sits on determines the memory behavior:

### Right-hand side: `lista = listb[:]` (New Object Copy)
A slice on the right-hand side creates a **shallow copy**. It allocates a brand new list in memory and copies the references over.
```python
listb = [1, 2, 3]
lista = listb[:]  # Brand new list in memory
listb.append(99)
print(lista)      # [1, 2, 3] (untouched!)
```

### Left-hand side: `listb[:] = [7, 8, 9]` (In-Place Overwrite)
A slice on the left-hand side is **slice assignment**. It empties out the existing list in-place and fills it with new elements **without changing its memory address**:
```python
listb = [1, 2, 3]
lista = listb
listb[:] = [7, 8, 9]  # Modifies in-place!
print(lista)          # [7, 8, 9] (both variables see the change!)
```

## 7. Slicing and concatenation memory mechanics

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

## 8. Sets, dictionaries, and hashability

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

## 9. Common Python syntax traps

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
