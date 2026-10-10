# ✂️ 27. Remove Element

> **Difficulty:** Easy  
> **Pattern:** Two Pointers — **Formation B: Scout & Writer (Fast & Slow Pointers)**  
> **Complexity:** $\mathcal{O}(n)$ Time, $\mathcal{O}(1)$ Auxiliary Space in-place.

---

## 🎯 1. Is Your Solution Good?

**YES! It is the textbook, 100% optimal FAANG solution.**

```python
class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k
```

### Why this is top-tier:
1. **$\mathcal{O}(n)$ Single Pass:** Visits every element exactly once.
2. **$\mathcal{O}(1)$ Auxiliary Space:** Modifies the array in-place without allocating a second list.
3. **Preserves Relative Order:** Although the problem says *"the order of the elements may be changed"*, this solution naturally keeps elements in their original relative sequence.

---

## 💡 2. The Mental Model: Scout & Writer

You intuitively applied **Formation B (Scout & Writer)**:

```text
                  Scout (i) -> sprints ahead to inspect every item
                  ▼
nums = [ 0 , 1 ,  2 ,  2 ,  3 ,  0 ,  4 ,  2 ],  val = 2
         ▲
         Writer (k) -> marks the boundary where the next VALID element belongs
```

### The Two Roles:
* **`i` (The Scout / Fast):** Sprints through the entire array. It inspects every element and asks: *"Is this number NOT equal to `val`?"*
* **`k` (The Writer / Slow):** Stands at the boundary of the **"clean zone"**. Whenever the Scout finds a valid number, the Writer copies it to `nums[k]` and takes one step forward (`k += 1`).

### 📐 The Array Partition Invariant:
At any point during the loop, the array is cleanly partitioned into two zones:
```text
┌───────────────────────────┬──────────────────────────────────┐
│   Clean Valid Elements    │    Trash / Ignored / Unexplored  │
│   (Indices 0 to k - 1)    │    (Indices k to len - 1)        │
└───────────────────────────┴──────────────────────────────────┘
```
When the loop finishes, **`k` is literally the count of valid elements**! Returning `k` is instant.

---

## 🎬 3. Visual Step-by-Step Trace

Let `nums = [ 3 , 2 , 2 , 3 ]`, `val = 3`:

```text
Start:
k = 0, i = 0: nums[0] is 3 (matches val). Skip!
nums = [ 3 , 2 , 2 , 3 ]
         ▲
        k, i

Step 1:
k = 0, i = 1: nums[1] is 2 (!= val). Write nums[0] = 2, k -> 1.
nums = [ 2 , 2 , 2 , 3 ]
             ▲
             k, i

Step 2:
k = 1, i = 2: nums[2] is 2 (!= val). Write nums[1] = 2, k -> 2.
nums = [ 2 , 2 , 2 , 3 ]
                 ▲
                 k, i

Step 3:
k = 2, i = 3: nums[3] is 3 (matches val). Skip!
Loop finishes.

Return k = 2.
The first 2 elements are [ 2 , 2 ] ✅
```

---

## 👯 4. The Family Resemblance: Notice the Pattern!

Notice how this exact same **Scout & Writer** template solves multiple classic problems with just a 1-line condition change:

| Problem | Condition to Keep Element | What Writer Does |
| :--- | :--- | :--- |
| **LC 27: Remove Element** | `if nums[i] != val:` | `nums[k] = nums[i]; k += 1` |
| **LC 283: Move Zeroes** | `if nums[i] != 0:` | `nums[k] = nums[i]; k += 1` *(fill tail with 0s)* |
| **LC 26: Remove Duplicates (Sorted)** | `if nums[i] != nums[k - 1]:` | `nums[k] = nums[i]; k += 1` |

Once you master this template, you've solved 3 different interview problems with the same muscle memory!

---

## 🧠 5. The Senior Follow-Up: What if `val` is Rare?

Interviewers love to ask:
> *"What if `nums` has 100,000 elements, but only 2 of them equal `val`? Your code will still execute `nums[k] = nums[i]` 99,998 times! Can you optimize the number of writes?"*

### 💡 The Alternative: Two Pointers Squeeze (Swap with Tail)
Because the problem states that **order does not matter**, we can swap the unwanted element with the **last** element and shrink the array size:

```python
class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        i = 0
        n = len(nums)
        
        while i < n:
            if nums[i] == val:
                nums[i] = nums[n - 1]  # Overwrite with last element
                n -= 1                 # Shrink array boundary
            else:
                i += 1                 # Only advance if current element is valid!
                
        return n
```

* **Why this is clever:** If `nums = [1, 2, 3, 5, 4]`, `val = 4`, we do only **1 assignment** instead of 4!
* **Trade-off:** It scrambles the original relative order of elements, which is fine for LC 27.

---

## 📊 6. Complexity Analysis

| Metric | Scout & Writer (Your Solution) | Swap with Tail (Alternative) |
| :--- | :---: | :---: |
| **Time Complexity** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ (fewer write operations) |
| **Space Complexity** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Preserves Order?** | ✅ Yes | ❌ No |
| **Interview Recommendation** | **Primary Choice (Clean & Standard)** | **Mention as Follow-up Optimization** |
