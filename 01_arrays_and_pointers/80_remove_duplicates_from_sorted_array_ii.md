# ✂️ 80. Remove Duplicates from Sorted Array II

> **Difficulty:** Medium ⭐  
> **Pattern:** Two Pointers — **Formation B: Scout & Writer (Fast & Slow with Streak Counter)**  
> **Complexity:** $\mathcal{O}(n)$ Time, $\mathcal{O}(1)$ Auxiliary Space in-place.

---

## 🏆 1. Celebration First: You Solved a LeetCode Medium!

Less than an hour ago, you said: *"Remember I'm a poor coder. I struggle with DSA."*

Look at what you just wrote:
```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 1
        tmp = 1
        for i in range(1, len(nums)):
            if nums[i] == nums[i-1] and tmp < 2:
                tmp += 1
                nums[k] = nums[i]
                k += 1
            elif nums[i] != nums[i-1]:
                nums[k] = nums[i]
                k += 1
                tmp = 1
        return k
```

### Why this is a huge achievement:
1. **It's a Medium problem** that trips up candidates with messy nested loops.
2. **It runs in $\mathcal{O}(n)$ time and strictly $\mathcal{O}(1)$ space.**
3. **Your logic is clean and structured:** You tracked state (`tmp`) and combined it with the **Scout & Writer** pointer choreography.

Be proud of this. This is real problem-solving progress!

---

## 💡 2. How Your Logic Works (The 3-Branch State Machine)

You treated the problem as a clean **consecutive streak tracker**:

```text
nums = [ 1 , 1 , 1 , 2 , 2 , 3 ]
         ▲
       k, tmp = 1
```

On every iteration of Scout `i`:
1. **Case A (Neighbor is equal, streak < 2):**  
   It's the second copy! Increment streak counter (`tmp += 1`), write `nums[k] = nums[i]`, advance `k`.
2. **Case B (Neighbor is different):**  
   Brand new number! Reset streak (`tmp = 1`), write `nums[k] = nums[i]`, advance `k`.
3. **Case C (Neighbor is equal, but streak >= 2):**  
   It's a 3rd+ unwanted duplicate! **Do nothing!** The Scout skips ahead without advancing Writer `k`.

---

## 🎬 3. Visual Step-by-Step Trace

Let `nums = [ 1 , 1 , 1 , 2 , 2 , 3 ]`:

```text
Initial:
k = 1, tmp = 1, nums[0] is settled as 1.

i = 1: nums[1] (1) == nums[0] (1) and tmp (1) < 2
       tmp -> 2. Write nums[1] = 1, k -> 2.
nums = [ 1 , 1 , 1 , 2 , 2 , 3 ]
                 ▲
                 k, i

i = 2: nums[2] (1) == nums[1] (1), but tmp is 2 (NOT < 2)!
       SKIP! (k stays at 2).
nums = [ 1 , 1 , 1 , 2 , 2 , 3 ]
                 ▲   ▲
                 k   i

i = 3: nums[3] (2) != nums[2] (1). NEW NUMBER!
       tmp -> 1. Write nums[2] = 2, k -> 3.
nums = [ 1 , 1 , 2 , 2 , 2 , 3 ]
                     ▲   ▲
                     k   i

i = 4: nums[4] (2) == nums[3] (2) and tmp (1) < 2
       tmp -> 2. Write nums[3] = 2, k -> 4.
nums = [ 1 , 1 , 2 , 2 , 2 , 3 ]
                         ▲   ▲
                         k   i

i = 5: nums[5] (3) != nums[4] (2). NEW NUMBER!
       tmp -> 1. Write nums[4] = 3, k -> 5.
nums = [ 1 , 1 , 2 , 2 , 3 , 3 ]
                             ▲
                             k = 5 (Done!)
```
Valid prefix length: **5**, values: `[ 1 , 1 , 2 , 2 , 3 ]` ✅

---

## 🚀 4. The Senior Follow-Up: The "Lookback $M$" Generalization

In a FAANG interview, once you present your working solution, the interviewer will often ask:
> *"What if at most 3 duplicates are allowed? What if at most M duplicates are allowed? Can you write a generalized solution without tracking a streak variable?"*

### 💡 The Senior Insight:
Instead of looking at the *input* neighbors (`nums[i] == nums[i - 1]`), look at what has **already been written** at `nums[k - M]`!

Because the array is sorted:
* If the incoming number `x` is the same as `nums[k - 2]`, writing it would create **3 identical numbers in a row**!
* If `x > nums[k - 2]`, it is **guaranteed safe to write**!

```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 0
        for x in nums:
            # Safe to write if we haven't written 2 items yet,
            # OR if x is strictly different from the item written 2 spots ago!
            if k < 2 or x != nums[k - 2]:
                nums[k] = x
                k += 1
        return k
```

### 🤯 Notice the Universal Formula:
* **Allow at most 1 duplicate ([LC 26](file:///Users/sathyat/Developer/projects/dsa/26_remove_duplicates_from_sorted_array.md)):** `if k < 1 or x != nums[k - 1]:`
* **Allow at most 2 duplicates ([LC 80](file:///Users/sathyat/Developer/projects/dsa/80_remove_duplicates_from_sorted_array_ii.md)):** `if k < 2 or x != nums[k - 2]:`
* **Allow at most $M$ duplicates:** `if k < M or x != nums[k - M]:`

---

## 📊 5. Complexity Analysis

| Metric | Your Streak Counter Solution | Lookback $M$ Solution |
| :--- | :---: | :---: |
| **Time Complexity** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ |
| **Auxiliary Space** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| **Lines of Code** | ~13 lines | **5 lines** |
| **Generalizability** | Needs adapting `tmp` thresholds | Single variable change (`k < M`, `nums[k - M]`) |

Both solutions are **100% optimal $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space**. Your intuitive solution is practical and got you the green "Accepted"!
