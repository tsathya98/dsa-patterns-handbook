# 🧭 DSA Patterns Master Study Guide
> **Based on:** Sheldon Chai's 75-Minute LeetCode Patterns Masterclass (freeCodeCamp)  
> **Audience:** First-Year CSE Student to FAANG Candidate  
> **Philosophy:** Learn the *patterns*, not just individual problems. When you recognize the pattern, the code writes itself.

---

## 🗺️ Visual Roadmap & Master Cheat Sheets

Click any pattern below to open its **deep-dive beginner cheat sheet** with full visual diagrams, step-by-step traces, and notebook-ready templates:

| # | Pattern | When to Use | Time Complexity | Deep-Dive Cheat Sheet |
|---|---|---|---|---|
| 1 | **Arrays, Strings & HashMaps** | Contiguous memory, $\mathcal{O}(1)$ lookups, frequency count | $\mathcal{O}(1)$ read / lookup | 📖 **[Arrays & HashMaps Guide](./cheat_sheets/arrays_hashmaps_cheat_sheet.md)** |
| 2 | **Two Pointers** | Sorted lists, pairs, palindromes, shrinking windows | $\mathcal{O}(n)$ | 📖 **[Two Pointers Master Guide](./cheat_sheets/two_pointers_cheat_sheet.md)** |
| 3 | **Sliding Window** | Contiguous subarrays/substrings ("longest/shortest") | $\mathcal{O}(n)$ | 📖 **[Sliding Window Guide](./cheat_sheets/sliding_window_cheat_sheet.md)** |
| 4 | **Binary Search** | Sorted search space, monotonic feasibility ("find min speed") | $\mathcal{O}(\log n)$ | 📖 **[Binary Search Guide](./cheat_sheets/binary_search_cheat_sheet.md)** |
| 5 | **BFS & DFS** | Shortest path (BFS), maze exploration & tree depth (DFS) | $\mathcal{O}(V + E)$ | 📖 **[BFS vs. DFS Guide](./cheat_sheets/bfs_dfs_cheat_sheet.md)** |
| 6 | **Backtracking** | Generate all combinations, subsets, permutations with "undo" | $\mathcal{O}(2^n)$ or $\mathcal{O}(n!)$ | 📖 **[Backtracking Guide](./cheat_sheets/backtracking_cheat_sheet.md)** |
| 7 | **Heaps / Priority Queues** | Constantly track min/max, "Top K", live median streams | Push/Pop: $\mathcal{O}(\log k)$ | 📖 **[Heaps & Priority Queues Guide](./cheat_sheets/heaps_priority_queues_cheat_sheet.md)** |
| 8 | **Kadane's Algorithm** | Contiguous subarray with negative penalties / max gain | $\mathcal{O}(n)$ | 📖 **[Kadane's Algorithm Guide](./cheat_sheets/kadanes_algorithm_cheat_sheet.md)** |
| 9 | **Greedy Subtraction (ATM Pattern)** | Canonical unit decomposition, Roman numerals, currency change | $\mathcal{O}(1)$ / $\mathcal{O}(D)$ | 📖 **[Greedy Subtraction Guide](./cheat_sheets/greedy_subtraction_atm_cheat_sheet.md)** |
| 10 | **Prefix Sum (Seesaw Balance Pattern)** | Finding equilibrium/pivot index, comparing left vs right sides | $\mathcal{O}(n)$ | 📖 **[Prefix Sum (Seesaw) Guide](./cheat_sheets/prefix_sum_seesaw_cheat_sheet.md)** |
| 11 | **Linked Lists (Pointers & Dummies)** | In-place node stitching, reversing arrows, fast/slow cycles | $\mathcal{O}(n)$ | 📖 **[Linked List Master Guide](./cheat_sheets/linked_list_master_cheat_sheet.md)**<br>🗺️ **[90% Taxonomy Guide](./02_linked_lists/linked_list_90_percent_taxonomy.md)** |
| 12 | **Tips & Tricks (Telescoping Sums & Loops)** | Bytecode optimization, collapsing intervals into adjacent steps | $\mathcal{O}(n)$ | 💡 **[Jump to Section 12](#12--tips--tricks-bytecode-telescoping-sums--interval-decomposition)** |
| 13 | **Bit Manipulation** | Direct silicon logic, LSB extraction, power of 2, Horner's stream shift | $\mathcal{O}(1)$ | 📖 **[Bit Manipulation Guide](./cheat_sheets/bitwise_cheat_sheet.md)** |

---

## 1. 🧱 Arrays, Strings, Sets & HashMaps

### 💡 The Big Idea
* **Array = A row of houses on the same street.** Because elements sit contiguously in memory, finding house #4 is instant ($\mathcal{O}(1)$ index access). However, inserting at index 0 requires every house to slide over ($\mathcal{O}(n)$).
* **String = Words carved in stone (Immutable).** Doing `s += char` inside a loop builds a brand-new string every iteration ($\mathcal{O}(n^2)$ trap!). Always use `[].append()` and `"".join()`.
* **Set = VIP bouncer's guest list.** Answers: *"Have I seen this before?"* in instant $\mathcal{O}(1)$ time.
* **HashMap = Coat-check ticket.** Hand in your key (ticket), instantly get back your value (jacket) in $\mathcal{O}(1)$ time.
* ⚡ **Performance Finding (Avoid Nested Lookups in Loops):** Avoid chaining lookups like `s[i+1] in sub[s[i]]` inside loops. Replacing nested dictionary-in-list checks with direct numeric comparisons (`val[s[i]] < val[s[i+1]]` like in Roman to Integer) cuts out multiple Python hash table and list scans, dropping runtime from 10 ms to 2 ms (Beats 90%+).
* 🔠 **Bijective (1-to-1) Mapping Pattern & The `in dict.values()` Trap (LC 290):**  
  * Checking `key in dict` is **$\mathcal{O}(1)$**, but checking `val in dict.values()` is **$\mathcal{O}(k)$ linear scan** because hash tables only index keys! Inside a loop, `val in dict.values()` silently degrades time to $\mathcal{O}(n^2)$ (290× slower on scale).
  * **The Fix:** Use **Two HashMaps** (`p_to_w` and `w_to_p`) or a secondary `seen` Set to maintain pure $\mathcal{O}(1)$ lookups in both directions, or the Pythonic Set Cardinality rule: `len(set(p)) == len(set(w)) == len(set(zip(p, w)))`.
* 🚗 **The Car Odometer & Schoolbook Carry Pattern (LC 66):**  
  * Avoid `int("".join(...)) + 1` in interviews: it overflows 64-bit integer limits in C++/Java and wastes $\mathcal{O}(n)$ string memory.
  * **The Odometer Model:** Walk right-to-left. If `digits[i] < 9`, bump by 1 and **return immediately** ($\mathcal{O}(1)$ best case!). If `digits[i] == 9`, roll it over to `0` and let the loop carry leftward.
  * If the loop finishes without returning, every digit was a 9 (e.g. `[9, 9, 9]` became `[0, 0, 0]`). Prepend `[1]` using `return [1] + digits` (avoiding the slow $\mathcal{O}(n)$ `digits.insert(0, 1)`).

### 📋 What Kind of Problems Fall Under Arrays, Strings & HashMaps?
| Category | Problem Statement / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **Instant Pair Lookup ($\mathcal{O}(1)$ Complement)** | Find two numbers that sum to target using `seen[target - num]`. | **LC 1: Two Sum** |
| **Frequency Anagrams / Counting** | Check if two strings have identical character frequencies. | **LC 242: Valid Anagram** |
| **Bijective / 1-to-1 Mapping** | Two strings follow exact same structure without duplicate bindings. | **LC 290: Word Pattern**, **LC 205: Isomorphic Strings** |
| **Prefix Sum with Hash Lookup** | Find total number of continuous subarrays summing to $K$. | **LC 560: Subarray Sum Equals K** |
| **Direct Numeric Lookahead** | Compare current element with next element without nested lookups. | **LC 13: Roman to Integer** |
| **Schoolbook Addition / Carry** | Simulate arithmetic from right to left; roll over 9s to 0s. | **LC 66: Plus One**, **LC 2: Add Two Numbers** |
| **Majority Element / Frequency** | Mutual cancellation in $\mathcal{O}(1)$ space vs. hash table frequency count. | **LC 169: Majority Element** |

👉 **Deep Dive Guide:** [Arrays, Strings & HashMaps Master Cheat Sheet](./cheat_sheets/arrays_hashmaps_cheat_sheet.md) | [Majority Element (LC 169)](./01_arrays_and_pointers/169_majority_element.md) | [Plus One (LC 66)](./01_arrays_and_pointers/66_plus_one.md) | [Roman to Integer (LC 13)](./01_arrays_and_pointers/13_roman_to_integer.md) | [Word Pattern (LC 290)](./01_arrays_and_pointers/290_word_pattern.md)

---

## 2. 🎯 Two Pointers

### 💡 The Big Idea
Instead of checking every pair with nested loops ($\mathcal{O}(n^2)$), use two index markers that move in a coordinated way, cutting runtime to $\mathcal{O}(n)$.

### 📐 The 5 Formations:
1. **The Squeeze (`l = 0, r = len - 1`):** Opposite ends walking inward (*Valid Palindrome*, *Container With Most Water*).
2. **Scout & Writer (`slow = 0, fast = 0`):** Same array, same direction (*Move Zeroes*, *Remove Duplicates*).
3. **Two Conveyor Belts (`p1 = 0, p2 = 0`):** Two separate arrays/strings (*Is Subsequence*, *Merge Sorted Lists*).
4. **Anchor & Scout (`start = nums[i]`, inner while):** Grouping contiguous runs or intervals (*Summary Ranges*, *String Compression*).
5. **The Tail-Buffer / Reverse Placement (`p = m + n - 1`, backwards):** Working right-to-left into safe trailing zeros to avoid the "Bulldozer Overwrite" collision (*Merge Sorted Array*).

### 📋 What Kind of Problems Fall Under Two Pointers?
| Formation | Problem Category / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **The Squeeze** | Symmetry / Palindrome check from outside in. | **LC 125: Valid Palindrome** |
| **The Squeeze** | Pair search in sorted array (`left` moves if sum too small, `right` if too large). | **LC 167: Two Sum II**, **LC 15: 3Sum** |
| **The Squeeze** | Maximum geometric container (move shorter wall inward). | **LC 11: Container With Most Water** |
| **The Squeeze** | In-place subsegment flipping / triple reversal rotation. | **LC 189: Rotate Array** |
| **Scout & Writer** | In-place element removal / compaction without extra memory. | **LC 283: Move Zeroes**, **LC 27: Remove Element**, **LC 26: Remove Duplicates I & II (LC 80)** |
| **Scout & Writer** | Linked list cycle detection / middle finding (Slow 1x, Fast 2x). | **LC 141: Linked List Cycle**, **LC 876: Middle of Linked List** |
| **Two Conveyor Belts** | Subsequence matching (progress pointer on match). | **LC 392: Is Subsequence** |
| **Tail-Buffer (Reverse)** | In-place merge using trailing garbage buffer from the back. | **LC 88: Merge Sorted Array** |
| **Anchor & Scout** | Contiguous chunk grouping / run-length encoding. | **LC 228: Summary Ranges**, **LC 443: String Compression** |

👉 **Deep Dive Guide:** [Two Pointers Master Cheat Sheet](./cheat_sheets/two_pointers_cheat_sheet.md) | [Rotate Array (LC 189)](./01_arrays_and_pointers/189_rotate_array.md) | [Remove Duplicates II (LC 80)](./01_arrays_and_pointers/80_remove_duplicates_from_sorted_array_ii.md) | [Remove Duplicates (LC 26)](./01_arrays_and_pointers/26_remove_duplicates_from_sorted_array.md) | [Remove Element (LC 27)](./01_arrays_and_pointers/27_remove_element.md) | [Merge Sorted Array (LC 88)](./01_arrays_and_pointers/88_merge_sorted_array.md) | [Summary Ranges (LC 228)](./01_arrays_and_pointers/228_summary_ranges.md) | [Container With Most Water (LC 11)](./01_arrays_and_pointers/11_container_with_most_water.md) | [3Sum (LC 15)](./01_arrays_and_pointers/15_3sum.md) | [Move Zeroes (LC 283)](./01_arrays_and_pointers/283_move_zeroes.md) | [Is Subsequence (LC 392)](./01_arrays_and_pointers/392_is_subsequence.md)

### ⚖️ Two Pointers (Anchor & Scout) vs. Sliding Window: What's the Difference?
Many candidates confuse **Anchor & Scout** with **Sliding Window** because both track a range `[start ... end]`.

* **Sliding Window (Overlapping Frames - Video Camera 📹):**  
  Windows slide and **overlap** (`[0..2]`, `[1..3]`, `[2..4]`). Single elements belong to **multiple candidate windows**. Used to find the "longest/shortest/maximum" segment (*LC 3, LC 643*).
* **Anchor & Scout (Non-Overlapping Chunks - Bread Knife 🥖):**  
  The array is sliced into **disjoint, independent chunks** (`[0..2]`, `[4..5]`, `[7]`). Elements belong to **exactly one chunk**. Once a chunk is cut, the anchor leapfrogs to the next chunk (*LC 228 Summary Ranges, LC 443 String Compression*).
* **The 3-Second Rule:** Does a single element belong to multiple candidate answers?  
  * **YES** $\implies$ Sliding Window.  
  * **NO** $\implies$ Two Pointers (Anchor & Scout).

---

## 3. 🪟 Sliding Window

### 💡 The Big Idea: The Expanding & Shrinking Rubber Band
Imagine stretching a rubber band across an array:
1. **Expand:** Stretch `right` forward to explore and include elements.
2. **Contract:** If a rule is violated (e.g. duplicate letter or sum too big), pull `left` forward until it becomes valid again.
3. **The Magic:** Neither pointer ever steps backward! Total time is strictly $\mathcal{O}(n)$.

### 🔄 The Universal "Subtract Old, Add New" Differential Pattern (Fixed Window of Size $K$)
Whenever a problem asks for the maximum/minimum/target property of a contiguous window of fixed size $K$:
* **The TLE Trap:** Re-slicing `nums[i:i+k]` or re-summing using a nested loop costs $\mathcal{O}(k)$ per position $\implies \mathcal{O}(n \cdot k)$ total time ($2.5 \times 10^9$ operations for $n=10^5$, instant TLE!).
* **The Running Differential:** Consecutive windows share $K-1$ elements in common! You never re-sum the whole window:
  $$\text{window\_sum} = \text{window\_sum} + \text{entering\_element} - \text{leaving\_element}$$
* **Clean Indexing Template (`range(k, len(nums))`):**
  ```python
  # 1. Establish initial window
  window_sum = sum(nums[:k])
  max_sum = window_sum
  
  # 2. Slide by 1 step from index k to end
  for i in range(k, len(nums)):
      window_sum += nums[i] - nums[i - k]  # Add entering (nums[i]), remove leaving (nums[i-k])
      if window_sum > max_sum:
          max_sum = window_sum
  ```
* ⚡ **Pro Optimization (Deferred Division):** For averages, never divide by $k$ inside the loop (`avg = tot / k` allocates $10^5$ floating point numbers and slows down code by ~1.6x). Maximize the integer sum first, and divide by $k$ once at the very end!
* 🔤 **Applying to Strings & Frequency Counters (LC 1456):** Strings do not support arithmetic, but your **integer counter** does! Update the counter based on boolean membership: `count += (s[i] in target) - (s[i - k] in target)`.
* 🛡️ **Why `count` Never Drops Below 0:** Beginners often defensively add `if count < 0: count = 0`. This is mathematically unnecessary: you only subtract an item when it leaves if it was already credited when it entered. Thus, total additions $\ge$ total subtractions at all times ($0 \le \text{count} \le k$).

### 📋 What Kind of Problems Fall Under Sliding Window?
| Flavor | Problem Category / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **Fixed ($K$) Sums** | Maximum or minimum sum/average of subarray of size $K$. | **LC 643: Maximum Average Subarray I** |
| **Fixed ($K$) Frequency** | Maximum occurrences of target condition in window of size $K$. | **LC 1456: Max Number of Vowels** |
| **Dynamic (Longest)** | Longest substring without repeating characters. | **LC 3: Longest Substring Without Repeating** |
| **Dynamic (Longest)** | Max consecutive ones with at most $K$ zero flips. | **LC 1004: Max Consecutive Ones III** |
| **Dynamic (Shortest)** | Minimum size subarray sum $\ge$ target. | **LC 209: Minimum Size Subarray Sum** |
| **Dynamic (Exact)** | Subarrays with $K$ different integers (`atMost(K) - atMost(K-1)`). | **LC 992: Subarrays with K Different Integers** |

👉 **Deep Dive Guide:** [Sliding Window Master Cheat Sheet](./cheat_sheets/sliding_window_cheat_sheet.md) | [Maximum Average Subarray I (LC 643)](./01_arrays_and_pointers/643_maximum_average_subarray_i.md) | [Maximum Number of Vowels (LC 1456)](./01_arrays_and_pointers/1456_maximum_number_of_vowels_in_a_substring_of_given_length.md)

---

## 4. 🔍 Binary Search

### 💡 The Big Idea: The "Higher or Lower" Guessing Game
When data is sorted, checking the exact middle lets you throw away 50% of the remaining search space every single step.
* Searching through $1,000,000$ items takes only **20 checks** ($\log_2 10^6 \approx 20$).
* **Binary Search on the Answer:** If you need to find the "minimum speed" or "maximum capacity" where answers transition from `[No, No, No, YES, YES]`, use binary search on that boundary!

### 📋 What Kind of Problems Fall Under Binary Search?
| Category | Problem Statement / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **Direct Value Search** | Find target in sorted array (or first/last occurrence). | **LC 704: Binary Search**, **LC 34: First and Last Position** |
| **Rotated Sorted Arrays** | Find target when sorted array was rotated at unknown pivot. | **LC 33: Search in Rotated Sorted Array** |
| **Peak Finding** | Find a local maximum where `nums[mid] > nums[mid+1]`. | **LC 162: Find Peak Element** |
| **Binary Search on Answer** | Find minimum eating speed $K$ to eat all bananas within $H$ hours. | **LC 875: Koko Eating Bananas** |
| **Binary Search on Answer** | Minimum ship capacity to ship packages within $D$ days. | **LC 1011: Capacity To Ship Packages** |

👉 **Deep Dive Guide:** [Binary Search Master Cheat Sheet](./cheat_sheets/binary_search_cheat_sheet.md)

---

## 5. 🌊 Breadth-First Search (BFS) vs. 🌲 Depth-First Search (DFS)

### 💡 The Big Idea
* **BFS (The Water Ripple):** Spreads outward layer-by-layer using a **Queue**.  
  ⭐ *Superpower:* In unweighted graphs/grids, **BFS guarantees the shortest path**!
* **DFS (The Maze Runner):** Dives as deep as possible down one branch using **Recursion** until it hits a dead end, then backtracks.  
  ⭐ *Superpower:* Cleanest way to explore all paths, calculate tree depths, and flood-fill islands.

### 📋 What Kind of Problems Fall Under BFS & DFS?
| Algorithm | Problem Category / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **BFS (Queue)** | Shortest path in unweighted maze / grid. | **LC 1091: Shortest Path in Binary Matrix** |
| **BFS (Queue)** | Level-order tree traversal / infection spread. | **LC 102: Binary Tree Level Order**, **LC 994: Rotting Oranges** |
| **DFS (Recursion)** | Flood fill / connected component counting. | **LC 200: Number of Islands** |
| **DFS (Recursion)** | Tree height, symmetry, and max path sum. | **LC 104: Max Depth of Binary Tree**, **LC 124: Tree Max Path Sum** |
| **DFS (Recursion)** | Cycle detection in directed graphs (Topological Sort). | **LC 207: Course Schedule** |

👉 **Deep Dive Guide:** [BFS vs. DFS Master Cheat Sheet](./cheat_sheets/bfs_dfs_cheat_sheet.md)

---

## 6. 🔄 Backtracking

### 💡 The Big Idea: The Decision Tree with an "Undo" Button
When you need to generate all possibilities (subsets, combinations, permutations):
1. **Choose:** Make a move (`path.append(choice)`).
2. **Explore:** Recurse deeper (`backtrack()`).
3. **Un-choose:** Undo your move (`path.pop()`) so the next branch starts with a clean slate!

### 📋 What Kind of Problems Fall Under Backtracking?
| Category | Problem Statement / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **Subsets (Power Set)** | Generate all possible subsets of an array (include / exclude). | **LC 78: Subsets** |
| **Combinations** | Pick $K$ elements that sum to target without reuse. | **LC 39: Combination Sum**, **LC 77: Combinations** |
| **Permutations** | Generate all orderings where position matters. | **LC 46: Permutations** |
| **Constraint Satisfaction** | Fill a board satisfying row, col, subgrid rules with pruning. | **LC 51: N-Queens**, **LC 37: Sudoku Solver** |
| **Word Search on Board** | Spell a word by moving 4-directionally without reusing cells. | **LC 79: Word Search** |

👉 **Deep Dive Guide:** [Backtracking Master Cheat Sheet](./cheat_sheets/backtracking_cheat_sheet.md)

---

## 7. ⛰️ Priority Queues & Heaps

### 💡 The Big Idea: Hospital ER Triage
In a hospital Emergency Room, patients aren't seen by arrival time — the person with the most critical condition (highest priority) is seen first.
* A **Heap** gives instant $\mathcal{O}(1)$ access to the smallest (or largest) item.
* Adding an item or removing the top item takes $\mathcal{O}(\log k)$ time.
* ⭐ *Counter-Intuitive Top-K Rule:* To find the $K$ **largest** elements, keep a **Min-Heap** of size $K$!

### 📋 What Kind of Problems Fall Under Heaps / Priority Queues?
| Category | Problem Statement / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **Top K Frequent / Largest** | Maintain a Min-Heap of size $K$ to evict small items. | **LC 215: Kth Largest Element**, **LC 347: Top K Frequent** |
| **Continuous Stream Median** | Two Heaps: Max-Heap for lower half, Min-Heap for upper half. | **LC 295: Find Median from Data Stream** |
| **K-Way Merge** | Merge $K$ sorted linked lists/arrays simultaneously. | **LC 23: Merge k Sorted Lists** |
| **Task Scheduling / Greedy** | Pick the most frequent or highest profit available task first. | **LC 621: Task Scheduler** |

👉 **Deep Dive Guide:** [Heaps & Priority Queues Master Cheat Sheet](./cheat_sheets/heaps_priority_queues_cheat_sheet.md)

---

## 8. 📈 Kadane's Algorithm

### 💡 The Big Idea: The Toxic Debt Rule
When finding the maximum contiguous subarray among negative numbers:
* Positive running balances help future numbers. Keep carrying them forward!
* The second your running balance drops below 0, it becomes **toxic debt**.
* **Declare bankruptcy, drop the past, and start fresh!**
* Formula: `current_sum = max(num, current_sum + num)`

### 📋 What Kind of Problems Fall Under Kadane's Algorithm?
| Category | Problem Statement / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **Max Subarray Sum** | Contiguous slice with largest sum in presence of negatives. | **LC 53: Maximum Subarray** |
| **Circular Max Subarray** | $\max(\text{Kadane Max}, \text{Total} - \text{Kadane Min})$. | **LC 918: Maximum Sum Circular Subarray** |
| **Max Product Subarray** | Track both `cur_max` and `cur_min` (negative flips to positive). | **LC 152: Maximum Product Subarray** |
| **Maximum Difference / Stock** | Convert price array into daily deltas: Kadane on differences. | **LC 121: Best Time to Buy and Sell Stock** |

👉 **Deep Dive Guide:** [Kadane's Algorithm Master Cheat Sheet](./cheat_sheets/kadanes_algorithm_cheat_sheet.md)

---

## 9. 🏧 Greedy Subtraction (The ATM / Cashier Pattern)

### 💡 The Big Idea: The ATM Dispenser Analogy
Instead of converting a number into a string and doing complicated digit-by-digit place-value math (`10 ** cur_l`), treat the problem like **an ATM dispensing cash with the fewest bills possible**:
* Define your denominations in **strictly descending order** (from largest to smallest).
* For Roman numerals, treat subtractive pairs (`900: 'CM'`, `4: 'IV'`) as standard bill denominations!
* For each denomination, repeatedly peel off bills (`while num >= bill: num -= bill; result.append(symbol)`) until you must drop to the next smaller bill.

### 📋 What Kind of Problems Fall Under Greedy Subtraction?
| Category | Problem Statement / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **Symbol Decomposition** | Decimal to Roman numerals with subtractive pairs. | **LC 12: Integer to Roman** |
| **Number to English Words** | Break number into billions, millions, thousands, hundreds. | **LC 273: Integer to English Words** |
| **Canonical Coin Change** | Dispense fewest coins for standard currencies ($0.25, 0.10, 0.05, 0.01$). | Real-World ATM Systems |
| **Time / Storage Conversion** | Convert seconds into days, hours, mins, secs without string math. | General CS Systems |

### 🎯 When to Use It?
1. Decomposing a total into standard predefined units (Roman numerals, currency change, seconds to days/hours/mins).
2. The unit system is canonical (greedily picking the largest never blocks an optimal answer).
3. Inner `while` loop runs $\le 3$ times per symbol for Roman numerals, making it strictly $\mathcal{O}(1)$ time with zero division math bugs.

👉 **Deep Dive Guide:** [Greedy Subtraction (ATM Pattern) Master Cheat Sheet](./cheat_sheets/greedy_subtraction_atm_cheat_sheet.md) | [LeetCode 12: Integer to Roman](./01_arrays_and_pointers/12_integer_to_roman.md)

---

## 10. ⚖️ Prefix Sum (The Seesaw Balance Pattern)

### 💡 The Big Idea: The Seesaw / Conservation Analogy
When a problem asks you to compare the left side of an array with the right side (pivots, equilibrium indices, split points):
* **The TLE Trap:** Calling `sum(nums[:i])` and `sum(nums[i+1:])` inside a loop takes $\mathcal{O}(n^2)$ time ($2.5 \times 10^9$ operations!).
* **Total Conservation Law:** In an array, total sum is constant. Thus:
  $$\text{Left Sum} + \text{nums}[i] + \text{Right Sum} = \text{Total Sum}$$
  $$\mathbf{\text{Right Sum} = \text{Total Sum} - \text{Left Sum} - \text{nums}[i]}$$
* You never calculate the right side! Just maintain one running integer: `left_sum`.

### 🎯 When to Use It? (The 3-Second Mental Radar)
1. Problem asks for an **index where left side equals right side** (or a comparison between elements before vs elements after).
2. The property is cumulative (sum, frequency, product, or count).
3. Check the balance condition **before** adding `nums[i]` to `left_sum`!

### 📋 What Kind of Problems Fall Under This Pattern?
The Seesaw Balance pattern applies to **4 major problem archetypes** on LeetCode:

| Category | Problem Type | Problem Statement / Goal | The Seesaw Equation |
| :--- | :--- | :--- | :--- |
| **1. Equilibrium / Pivot Points** | **LC 724 / LC 1991: Find Pivot Index** | Find an index where sum of elements on left equals sum on right. | `left_sum == total - left_sum - nums[i]` |
| **2. Valid Split Points** | **LC 2270: Number of Ways to Split Array** | Count indices where left subarray sum is $\ge$ right subarray sum. | `left_sum >= total - left_sum` |
| **3. String / Character Balances** | **LC 1422: Maximum Score After Splitting a String** | Split string into two non-empty substrings: maximize (zeros on left + ones on right). | `left_zeros + (total_ones - left_ones)` |
| **4. Multiplicative Balance (No Division)** | **LC 238: Product of Array Except Self** | Find product of all elements except self without using division. | $\text{left\_prod} \times \text{right\_prod}$ (two running passes) |
| **5. Two-Row Grid Path Balances** | **LC 2017: Grid Game** | Robot 1 picks a column to drop from Row 0 to Row 1; minimize Robot 2's score. | Robot 2 gets $\max(\text{Row 0 Right}, \text{Row 1 Left})$ |

👉 **Deep Dive Guide:** [Prefix Sum (Seesaw) Master Cheat Sheet](./cheat_sheets/prefix_sum_seesaw_cheat_sheet.md) | [Find Pivot Index (LC 724)](./01_arrays_and_pointers/724_find_pivot_index.md)

---

## 11. 🔗 Linked Lists (Pointer Choreography & The Dummy Head)

### 💡 The Big Idea: The Nested Russian Doll
* A Linked List is **NOT** a flat array! It is a chain of nested objects: `ListNode(val, next=ListNode(...))`.
* A node only knows its own value and where the next node lives (`.next`). Finding length is **$\mathcal{O}(n)$**, not $\mathcal{O}(1)$! Calling `len(head)` will crash with a `TypeError`!

### 🛡️ The Dummy Head Superweapon:
* When building or modifying a list, use a **Dummy Node** (`dummy = ListNode()`) to anchor the front.
* **`dummy` (The Coat Rack):** Never moves! Retains the pointer to the start so you never lose the head.
* **`cur` (Your Hand):** Walks forward (`cur = cur.next`), stitching new nodes to the tail.
* **`return dummy.next`:** Skips the fake placeholder node and returns the first real node of your result!

### 🎒 In-Place Reversal: The Conga Line Backpack Model (LC 206)
* A line of children holding each other's backpacks: `[ Alice ] ──► [ Bob ] ──► [ Charlie ] ──► None`.
* You want Charlie at the front and Alice at the back. **If Bob turns around without a spotter, Charlie runs off!**
* **The 4-Beat Rhythmic Dance:**
  1. `nxt = curr.next` $\implies$ **SPOTTER:** Hold child in front so they don't run away!
  2. `curr.next = prev` $\implies$ **TURN AROUND:** Grab backpack of person behind you!
  3. `prev = curr` $\implies$ **SLIDE PREV:** You are now the person "behind" for the next round.
  4. `curr = nxt` $\implies$ **SLIDE CURR:** Next child's turn to turn around.
* When loop ends (`curr = None`), **`return prev`** (pointing to Charlie, the new front of the line!).

### 🪞 The 3-Step Triple Crown: Palindrome & Reorder (LC 234, LC 143)
* **Goal:** Verify palindromes or reorder nodes in **$\mathcal{O}(n)$ time and $\mathcal{O}(1)$ auxiliary space**.
* **Step 1 (Find Mid):** `while fast.next and fast.next.next:` (slow stops at end of 1st half).
* **Step 2 (Reverse 2nd Half):** In-place Conga Line 4-beat dance on `slow.next`.
* **Step 3 (Compare / Merge):** Walk `p1 = head` and `p2 = reversed_second_half` until `p2` is exhausted.
* **Senior Bonus (Restore):** Re-reverse the second half back to original so caller's memory is intact.
* **Baseline vs Slicing:** Two Pointers Squeeze (`l < r`) beats `lst == lst[::-1]` by avoiding $\mathcal{O}(n)$ array duplication and exiting in $\mathcal{O}(1)$ time on mismatch ($1,685\times$ faster).

### 📏 The Measuring Stick / Offset Two Pointers (LC 19, LC 1721)
* **Goal:** Locate or swap the $k$-th node from the beginning and $k$-th node from the end in **$\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space**.
* **The "Fencepost" Step Rule:** To reach Node $k$ from Node 1, take **`k - 1` steps** (`range(k - 1)`). Taking $k$ steps lands you on Node $k+1$!
* **The Measuring Stick:** Set `fast = first` ($k$-th from start) and `second = head`. Slide both until `fast.next is None`. `second` is guaranteed to be on the $k$-th node from the end!
* **Direction-Dependent Swap Bug:** If using an array to rebuild, never swap inside the loop (`if i == k - 1:`). When $k$ is in the second half (e.g. `[100, 90], k = 2`), earlier nodes are read before swapping, causing duplicate values (`[100, 100]`). Always swap *before* the loop!

### ⚡ The Positional Stream Accumulator / Horner's Rule (LC 1290)
* **Goal:** Convert an incoming stream of bits/digits into an integer in **$\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space** without string conversions (`s += ...`) or powers (`2 ** k`).
* **The Shift-and-Add Model:** Just like reading base-10 digits (`ans = ans * 10 + digit`), in binary we shift left by 1 and add the bit: `ans = ans * 2 + head.val` or `ans = (ans << 1) | head.val`.

### 📋 What Kind of Problems Fall Under Linked Lists?
| Pattern / Technique | Problem Category / Goal | Classic LeetCode |
| :--- | :--- | :--- |
| **Dummy Head + Zipper Merge** | Merge two sorted lists into one sorted list in-place. | **LC 21: Merge Two Sorted Lists** |
| **Conga Line Reversal (Prev/Curr/Next)** | Reverse all arrows in a single pass without extra space. | **LC 206: Reverse Linked List** |
| **Tortoise & Hare (Slow 1x, Fast 2x)** | Detect cycles without using sets; find exact middle node. | **LC 141: Linked List Cycle**, **LC 876: Middle of Linked List** |
| **Pointer Skipping (Snip & Recheck)** | Remove duplicate nodes in-place (advance only in `else`). | **LC 83: Remove Duplicates from Sorted List** |
| **Dummy + Offset Two Pointers** | Remove $N$-th node from end in a single pass. | **LC 19: Remove Nth Node From End** |
| **Reorder / Palindrome (3-Step)** | Find mid $\to$ reverse second half $\to$ merge/compare. | **LC 143: Reorder List**, **LC 234: Palindrome Linked List** |
| **Measuring Stick (Offset Runners)** | Swap $k$-th from start and $k$-th from end in $\mathcal{O}(1)$ space. | **LC 1721: Swapping Nodes in a Linked List** |
| **Horner's Stream Accumulation** | Convert binary linked list to decimal in $\mathcal{O}(1)$ space. | **LC 1290: Convert Binary in Linked List** |

### 🗺️ The 11 Archetypes of Linked Lists (The 90% Rule)
According to the viral LeetCode master taxonomy, 90%+ of all linked list problems collapse into **11 archetypes**:
1. **Type 0:** Design & Sentinels (`LC 707`)
2. **Type 1:** Single-Pass / Stream / Recursion (`LC 1290`, `LC 1721`, `LC 369`)
3. **Type 2:** Conga Line Reversals (`LC 206`, `LC 92`, `LC 234`, `LC 25`)
4. **Type 3:** Reordering & Conveyor Belts (`LC 86`, `LC 143`, `LC 24`, `LC 328`)
5. **Type 4:** Deleting Nodes / Skip & Bypass (`LC 19`, `LC 83`, `LC 82`, `LC 203`)
   *(Rule: Sorted duplicates = $\mathcal{O}(1)$ space; Unsorted duplicates = Hash Table $\mathcal{O}(n)$ space!)*
6. **Type 5:** Circular List Insertion (`LC 708`)
7. **Type 6:** Multiple Lists & Zipper Merge (`LC 21`, `LC 2`, `LC 445`, `LC 23`)
8. **Type 7:** Fast & Slow Pointers / Tortoise & Hare (`LC 141`, `LC 876`, `LC 2095`, `LC 142`)
9. **Type 8:** Hash Table Augmented (`LC 138` Random Pointer, `LC 1836`)
10. **Type 9:** Custom Data Structures: DLL + HashMap (`LC 146` LRU Cache, `LC 1472`)
11. **Type 10:** Divide & Conquer / Tree Hybrids (`LC 148` Sort List, `LC 426`, `LC 430`, `LC 237`)

👉 **Deep Dive Guides:** [90% Linked List Taxonomy Guide](./02_linked_lists/linked_list_90_percent_taxonomy.md) | [Linked List Master Cheat Sheet](./cheat_sheets/linked_list_master_cheat_sheet.md) | [Convert Binary in Linked List (LC 1290)](./02_linked_lists/1290_convert_binary_number_in_a_linked_list_to_integer.md) | [Swapping Nodes in a Linked List (LC 1721)](./02_linked_lists/1721_swapping_nodes_in_a_linked_list.md) | [Reverse Linked List (LC 206)](./02_linked_lists/206_reverse_linked_list.md) | [Merge Two Sorted Lists (LC 21)](./02_linked_lists/21_merge_two_sorted_lists.md) | [Remove Duplicates (LC 83)](./02_linked_lists/83_remove_duplicates_from_sorted_list.md) | [Palindrome Linked List (LC 234)](./02_linked_lists/234_palindrome_linked_list.md) | [Linked List Fundamentals](./02_linked_lists/01_linked_list_fundamentals.md)

---

## 💡 12. Python Under-the-Hood & Interview Pro Tips

### ⚡ 12.1. The Python Loop Speed Hierarchy: Direct vs. Range vs. While

Many candidates wonder: *"Does loop syntax actually matter in Python?"*  
**Answer: YES, dramatically!** The difference can be the difference between **3 ms (Beats 30%)** and **0 ms (Beats 100%)** on LeetCode.

```text
🥇 FASTEST:  for ch in s:              (Direct C-Pointer Iteration)
🥈 MIDDLE:   for i in range(len(s)):   (Range Index Generation)
🥉 SLOWEST:  while i < len(s):         (Manual Bytecode While Loop)
```

#### Why is `for ch in s` faster than `for i in range(len(s))`?

Look at what Python has to do on **every single iteration**:

| What happens in: `for i in range(len(s)): s[i]` | What happens in: `for ch in s:` |
| :--- | :--- |
| 1. `len(s)` computes string length. | 1. Internal C pointer advances 1 memory address. |
| 2. `range()` iterator generates an integer object `i`. | 2. Yields the character directly to your variable. |
| 3. `s[i]` performs array bounds check (`0 <= i < len`). | **No integer objects created, no bounds check!** |
| 4. Fetches the character object. | **Runs entirely in compiled C machine code.** |

#### 🎯 The Golden Rule for Loop Selection:
* **Default to `for item in collection:`** whenever you only need the value.
* **Use `for i, item in enumerate(collection):`** when you need *both* the index and the value.
* **Use `for i in range(n):`** only when generating synthetic numbers or step jumps.
* **Only use `while`** when step sizes are dynamic (e.g. `i += k`), pointers squeeze inwards (`while l < r:`), or checking node pointers (`while fast and fast.next:`).

---

### 🎒 12.2. The 4 Golden Python Micro-Rules for High-Performance DSA

You don't need obscure hacks to write blazing-fast Python. Remember these 4 core idioms:

1. **Iterate items directly:**  
   `for ch in s:` ✅  
   `for i in range(len(s)): s[i]` ❌ *(unless indices are strictly needed)*.
2. **Use Python "Truthiness" for empty checks:**  
   `if not stack:` ✅ (evaluates directly in C via `tp_as_sequence->sq_length == 0`)  
   `if len(stack) == 0:` ❌ (involves function call overhead and integer comparison).
3. **Check mathematical invariants BEFORE starting loops:**  
   In [LC 20: Valid Parentheses](./03_stacks_and_queues/20_valid_parentheses.md):  
   Every opening bracket requires a closing bracket. A valid string **can never have an odd length**!  
   ```python
   if len(s) % 2 != 0:
       return False  # Instant O(1) early exit before touching stack/memory!
   ```
4. **Combine Peek + Pop in short-circuit evaluation:**  
   Instead of checking `stack[-1]` in an `elif` and calling `stack.pop()` in `else`:
   ```python
   # Combined in 1 line:
   if not stack or stack.pop() != expected:
       return False
   ```

---

### 📥 12.3. The "Push-Expected" Stack Pattern (LC 20)

When matching pairs (parentheses, tags, brackets), beginners map `closing -> opening` and constantly check `stack[-1]`.

Top-tier candidates flip the logic: **Map opening brackets to what you EXPECT to see next!**

```python
class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2 != 0:
            return False  # Early exit on odd length

        mapping = {'(': ')', '[': ']', '{': '}'}
        stack = []

        for ch in s:
            if ch in mapping:
                stack.append(mapping[ch])  # Push the EXPECTED closer!
            elif not stack or stack.pop() != ch:
                return False

        return not stack
```

#### 💡 Why "Push-Expected" is Superior:
* When you see `'('`, you push `')'` to the stack.
* When you encounter a closing character (`')'`), **you don't even need a dictionary lookup!** You just pop and compare directly: `stack.pop() != ch`.
* This **cuts dictionary lookups in half** (lookup only occurs on opening brackets)!

---

### 🪜 12.4. Telescoping Sums & Interval Decomposition

#### The Big Idea: The Staircase Analogy
Suppose you walk from **Floor 1 to Floor 5**:
* **Direct Calculation:** $\text{Top} - \text{Bottom} = 5 - 1 = \mathbf{4}$
* **Step-by-Step Sum:** $(2 - 1) + (3 - 2) + (4 - 3) + (5 - 4) = 1 + 1 + 1 + 1 = \mathbf{4}$

Both give the **exact same answer**. The intermediate steps cancel out:
$$(C - A) = (B - A) + (C - B)$$

#### 🎯 When to Use This in Interviews?
Ask yourself: **"Can I break a multi-day / multi-step action into single 1-step moves with ZERO penalty?"**

1. **When it WORKS (e.g. Stock II - LC 122):**  
   You have **unlimited transactions** and no fees. Holding a stock for 5 days is mathematically identical to buying and selling every single day!  
   👉 *Action:* Don't track valleys or peaks. Just loop through adjacent pairs: `if prices[i] > prices[i-1]: profit += prices[i] - prices[i-1]`.
2. **When it FAILS (e.g. Stock I - LC 121):**  
   You are strictly limited to **1 transaction total**. If you cash out on Day 2, your quota is spent. You cannot break it into daily steps.  
   👉 *Action:* Forced to track the single lowest day (`min_price`).

*👉 See [`122_best_time_to_buy_and_sell_stock_ii.md`](./01_arrays_and_pointers/122_best_time_to_buy_and_sell_stock_ii.md) for the complete problem walkthrough.*



