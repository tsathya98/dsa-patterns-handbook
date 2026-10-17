# 🎯 10-Week FAANG DSA Mastery Roadmap & Targets

> **Pace Formula:** 2 problems/day on weekdays (Mon–Fri = 10 problems) + 5 problems/day on weekends (Sat–Sun = 10 problems)  
> **Target Velocity:** **20 problems/week** $\approx$ **80 problems/month**  
> **Total Horizon:** **10–12 Weeks (~150 to 180 high-yield Top Interview problems)**  
> **Philosophy:** *Solve by archetype and pattern, not by memorizing problem IDs.*

---

## 📊 Summary of Velocity & Milestones

| Phase | Duration | Core Focus Topics | Target Total Solved |
|---|---|---|---|
| **Phase 1: Foundations & Arrays** | Weeks 1 – 3 | Two Pointers, Sliding Window, Prefix Sum, HashMaps, Kadane | 0 $\rightarrow$ 60 |
| **Phase 2: Linked Lists, Stacks & Binary Search** | Weeks 4 – 6 | Fast/Slow Pointers, Reversals, Monotonic Stack, Binary Search Boundaries | 60 $\rightarrow$ 120 |
| **Phase 3: Trees, BFS/DFS & Heaps** | Weeks 7 – 9 | Binary Trees, BSTs, Level-order BFS, Graph Traversals, Top-K Heaps | 120 $\rightarrow$ 180 |
| **Phase 4: Backtracking & Dynamic Programming** | Weeks 10 – 12 | Decision Trees, Subsets/Permutations, 1D/2D DP, Interval & Matrix | 180 $\rightarrow$ 210+ & Mock Interviews |

---

## 🗓️ Detailed Week-by-Week Breakdown

### 📍 Phase 1: Arrays, Strings & Pointers (Weeks 1 – 3)
* **Goal:** Never get stuck on indices, pointers, or off-by-one errors. Master $\mathcal{O}(1)$ space in-place manipulation.

#### **Week 1: Two Pointers & In-Place Array Transformations**
* **Weekday Target (10 problems):**
  * ✅ [LC 88. Merge Sorted Array (Easy)](./01_arrays_and_pointers/88_merge_sorted_array.md)
  * ✅ [LC 27. Remove Element (Easy)](./01_arrays_and_pointers/27_remove_element.md)
  * ✅ [LC 26. Remove Duplicates from Sorted Array (Easy)](./01_arrays_and_pointers/26_remove_duplicates_from_sorted_array.md)
  * ✅ [LC 80. Remove Duplicates from Sorted Array II (Medium)](./01_arrays_and_pointers/80_remove_duplicates_from_sorted_array_ii.md)
  * ✅ [LC 169. Majority Element (Easy)](./01_arrays_and_pointers/169_majority_element.md)
  * ✅ [LC 189. Rotate Array (Medium)](./01_arrays_and_pointers/189_rotate_array.md)
  * ✅ [LC 121. Best Time to Buy and Sell Stock (Easy)](./01_arrays_and_pointers/121_best_time_to_buy_and_sell_stock.md)
  * [ ] LC 122. Best Time to Buy and Sell Stock II (Medium)
  * [ ] LC 55. Jump Game (Medium)
  * [ ] LC 45. Jump Game II (Medium)
* **Weekend Target (10 problems):**
  * [ ] LC 125. Valid Palindrome (Easy)
  * [ ] LC 392. Is Subsequence (Easy)
  * [ ] LC 167. Two Sum II - Input Array Is Sorted (Medium)
  * [ ] LC 11. Container With Most Water (Medium)
  * [ ] LC 15. 3Sum (Medium)
  * [ ] LC 238. Product of Array Except Self (Medium)
  * [ ] LC 134. Gas Station (Medium)
  * [ ] LC 274. H-Index (Medium)
  * [ ] LC 380. Insert Delete GetRandom O(1) (Medium)
  * [ ] LC 42. Trapping Rain Water (Hard - *FAANG Classic Milestone*)

---

#### **Week 2: Sliding Window & HashMaps**
* **Weekday Target (10 problems):**
  * Fixed window: LC 643 (Max Average Subarray I), LC 1456 (Max Vowels)
  * Dynamic window: LC 3 (Longest Substring Without Repeating Characters), LC 209 (Minimum Size Subarray Sum)
  * HashMaps: LC 1 (Two Sum), LC 205 (Isomorphic Strings), LC 290 (Word Pattern), LC 242 (Valid Anagram), LC 49 (Group Anagrams), LC 128 (Longest Consecutive Sequence)
* **Weekend Target (10 problems):**
  * Hard Window: LC 76 (Minimum Window Substring), LC 30 (Substring with Concatenation of All Words)
  * Matrix: LC 36 (Valid Sudoku), LC 54 (Spiral Matrix), LC 48 (Rotate Image), LC 73 (Set Matrix Zeroes), LC 289 (Game of Life)
  * Intervals: LC 228 (Summary Ranges), LC 56 (Merge Intervals), LC 57 (Insert Interval)

---

#### **Week 3: Prefix Sums, Kadane & Matrix Manipulation**
* **Weekday Target (10 problems):**
  * Prefix sums: LC 724 (Find Pivot Index), LC 560 (Subarray Sum Equals K), LC 525 (Contiguous Array), LC 238 (Prefix/Suffix Products)
  * Kadane variants: LC 53 (Maximum Subarray), LC 918 (Maximum Sum Circular Subarray), LC 152 (Maximum Product Subarray)
  * String transforms: LC 14 (Longest Common Prefix), LC 58 (Length of Last Word), LC 151 (Reverse Words in a String)
* **Weekend Target (10 problems):**
  * Simulation: LC 6 (Zigzag Conversion), LC 68 (Text Justification - Hard)
  * Greedy Cashier / ATM: LC 13 (Roman to Integer), LC 12 (Integer to Roman)
  * Substrings: LC 28 (Find Index of First Occurrence), LC 452 (Minimum Number of Arrows to Burst Balloons)

---

### 📍 Phase 2: Linked Lists, Stacks & Binary Search (Weeks 4 – 6)
* **Goal:** Fluid pointer rewiring with $\mathcal{O}(1)$ space; understanding LIFO monotonicity and logarithmic boundary searches.

#### **Week 4: Linked List Mastery (11 Archetypes)**
* **Weekday Target (10 problems):**
  * Traversal & dummy node: LC 206 (Reverse LL), LC 21 (Merge Two Sorted Lists), LC 83 (Remove Duplicates from Sorted List), LC 82 (Remove Duplicates II)
  * Tortoise & Hare: LC 141 (Cycle), LC 142 (Cycle II), LC 876 (Middle of LL)
  * Measuring stick: LC 19 (Remove Nth from End), LC 1721 (Swapping Nodes), LC 61 (Rotate List)
* **Weekend Target (10 problems):**
  * Triple crowns: LC 234 (Palindrome LL), LC 143 (Reorder List), LC 92 (Reverse Linked List II)
  * Hard rewiring: LC 25 (Reverse Nodes in k-Group - *FAANG Bar Raiser*), LC 138 (Copy List with Random Pointer), LC 2 (Add Two Numbers), LC 445 (Add Two Numbers II), LC 86 (Partition List), LC 23 (Merge k Sorted Lists - Hard), LC 146 (LRU Cache - *Top 1 FAANG Question*)

---

#### **Week 5: Stacks & Monotonic Stacks**
* **Weekday Target (10 problems):**
  * Classical stack: LC 20 (Valid Parentheses), LC 678 (Valid Parenthesis String - Parked), LC 71 (Simplify Path), LC 155 (Min Stack), LC 150 (Evaluate Reverse Polish Notation)
  * Two stacks / Queues: LC 232 (Queue using Stacks), LC 225 (Stack using Queues)
  * Monotonic stack introduction: LC 739 (Daily Temperatures), LC 496 (Next Greater Element I), LC 503 (Next Greater Element II), LC 901 (Online Stock Span)
* **Weekend Target (10 problems):**
  * Deep monotonic stack: LC 84 (Largest Rectangle in Histogram - Hard), LC 85 (Maximal Rectangle - Hard), LC 402 (Remove K Digits), LC 316 (Remove Duplicate Letters)
  * Calculator series: LC 224 (Basic Calculator - Hard), LC 227 (Basic Calculator II), LC 394 (Decode String), LC 735 (Asteroid Collision), LC 856 (Score of Parentheses), LC 946 (Validate Stack Sequences)

---

#### **Week 6: Binary Search & Monotonic Spaces**
* **Weekday Target (10 problems):**
  * Standard & rotated: LC 704 (Binary Search), LC 35 (Search Insert Position), LC 74 (Search a 2D Matrix), LC 33 (Search in Rotated Sorted Array), LC 81 (Search in Rotated II), LC 153 (Find Minimum in Rotated), LC 154 (Find Minimum II)
  * Ranges: LC 34 (First and Last Position), LC 162 (Find Peak Element), LC 278 (First Bad Version)
* **Weekend Target (10 problems):**
  * Binary search on answer space: LC 875 (Koko Eating Bananas), LC 1011 (Capacity To Ship Packages), LC 410 (Split Array Largest Sum - Hard), LC 4 (Median of Two Sorted Arrays - Hard)
  * 2D binary search: LC 240 (Search a 2D Matrix II), LC 378 (Kth Smallest in Sorted Matrix)
  * Math & Bitwise: LC 69 (Sqrt(x)), LC 50 (Pow(x, n)), LC 66 (Plus One), LC 1290 (Binary LL to Integer)

---

### 📍 Phase 3: Trees, BFS/DFS & Heaps (Weeks 7 – 9)
* **Goal:** Master recursion, tree depth, level-order queues, and min/max heap invariants.

#### **Week 7: Binary Trees & BSTs**
* **Weekday Target (10 problems):**
  * Traversals: LC 104 (Max Depth), LC 111 (Min Depth), LC 100 (Same Tree), LC 101 (Symmetric Tree), LC 226 (Invert Binary Tree), LC 112 (Path Sum), LC 113 (Path Sum II), LC 129 (Sum Root to Leaf), LC 222 (Count Complete Tree Nodes), LC 110 (Balanced Tree)
* **Weekend Target (10 problems):**
  * Construction & Ancestors: LC 236 (Lowest Common Ancestor - Classic), LC 235 (LCA of BST), LC 105 (Construct from Preorder/Inorder), LC 106 (Construct from Inorder/Postorder), LC 114 (Flatten to LL), LC 116 / 117 (Populating Next Pointers)
  * BST properties: LC 98 (Validate BST), LC 530 (Minimum Absolute Difference), LC 230 (Kth Smallest in BST), LC 297 (Serialize & Deserialize Tree - Hard)

---

#### **Week 8: Level-Order BFS & Graphs Basics**
* **Weekday Target (10 problems):**
  * Tree BFS: LC 102 (Level Order Traversal), LC 107 (Bottom-Up Level Order), LC 103 (Zigzag Level Order), LC 199 (Right Side View), LC 637 (Average of Levels)
  * Graph BFS/DFS: LC 200 (Number of Islands - *Meta Favorite*), LC 133 (Clone Graph), LC 695 (Max Area of Island), LC 417 (Pacific Atlantic Water Flow), LC 130 (Surrounded Regions)
* **Weekend Target (10 problems):**
  * Topological sort: LC 207 (Course Schedule), LC 210 (Course Schedule II), LC 802 (Find Eventual Safe States)
  * Word ladder: LC 127 (Word Ladder - Hard), LC 909 (Snakes and Ladders), LC 433 (Minimum Genetic Mutation), LC 399 (Evaluate Division), LC 994 (Rotting Oranges), LC 752 (Open the Lock), LC 785 (Is Graph Bipartite?)

---

#### **Week 9: Priority Queues (Heaps) & Tries**
* **Weekday Target (10 problems):**
  * Heaps: LC 215 (Kth Largest Element in Array), LC 373 (Find K Pairs with Smallest Sums), LC 347 (Top K Frequent Elements), LC 973 (K Closest Points to Origin), LC 1046 (Last Stone Weight), LC 621 (Task Scheduler), LC 767 (Reorganize String)
  * Tries: LC 208 (Implement Trie), LC 211 (Design Add and Search Words), LC 648 (Replace Words)
* **Weekend Target (10 problems):**
  * Advanced Heaps & Two Heaps: LC 295 (Find Median from Data Stream - Hard), LC 502 (IPO - Hard), LC 23 (Merge k Sorted Lists with Heap)
  * Trie Hard: LC 212 (Word Search II - Hard), LC 421 (Maximum XOR of Two Numbers)
  * Union-Find / DSU: LC 547 (Number of Provinces), LC 684 (Redundant Connection), LC 1319 (Number of Operations to Make Network Connected), LC 721 (Accounts Merge), LC 128 (Longest Consecutive with DSU)

---

### 📍 Phase 4: Backtracking & Dynamic Programming (Weeks 10 – 12)
* **Goal:** Develop 100% confidence with recursion trees, memoization, and bottom-up DP tables.

#### **Week 10: Backtracking & Decision Trees**
* **Weekday Target (10 problems):**
  * Subsets & combinations: LC 78 (Subsets), LC 90 (Subsets II), LC 77 (Combinations), LC 39 (Combination Sum), LC 40 (Combination Sum II), LC 216 (Combination Sum III)
  * Permutations: LC 46 (Permutations), LC 47 (Permutations II), LC 17 (Letter Combinations of a Phone Number), LC 22 (Generate Parentheses)
* **Weekend Target (10 problems):**
  * Grid search & constraints: LC 79 (Word Search), LC 51 (N-Queens - Hard), LC 52 (N-Queens II), LC 37 (Sudoku Solver - Hard), LC 131 (Palindrome Partitioning), LC 93 (Restore IP Addresses), LC 842 (Split Array into Fibonacci), LC 140 (Word Break II - Hard), LC 282 (Expression Add Operators - Hard), LC 698 (Partition to K Equal Sum Subsets)

---

#### **Week 11: 1D Dynamic Programming & Interval DP**
* **Weekday Target (10 problems):**
  * Climbing & Fibonacci: LC 70 (Climbing Stairs), LC 746 (Min Cost Climbing Stairs), LC 198 (House Robber), LC 213 (House Robber II)
  * Unbounded / Knapsack: LC 322 (Coin Change), LC 518 (Coin Change II), LC 279 (Perfect Squares)
  * Word break & LIS: LC 139 (Word Break), LC 300 (Longest Increasing Subsequence), LC 673 (Number of LIS)
* **Weekend Target (10 problems):**
  * Partition & Stock DP: LC 416 (Partition Equal Subset Sum), LC 494 (Target Sum), LC 123 (Best Time to Buy and Sell Stock III - Hard), LC 188 (Stock IV - Hard), LC 309 (Stock with Cooldown), LC 714 (Stock with Transaction Fee), LC 152 (Max Product Subarray DP), LC 354 (Russian Doll Envelopes - Hard), LC 410 (Split Array DP), LC 1048 (Longest String Chain)

---

#### **Week 12: 2D DP, Strings & Final Mock Sprint**
* **Weekday Target (10 problems):**
  * Grid paths: LC 62 (Unique Paths), LC 63 (Unique Paths II), LC 64 (Minimum Path Sum), LC 120 (Triangle)
  * String 2D DP: LC 1143 (Longest Common Subsequence), LC 72 (Edit Distance - Hard), LC 97 (Interleaving String), LC 115 (Distinct Subsequences - Hard), LC 10 (Regular Expression Matching - Hard), LC 44 (Wildcard Matching - Hard)
* **Weekend Target (10 problems):**
  * 10 Final FAANG Simulated Mock Interview Timed Sessions (45 min each, 2 random questions).

---

## 📈 Daily & Weekly Target Tracking Formula

* **Weekly Quota:** 20 problems
* **Daily Weekday Routine:** 
  * 🌅 **Morning (30–40 min):** 1 problem (solve, reflect, document key archetype).
  * 🌆 **Evening (30–40 min):** 1 problem (solve, review time/space trade-offs).
* **Weekend Deep Sprint:**
  * ☕ **Saturday:** 5 problems (mixed Mediums).
  * ☕ **Sunday:** 5 problems (including 1 Hard milestone + review cheat sheets).
