# 🪟 Sliding Window Master Cheat Sheet & Decision Guide

> **Pattern:** Sliding Window (Contiguous Subarrays & Substrings)  
> **Audience:** Complete Beginner / 1st-Year CS Student  
> **Analogy:** The Expanding & Contracting Rubber Band

---

## 💡 1. What is Sliding Window?

Imagine looking through a small rectangular window cut into a cardboard sheet, sliding it across a long sentence. 

Instead of re-calculating the sum or checking all characters of every possible slice using nested loops ($\mathcal{O}(n^2)$), we slide a **window** across the array. 

When the window moves:
* We **add** the new element entering on the right: `+ nums[right]`.
* We **remove** the old element leaving on the left: `- nums[left]`.

This turns an $\mathcal{O}(n^2)$ brute force into a lightning-fast **$\mathcal{O}(n)$** single pass!

```text
Brute Force (Nested Loops): Re-calculates 1+2+3, then 2+3+4, then 3+4+5 from scratch... (Wasteful!)
Sliding Window:             Take old sum, add new guy, subtract old guy. Done in 1 step!
```

---

## 🔍 2. How to Spot It in 3 Seconds (The Trigger Words)

Look for these **two key phrases** in any problem:
1. **"Contiguous"** (elements must be right next to each other, no skipping).
2. **"Subarray"** or **"Substring"** + asking for **"Maximum"**, **"Minimum"**, or **"Longest / Shortest"**.

> ⚠️ **Difference between Two Pointers & Sliding Window:**  
> * **Two Pointers:** Pointers often move independently or from opposite ends to find *pairs* or *boundaries*.  
> * **Sliding Window:** Both pointers move in the *same direction* to define a *continuous range of elements* (a window).

---

## 📐 3. The Two Flavors of Sliding Window

### 🔹 Flavor 1: Fixed Size Window ($K$)
* **The Window Size Never Changes:** It is always exactly length $K$.
* **Analogy:** A magnifying glass of width $K$ sliding across a book 1 character at a time.
* **The Golden Principle (Running Differential):**
  Never recalculate the entire window ($\mathcal{O}(k)$ per step $\implies \mathcal{O}(n \cdot k)$ TLE). Instead, update only the 2 boundary elements in **$\mathcal{O}(1)$**:
  $$\text{window} = \text{window} + \text{entering\_element} - \text{leaving\_element}$$

#### ⚙️ Template A: Numerical Sum / Average (LC 643)
```python
def max_sum_fixed_window(nums: list[int], k: int) -> int:
    # 1. Establish baseline for first window of size k
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    # 2. Slide from index k to end
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]  # Add entering nums[i], subtract leaving nums[i-k]
        if window_sum > max_sum:
            max_sum = window_sum
            
    return max_sum
```
> [!TIP]
> **Deferred Division for Averages:** Never divide by $k$ inside the loop (`avg = tot / k`). Doing float math $100,000$ times is 1.6× slower. Maximize the integer sum first, and divide by $k$ **once at return**!

#### ⚙️ Template B: String Frequency / Condition Counter (LC 1456)
*Strings don't support arithmetic (`+` / `-`), so you update an **integer score counter**:*
```python
def max_vowels_fixed_window(s: str, k: int) -> int:
    vowels = {'a', 'e', 'i', 'o', 'u'}
    
    # 1. Base window
    count = sum(1 for ch in s[:k] if ch in vowels)
    max_count = count
    
    # 2. Slide window
    for i in range(k, len(s)):
        # Entering element: s[i]
        if s[i] in vowels:
            count += 1
        # Leaving element: s[i - k]
        if s[i - k] in vowels:
            count -= 1
            
        if count > max_count:
            max_count = count
            
    return max_count
```

👉 *Walkthroughs:* [LC 643: Maximum Average Subarray I](../01_arrays_and_pointers/643_maximum_average_subarray_i.md) | [LC 1456: Maximum Number of Vowels](../01_arrays_and_pointers/1456_maximum_number_of_vowels_in_a_substring_of_given_length.md)

---

### 🔹 Flavor 2: Dynamic (Variable Size) Window
* **The Window Grows and Shrinks Like a Rubber Band:**
  * **Stretch Right:** Keep expanding `right` to explore and include elements.
  * **Shrink Left:** If the window violates a rule (e.g., has a duplicate letter or sum is too big), pull `left` forward until it becomes valid again.
* **Classic Problem:** *Longest Substring Without Repeating Characters* (LC 3).

```text
Array: [ a , b , c , a , b , c ]

Step 1 (Expand): Window has 'a', 'b', 'c' -> [a, b, c] (Valid! Length 3)
Step 2 (Conflict): 'a' enters -> [a, b, c, a] (Duplicate 'a'! Invalid!)
Step 3 (Shrink):   Move left past the old 'a' -> [b, c, a] (Valid again! Length 3)
```

#### ⚙️ Universal Dynamic Window Template
```python
def dynamic_sliding_window(s: str) -> int:
    left = 0
    seen = set()  # Tracks current elements in the window
    max_len = 0
    
    for right in range(len(s)):
        # While window is INVALID, shrink it from the left
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
            
        # Add right element to make window valid
        seen.add(s[right])
        
        # Update best answer (window size is right - left + 1)
        max_len = max(max_len, right - left + 1)
        
    return max_len
```

---

## 🏆 4. Quick Decision Matrix

| Problem Goal | Window Type | Condition to Shrink `left` | Classic LeetCode |
|---|---|---|---|
| Max sum of size $K$ | **Fixed ($K$)** | Automatically slide when index $\ge K$ | LC 643: Max Average Subarray |
| Longest substring without duplicates | **Dynamic** | While `s[right]` is already in `set` | LC 3: Longest Substring Without Repeats |
| Minimum size subarray with sum $\ge S$ | **Dynamic** | While `current_sum >= target` (try to make it smaller!) | LC 209: Minimum Size Subarray Sum |
| Max consecutive ones if you can flip $K$ zeroes | **Dynamic** | While `zero_count > k` | LC 1004: Max Consecutive Ones III |

---

## ⚠️ 5. Student Pitfalls to Avoid

1. **Off-by-one window length formula:**  
   The number of elements between `left` and `right` inclusive is **`right - left + 1`** (NOT `right - left`).
   * Example: indices 2 to 4 has $4 - 2 + 1 = 3$ elements (indices 2, 3, 4).
2. **Forgetting that `left` can move multiple times:**  
   Notice the `while` loop inside: `while condition: left += 1`. Don't use an `if` statement when multiple items need to be kicked out of the window!
3. **The `s[k]` vs `s[i]` indexing trap:**  
   Inside `for i in range(k, len(s)):`, always use **`s[i]`** for the entering element. Using `s[k]` accidentally freezes the lookup at the exact same index $k$ on every step!
4. **The "Can `count` drop below 0?" myth:**  
   Beginners often write `if count < 0: count = 0`. This is mathematically impossible in a bug-free window! Every element leaving at `i - k` was previously added when it entered at `i`. You only subtract if the leaving element satisfies the condition (meaning it was already counted and `count >= 1`). Total additions $\ge$ total subtractions at all times:
   $$0 \le \text{count} \le k$$
