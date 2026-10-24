# DSA & System Design Study Handbook

Personal notes, pattern cheat sheets, and problem walkthroughs for Data Structures, Algorithms, and System Design (covering CodeKerdos lectures, LeetCode 75 / Top Interview 150, and distributed systems fundamentals).

## Quick Navigation

| Resource | What It Is |
| :--- | :--- |
| **[viewer.html](../generated/legacy/viewer.html)** | Offline-ready study viewer bundling all markdown notes in one sidebar UI. |
| **[tracker.html](../generated/legacy/tracker.html)** | Daily problem log and difficulty breakdown dashboard. |
| **[faang_plan.html](../generated/legacy/faang_plan.html)** | Interactive 12-week roadmap UI ([markdown version](../content/plans/faang_preparation_plan.md)). |
| **[dsa_patterns_study_guide.md](../content/plans/dsa_patterns_study_guide.md)** | All 13 core DSA patterns in one single-page summary. |
| **[`cheat_sheets/`](../content/cheat-sheets)** | 21 quick-reference pattern and system design cheat sheets. |

### Study Progression:
* **1. Foundations (`00_foundations/`):** Big-O asymptotic analysis, Python memory model, pointer references, primes, and iteration counting.
* **2. Arrays & Pointers (`01_arrays_and_pointers/`):** Two pointers, sliding window, prefix sums, seesaw pivot, contribution technique, and 2D matrix rotations.
* **3. Linked Lists (`02_linked_lists/`):** Dummy nodes, fast & slow pointers (Tortoise & Hare), and in-place 4-step pointer reversal.
* **4. Stacks, Sorting & Binary Search (`03_` to `05_`):** LIFO matching, monotonic stacks, elementary and divide-and-conquer sorting, and $\mathcal{O}(\log n)$ search spaces.
* **5. Recursion & Backtracking (`06_recursion_and_backtracking/`):** Call stack frames, branch exploration, and state backtracking.
* **6. System Design (`system_design/`):** Scalability, caching, database sharding, message queues, API gateways, and distributed resilience.


---

## 0. Foundations, Complexity & Python Internals (`00_foundations/`)

- [01. Algorithms, Correctness & Efficiency](../content/dsa/00_foundations/01_algorithms_correctness_efficiency.md) - Counting elementary operations instead of wall-clock seconds.
- [02. Time & Space Complexity (Big-O)](../content/dsa/00_foundations/02_time_and_space_complexity_big_o.md) - Simplification rules, loop archetypes, and auxiliary vs. total space.
- [03. Python Memory Model, Pointers & Core Collections](../content/dsa/00_foundations/03_python_memory_model_and_collections.md) - Pointers, dynamic arrays vs. lists, mutating lists inside tuples (`t[1].append()`), slice garbage collection, and hashability.
- [04. Factors, Primes & Iteration Counting](../content/dsa/00_foundations/04_factors_primes_and_iteration_counting.md) - Symmetric factor pairs in $\mathcal{O}(\sqrt{N})$, prime checks, and exact loop iteration formulas.
- [LC 1492: The kth Factor of n](../content/dsa/00_foundations/1492_the_kth_factor_of_n.md) - Two-pass $\mathcal{O}(\sqrt{N})$ time and $\mathcal{O}(1)$ space factor enumeration without sorting.

---

## 1. Arrays, Prefix Sums, Subarrays, Matrices & Two Pointers (`01_arrays_and_pointers/`)

### Concept Guides (CodeKerdos Classes 4-7)
- [Array Fundamentals, Max Elements & Leaders](../content/dsa/01_arrays_and_pointers/00_array_fundamentals_and_max_elements.md) - Counting elements with a strictly greater value in $\mathcal{O}(N)$ and right-to-left leader scans.
- [Prefix Sums & Special Index Parity Queries](../content/dsa/01_arrays_and_pointers/00_prefix_sums_and_special_index_queries.md) - $\mathcal{O}(1)$ range sum queries, equilibrium indices, and even/odd parity shifts when deleting an index (LC 1664).
- [Subarray Mechanics & Contribution Technique](../content/dsa/01_arrays_and_pointers/00_subarray_mechanics_and_contribution_technique.md) - Total subarrays $\frac{N(N+1)}{2}$, Closest Min-Max subarray, and the $(i+1)(N-i)$ contribution formula.
- [2D Matrices, Diagonals & In-Place Rotations](../content/dsa/01_arrays_and_pointers/00_matrix_2d_arrays_and_rotations.md) - Diagonal coordinate rules (`r == c`, `r + c == N - 1`), in-place transpose, 90° rotations (LC 48), and 4-pointer spiral order (LC 54).

### Problem Walkthroughs (Sorted by LeetCode #)
- [LC 3: Longest Substring Without Repeating Characters](../content/dsa/01_arrays_and_pointers/3_longest_substring_without_repeating_characters.md) - Dynamic sliding window with a set.
- [LC 5: Longest Palindromic Substring](../content/dsa/01_arrays_and_pointers/5_longest_palindromic_substring.md) - Outward two-pointer expansion around odd `(i, i)` and even `(i, i+1)` centers.
- [LC 11: Container With Most Water](../content/dsa/01_arrays_and_pointers/11_container_with_most_water.md) - Two-pointer inward squeeze moving the shorter bottleneck wall.
- [LC 12: Integer to Roman](../content/dsa/01_arrays_and_pointers/12_integer_to_roman.md) - Greedy subtraction from largest denomination to smallest.
- [LC 13: Roman to Integer](../content/dsa/01_arrays_and_pointers/13_roman_to_integer.md) - Lookahead subtraction rule (`val[s[i]] < val[s[i+1]]`).
- [LC 15: 3Sum](../content/dsa/01_arrays_and_pointers/15_3sum.md) - Sorting + fixed anchor + two-pointer squeeze with duplicate skipping.
- [LC 26: Remove Duplicates from Sorted Array](../content/dsa/01_arrays_and_pointers/26_remove_duplicates_from_sorted_array.md) - Scout and writer (`slow`/`fast`) in-place deduplication.
- [LC 27: Remove Element](../content/dsa/01_arrays_and_pointers/27_remove_element.md) - Scout and writer in-place compaction.
- [LC 48: Rotate Image](../content/dsa/01_arrays_and_pointers/48_rotate_image.md) - In-place 90° clockwise matrix rotation (reverse rows top-to-bottom then transpose upper triangle).
- [LC 53: Maximum Subarray](../content/dsa/01_arrays_and_pointers/53_maximum_subarray.md) - Kadane's algorithm (dropping negative prefix sums).
- [LC 55: Jump Game](../content/dsa/01_arrays_and_pointers/55_jump_game.md) - Greedy horizon tracking (`max_reach`).
- [LC 66: Plus One](../content/dsa/01_arrays_and_pointers/66_plus_one.md) - Right-to-left odometer carry propagation.
- [LC 80: Remove Duplicates from Sorted Array II](../content/dsa/01_arrays_and_pointers/80_remove_duplicates_from_sorted_array_ii.md) - Generalized `nums[k - 2]` lookback writer.
- [LC 88: Merge Sorted Array](../content/dsa/01_arrays_and_pointers/88_merge_sorted_array.md) - Right-to-left tail-buffer placement.
- [LC 121: Best Time to Buy and Sell Stock](../content/dsa/01_arrays_and_pointers/121_best_time_to_buy_and_sell_stock.md) - Single-pass running minimum price.
- [LC 122: Best Time to Buy and Sell Stock II](../content/dsa/01_arrays_and_pointers/122_best_time_to_buy_and_sell_stock_ii.md) - Greedy harvesting of positive daily price deltas.
- [LC 125: Valid Palindrome](../content/dsa/01_arrays_and_pointers/125_valid_palindrome.md) - Inward two-pointer squeeze skipping non-alphanumerics.
- [LC 167: Two Sum II (Input Array Is Sorted)](../content/dsa/01_arrays_and_pointers/167_two_sum_ii_input_array_is_sorted.md) - Inward squeeze in $\mathcal{O}(1)$ space.
- [LC 169: Majority Element](../content/dsa/01_arrays_and_pointers/169_majority_element.md) - Boyer-Moore voting cancellation in $\mathcal{O}(1)$ space.
- [LC 189: Rotate Array](../content/dsa/01_arrays_and_pointers/189_rotate_array.md) - In-place triple reversal in $\mathcal{O}(1)$ space.
- [LC 228: Summary Ranges](../content/dsa/01_arrays_and_pointers/228_summary_ranges.md) - Anchor and scout chunking for consecutive streaks.
- [LC 238: Product of Array Except Self](../content/dsa/01_arrays_and_pointers/238_product_of_array_except_self.md) - Prefix product pass followed by suffix product pass without division.
- [LC 274: H-Index](../content/dsa/01_arrays_and_pointers/274_h_index.md) - Descending sort rank check and $\mathcal{O}(n)$ bucket counting sort.
- [LC 283: Move Zeroes](../content/dsa/01_arrays_and_pointers/283_move_zeroes.md) - Scout and writer single-pass swap.
- [LC 290: Word Pattern](../content/dsa/01_arrays_and_pointers/290_word_pattern.md) - Bijective 1-to-1 mapping and avoiding the $\mathcal{O}(n)$ `in dict.values()` trap.
- [LC 392: Is Subsequence](../content/dsa/01_arrays_and_pointers/392_is_subsequence.md) - Two-conveyor-belt pointer matching.
- [LC 560: Subarray Sum Equals K](../content/dsa/01_arrays_and_pointers/560_subarray_sum_equals_k.md) - Running prefix sum with hash map frequency lookup (`cur_sum - k`).
- [LC 643: Maximum Average Subarray I](../content/dsa/01_arrays_and_pointers/643_maximum_average_subarray_i.md) - Fixed-size $K$ sliding window with deferred division.
- [LC 724: Find Pivot Index](../content/dsa/01_arrays_and_pointers/724_find_pivot_index.md) - Seesaw balance equation (`left_sum == total - left_sum - num`).
- [LC 867: Transpose Matrix](../content/dsa/01_arrays_and_pointers/867_transpose_matrix.md) - 2D coordinate transformation (`mat[j][i] = matrix[i][j]`), list comprehension allocation, and `zip(*matrix)`.
- [LC 1456: Maximum Number of Vowels in a Substring](../content/dsa/01_arrays_and_pointers/1456_maximum_number_of_vowels_in_a_substring_of_given_length.md) - Fixed-size $K$ sliding window on character counts.

---

## 2. Linked Lists (`02_linked_lists/`)

- [01. Linked List Fundamentals](../content/dsa/02_linked_lists/01_linked_list_fundamentals.md) - Node pointers, `cur = cur.next` vs. `cur.next = ...`, and `dummy` anchors.
- [90% Linked List Taxonomy Guide](../content/dsa/02_linked_lists/linked_list_90_percent_taxonomy.md) - The 11 linked list archetypes and problem classifier.
- [LC 2: Add Two Numbers](../content/dsa/02_linked_lists/2_add_two_numbers.md) - Digit-by-digit addition with carry and `dummy` head.
- [LC 19: Remove Nth Node From End of List](../content/dsa/02_linked_lists/19_remove_nth_node_from_end.md) - Fixed-gap two-pointer measuring stick.
- [LC 21: Merge Two Sorted Lists](../content/dsa/02_linked_lists/21_merge_two_sorted_lists.md) - Zipper merge using a `dummy` anchor.
- [LC 83: Remove Duplicates from Sorted List](../content/dsa/02_linked_lists/83_remove_duplicates_from_sorted_list.md) - In-place pointer bypass (`cur.next = cur.next.next`).
- [LC 141: Linked List Cycle](../content/dsa/02_linked_lists/141_linked_list_cycle.md) - Floyd's Tortoise and Hare (`slow` 1x, `fast` 2x).
- [LC 143: Reorder List](../content/dsa/02_linked_lists/143_reorder_list.md) - Find middle + reverse second half + alternating merge.
- [LC 206: Reverse Linked List](../content/dsa/02_linked_lists/206_reverse_linked_list.md) - Three-pointer (`prev`, `cur`, `nxt`) in-place arrow flip.
- [LC 234: Palindrome Linked List](../content/dsa/02_linked_lists/234_palindrome_linked_list.md) - Array two-pointer baseline vs. $\mathcal{O}(1)$ space second-half reversal.
- [LC 1290: Convert Binary Number in a Linked List to Integer](../content/dsa/02_linked_lists/1290_convert_binary_number_in_a_linked_list_to_integer.md) - Left-shift stream accumulation (`(ans << 1) | val`).
- [LC 1721: Swapping Nodes in a Linked List](../content/dsa/02_linked_lists/1721_swapping_nodes_in_a_linked_list.md) - Single-pass `k - 1` step ruler to find $k$-th from start and end.

---

## 3. Stacks & Queues (`03_stacks_and_queues/`)

- [LC 20: Valid Parentheses](../content/dsa/03_stacks_and_queues/20_valid_parentheses.md) - Odd-length early exit and pushing expected closing brackets.
- [LC 678: Valid Parenthesis String](../content/dsa/03_stacks_and_queues/678_valid_parenthesis_string.md) - Tracking open bracket indices against wildcard `*` indices.

---

## 4. Sorting Algorithms (`04_sorting/`)

- [01. Bubble Sort](../content/dsa/04_sorting/01_bubble_sort.md) - Adjacent swaps and the `swapped` early-exit flag.
- [02. Selection Sort](../content/dsa/04_sorting/02_selection_sort.md) - Minimum-swaps selection ($\le n$ writes) and why it is unstable.
- [03. Insertion Sort](../content/dsa/04_sorting/03_insertion_sort.md) - Shifting sorted prefixes and $\mathcal{O}(n)$ performance on nearly sorted data.
- [04. Merge Sort](../content/dsa/04_sorting/04_merge_sort.md) - Divide-and-conquer splitting and two-pointer merge in $\mathcal{O}(n \log n)$.
- [05. Quick Sort](../content/dsa/04_sorting/05_quick_sort.md) - In-place pivot partitioning and avoiding the $\mathcal{O}(n^2)$ worst case.

---

## 5. Binary Search Masterclass (`05_binary_search/`, CodeKerdos Classes 8-10)

- [01. Binary Search Fundamentals & Occurrence Boundaries](../content/dsa/05_binary_search/01_binary_search_fundamentals_and_occurrences.md) - Exact match, first/last occurrence (LC 34), count of duplicates, and floor/ceil.
- [02. Local Minima & Peak Finding in Unsorted Arrays](../content/dsa/05_binary_search/02_local_minima_and_peak_finding.md) - Navigating slopes in $\mathcal{O}(\log n)$ without sorting (LC 162).
- [03. Single Element in Duplicates (Index Parity)](../content/dsa/05_binary_search/03_index_parity_single_element_in_duplicates.md) - Detecting the `(even, odd)` to `(odd, even)` pair shift (LC 540).
- [04. Search in Rotated Sorted Array](../content/dsa/05_binary_search/04_search_in_rotated_sorted_array.md) - Identifying which half is strictly sorted (LC 33, LC 153).
- [05. Exponential Search in Infinite / Unbounded Arrays](../content/dsa/05_binary_search/05_exponential_search_infinite_arrays.md) - Doubling window bounds `1, 2, 4, 8...` before binary searching (LC 702).
- [06. Binary Search on the Answer (Greedy Predicates)](../content/dsa/05_binary_search/06_binary_search_on_answer_greedy_predicates.md) - Monotonic feasibility functions for Painter's Partition, Aggressive Cows, Koko (LC 875), and Split Array (LC 410).

---

## 6. Cheat Sheets (`cheat_sheets/`)

### DSA Cheat Sheets
- [Time & Space Complexity](../content/cheat-sheets/time_and_space_complexity_cheat_sheet.md)
- [Python Internals, Memory & Collections](../content/cheat-sheets/python_internals_and_collections_cheat_sheet.md)
- [Arrays, Strings & HashMaps](../content/cheat-sheets/arrays_hashmaps_cheat_sheet.md)
- [Prefix Sum & Seesaw Balance](../content/cheat-sheets/prefix_sum_seesaw_cheat_sheet.md)
- [Subarrays & Contribution Technique](../content/cheat-sheets/subarrays_and_contribution_technique_cheat_sheet.md)
- [2D Matrix Manipulation](../content/cheat-sheets/matrix_2d_manipulation_cheat_sheet.md)
- [Two Pointers (All 6 Formations)](../content/cheat-sheets/two_pointers_cheat_sheet.md)
- [Sliding Window (Fixed & Dynamic)](../content/cheat-sheets/sliding_window_cheat_sheet.md)
- [Kadane's Algorithm](../content/cheat-sheets/kadanes_algorithm_cheat_sheet.md)
- [Greedy Algorithms](../content/cheat-sheets/greedy_cheat_sheet.md)
- [Greedy Subtraction (ATM Pattern)](../content/cheat-sheets/greedy_subtraction_atm_cheat_sheet.md)
- [Binary Search (7 Archetypes)](../content/cheat-sheets/binary_search_cheat_sheet.md)
- [Linked List Master Cheat Sheet](../content/cheat-sheets/linked_list_master_cheat_sheet.md)
- [Sorting Algorithms Comparison](../content/cheat-sheets/sorting_cheat_sheet.md)
- [BFS vs. DFS](../content/cheat-sheets/bfs_dfs_cheat_sheet.md)
- [Backtracking](../content/cheat-sheets/backtracking_cheat_sheet.md)
- [Priority Queues & Heaps](../content/cheat-sheets/heaps_priority_queues_cheat_sheet.md)
- [Bit Manipulation](../content/cheat-sheets/bitwise_cheat_sheet.md)

### System Design Cheat Sheets
- [System Design Fundamentals](../content/cheat-sheets/system_design_fundamentals_cheat_sheet.md)
- [Back-of-the-Envelope Calculations](../content/cheat-sheets/system_design_calculations_cheat_sheet.md)
- [System Design Failure Modes & Fixes (39 Concepts)](../content/cheat-sheets/system_design_failure_modes_cheat_sheet.md)

---

## 7. System Design & Production Infrastructure (`system_design/`)

- [00. FAANG System Design 4-Step Interview Framework](../content/system-design/00_faang_system_design_framework.md)
- [01. Production Infrastructure & Protocol Fundamentals](../content/system-design/01_production_infrastructure_fundamentals.md)
- [02. Caching Strategies, Patterns & Redis](../content/system-design/02_caching_patterns_and_redis.md)
- [03. Database Scaling, Sharding & CAP Theorem](../content/system-design/03_database_scaling_sharding_and_cap.md)
- [04. Message Queues & Event-Driven Architecture](../content/system-design/04_message_queues_and_async_processing.md)
- [05. API Gateway & Rate Limiting](../content/system-design/05_api_gateway_and_rate_limiting.md)
- [06. Distributed Failure Modes, Traffic Spikes & Latency](../content/system-design/06_distributed_failure_modes_and_resilience.md)
- [07. Distributed Coordination, Exactly-Once & Concurrency](../content/system-design/07_distributed_coordination_and_transactions.md)
- [Excalidraw Dry-Run #1: Scalable Photo Service](../content/system-design/excalidraw_practice_01_core_infra.md)
