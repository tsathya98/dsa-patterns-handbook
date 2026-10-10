# 🔄 189. Rotate Array

> **Difficulty:** Medium ⭐  
> **Pattern:** Two Pointers — **Formation A: The Squeeze (The Triple Reversal Algorithm)**  
> **Constraints:** $\mathcal{O}(n)$ Time, strictly $\mathcal{O}(1)$ Auxiliary Space in-place.

---

## 🔍 1. Analysis of Your Solution

Your solution:
```python
class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        k %= len(nums)
        nums[:] = nums[len(nums) - k:] + nums[:len(nums) - k]
```

### ✅ What You Did Great:
1. **Handled the Modulo Edge Case:**  
   `k %= len(nums)` is mandatory. If $k = 10$ and $n = 4$, rotating 10 times is identical to rotating $10 \pmod 4 = 2$ times. Many candidates crash on $k > n$ because they forget this!
2. **Proper In-Place Replacement (`nums[:] = ...`):**  
   You correctly used `nums[:] = ...` instead of `nums = ...`. Writing `nums = ...` only rebinds a local variable, leaving the caller's original list unmutated. `nums[:]` modifies the memory buffer in-place!
3. **High LeetCode Percentile:** Beats **82.92%** on runtime!

---

## ⚠️ 2. The Big Interview Catch: The Space Constraint

Look at the **Follow-up** on the LeetCode problem description:
> *"Could you solve it in-place with $\mathcal{O}(1)$ extra space?"*

### Why Slicing Fails the Follow-Up:
Under the hood in Python:
* `nums[len(nums) - k:]` creates a **brand new list** of size $k$.
* `nums[:len(nums) - k]` creates a **second brand new list** of size $n - k$.
* The `+` operator creates a **third brand new list** of size $n$.

Total memory allocated behind the scenes: **$\mathcal{O}(n)$ extra space**!

If an interviewer asks:
> *"What if `nums` is a 10 GB file on disk and your machine only has 100 MB of RAM? You cannot allocate slices. Can you rotate it in strictly $\mathcal{O}(1)$ space?"*

---

## 💡 3. The FAANG $\mathcal{O}(1)$ Superweapon: The Triple Reversal Algorithm

Look at the structure of the array:
```text
nums = [ 1 , 2 , 3 , 4 ,   5 , 6 , 7 ],  k = 3
         └───────────┘     └───────┘
            Part A          Part B
```
When rotated to the right by $k = 3$, the target result is:
```text
target = [ 5 , 6 , 7 ,   1 , 2 , 3 , 4 ]
           └───────┘     └───────────┘
            Part B          Part A
```
Notice what happened: **Part B moved to the front, and Part A moved to the back!**

### 🎩 The 3-Step Reversal Magic:

#### Step 1: Reverse the ENTIRE array (`0` to `n - 1`)
```text
[ 7 , 6 , 5 ,   4 , 3 , 2 , 1 ]
 └───────┘     └───────────┘
(Part B front,  Part A back — but both are inside-out!)
```

#### Step 2: Reverse the first $k$ elements (`0` to `k - 1`)
Flip `[ 7 , 6 , 5 ]` back to normal:
```text
[ 5 , 6 , 7 ,   4 , 3 , 2 , 1 ]
 └───────┘
  Part B is now in perfect order!
```

#### Step 3: Reverse the remaining $n - k$ elements (`k` to `n - 1`)
Flip `[ 4 , 3 , 2 , 1 ]` back to normal:
```text
[ 5 , 6 , 7 ,   1 , 2 , 3 , 4 ]  ✅ PERFECTLY ROTATED IN O(1) SPACE!
```

---

## 💻 4. Python Implementation (Two Pointers Squeeze)

Reversing a subsegment in-place is just our standard **Two Pointers Squeeze (`start < end`)**:

```python
class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k %= n

        # Helper: Two Pointers Squeeze to reverse a slice in-place
        def reverse_sub(start: int, end: int) -> None:
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1

        # 1. Reverse the entire array
        reverse_sub(0, n - 1)
        # 2. Reverse first k elements
        reverse_sub(0, k - 1)
        # 3. Reverse the remaining n - k elements
        reverse_sub(k, n - 1)
```

---

## 📊 5. Comparison: Your Slice Solution vs. Triple Reversal

| Metric | Your Slicing Solution | Triple Reversal (Two Pointers) |
| :--- | :---: | :---: |
| **Time Complexity** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ |
| **Auxiliary Space** | **$\mathcal{O}(n)$** (allocates new slices) | **$\mathcal{O}(1)$** (pure in-place swaps) |
| **Code Length** | 2 lines | 12 lines |
| **Interview Verdict** | Great starter (shows Python fluency) | **Required for the follow-up question** |

### 🎯 Interview Recommendation:
In an interview:
1. First, state the slicing approach: *"In Python, we can do this in $\mathcal{O}(n)$ time using slice replacement."*
2. Then proactively add: *"However, slicing allocates $\mathcal{O}(n)$ auxiliary memory. To solve it in strictly $\mathcal{O}(1)$ space, we can use the **Triple Reversal** algorithm with Two Pointers."*

This demonstrates both practical Python productivity AND deep algorithmic mastery!
