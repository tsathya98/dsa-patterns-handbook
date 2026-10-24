# 12-Week FAANG DSA Preparation Plan

- **Pace:** 2 problems/day on weekdays (10/week) + 5 problems/day on weekends (10/week) = **20 problems/week**.
- **Goal:** Solve by pattern and archetype rather than memorizing problem numbers.

## Phase Overview

| Phase | Weeks | Focus | Target Solved |
| :--- | :--- | :--- | :--- |
| **Phase 1: Arrays & Pointers** | Weeks 1-3 | Two Pointers, Sliding Window, Prefix Sum, HashMaps, Kadane, 2D Matrices | 0 $\to$ 60 |
| **Phase 2: Linked Lists, Stacks & Binary Search** | Weeks 4-6 | Fast/Slow Pointers, In-Place Reversals, Monotonic Stack, 7 Binary Search Archetypes | 60 $\to$ 120 |
| **Phase 3: Trees, Graphs & Heaps** | Weeks 7-9 | Tree DFS/BFS, Graph Flood-Fill & Topological Sort, Top-K Heaps, Tries | 120 $\to$ 180 |
| **Phase 4: Backtracking & DP** | Weeks 10-12 | Subsets/Permutations, 1D/2D DP, Timed 45-Minute Mock Interviews | 180 $\to$ 210+ |

### 12-Week Roadmap Phases:
* **Phase 1 (Weeks 1-3):** Arrays, Two Pointers, Sliding Window, Prefix Sums, Contribution Technique, and 2D Matrices.
* **Phase 2 (Weeks 4-6):** Linked Lists (Fast/Slow, Reversal), Stacks, Queues, Elementary Sorting, and 7 Binary Search Patterns.
* **Phase 3 (Weeks 7-9):** Binary Trees, Tree Traversals (BFS/DFS), BSTs, Graph General, Topological Sort, and Heaps.
* **Phase 4 (Weeks 10-12):** Recursion & Backtracking, 1D/2D Dynamic Programming, System Design Deep Dives, and Full Mock Interviews.


---

## Phase 1: Arrays, Strings & Pointers (Weeks 1-3)

### Week 1: Two Pointers, Greedy & In-Place Array Manipulation
- **Weekday (10):**
  - [x] [LC 88: Merge Sorted Array](../dsa/01_arrays_and_pointers/88_merge_sorted_array.md)
  - [x] [LC 27: Remove Element](../dsa/01_arrays_and_pointers/27_remove_element.md)
  - [x] [LC 26: Remove Duplicates from Sorted Array](../dsa/01_arrays_and_pointers/26_remove_duplicates_from_sorted_array.md)
  - [x] [LC 80: Remove Duplicates from Sorted Array II](../dsa/01_arrays_and_pointers/80_remove_duplicates_from_sorted_array_ii.md)
  - [x] [LC 283: Move Zeroes](../dsa/01_arrays_and_pointers/283_move_zeroes.md)
  - [x] [LC 169: Majority Element](../dsa/01_arrays_and_pointers/169_majority_element.md)
  - [x] [LC 189: Rotate Array](../dsa/01_arrays_and_pointers/189_rotate_array.md)
  - [x] [LC 121: Best Time to Buy and Sell Stock](../dsa/01_arrays_and_pointers/121_best_time_to_buy_and_sell_stock.md)
  - [x] [LC 122: Best Time to Buy and Sell Stock II](../dsa/01_arrays_and_pointers/122_best_time_to_buy_and_sell_stock_ii.md)
  - [x] [LC 55: Jump Game](../dsa/01_arrays_and_pointers/55_jump_game.md)
- **Weekend (10):**
  - [x] [LC 125: Valid Palindrome](../dsa/01_arrays_and_pointers/125_valid_palindrome.md)
  - [x] [LC 392: Is Subsequence](../dsa/01_arrays_and_pointers/392_is_subsequence.md)
  - [x] [LC 167: Two Sum II (Input Array Is Sorted)](../dsa/01_arrays_and_pointers/167_two_sum_ii_input_array_is_sorted.md)
  - [x] [LC 11: Container With Most Water](../dsa/01_arrays_and_pointers/11_container_with_most_water.md)
  - [x] [LC 15: 3Sum](../dsa/01_arrays_and_pointers/15_3sum.md)
  - [x] [LC 238: Product of Array Except Self](../dsa/01_arrays_and_pointers/238_product_of_array_except_self.md)
  - [x] [LC 274: H-Index](../dsa/01_arrays_and_pointers/274_h_index.md)
  - [x] [LC 5: Longest Palindromic Substring](../dsa/01_arrays_and_pointers/5_longest_palindromic_substring.md)
  - [ ] LC 45: Jump Game II
  - [ ] LC 42: Trapping Rain Water

### Week 2: Sliding Window, HashMaps & 2D Matrices
- **Weekday (10):**
  - [x] [LC 643: Maximum Average Subarray I](../dsa/01_arrays_and_pointers/643_maximum_average_subarray_i.md)
  - [x] [LC 1456: Maximum Number of Vowels in a Substring](../dsa/01_arrays_and_pointers/1456_maximum_number_of_vowels_in_a_substring_of_given_length.md)
  - [x] [LC 3: Longest Substring Without Repeating Characters](../dsa/01_arrays_and_pointers/3_longest_substring_without_repeating_characters.md)
  - [x] [LC 290: Word Pattern](../dsa/01_arrays_and_pointers/290_word_pattern.md)
  - [x] [LC 228: Summary Ranges](../dsa/01_arrays_and_pointers/228_summary_ranges.md)
  - [ ] LC 209: Minimum Size Subarray Sum
  - [ ] LC 1: Two Sum
  - [ ] LC 242: Valid Anagram
  - [ ] LC 49: Group Anagrams
  - [ ] LC 128: Longest Consecutive Sequence
- **Weekend (10):**
  - [x] [2D Matrices: Transpose, Rotate Image (LC 48) & Spiral Matrix (LC 54)](../dsa/01_arrays_and_pointers/00_matrix_2d_arrays_and_rotations.md)
  - [x] [LC 867: Transpose Matrix](../dsa/01_arrays_and_pointers/867_transpose_matrix.md)
  - [ ] LC 76: Minimum Window Substring
  - [ ] LC 36: Valid Sudoku
  - [ ] LC 73: Set Matrix Zeroes
  - [ ] LC 56: Merge Intervals
  - [ ] LC 57: Insert Interval

### Week 3: Prefix Sums, Subarray Contribution & Kadane
- **Weekday (10):**
  - [x] [LC 724: Find Pivot Index](../dsa/01_arrays_and_pointers/724_find_pivot_index.md)
  - [x] [Prefix Sums & Fair Array Parity (LC 1664)](../dsa/01_arrays_and_pointers/00_prefix_sums_and_special_index_queries.md)
  - [x] [Subarray Mechanics & Contribution Technique](../dsa/01_arrays_and_pointers/00_subarray_mechanics_and_contribution_technique.md)
  - [x] [LC 53: Maximum Subarray](../dsa/01_arrays_and_pointers/53_maximum_subarray.md)
  - [x] [LC 66: Plus One](../dsa/01_arrays_and_pointers/66_plus_one.md)
  - [x] [LC 13: Roman to Integer](../dsa/01_arrays_and_pointers/13_roman_to_integer.md)
  - [x] [LC 12: Integer to Roman](../dsa/01_arrays_and_pointers/12_integer_to_roman.md)
  - [ ] LC 560: Subarray Sum Equals K
  - [ ] LC 918: Maximum Sum Circular Subarray
  - [ ] LC 152: Maximum Product Subarray

---

## Phase 2: Linked Lists, Stacks & Binary Search (Weeks 4-6)

### Week 4: Linked Lists ([11 Archetypes](../dsa/02_linked_lists/linked_list_90_percent_taxonomy.md))
- **Solved & Documented:**
  - [x] [LC 2: Add Two Numbers](../dsa/02_linked_lists/2_add_two_numbers.md)
  - [x] [LC 19: Remove Nth Node From End of List](../dsa/02_linked_lists/19_remove_nth_node_from_end.md)
  - [x] [LC 21: Merge Two Sorted Lists](../dsa/02_linked_lists/21_merge_two_sorted_lists.md)
  - [x] [LC 83: Remove Duplicates from Sorted List](../dsa/02_linked_lists/83_remove_duplicates_from_sorted_list.md)
  - [x] [LC 141: Linked List Cycle](../dsa/02_linked_lists/141_linked_list_cycle.md)
  - [x] [LC 143: Reorder List](../dsa/02_linked_lists/143_reorder_list.md)
  - [x] [LC 206: Reverse Linked List](../dsa/02_linked_lists/206_reverse_linked_list.md)
  - [x] [LC 234: Palindrome Linked List](../dsa/02_linked_lists/234_palindrome_linked_list.md)
  - [x] [LC 1290: Convert Binary Number in a Linked List to Integer](../dsa/02_linked_lists/1290_convert_binary_number_in_a_linked_list_to_integer.md)
  - [x] [LC 1721: Swapping Nodes in a Linked List](../dsa/02_linked_lists/1721_swapping_nodes_in_a_linked_list.md)
- **Remaining Targets:** LC 82, LC 92, LC 138 (Copy List with Random Pointer), LC 146 (LRU Cache), LC 25 (Reverse Nodes in k-Group).

### Week 5: Stacks & Monotonic Stacks
- **Solved & Documented:**
  - [x] [LC 20: Valid Parentheses](../dsa/03_stacks_and_queues/20_valid_parentheses.md)
  - [x] [LC 678: Valid Parenthesis String](../dsa/03_stacks_and_queues/678_valid_parenthesis_string.md)
- **Remaining Targets:** LC 155 (Min Stack), LC 150 (Reverse Polish Notation), LC 739 (Daily Temperatures), LC 496 (Next Greater Element I), LC 84 (Largest Rectangle in Histogram).

### Week 6: Binary Search ([7 Universal Archetypes](../cheat-sheets/binary_search_cheat_sheet.md))
- **Documented Masterclass Guides:**
  - [x] [01. Exact Lookup, First/Last Occurrence (LC 34) & Floor/Ceil](../dsa/05_binary_search/01_binary_search_fundamentals_and_occurrences.md)
  - [x] [02. Local Minima & Peak Finding (LC 162)](../dsa/05_binary_search/02_local_minima_and_peak_finding.md)
  - [x] [03. Single Element in Duplicates via Index Parity (LC 540)](../dsa/05_binary_search/03_index_parity_single_element_in_duplicates.md)
  - [x] [04. Search in Rotated Sorted Array (LC 33, LC 153)](../dsa/05_binary_search/04_search_in_rotated_sorted_array.md)
  - [x] [05. Exponential Search in Infinite Arrays (LC 702)](../dsa/05_binary_search/05_exponential_search_infinite_arrays.md)
  - [x] [06. Binary Search on Answer: Painter's Partition, Aggressive Cows, Koko (LC 875), Split Array (LC 410)](../dsa/05_binary_search/06_binary_search_on_answer_greedy_predicates.md)

---

## Phase 3: Trees, BFS/DFS & Heaps (Weeks 7-9)
- **Week 7 (Binary Trees & BSTs):** LC 104, LC 100, LC 226, LC 112, LC 236 (LCA), LC 98 (Validate BST), LC 230 (Kth Smallest in BST).
- **Week 8 (BFS & Graphs):** LC 102 (Level Order), LC 199 (Right Side View), LC 200 (Number of Islands), LC 994 (Rotting Oranges), LC 207/210 (Course Schedule I & II).
- **Week 9 (Heaps & Tries):** LC 215 (Kth Largest), LC 347 (Top K Frequent), LC 973 (K Closest Points), LC 23 (Merge k Sorted Lists), LC 295 (Find Median from Data Stream), LC 208 (Implement Trie).

---

## Phase 4: Backtracking & Dynamic Programming (Weeks 10-12)
- **Week 10 (Backtracking):** LC 78 (Subsets), LC 77 (Combinations), LC 39 (Combination Sum), LC 46 (Permutations), LC 79 (Word Search), LC 51 (N-Queens).
- **Week 11 (1D DP):** LC 70 (Climbing Stairs), LC 198/213 (House Robber I & II), LC 322 (Coin Change), LC 139 (Word Break), LC 300 (LIS), LC 416 (Partition Equal Subset Sum).
- **Week 12 (2D DP & Timed Mocks):** LC 62 (Unique Paths), LC 64 (Min Path Sum), LC 1143 (Longest Common Subsequence), LC 72 (Edit Distance).
