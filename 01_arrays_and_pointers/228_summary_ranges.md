# 📊 LeetCode 228: Summary Ranges – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** Top Interview 150 / Arrays & Strings  
> **Pattern:** Two Pointers Formation D: Anchor & Scout (Interval Chunking)  
> **LeetCode Link:** [LeetCode 228: Summary Ranges](https://leetcode.com/problems/summary-ranges/)

---

## 📌 Problem in Plain English

You are given a **sorted unique** integer array `nums`.

A range `[a, b]` is the set of all integers from `a` to `b`, inclusive. Return the smallest sorted list of ranges that cover all the numbers in the array exactly:
* Each element of `nums` is covered by exactly one range.
* There is no integer `x` such that `x` is in one of the ranges but not in `nums`.
* Format: `"a->b"` if `a != b`, or `"a"` if `a == b`.

```text
Example 1:
Input:  nums = [0, 1, 2, 4, 5, 7]
Output: ["0->2", "4->5", "7"]

Example 2:
Input:  nums = [0, 2, 3, 4, 6, 8, 9]
Output: ["0", "2->4", "6", "8->9"]
```

---

## 🎒 The "Aha!" Mental Model: The Anchor & Scout

Why did your initial `for` loop feel awkward? Because in a traditional `for i in range(len(nums)):`:
* You detect the break on the **next** number (`nums[i] - nums[i-1] != 1`).
* This causes an **off-by-one trap** on where the range ended (`nums[i-1]` vs `nums[i]`).
* More importantly: **the final range disappears!** When the loop reaches the end of the array, there is no next number to trigger the `else` block, leaving the last range un-appended.

### ⚓ The Fix: Anchor & Scout
Instead of checking backwards, look forward with an **inner `while` loop**:

```text
nums = [ 0 ,  1 ,  2 ,  4 ,  5 ,  7 ]

Round 1:
  Anchor drops at index 0:  start = nums[0] (0)
  Scout sprints forward:    0 -> 1 -> 2
  Scout stops at 2 (since next number 4 != 2 + 1)
  
  📝 Record: "0->2"
  Advance to index 3!

Round 2:
  Anchor drops at index 3:  start = nums[3] (4)
  Scout sprints forward:    4 -> 5
  Scout stops at 5 (since next number 7 != 5 + 1)
  
  📝 Record: "4->5"
  Advance to index 5!

Round 3:
  Anchor drops at index 5:  start = nums[5] (7)
  Scout looks ahead:        No more numbers!
  
  📝 Record: "7" (since start == nums[i])
```

---

## 💻 Clean Production Code

```python
class Solution:
    def summaryRanges(self, nums: list[int]) -> list[str]:
        res = []
        i = 0
        n = len(nums)

        while i < n:
            start = nums[i]

            # Fast-forward i as long as the sequence is consecutive
            while i + 1 < n and nums[i + 1] == nums[i] + 1:
                i += 1

            # Format single numbers vs ranges
            if start == nums[i]:
                res.append(str(start))
            else:
                res.append(f"{start}->{nums[i]}")

            # Move to the start of the next run
            i += 1

        return res
```

---

## 🔬 Why This Pattern Beats the Single `for` Loop

| Feature | Single `for` Loop with `if/else` | Two Pointers `while` Loop (Anchor & Scout) |
| :--- | :--- | :--- |
| **Handling the Last Range** | ❌ Lost! Must copy-paste append logic after loop | ✅ Automatically processed on the final iteration |
| **Off-by-One Traps** | ⚠️ High (is it `nums[i]` or `nums[i-1]`?) | ✅ Zero (when inner loop terminates, `nums[i]` is the exact end) |
| **Empty Array `[]`** | Needs explicit `if not nums: return []` check | ✅ `0 < 0` is false, returns `[]` automatically |
| **Time Complexity** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ (pointer `i` only moves forward) |
| **Space Complexity** | $\mathcal{O}(1)$ auxiliary memory | $\mathcal{O}(1)$ auxiliary memory |

---

## 🎯 Related Benchmark Problems
This exact **Anchor & Scout** pattern solves:
1. **LC 443: String Compression** (Count runs of `['a', 'a', 'a', 'b', 'b']`).
2. **LC 56: Merge Intervals** (Group contiguous overlapping time blocks).
3. **LC 1869: Longer Contiguous Segments of Ones than Zeros**.
