# 🏃 LeetCode 283: Move Zeroes – Master Guide

> **Difficulty:** Easy  
> **Study Plan:** LeetCode 75 / Top Interview 150  
> **Pattern:** Two Pointers (Formation B: Scout & Writer / Fast & Slow)  
> **LeetCode Link:** [LeetCode 283: Move Zeroes](https://leetcode.com/problems/move-zeroes/)

---

## 📌 Problem in Plain English

Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.

**Constraint:** You must do this **in-place** without making a copy of the array ($\mathcal{O}(1)$ extra space).

### Example:
```text
Input: nums = [0, 1, 0, 3, 12]
Output: [1, 3, 12, 0, 0]
```

---

## 💡 The "Aha!" Moment: The Two Pointers Scout & Writer

Instead of shifting elements repeatedly ($\mathcal{O}(n^2)$), use **two pointers** moving in the same direction:

* **`fast` (The Scout):** Scans through every index hunting for non-zero numbers.
* **`slow` (The Writer):** Points to the exact spot where the **next non-zero number belongs** (which is also the front of the "Wall of Zeros").

---

## 🚜 The "Snowplow / Wall of Zeros" Visual Diagram

Think of the array as partitioned into three distinct zones:
```text
[ Non-Zeros (Done!) ] | [ Wall of 0s ] | [ Unexplored Elements ... ]
                      ▲                ▲
                    slow              fast
```

### 🎬 Visual Step-by-Step Trace on `nums = [0, 1, 0, 0, 3, 12]`

#### 📍 START:
```text
Indices:     0       1       2       3       4       5
          ┌─────┬───────┬───────┬───────┬───────┬────────┐
Array:    │  0  │   1   │   0   │   0   │   3   │   12   │
          └─────┴───────┴───────┴───────┴───────┴────────┘
             ▲
        slow = 0
        fast = 0
```
* `nums[fast] == 0` $\implies$ Ignore! `slow` stays parked at index 0. `fast` steps ahead.

---

#### 📍 STEP 1: `fast` finds `1` (First Swap!)
```text
Indices:     0       1       2       3       4       5
          ┌─────┬───────┬───────┬───────┬───────┬────────┐
Array:    │  0  │   1   │   0   │   0   │   3   │   12   │
          └─────┴───────┴───────┴───────┴───────┴────────┘
             ▲       ▲
           slow     fast
             │       │
             └──Swap─┘
```
**After Swap & `slow += 1`:**
```text
          ┌─────┐ ┌──────────────────────────────────────┐
Array:    │  1  │ │   0   │   0   │   0   │   3   │  12  │
          └─────┘ └──────────────────────────────────────┘
          [Done!]     ▲
                    slow=1
```
* Index `0` is locked in! `slow` moves to index `1` (which now holds a `0`).

---

#### 📍 STEPS 2 & 3: Consecutive Zeros Accumulate (The Wall Grows!)
`fast` scans index `2` and index `3`. Both are `0`.  
`slow` stays parked at index `1`.

```text
Indices:     0       1       2       3       4       5
          ┌─────┐ ┌───────────────┐
Array:    │  1  │ │   0   │   0   │   0   │   3   │   12   │
          └─────┘ └───────────────┘
          [Done!]  [ Wall of 0s  ]
                     ▲                ▲
                   slow=1           fast=3
```
* Notice how the **Wall of Zeros** is naturally bunching up between `slow` and `fast`!

---

#### 📍 STEP 4: `fast` finds `3` (Second Swap!)
`fast` arrives at index `4` and spots `3`!

```text
Indices:     0       1       2       3       4       5
          ┌─────┐ ┌───────────────┐
Array:    │  1  │ │   0   │   0   │   0   │   3   │   12   │
          └─────┘ └───────────────┘
                     ▲                        ▲
                    slow                     fast
                     │                         │
                     └──────────Swap───────────┘
```
**After Swap & `slow += 1`:**
```text
Indices:     0       1       2       3       4       5
          ┌─────────────┐ ┌───────────────┐
Array:    │  1  │   3   │ │   0   │   0   │   0   │   12   │
          └─────────────┘ └───────────────┘
          [    Done!    ]  [ Wall of 0s  ]
                             ▲
                           slow=2
```
* `3` is placed in the front of the wall!
* The `0` was kicked to index `4`.
* `slow += 1` steps to index `2` — which is **already the next `0` in the wall**!

---

#### 📍 STEP 5: `fast` finds `12` (Final Swap!)
`fast` reaches the last index `5` and spots `12`!

```text
Indices:     0       1       2       3       4       5
          ┌─────────────┐ ┌───────────────┐
Array:    │  1  │   3   │ │   0   │   0   │   0   │   12   │
          └─────────────┘ └───────────────┘
                             ▲                        ▲
                            slow                     fast
                             │                         │
                             └──────────Swap───────────┘
```
**After Swap & `slow += 1`:**
```text
Indices:     0       1       2       3       4       5
          ┌─────────────────────┐ ┌──────────────────────┐
Array:    │  1  │   3   │  12   │ │   0   │   0   │   0  │
          └─────────────────────┘ └──────────────────────┘
          [    ALL NON-ZEROS    ] [     ALL ZEROS        ]
                                    ▲
                                  slow=3
```

---

## 💻 The Clean 4-Line Implementation

```python
class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow], nums[fast] = nums[fast], nums[slow]
                slow += 1
```

---

## 📊 Iteration-by-Iteration Trace Table

| Step | `fast` | `nums[fast]` | `slow` | `nums[slow]` | Action Taken | Array After Step |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **0** | `0` | `0` | `0` | `0` | Do nothing (`slow` waits) | `[0, 1, 0, 0, 3, 12]` |
| **1** | `1` | `1` | `0` | `0` | **Swap** indices 0 & 1, `slow=1` | `[1, 0, 0, 0, 3, 12]` |
| **2** | `2` | `0` | `1` | `0` | Do nothing (`slow` waits) | `[1, 0, 0, 0, 3, 12]` |
| **3** | `3` | `0` | `1` | `0` | Do nothing (`slow` waits) | `[1, 0, 0, 0, 3, 12]` |
| **4** | `4` | `3` | `1` | `0` | **Swap** indices 1 & 4, `slow=2` | `[1, 3, 0, 0, 0, 12]` |
| **5** | `5` | `12` | `2` | `0` | **Swap** indices 2 & 5, `slow=3` | `[1, 3, 12, 0, 0, 0]` |

---

## 💡 Why `slow += 1` Works (Even with Consecutive Zeros)

1. **The Invariant:** All elements between `slow` and `fast` are **always `0`s**.
2. **The Advance:** When you swap `nums[slow]` with `nums[fast]`, slot `slow` receives the non-zero number.
3. The very next slot (`slow + 1`) is guaranteed to be the next `0` in that contiguous block of zeros. No searching needed!

---

## ⏱️ Complexity Blueprint

* **Time Complexity:** $\mathcal{O}(n)$ — exactly one pass through the array with `fast`.
* **Space Complexity:** $\mathcal{O}(1)$ — strictly in-place modifications, zero additional memory allocated.
