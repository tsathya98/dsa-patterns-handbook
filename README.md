# 🚀 Data Structures & Algorithms (DSA) Interview Master Guide

> **Course Reference:** AlgoMaster.io, NeetCode 150 & freeCodeCamp LeetCode Patterns  
> **Repository:** `~/Developer/projects/dsa/`  
> **Goal:** Build intuitive, pattern-based thinking for coding interviews without rote memorization.

---

## 🗺️ How This Repository Is Organized

| Document / Tool | Purpose | How to Use It |
|---|---|---|
| 📑 **[README.md](./README.md)** | **The Central Index** | Your master roadmap and directory. |
| 📊 **[Daily DSA Tracker](./tracker.html)** | **Interactive Progress Dashboard** | Visual timeline of problems solved per day, difficulty breakdown, and LocalStorage persistence. |
| 🗺️ **[FAANG 10-Week Roadmap UI](./faang_plan.html)** | **Interactive Roadmap & Pacing** | Tabbed phases (Phase 1–4), weekly quotas (2 weekdays / 5 weekends), milestone checklist. |
| 🧭 **[dsa_patterns_study_guide.md](./dsa_patterns_study_guide.md)** | **Universal Pattern Master Guide** | The 9 core algorithmic patterns with visual templates and Big-O cheat sheets. |
| 📚 **[`cheat_sheets/`](./cheat_sheets/)** | **High-Yield Pattern Reference** | 12 dedicated cheat sheets for Two Pointers, Sliding Window, DP, Trees, Graphs, etc. |
| 📁 **`00_foundations/`** | **Algorithm Fundamentals & Big-O** | Correctness vs. efficiency, counting elementary steps, Big-O simplification, loop archetypes. |
| 📁 **`01_arrays_and_pointers/`** | **Arrays & Transformations** | Clean in-place array manipulation, Two Pointers, Sliding Window, Kadane, Prefix Sums. |
| 📁 **`02_linked_lists/`** | **Linked Lists Masterclass** | 11 Archetypes, Floyd Cycle, In-Place Reversals, Zipper Merges, LRU Cache. |
| 📁 **`03_stacks_and_queues/`** | **Stacks & Monotonicity** | LIFO plates, monotonic stacks, calculator parsers, parentheses validators. |
| 📁 **`04_sorting/`** | **Sorting Algorithms from Scratch** | Bubble, Selection, Insertion, Merge, Quick Sort + Decision Matrix. |

---

## 🏛️ 0. Foundations & Algorithm Complexity (Airtribe Cohort)
First principles of algorithmic thinking, counting elementary operations, and Big-O mastery:

* [📐 **01. Algorithms, Correctness & Efficiency**](./00_foundations/01_algorithms_correctness_efficiency.md) – What makes an algorithm "good", why wall-clock stopwatches fail, counting elementary operations, and payroll scaling.
* [⚡ **02. Time & Space Complexity and Big-O Notation**](./00_foundations/02_time_and_space_complexity_big_o.md) – Big-O simplification rules, dominant terms, the 6 core loop archetypes (linear, halving, quadratic, break trap), and auxiliary space vs total space.
* [📊 **Time & Space Complexity Master Cheat Sheet**](./cheat_sheets/time_and_space_complexity_cheat_sheet.md) – 3-second decision table, input size ($N$) constraint limits, and common loop pattern speed ladder.

---

## 🗂️ 1. Sorting Algorithms Series (AlgoMaster.io & Cohort)
Learn how comparison-based sorting works from first principles:

* [🫧 **08. Bubble Sort – Complete Guide & Intuition**](./04_sorting/08_bubble_sort.md) – Adjacent swapping, soda bubble analogy, and the early termination `swapped` flag.
* [🎯 **09. Selection Sort – Complete Guide & Intuition**](./04_sorting/09_selection_sort.md) – Finding minimums, minimal write swaps, unstable swapping, and why early termination is impossible.
* [🃏 **10. Insertion Sort – Complete Guide & Intuition**](./04_sorting/10_insertion_sort.md) – Card player shifting technique, adaptive $\mathcal{O}(n)$ on nearly-sorted data.
* [🌲 **11. Merge Sort – Complete Guide & Intuition**](./04_sorting/11_merge_sort.md) – Divide and conquer, two-way zipper merge, guaranteed $\mathcal{O}(n \log n)$ time.
* [⚡ **12. Quick Sort – Complete Guide & Intuition**](./04_sorting/12_quick_sort.md) – Pivot partitioning (Lomuto scheme), in-place recursion, and average vs. worst-case.
* [📊 **13. Ultimate Sorting Cheat Sheet & Decision Tree**](./cheat_sheets/13_sorting_cheat_sheet.md) – Comparison matrix of all 10 sorting algorithms + interview decision tree.

---

## 📑 2. Linked List Masterclass Series
Master pointer mechanics and in-place manipulations:

* [🧠 **01. Linked List Fundamentals: How to Think Like a Computer**](./02_linked_lists/01_linked_list_fundamentals.md) – Node anatomy, pointer mechanics (`curr = curr.next` vs `curr.next = ...`), garbage collection, and the Train & Anchor analogy.
* [🔢 **02. Add Two Numbers (LeetCode 2)**](./02_linked_lists/02_add_two_numbers.md) – Reverse-order addition, carry propagation, and deep dive into `cur = dummy`.
* [🔄 **03. Reverse a Linked List (LeetCode 206)**](./02_linked_lists/206_reverse_linked_list.md) – The Preschool Conga Line 4-beat dance, why `cur` steps into `None`, and why you must `return prev`.
* [🪢 **04. Merge Two Sorted Lists (LeetCode 21)**](./02_linked_lists/21_merge_two_sorted_lists.md) – The zipper merge technique with a dummy anchor.
* [✂️ **05. Remove N-th Node From End (LeetCode 19)**](./02_linked_lists/05_remove_nth_node_from_end.md) – The measuring stick / runner technique in a single pass.
* [🔁 **06. Linked List Cycle Detection (LeetCode 141 & 142)**](./02_linked_lists/06_linked_list_cycle.md) – Floyd's Tortoise and Hare race track pattern.
* [🔄 **07. Reorder List (LeetCode 143)**](./02_linked_lists/143_reorder_list.md) – The 3-in-1 Triple Crown (Find Middle + In-Place Reversal + Zipper Merge).
* [✂️ **08. Remove Duplicates from Sorted List (LeetCode 83)**](./02_linked_lists/83_remove_duplicates_from_sorted_list.md) – In-place pointer skipping, why `cur` must stay put during duplicates, and `return head` vs `return dummy.next`.
* [🪞 **09. Palindrome Linked List (LeetCode 234)**](./02_linked_lists/234_palindrome_linked_list.md) – Two Pointers Squeeze vs. The In-Place Triple Crown (Tortoise & Hare Middle + Conga Line Reversal + $\mathcal{O}(1)$ Space Verification).
* [🔄 **10. Swapping Nodes in a Linked List (LeetCode 1721)**](./02_linked_lists/1721_swapping_nodes_in_a_linked_list.md) – The Measuring Stick / Offset Two Pointers technique, fencepost steps (k-1), and avoiding direction-dependent reconstruction bugs.
* [⚡ **11. Convert Binary Number in a Linked List to Integer (LeetCode 1290)**](./02_linked_lists/1290_convert_binary_number_in_a_linked_list_to_integer.md) – Horner's stream accumulator, avoiding $\mathcal{O}(n^2)$ string copying, and bitwise shift-and-OR.
* 🗺️ [**The 90% Linked List Master Taxonomy & Archetype Guide**](./02_linked_lists/linked_list_90_percent_taxonomy.md) – Based on the viral LeetCode masterclass: The 11 archetypes, decision tree, visual templates, and complete 30+ problem checklist.

---

## 📚 3. Two Pointers & Array Patterns
Learn when and how to avoid nested $\mathcal{O}(n^2)$ loops:

* [📊 **Two Pointers Master Cheat Sheet & Decision Guide**](./cheat_sheets/two_pointers_cheat_sheet.md) – Quick reference: The 3 formations (Squeeze, Scout & Writer, Conveyor Belts), 3-second mental triggers, and decision matrix.
* [🪣 **11. Container With Most Water (LeetCode 11)**](./01_arrays_and_pointers/11_container_with_most_water.md) – Two pointers from opposite ends, greedy choice proof, fast-forward micro-optimizations, and FAANG/Google interview strategies.
* [🎯 **15. 3Sum (LeetCode 15)**](./01_arrays_and_pointers/15_3sum.md) – 1 Anchor + Squeeze, the Volume Knob steering rule, the Clothing Outfit analogy for skipping duplicates, and the 4 speedup optimizations.
* [🏃 **392. Is Subsequence (LeetCode 392)**](./01_arrays_and_pointers/392_is_subsequence.md) – Dual-sequence synchronization, beginner traps (dict & `.index()`), the 3-question Two-Pointer checklist, and binary search follow-up.
* [📈 **122. Best Time to Buy and Sell Stock II (LeetCode 122)**](./01_arrays_and_pointers/122_best_time_to_buy_and_sell_stock_ii.md) – Valley-to-Peak vs. Telescoping daily step accumulation, unlimited transactions, and why it is pure Greedy (not Kadane).
* [🏛️ **13. Roman to Integer (LeetCode 13)**](./01_arrays_and_pointers/13_roman_to_integer.md) – Lookahead subtraction rule, why nested dict/list lookups cost 6 ms, and the 2-ms direct comparison optimization.
* [🏛️ **12. Integer to Roman (LeetCode 12)**](./01_arrays_and_pointers/12_integer_to_roman.md) – The ATM / Cashier Greedy Subtraction pattern, why repeated subtraction `while` loop beats division in interviews, and code comparison.
* [🪟 **643. Maximum Average Subarray I (LeetCode 643)**](./01_arrays_and_pointers/643_maximum_average_subarray_i.md) – Fixed-size sliding window, the running differential pattern (add new, subtract old), eliminating TLE, and why deferred division is 1.6x faster.
* [🔤 **1456. Maximum Number of Vowels in a Substring of Given Length (LeetCode 1456)**](./01_arrays_and_pointers/1456_maximum_number_of_vowels_in_a_substring_of_given_length.md) – Running differential on frequency counters, the `s[k]` vs `s[i]` indexing trap, and why `count` can mathematically never drop below 0.
* [🏃 **283. Move Zeroes (LeetCode 283)**](./01_arrays_and_pointers/283_move_zeroes.md) – Fast & Slow pointers (Scout & Writer), the Snowplow / Wall of Zeros visual diagram, and why `slow += 1` handles consecutive zeros cleanly.
* [🔠 **290. Word Pattern (LeetCode 290)**](./01_arrays_and_pointers/290_word_pattern.md) – Bijective (1-to-1) mapping, why `in dict.values()` is an $\mathcal{O}(k)$ linear scan trap (290x slower), and the two pure $\mathcal{O}(n)$ solutions (Two Maps & Set Cardinality).
* [⚖️ **724. Find Pivot Index (LeetCode 724)**](./01_arrays_and_pointers/724_find_pivot_index.md) – Prefix Sum (The Seesaw Balance Pattern), total sum conservation, eliminating $\mathcal{O}(n^2)$ slicing to achieve a 123x speedup.
* [🧱 **20. Valid Parentheses (LeetCode 20)**](./03_stacks_and_queues/20_valid_parentheses.md) – Cafeteria plate stack analogy, instant $\mathcal{O}(1)$ odd-length pruning, and the "Push-Expected" 0-ms pattern.
* [🎯 **678. Valid Parenthesis String (LeetCode 678 - Medium)**](./03_stacks_and_queues/678_valid_parenthesis_string.md) – Two Stacks (Indices) pattern for wildcard characters (`*`), handling index ordering, and greedy cleanup.
* [📊 **228. Summary Ranges (LeetCode 228)**](./01_arrays_and_pointers/228_summary_ranges.md) – Two Pointers Formation D (Anchor & Scout), eliminating lost-tail bugs, and consecutive chunking.
* [🚗 **66. Plus One (LeetCode 66)**](./01_arrays_and_pointers/66_plus_one.md) – The Car Odometer pattern, why integer string conversion is rejected in interviews, and schoolbook carry propagation.
* [🪢 **88. Merge Sorted Array (LeetCode 88)**](./01_arrays_and_pointers/88_merge_sorted_array.md) – Two Pointers Formation E (The Tail-Buffer / Reverse Placement Pattern), avoiding the Bulldozer Overwrite collision, and why `while p1 >= 0` is omitted.
* [✂️ **27. Remove Element (LeetCode 27)**](./01_arrays_and_pointers/27_remove_element.md) – Two Pointers Formation B (Scout & Writer / Fast & Slow), in-place clean zone partitioning, and the swap-with-tail follow-up.
* [✂️ **26. Remove Duplicates from Sorted Array (LeetCode 26)**](./01_arrays_and_pointers/26_remove_duplicates_from_sorted_array.md) – Two Pointers Formation B (Scout & Writer), the Sorted vs. Unsorted duplicate rule, and why `Counter` is an interview space trap.
* [✂️ **80. Remove Duplicates from Sorted Array II (LeetCode 80 - Medium)**](./01_arrays_and_pointers/80_remove_duplicates_from_sorted_array_ii.md) – Two Pointers Formation B (Scout & Writer with streak state machine) and the Senior FAANG Lookback $M$ formula (`x != nums[k - M]`).
* [🗳️ **169. Majority Element (LeetCode 169)**](./01_arrays_and_pointers/169_majority_element.md) – Boyer-Moore Voting Algorithm, Battle Royale 1-for-1 mutual cancellation, Tug-of-War invariant, and Python bytecode `elif` optimization.
* [🔄 **189. Rotate Array (LeetCode 189 - Medium)**](./01_arrays_and_pointers/189_rotate_array.md) – Pythonic slice replacement vs. The FAANG $\mathcal{O}(1)$ space Triple Reversal Algorithm (Two Pointers Formation A Squeeze).
* [📈 **121. Best Time to Buy and Sell Stock (LeetCode 121)**](./01_arrays_and_pointers/121_best_time_to_buy_and_sell_stock.md) – Running minimum tracking, avoiding `min()/max()` function overhead, and the Kadane Maximum Subarray equivalence.
* [🎮 **55. Jump Game (LeetCode 55 - Medium)**](./01_arrays_and_pointers/55_jump_game.md) – The Horizon / Laser Reach greedy expansion pattern (`max_reach = max(max_reach, i + jump)`), quicksand zero traps, and eliminating $\mathcal{O}(n^2)$ recursion.
* [📊 **274. H-Index (LeetCode 274 - Medium)**](./01_arrays_and_pointers/274_h_index.md) – The Runner Finish Line rank comparison, greedy descending sort $\mathcal{O}(n \log n)$ vs counting sort $\mathcal{O}(n)$, and handling all tie-breaks.
* [🎯 **125. Valid Palindrome (LeetCode 125)**](./01_arrays_and_pointers/125_valid_palindrome.md) – Two Pointers Formation A (Inward Squeeze), skipping non-alphanumeric characters, and why $\mathcal{O}(1)$ auxiliary space beats string reversal.
* [🎯 **392. Is Subsequence (LeetCode 392)**](./01_arrays_and_pointers/392_is_subsequence.md) – Two Pointers Formation C (Two Conveyor Belts), checklist matching, and the HashMap + Binary Search follow-up for $10^9$ queries.
* [🎯 **167. Two Sum II - Input Array Is Sorted (LeetCode 167 - Medium)**](./01_arrays_and_pointers/167_two_sum_ii_input_array_is_sorted.md) – Two Pointers Formation A (Inward Squeeze), why HashMap is rejected for $\mathcal{O}(1)$ space constraint, and sum steering rules.
* [🪣 **11. Container With Most Water (LeetCode 11 - Medium)**](./01_arrays_and_pointers/11_container_with_most_water.md) – Two Pointers Formation A (Inward Squeeze) with Greedy Bottleneck rule, mathematical proof of why the shorter wall must move, and reducing Python overhead.
* [🎯 **15. 3Sum (LeetCode 15 - Medium)**](./01_arrays_and_pointers/15_3sum.md) – Two Pointers (Fixed Anchor + Inward Squeeze), eliminating $\mathcal{O}(n^3)$ brute force, in-place deduplication without sets, and positive-anchor early pruning.
* [🍞 **238. Product of Array Except Self (LeetCode 238 - Medium)**](./01_arrays_and_pointers/238_product_of_array_except_self.md) – Prefix & Suffix Accumulator (The Sandwich Pattern), eliminating division operations, and reducing auxiliary space from $\mathcal{O}(n)$ to $\mathcal{O}(1)$.
* [🪟 **3. Longest Substring Without Repeating Characters (LeetCode 3 - Medium)**](./01_arrays_and_pointers/3_longest_substring_without_repeating_characters.md) – Dynamic Sliding Window (The Rubber Band), eliminating $\mathcal{O}(n^3)$ substring rebuilds, and linear pass state maintenance with a hash set.

---

## 🧭 4. Algorithmic Patterns Master Study Guide & Cheat Sheets
For universal templates, mental models, and decision checklists across all major patterns:
👉 **[Open DSA Patterns Master Study Guide](./dsa_patterns_study_guide.md)**

* ⚡ [**Time & Space Complexity Master Cheat Sheet**](./cheat_sheets/time_and_space_complexity_cheat_sheet.md) – 3-second decision table, $N$-limit rules ($10^8$ operations/sec), and Big-O loop speed ladder.
* 🦅 [**Greedy Algorithms Master Cheat Sheet**](./cheat_sheets/greedy_cheat_sheet.md) – The 4 Archetypes (The Cashier, The Horizon, The Scheduler, The Accumulator), Greedy vs. Two Pointers distinction, and 3-second triggers.
* 🧱 [**Arrays, Strings & HashMaps Cheat Sheet**](./cheat_sheets/arrays_hashmaps_cheat_sheet.md) – Contiguous memory, avoiding $\mathcal{O}(n^2)$ string concatenation, Two-Sum complement trick.
* 🎯 [**Two Pointers Master Cheat Sheet**](./cheat_sheets/two_pointers_cheat_sheet.md) – Squeeze, Scout & Writer, Two Conveyor Belts.
* 🪟 [**Sliding Window Master Cheat Sheet**](./cheat_sheets/sliding_window_cheat_sheet.md) – The rubber-band technique for contiguous subarrays/substrings (Fixed vs. Dynamic).
* 🔍 [**Binary Search Master Cheat Sheet**](./cheat_sheets/binary_search_cheat_sheet.md) – Phonebook halving, avoiding infinite loops, and binary search on monotonic answers.
* 🌲 [**BFS vs. DFS Master Cheat Sheet**](./cheat_sheets/bfs_dfs_cheat_sheet.md) – The water ripple (shortest path) vs. the maze runner (tree depth & flood-fill).
* 🔄 [**Backtracking Master Cheat Sheet**](./cheat_sheets/backtracking_cheat_sheet.md) – Decision trees with an "Undo" button (Subsets, Permutations, Combinations).
* ⛰️ [**Priority Queues & Heaps Cheat Sheet**](./cheat_sheets/heaps_priority_queues_cheat_sheet.md) – Hospital ER triage, `heapq` in Python, and the Top-K Min-Heap pattern.
* 📈 [**Kadane's Algorithm Master Cheat Sheet**](./cheat_sheets/kadanes_algorithm_cheat_sheet.md) – The Toxic Debt analogy, Maximum Subarray (LC 53), stock differences, and circular arrays.
* 🏧 [**Greedy Subtraction (ATM Pattern) Cheat Sheet**](./cheat_sheets/greedy_subtraction_atm_cheat_sheet.md) – Decomposing quantities into canonical units (Roman numerals, currency change, time units), `while` vs `//` trade-offs.
* ⚖️ [**Prefix Sum (The Seesaw Balance) Cheat Sheet**](./cheat_sheets/prefix_sum_seesaw_cheat_sheet.md) – Total sum conservation, finding pivot/equilibrium indices in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.
* 🔗 [**Linked List Master Cheat Sheet**](./cheat_sheets/linked_list_master_cheat_sheet.md) – Russian nesting dolls mental model, `dummy` vs `cur`, in-place pointer stitching, and avoiding `TypeError: len()`.
* 🗺️ [**90% Linked List Master Taxonomy Guide**](./02_linked_lists/linked_list_90_percent_taxonomy.md) – The 11 archetypes classifying 90%+ of LeetCode linked list problems, 10-second classifier decision tree, and complete problem checklists.
* 🕹️ [**Bit Manipulation Master Cheat Sheet**](./cheat_sheets/bitwise_cheat_sheet.md) – The 6 silicon operators, Horner's stream shift, power-of-two check, Brian Kernighan bit clearing, and XOR cancellation.
