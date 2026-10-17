# DSA Patterns Master Study Guide

A single-page map of the 13 core DSA patterns, when to reach for each one, and the traps that cause bugs or Time Limit Exceeded (TLE).

## How to pick a pattern in 10 seconds

* **Sorted array with $\mathcal{O}(\log n)$ target or monotonic condition:** Reach for **Binary Search** (exact match, occurrence boundary, or search on answer).
* **Sorted array looking for pairs, triplets, or palindrome symmetry:** Reach for **Two Pointers** (squeeze inward from ends).
* **In-place array partitioning or compaction (zeros/duplicates):** Reach for **Fast & Slow Two Pointers** (scout and writer).
* **Contiguous subarray/substring with fixed length $K$ or dynamic constraint:** Reach for **Sliding Window** (expand right, shrink left when invalid).
* **Max contiguous subarray sum with negative values:** Reach for **Kadane's Algorithm** (reset when running sum $< 0$).
* **Range sum queries $[L, R]$ or pivot balance index:** Reach for **Prefix Sum & Seesaw Balance**.
* **Sum of all subarrays or contribution to totals:** Reach for **Contribution Technique** ($(i+1)(N-i)$ multiplier).
* **LIFO matching (parentheses, undo, next greater element):** Reach for **Stack** (or Monotonic Stack).
* **Linked list manipulation (cycles, middle, reverse):** Reach for **Fast & Slow Pointers (Tortoise & Hare)** or **4-Step Pointer Flip**.
* **Tree/Graph traversal:** **BFS** for shortest unweighted path/levels; **DFS** for exhaustively exploring branches/components.
* **Combinations, permutations, subsets, or constraint grids:** Reach for **Backtracking** (choose, explore, un-choose).
* **Top $K$ elements or continuous running median:** Reach for **Heaps / Priority Queues**.
* **Pairwise cancellation or bit masks:** Reach for **Bit Manipulation** (XOR, bitwise shifts).


## Pattern Index

| # | Pattern | Trigger Clue | Target Complexity | Cheat Sheet |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Arrays, Strings & HashMaps** | $\mathcal{O}(1)$ complement lookup, frequency counting, grouping | $\mathcal{O}(n)$ time, $\mathcal{O}(n)$ space | [Arrays & HashMaps](./cheat_sheets/arrays_hashmaps_cheat_sheet.md) |
| 2 | **Prefix Sum & Seesaw Balance** | Range sums $[L, R]$, pivot index, left vs. right split | $\mathcal{O}(n)$ time, $\mathcal{O}(1)$–$\mathcal{O}(n)$ space | [Prefix Sum Cheat Sheet](./cheat_sheets/prefix_sum_seesaw_cheat_sheet.md) |
| 3 | **Subarrays & Contribution** | Sum across all subarrays, leaders, closest min-max | $\mathcal{O}(n)$ time, $\mathcal{O}(1)$ space | [Subarrays Cheat Sheet](./cheat_sheets/subarrays_and_contribution_technique_cheat_sheet.md) |
| 4 | **2D Matrix Manipulation** | Diagonals, in-place 90° rotation, spiral order | $\mathcal{O}(R \cdot C)$ time, $\mathcal{O}(1)$ space | [2D Matrix Cheat Sheet](./cheat_sheets/matrix_2d_manipulation_cheat_sheet.md) |
| 5 | **Two Pointers** | Sorted pair sums, palindromes, in-place array compaction | $\mathcal{O}(n)$ time, $\mathcal{O}(1)$ space | [Two Pointers Cheat Sheet](./cheat_sheets/two_pointers_cheat_sheet.md) |
| 6 | **Sliding Window** | Longest/shortest/max contiguous subarray or substring | $\mathcal{O}(n)$ time, $\mathcal{O}(1)$–$\mathcal{O}(k)$ space | [Sliding Window Cheat Sheet](./cheat_sheets/sliding_window_cheat_sheet.md) |
| 7 | **Kadane's Algorithm** | Max contiguous subarray sum when negative numbers exist | $\mathcal{O}(n)$ time, $\mathcal{O}(1)$ space | [Kadane's Cheat Sheet](./cheat_sheets/kadanes_algorithm_cheat_sheet.md) |
| 8 | **Greedy & ATM Subtraction** | Max reach horizon, earliest finish interval, unit breakdown | $\mathcal{O}(n)$ or $\mathcal{O}(n \log n)$ | [Greedy](./cheat_sheets/greedy_cheat_sheet.md) / [ATM Pattern](./cheat_sheets/greedy_subtraction_atm_cheat_sheet.md) |
| 9 | **Binary Search** | Sorted array, rotated array, index parity, min/max feasibility | $\mathcal{O}(\log n)$ time, $\mathcal{O}(1)$ space | [Binary Search Cheat Sheet](./cheat_sheets/binary_search_cheat_sheet.md) |
| 10 | **Linked Lists** | In-place pointer reversal, cycle detection, zipper merge | $\mathcal{O}(n)$ time, $\mathcal{O}(1)$ space | [Linked List Cheat Sheet](./cheat_sheets/linked_list_master_cheat_sheet.md) |
| 11 | **BFS & DFS** | Shortest path on unweighted grid (BFS), tree depth/islands (DFS) | $\mathcal{O}(V + E)$ | [BFS vs. DFS Cheat Sheet](./cheat_sheets/bfs_dfs_cheat_sheet.md) |
| 12 | **Backtracking & Heaps** | Generate all subsets/permutations; track Top $K$ elements | $\mathcal{O}(2^n)$ / $\mathcal{O}(n \log k)$ | [Backtracking](./cheat_sheets/backtracking_cheat_sheet.md) / [Heaps](./cheat_sheets/heaps_priority_queues_cheat_sheet.md) |
| 13 | **Bit Manipulation** | Single number XOR, power of 2, bit stream accumulation | $\mathcal{O}(1)$ space | [Bitwise Cheat Sheet](./cheat_sheets/bitwise_cheat_sheet.md) |

---

## 1. Arrays, Strings & HashMaps
- **Never concatenate strings in a loop (`s += ch`):** Strings are immutable in Python, so `s += ch` copies the whole string each step ($\mathcal{O}(n^2)$). Append to a `list` and call `"".join(res)` ($\mathcal{O}(n)$).
- **Avoid `val in my_dict.values()` inside a loop ([LC 290](./01_arrays_and_pointers/290_word_pattern.md)):** Dictionary keys are hashed ($\mathcal{O}(1)$), but `.values()` does a linear scan ($\mathcal{O}(n)$). Use two dicts or a `seen` set for 1-to-1 mappings.
- **Right-to-left carry ([LC 66](./01_arrays_and_pointers/66_plus_one.md)):** Walk backward from the last digit; if `digits[i] < 9`, increment and return immediately. If `9`, set to `0` and let the loop carry leftward.

---

## 2. Prefix Sum & Seesaw Balance
- **Range sum `[L..R]` in $\mathcal{O}(1)$:** `pref[R] - (pref[L - 1] if L > 0 else 0)`.
- **Seesaw pivot equation ([LC 724](./01_arrays_and_pointers/724_find_pivot_index.md)):** Compute `total = sum(nums)` once. As you walk left-to-right tracking `left_sum`, the right sum is `total - left_sum - nums[i]`. Check the balance condition **before** adding `nums[i]` to `left_sum`.
- **Parity shift on deletion ([00_prefix_sums](./01_arrays_and_pointers/00_prefix_sums_and_special_index_queries.md), LC 1664):** Deleting index `i` shifts every element after `i` left by 1, swapping their even and odd indices (`new_even = even_L + odd_R`).

---

## 3. Subarrays & Contribution Technique
- **Total subarrays of length $N$:** $\frac{N(N+1)}{2}$.
- **Contribution formula ([00_subarrays](./01_arrays_and_pointers/00_subarray_mechanics_and_contribution_technique.md)):** Index `i` appears in $(i + 1)(N - i)$ subarrays (`i + 1` choices for start $L \le i$, `N - i` choices for end $R \ge i$). Multiply `arr[i] * (i + 1) * (N - i)` to sum all subarrays in $\mathcal{O}(N)$ time.

---

## 4. 2D Matrix Manipulation
- **Diagonals ([00_matrix](./01_arrays_and_pointers/00_matrix_2d_arrays_and_rotations.md)):** Main diagonal has `r == c` (and `r - c == const`); anti-diagonal has `r + c == N - 1` (and `r + c == const`).
- **In-place 90° clockwise rotation (LC 48):** Transpose across the main diagonal (`for r in range(n): for c in range(r + 1, n): swap`), then reverse each row (`row.reverse()`).

---

## 5. Two Pointers (6 Formations)
1. **The Squeeze (`l = 0, r = n - 1`):** Walk inward from both ends ([LC 11](./01_arrays_and_pointers/11_container_with_most_water.md), [LC 15](./01_arrays_and_pointers/15_3sum.md), [LC 125](./01_arrays_and_pointers/125_valid_palindrome.md), [LC 167](./01_arrays_and_pointers/167_two_sum_ii_input_array_is_sorted.md)). In a sorted array, `l += 1` increases the sum and `r -= 1` decreases the sum.
2. **Scout & Writer (`slow = 0, fast = 0`):** Filter or compact an array in place ([LC 26](./01_arrays_and_pointers/26_remove_duplicates_from_sorted_array.md), [LC 27](./01_arrays_and_pointers/27_remove_element.md), [LC 80](./01_arrays_and_pointers/80_remove_duplicates_from_sorted_array_ii.md), [LC 283](./01_arrays_and_pointers/283_move_zeroes.md)).
3. **Two Conveyor Belts (`p1 = 0, p2 = 0`):** Match across two separate sequences ([LC 392](./01_arrays_and_pointers/392_is_subsequence.md)).
4. **Anchor & Scout:** Group non-overlapping consecutive runs ([LC 228](./01_arrays_and_pointers/228_summary_ranges.md)).
5. **Tail-Buffer (Right-to-Left):** Fill into trailing empty buffer slots from the back so you never overwrite unread items ([LC 88](./01_arrays_and_pointers/88_merge_sorted_array.md)).
6. **Outward Expand (Flashlight Beam):** Expand `(i, i)` and `(i, i + 1)` outward to find palindromic substrings ([LC 5](./01_arrays_and_pointers/5_longest_palindromic_substring.md)).

---

## 6. Sliding Window
- **Fixed window of size $K$ ([LC 643](./01_arrays_and_pointers/643_maximum_average_subarray_i.md), [LC 1456](./01_arrays_and_pointers/1456_maximum_number_of_vowels_in_a_substring_of_given_length.md)):** Add entering item `nums[i]` and subtract leaving item `nums[i - k]` in $\mathcal{O}(1)$.
- **Dynamic window ([LC 3](./01_arrays_and_pointers/3_longest_substring_without_repeating_characters.md)):** Expand `right` each step, and use a `while` loop to advance `left` whenever the window condition is broken. Window size is `right - left + 1`.

---

## 7. Kadane's Algorithm & Greedy
- **Kadane's rule ([LC 53](./01_arrays_and_pointers/53_maximum_subarray.md)):** `cur_sum = max(num, cur_sum + num)`. Drop the running prefix the instant it turns negative. Initialize `max_sum = nums[0]` (never `0`) so all-negative arrays work.
- **Telescoping sums ([LC 122](./01_arrays_and_pointers/122_best_time_to_buy_and_sell_stock_ii.md)):** With unlimited trades, summing every positive step `prices[i] - prices[i - 1] > 0` equals the full valley-to-peak profit. With only 1 trade allowed ([LC 121](./01_arrays_and_pointers/121_best_time_to_buy_and_sell_stock.md)), track the running `min_price` instead.

---

## 8. Binary Search (7 Archetypes)
1. **Exact match:** `lo <= hi`, `mid = lo + (hi - lo) // 2`.
2. **First / last occurrence ([01_occurrences](./05_binary_search/01_binary_search_fundamentals_and_occurrences.md), LC 34):** Save `ans = mid`, then keep searching left (`hi = mid - 1`) or right (`lo = mid + 1`).
3. **Peak / local minimum ([02_local_minima](./05_binary_search/02_local_minima_and_peak_finding.md), LC 162):** Follow the rising slope for a peak or the falling slope for a valley.
4. **Index parity ([03_index_parity](./05_binary_search/03_index_parity_single_element_in_duplicates.md), LC 540):** Pairs start at even indices before the single element and odd indices after it.
5. **Rotated sorted array ([04_rotated](./05_binary_search/04_search_in_rotated_sorted_array.md), LC 33):** Check `nums[lo] <= nums[mid]` to see which half is sorted, then check if `target` lies inside that half.
6. **Infinite array ([05_exponential](./05_binary_search/05_exponential_search_infinite_arrays.md), LC 702):** Double `hi` (`1, 2, 4, 8...`) until `arr[hi] >= target`, then binary search `[lo, hi]`.
7. **Binary search on the answer ([06_search_on_answer](./05_binary_search/06_binary_search_on_answer_greedy_predicates.md), LC 875, 410):** Binary search the capacity/speed range `[lo, hi]` using a greedy `can_finish(mid)` check.

---

## 9. Linked Lists, Stacks, Trees & Heaps
- **Linked List 4-step reversal ([LC 206](./02_linked_lists/206_reverse_linked_list.md)):** `nxt = cur.next; cur.next = prev; prev = cur; cur = nxt`, then `return prev`.
- **Push-expected stack ([LC 20](./03_stacks_and_queues/20_valid_parentheses.md)):** When you see an opening bracket `'('`, push its expected closer `')'` onto the stack so closing checks only need `not stack or stack.pop() != ch`.
- **Top-$K$ Heap ([Heaps Cheat Sheet](./cheat_sheets/heaps_priority_queues_cheat_sheet.md)):** Use a **Min-Heap** of size $K$ to track the $K$ **largest** elements (pop whenever `len(heap) > k`).

---

## 10. Python Speed & Loop Rules
1. **`for x in nums` beats `for i in range(len(nums))`:** Direct iteration advances a C pointer without allocating integer index objects or running bounds checks on `nums[i]`. Use `enumerate(nums)` when you need both index and value.
2. **Use `if not stack:` instead of `if len(stack) == 0:`:** Direct C struct length check without `len()` function call overhead.
3. **Check $\mathcal{O}(1)$ parity/length invariants before looping:** In [LC 20: Valid Parentheses](./03_stacks_and_queues/20_valid_parentheses.md), `if len(s) % 2 == 1: return False` exits immediately before allocating a stack.
