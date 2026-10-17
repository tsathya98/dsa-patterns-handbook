# 📝 Two Pointers Master Cheat Sheet & Decision Guide

> **Pattern:** Two Pointers Technique  
> **Core Idea:** Coordinated two-marker traversal across 6 formations to replace $\mathcal{O}(n^2)$ nested loops with $\mathcal{O}(n)$.

---

## 💡 1. What is Two Pointers?

Instead of using two nested loops (`for i in ... for j in ...`) which takes **$\mathcal{O}(n^2)$** time, we use **two integer index variables** (`left/right`, `slow/fast`, or `p1/p2`) that move through the data in a coordinated way, reducing time to **$\mathcal{O}(n)$**.

> **Analogy:**  
> A nested loop tests every key against every lock.  
> Two pointers keeps one finger on a word while your other hand turns pages.

---

## 🎯 2. When to Use It? (The 3-Second Mental Checklist)

Ask yourself these 3 questions:

1. **Are the relative positions fixed or sorted?**  
   *(Order matters; you cannot randomly shuffle elements).*
2. **Can I make decisions without backtracking?**  
   *(Once a pointer moves, it never needs to step backward).*
3. **Am I searching for pairs, boundaries, or comparing/matching TWO sequences?**

👉 If all three are **YES**, use Two Pointers.

---

## 📐 3. The 6 Formations (How to Pick Which One)

```text
Formation A: THE SQUEEZE         Formation B: SCOUT & WRITER       Formation C: TWO CONVEYOR BELTS
(Opposite ends, 1 array)         (Same direction, 1 array)         (Same direction, 2 separate arrays)

 l ────►             ◄──── r     slow (writer)                     p1 ────► (on Array 1)
 [ .   .   .   .   .   .   . ]    ▼                                [ .   .   . ]
                                 [ .   .   .   .   .   . ]         [ .   .   .   .   . ]
                                  ▲                                p2 ────────────► (on Array 2)
                                 fast (scout) ──────►

Formation D: ANCHOR & SCOUT (Chunking / Grouping)
(Same direction, 1 array, leapfrogging runs)

 anchor (marks start of streak)
  ▼
 [ 0 ,  1 ,  2 ,  4 ,  5 ,  7 ]
  └───────────┘
              ▲
             scout (sprints until streak breaks)

Formation E: TAIL-BUFFER / REVERSE PLACEMENT
(Backward movement, avoids overwriting unread elements)

                   p1 ◄────                p (write pointer) ◄────
 nums1 = [ 2 , 5 , 6 ,  0 , 0 , 0 ]
 nums2 = [ 1 , 3 , 4 ]
                   ▲
                   p2 ◄────
```

---

### 🔹 Formation A: "The Squeeze"
* **Pointers:** `l = 0`, `r = len(arr) - 1` (opposite ends walking inward).
* **When to use:**
  * Testing symmetry from outside in (*Valid Palindrome*).
  * Pair search in a sorted array (*Two Sum II*, *3Sum*).
  * Boundary limits / geometric containers (*Container With Most Water*).
  * In-place subsegment flipping (*Rotate Array - LC 189*, *Reverse String - LC 344*).
* **Template:**
  ```python
  l, r = 0, len(arr) - 1
  while l < r:
      if condition(arr[l], arr[r]):
          l += 1
      else:
          r -= 1
  ```

👉 *See full breakdown in [`11_container_with_most_water.md`](../01_arrays_and_pointers/11_container_with_most_water.md), [`15_3sum.md`](../01_arrays_and_pointers/15_3sum.md), and [`189_rotate_array.md`](../01_arrays_and_pointers/189_rotate_array.md).*

---

### 🔹 Formation B: "Scout & Writer" (Fast & Slow)
* **Pointers:** `slow = 0`, `fast = 0` (same direction, 1 array).
* **Roles:**
  * `fast` (Scout): Inspects every element.
  * `slow` (Writer): Marks the boundary where the next valid element belongs.
* **When to use:**
  * Modifying an array **in-place** without extra memory (*Move Zeroes*, *Remove Duplicates*).
  * Cycle detection in linked lists (Tortoise & Hare: `slow += 1`, `fast += 2`).
* **Template:**
  ```python
  slow = 0
  for fast in range(len(nums)):
      if is_valid(nums[fast]):
          nums[slow] = nums[fast]
          slow += 1
  ```

👉 *See full breakdown in [`283_move_zeroes.md`](../01_arrays_and_pointers/283_move_zeroes.md), [`27_remove_element.md`](../01_arrays_and_pointers/27_remove_element.md), [`26_remove_duplicates_from_sorted_array.md`](../01_arrays_and_pointers/26_remove_duplicates_from_sorted_array.md), and [`80_remove_duplicates_from_sorted_array_ii.md`](../01_arrays_and_pointers/80_remove_duplicates_from_sorted_array_ii.md).*

---

### 🔹 Formation C: "Two Conveyor Belts"
* **Pointers:** `p1 = 0` on Sequence 1, `p2 = 0` on Sequence 2.
* **Roles:** Move forward independently based on element comparison.
* **When to use:**
  * Comparing, matching, or merging **two separate sequences/strings** (*Is Subsequence*, *Merge Two Sorted Arrays*).
* **Template:**
  ```python
  p1, p2 = 0, 0
  while p1 < len(arr1) and p2 < len(arr2):
      if arr1[p1] == arr2[p2]:
          p1 += 1
      p2 += 1
  ```

---

### 🔹 Formation D: "Anchor & Scout" (Chunking / Intervals)
* **Pointers:** `anchor` (start of streak), `scout` / `i` (advancing through the streak).
* **Roles:**
  * `anchor` (`start`): Drops an anchor at the start of a continuous streak or category.
  * `scout` (`i`): Sprints forward with an inner `while` loop as long as the streak condition holds.
  * When streak breaks: Record the chunk `[anchor, scout]`, then leapfrog `anchor` to the next element.
* **When to use:**
  * Grouping contiguous ranges (*Summary Ranges - LC 228*).
  * Run-Length Encoding / In-place string compression (*String Compression - LC 443*).
  * Merging overlapping time blocks (*Merge Intervals - LC 56*).
* **Template:**
  ```python
  res = []
  i = 0
  while i < len(nums):
      start = nums[i]
      while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
          i += 1
      
      # Process chunk from start to nums[i]
      res.append(f"{start}->{nums[i]}" if start != nums[i] else str(start))
      i += 1
  ```

👉 *See full breakdown in [`228_summary_ranges.md`](../01_arrays_and_pointers/228_summary_ranges.md).*

---

### 🔹 Formation E: "The Tail-Buffer / Reverse Placement Pattern"
* **Pointers:** `p1 = m - 1` (last valid item in Array 1), `p2 = n - 1` (last item in Array 2), `p = m + n - 1` (write pointer at safe tail).
* **The "Bulldozer Collision" Problem:** Moving left-to-right overwrites elements you haven't read yet!
* **The Tail-Buffer Rule:** Look for where the empty space lives. If the zeros/buffer are at the **tail**, iterate from **right-to-left**. Place the **largest** elements first!
* **When to use:**
  * Merging sorted arrays in-place with trailing buffer (*Merge Sorted Array - LC 88*).
  * Replacing characters in-place with extra buffer space (*URLify / Replace Spaces*).
  * Processing operations with backspaces from the end (*Backspace String Compare - LC 844*).
  * Squeezing extremes from outside inward to fill an array backwards (*Squares of a Sorted Array - LC 977*).
* **Template:**
  ```python
  p1, p2, p = m - 1, n - 1, m + n - 1
  while p1 >= 0 and p2 >= 0:
      if nums1[p1] > nums2[p2]:
          nums1[p] = nums1[p1]
          p1 -= 1
      else:
          nums1[p] = nums2[p2]
          p2 -= 1
      p -= 1
  while p2 >= 0:  # Copy any remaining nums2 items
      nums1[p] = nums2[p2]
      p2 -= 1
      p -= 1
  ```

👉 *See full breakdown in [`88_merge_sorted_array.md`](../01_arrays_and_pointers/88_merge_sorted_array.md).*

---

### 🔹 Formation F: "Outward Expand Around Center (The Flashlight Beam)"
* **Pointers:** `l = i`, `r = i` (odd-length center) AND `l = i`, `r = i + 1` (even-length center), expanding outward (`l -= 1`, `r += 1`).
* **Mental Rule:**
  * *Validating* if a full string is a palindrome (*LC 125*) = **Inward Squeeze** (`l = 0, r = n - 1`).
  * *Finding* a palindrome hidden inside a string (*LC 5, LC 647*) = **Outward Flashlight Beam** from all $2N$ centers!
* **Boundary Rule:** When `while l >= 0 and r < len(s) and s[l] == s[r]` stops, `l` and `r` have stepped **1 index too far**. The valid palindrome slice is **`s[l + 1 : r]`**.
* **Template:**
  ```python
  def _expand(l: int, r: int) -> str:
      while l >= 0 and r < len(s) and s[l] == s[r]:
          l -= 1
          r += 1
      return s[l + 1 : r]

  for i in range(len(s)):
      odd_pal = _expand(i, i)       # Center on char i ("bab")
      even_pal = _expand(i, i + 1)  # Center between i and i+1 ("cbbd")
  ```

👉 *See full breakdown in [`5_longest_palindromic_substring.md`](../01_arrays_and_pointers/5_longest_palindromic_substring.md).*

---

## 🏆 4. Quick Decision Matrix

| What is the problem asking? | Input Data | Formation | Initial Pointers | Classic Problem |
|---|---|---|---|---|
| Search for a pair with target sum | 1 Sorted Array | **The Squeeze** | `l = 0`, `r = len - 1` | Two Sum II (LC 167) |
| Check symmetry / Palindrome | 1 String / Array | **The Squeeze** | `l = 0`, `r = len - 1` | Valid Palindrome (LC 125) |
| Find longest/count palindromic substrings | 1 String | **Outward Expand (Flashlight)** | `(i, i)` & `(i, i + 1)` | Longest Palindromic Substring (LC 5), Palindromic Substrings (LC 647) |
| Find maximum container area | 1 Array | **The Squeeze** | `l = 0`, `r = len - 1` | Container With Most Water (LC 11) |
| Remove duplicates / Move zeroes / Remove element in-place | 1 Array | **Scout & Writer** | `slow = 0`, `fast = 0` | Move Zeroes (LC 283), Remove Element (LC 27), Remove Duplicates I & II (LC 26, LC 80) |
| Detect loop in a linked list | 1 Linked List | **Scout & Writer** | `slow = head`, `fast = head` | Linked List Cycle (LC 141) |
| Check if String A is subsequence of String B | 2 Strings / Arrays | **Conveyor Belts** | `p1 = 0`, `p2 = 0` | Is Subsequence (LC 392) |
| Merge two arrays in-place with tail buffer | 2 Arrays (1 with buffer) | **Tail-Buffer (Reverse)** | `p1 = m - 1`, `p2 = n - 1`, `p = end` | Merge Sorted Array (LC 88) |
| Group contiguous runs / summary ranges | 1 Sorted Array / String | **Anchor & Scout** | `i = 0`, inner while | Summary Ranges (LC 228), String Compression (LC 443) |

---

## 🔍 5. Anchor & Scout vs. Sliding Window: What's the Difference?

Many candidates ask: *"Isn't Summary Ranges or String Compression just a Sliding Window since we have a `start` and an `end`?"*

**Answer:** No! The difference is **Overlapping vs. Non-Overlapping**:

```text
SLIDING WINDOW (Overlapping Frames):
  Frame 1: [ 0 , 1 , 2 ]
  Frame 2:     [ 1 , 2 , 4 ]
  Frame 3:         [ 2 , 4 , 5 ]
  👉 Windows slide step-by-step and OVERLAP!
  👉 Elements (like 1 and 2) are tested inside multiple candidate windows.

ANCHOR & SCOUT / CHUNKING (Summary Ranges):
  Chunk 1: [ 0 , 1 , 2 ] 
  Chunk 2:               [ 4 , 5 ] 
  Chunk 3:                         [ 7 ]
  👉 Chunks NEVER overlap!
  👉 Every element belongs to EXACTLY ONE chunk.
```

### 🎥 The Real-World Analogies:
* **Sliding Window = A Moving Video Camera 📹:** Panning smoothly across a street. Every frame overlaps 90% with the previous frame to find the "longest/shortest/maximum" segment (*LC 3, LC 643*).
* **Anchor & Scout = A Bread Knife Slicing a Baguette 🥖:** You slice off a clean piece, wrap it up, and the knife leapfrogs forward to cut the next independent piece (*LC 228, LC 443*).

### 🚨 The 3-Second Rule:
Ask yourself: **"Does a single element belong to multiple candidate answers?"**
* **If YES:** $\implies$ **Sliding Window**
* **If NO:** $\implies$ **Two Pointers (Anchor & Scout / Partitioning)**

---

## 🎛️ 6. The Universal Mental Rule: "Which Pointer Do I Move?"

Never guess or memorize whether to move `left` or `right`. Use the **Volume Knob Analogy**:

In a sorted array, numbers go from **Smallest $\to$ Largest**:
```text
[ -4 ,  -1 ,   0 ,   1 ,   2 ,   5 ]
  ▲                               ▲
 Smallest                       Biggest
 (left)                         (right)
```

Think of your pointers as two knobs controlling your state:
* **Moving `left` forward (`left += 1`)** $\to$ picks a **bigger** number $\to$ **Turns the sum UP 🔊**
* **Moving `right` backward (`right -= 1`)** $\to$ picks a **smaller** number $\to$ **Turns the sum DOWN 🔉**

### The 2-Question Steering Checklist:
1. **What is wrong with my current state?**
   * *Is my sum too small / too cold?* (e.g. `sum < target`) $\to$ I need a bigger number!
   * *Is my sum too big / too hot?* (e.g. `sum > target`) $\to$ I need a smaller number!
   * *Is my container bottlenecked?* $\to$ The shorter wall is limiting my area!
2. **Which pointer has the power to fix that problem?**
   * Need to **increase** the value? $\to$ Move `left += 1`.
   * Need to **decrease** the value? $\to$ Move `right -= 1`.
   * Bottlenecked by the shorter wall? $\to$ Move the shorter wall inward!

> ⭐ **Why this never fails:** Because the array is sorted, every move has a **100% predictable, monotonic outcome**. Moving `left` can only increase values; moving `right` can only decrease them.

---

## ⚠️ 7. The Golden Rule
> **"Pointers only move in one direction. If you ever find yourself moving a pointer backward, you don't need Two Pointers: you need a Stack, a Sliding Window, or Backtracking."**

