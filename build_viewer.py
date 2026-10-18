#!/usr/bin/env python3
"""
Generate the unified DSA Study Hub & Tracker web application:
- Separates Concept/Theory Notes from LeetCode Problem Walkthroughs & Cheat Sheets.
- Embeds the complete official LeetCode Top Interview 150 (150 problems) and
  LeetCode 75 (75 problems) catalogs, automatically cross-linked with local .md study guides!
- Collapsible Left Sidebar (Topics) and Right Sidebar (On This Page) with keyboard shortcuts.
- Dedicated Pomodoro Focus Tracker Tab + persistent live mini-timer in the top bar +
  soothing Web Audio API harmonic chime when the timer completes.
- 4 modern developer palettes: Linear Indigo, Tokyo Night, Catppuccin Mocha, Daylight Clean.
"""

import os
import json
import re

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORY_META = {
    "Root": {"label": "Overview & Plans", "order": 0, "icon": "🧭"},
    "00_foundations": {"label": "00. Foundations", "order": 1, "icon": "🧱"},
    "01_arrays_and_pointers": {"label": "01. Arrays & Pointers", "order": 2, "icon": "🎯"},
    "02_linked_lists": {"label": "02. Linked Lists", "order": 3, "icon": "🔗"},
    "03_stacks_and_queues": {"label": "03. Stacks & Queues", "order": 4, "icon": "🥞"},
    "04_sorting": {"label": "04. Sorting", "order": 5, "icon": "📊"},
    "05_binary_search": {"label": "05. Binary Search", "order": 6, "icon": "🔍"},
    "06_recursion_and_backtracking": {"label": "06. Recursion & Backtracking", "order": 7, "icon": "🌳"},
    "system_design": {"label": "System Design", "order": 8, "icon": "🏗️"},
    "cheat_sheets": {"label": "Cheat Sheets", "order": 9, "icon": "⚡"},
}

DEFAULT_SOLVED_NUMBERS = {
    2, 3, 5, 11, 12, 13, 15, 19, 20, 21, 26, 27, 48, 51, 53, 54, 55, 66,
    75, 78, 80, 83, 88, 121, 122, 125, 141, 142, 143, 167, 169, 189, 206, 228,
    234, 238, 241, 274, 283, 290, 392, 459, 643, 678, 704, 724, 779, 1290, 1456, 1721
}

# Official LeetCode Top Interview 150 (Exact 150 problems across 23 categories)
TOP_150_RAW = [
    # 1. Array / String (24)
    (88, "Merge Sorted Array", "Easy", "Array / String", "merge-sorted-array"),
    (27, "Remove Element", "Easy", "Array / String", "remove-element"),
    (26, "Remove Duplicates from Sorted Array", "Easy", "Array / String", "remove-duplicates-from-sorted-array"),
    (80, "Remove Duplicates from Sorted Array II", "Medium", "Array / String", "remove-duplicates-from-sorted-array-ii"),
    (169, "Majority Element", "Easy", "Array / String", "majority-element"),
    (189, "Rotate Array", "Medium", "Array / String", "rotate-array"),
    (121, "Best Time to Buy and Sell Stock", "Easy", "Array / String", "best-time-to-buy-and-sell-stock"),
    (122, "Best Time to Buy and Sell Stock II", "Medium", "Array / String", "best-time-to-buy-and-sell-stock-ii"),
    (55, "Jump Game", "Medium", "Array / String", "jump-game"),
    (45, "Jump Game II", "Medium", "Array / String", "jump-game-ii"),
    (274, "H-Index", "Medium", "Array / String", "h-index"),
    (380, "Insert Delete GetRandom O(1)", "Medium", "Array / String", "insert-delete-getrandom-o1"),
    (238, "Product of Array Except Self", "Medium", "Array / String", "product-of-array-except-self"),
    (134, "Gas Station", "Medium", "Array / String", "gas-station"),
    (135, "Candy", "Hard", "Array / String", "candy"),
    (42, "Trapping Rain Water", "Hard", "Array / String", "trapping-rain-water"),
    (13, "Roman to Integer", "Easy", "Array / String", "roman-to-integer"),
    (12, "Integer to Roman", "Medium", "Array / String", "integer-to-roman"),
    (58, "Length of Last Word", "Easy", "Array / String", "length-of-last-word"),
    (14, "Longest Common Prefix", "Easy", "Array / String", "longest-common-prefix"),
    (151, "Reverse Words in a String", "Medium", "Array / String", "reverse-words-in-a-string"),
    (6, "Zigzag Conversion", "Medium", "Array / String", "zigzag-conversion"),
    (28, "Find the Index of the First Occurrence in a String", "Easy", "Array / String", "find-the-index-of-the-first-occurrence-in-a-string"),
    (68, "Text Justification", "Hard", "Array / String", "text-justification"),
    # 2. Two Pointers (5)
    (125, "Valid Palindrome", "Easy", "Two Pointers", "valid-palindrome"),
    (392, "Is Subsequence", "Easy", "Two Pointers", "is-subsequence"),
    (167, "Two Sum II - Input Array Is Sorted", "Medium", "Two Pointers", "two-sum-ii-input-array-is-sorted"),
    (11, "Container With Most Water", "Medium", "Two Pointers", "container-with-most-water"),
    (15, "3Sum", "Medium", "Two Pointers", "3sum"),
    # 3. Sliding Window (4)
    (209, "Minimum Size Subarray Sum", "Medium", "Sliding Window", "minimum-size-subarray-sum"),
    (3, "Longest Substring Without Repeating Characters", "Medium", "Sliding Window", "longest-substring-without-repeating-characters"),
    (30, "Substring with Concatenation of All Words", "Hard", "Sliding Window", "substring-with-concatenation-of-all-words"),
    (76, "Minimum Window Substring", "Hard", "Sliding Window", "minimum-window-substring"),
    # 4. Matrix (5)
    (36, "Valid Sudoku", "Medium", "Matrix", "valid-sudoku"),
    (54, "Spiral Matrix", "Medium", "Matrix", "spiral-matrix"),
    (48, "Rotate Image", "Medium", "Matrix", "rotate-image"),
    (73, "Set Matrix Zeroes", "Medium", "Matrix", "set-matrix-zeroes"),
    (289, "Game of Life", "Medium", "Matrix", "game-of-life"),
    # 5. Hashmap (9)
    (383, "Ransom Note", "Easy", "Hashmap", "ransom-note"),
    (205, "Isomorphic Strings", "Easy", "Hashmap", "isomorphic-strings"),
    (290, "Word Pattern", "Easy", "Hashmap", "word-pattern"),
    (242, "Valid Anagram", "Easy", "Hashmap", "valid-anagram"),
    (49, "Group Anagrams", "Medium", "Hashmap", "group-anagrams"),
    (1, "Two Sum", "Easy", "Hashmap", "two-sum"),
    (202, "Happy Number", "Easy", "Hashmap", "happy-number"),
    (219, "Contains Duplicate II", "Easy", "Hashmap", "contains-duplicate-ii"),
    (128, "Longest Consecutive Sequence", "Medium", "Hashmap", "longest-consecutive-sequence"),
    # 6. Intervals (4)
    (228, "Summary Ranges", "Easy", "Intervals", "summary-ranges"),
    (56, "Merge Intervals", "Medium", "Intervals", "merge-intervals"),
    (57, "Insert Interval", "Medium", "Intervals", "insert-interval"),
    (452, "Minimum Number of Arrows to Burst Balloons", "Medium", "Intervals", "minimum-number-of-arrows-to-burst-balloons"),
    # 7. Stack (5)
    (20, "Valid Parentheses", "Easy", "Stack", "valid-parentheses"),
    (71, "Simplify Path", "Medium", "Stack", "simplify-path"),
    (155, "Min Stack", "Medium", "Stack", "min-stack"),
    (150, "Evaluate Reverse Polish Notation", "Medium", "Stack", "evaluate-reverse-polish-notation"),
    (224, "Basic Calculator", "Hard", "Stack", "basic-calculator"),
    # 8. Linked List (11)
    (141, "Linked List Cycle", "Easy", "Linked List", "linked-list-cycle"),
    (2, "Add Two Numbers", "Medium", "Linked List", "add-two-numbers"),
    (21, "Merge Two Sorted Lists", "Easy", "Linked List", "merge-two-sorted-lists"),
    (138, "Copy List with Random Pointer", "Medium", "Linked List", "copy-list-with-random-pointer"),
    (92, "Reverse Linked List II", "Medium", "Linked List", "reverse-linked-list-ii"),
    (25, "Reverse Nodes in k-Group", "Hard", "Linked List", "reverse-nodes-in-k-group"),
    (19, "Remove Nth Node From End of List", "Medium", "Linked List", "remove-nth-node-from-end-of-list"),
    (82, "Remove Duplicates from Sorted List II", "Medium", "Linked List", "remove-duplicates-from-sorted-list-ii"),
    (61, "Rotate List", "Medium", "Linked List", "rotate-list"),
    (86, "Partition List", "Medium", "Linked List", "partition-list"),
    (146, "LRU Cache", "Medium", "Linked List", "lru-cache"),
    # 9. Binary Tree General (14)
    (104, "Maximum Depth of Binary Tree", "Easy", "Binary Tree General", "maximum-depth-of-binary-tree"),
    (100, "Same Tree", "Easy", "Binary Tree General", "same-tree"),
    (226, "Invert Binary Tree", "Easy", "Binary Tree General", "invert-binary-tree"),
    (101, "Symmetric Tree", "Easy", "Binary Tree General", "symmetric-tree"),
    (105, "Construct Binary Tree from Preorder and Inorder Traversal", "Medium", "Binary Tree General", "construct-binary-tree-from-preorder-and-inorder-traversal"),
    (106, "Construct Binary Tree from Inorder and Postorder Traversal", "Medium", "Binary Tree General", "construct-binary-tree-from-inorder-and-postorder-traversal"),
    (117, "Populating Next Right Pointers in Each Node II", "Medium", "Binary Tree General", "populating-next-right-pointers-in-each-node-ii"),
    (114, "Flatten Binary Tree to Linked List", "Medium", "Binary Tree General", "flatten-binary-tree-to-linked-list"),
    (112, "Path Sum", "Easy", "Binary Tree General", "path-sum"),
    (129, "Sum Root to Leaf Numbers", "Medium", "Binary Tree General", "sum-root-to-leaf-numbers"),
    (124, "Binary Tree Maximum Path Sum", "Hard", "Binary Tree General", "binary-tree-maximum-path-sum"),
    (173, "Binary Search Tree Iterator", "Medium", "Binary Tree General", "binary-search-tree-iterator"),
    (222, "Count Complete Tree Nodes", "Easy", "Binary Tree General", "count-complete-tree-nodes"),
    (236, "Lowest Common Ancestor of a Binary Tree", "Medium", "Binary Tree General", "lowest-common-ancestor-of-a-binary-tree"),
    # 10. Binary Tree BFS (4)
    (199, "Binary Tree Right Side View", "Medium", "Binary Tree BFS", "binary-tree-right-side-view"),
    (637, "Average of Levels in Binary Tree", "Easy", "Binary Tree BFS", "average-of-levels-in-binary-tree"),
    (102, "Binary Tree Level Order Traversal", "Medium", "Binary Tree BFS", "binary-tree-level-order-traversal"),
    (103, "Binary Tree Zigzag Level Order Traversal", "Medium", "Binary Tree BFS", "binary-tree-zigzag-level-order-traversal"),
    # 11. Binary Search Tree (3)
    (530, "Minimum Absolute Difference in BST", "Easy", "Binary Search Tree", "minimum-absolute-difference-in-bst"),
    (230, "Kth Smallest Element in a BST", "Medium", "Binary Search Tree", "kth-smallest-element-in-a-bst"),
    (98, "Validate Binary Search Tree", "Medium", "Binary Search Tree", "validate-binary-search-tree"),
    # 12. Graph General (6)
    (200, "Number of Islands", "Medium", "Graph General", "number-of-islands"),
    (130, "Surrounded Regions", "Medium", "Graph General", "surrounded-regions"),
    (133, "Clone Graph", "Medium", "Graph General", "clone-graph"),
    (399, "Evaluate Division", "Medium", "Graph General", "evaluate-division"),
    (207, "Course Schedule", "Medium", "Graph General", "course-schedule"),
    (210, "Course Schedule II", "Medium", "Graph General", "course-schedule-ii"),
    # 13. Graph BFS (3)
    (909, "Snakes and Ladders", "Medium", "Graph BFS", "snakes-and-ladders"),
    (433, "Minimum Genetic Mutation", "Medium", "Graph BFS", "minimum-genetic-mutation"),
    (127, "Word Ladder", "Hard", "Graph BFS", "word-ladder"),
    # 14. Trie (3)
    (208, "Implement Trie (Prefix Tree)", "Medium", "Trie", "implement-trie-prefix-tree"),
    (211, "Design Add and Search Words Data Structure", "Medium", "Trie", "design-add-and-search-words-data-structure"),
    (212, "Word Search II", "Hard", "Trie", "word-search-ii"),
    # 15. Backtracking (7)
    (17, "Letter Combinations of a Phone Number", "Medium", "Backtracking", "letter-combinations-of-a-phone-number"),
    (77, "Combinations", "Medium", "Backtracking", "combinations"),
    (46, "Permutations", "Medium", "Backtracking", "permutations"),
    (39, "Combination Sum", "Medium", "Backtracking", "combination-sum"),
    (52, "N-Queens II", "Hard", "Backtracking", "n-queens-ii"),
    (22, "Generate Parentheses", "Medium", "Backtracking", "generate-parentheses"),
    (79, "Word Search", "Medium", "Backtracking", "word-search"),
    # 16. Divide & Conquer (4)
    (108, "Convert Sorted Array to Binary Search Tree", "Easy", "Divide & Conquer", "convert-sorted-array-to-binary-search-tree"),
    (148, "Sort List", "Medium", "Divide & Conquer", "sort-list"),
    (427, "Construct Quad Tree", "Medium", "Divide & Conquer", "construct-quad-tree"),
    (23, "Merge k Sorted Lists", "Hard", "Divide & Conquer", "merge-k-sorted-lists"),
    # 17. Kadane's Algorithm (2)
    (53, "Maximum Subarray", "Medium", "Kadane's Algorithm", "maximum-subarray"),
    (918, "Maximum Sum Circular Subarray", "Medium", "Kadane's Algorithm", "maximum-sum-circular-subarray"),
    # 18. Binary Search (7)
    (35, "Search Insert Position", "Easy", "Binary Search", "search-insert-position"),
    (74, "Search a 2D Matrix", "Medium", "Binary Search", "search-a-2d-matrix"),
    (162, "Find Peak Element", "Medium", "Binary Search", "find-peak-element"),
    (33, "Search in Rotated Sorted Array", "Medium", "Binary Search", "search-in-rotated-sorted-array"),
    (34, "Find First and Last Position of Element in Sorted Array", "Medium", "Binary Search", "find-first-and-last-position-of-element-in-sorted-array"),
    (153, "Find Minimum in Rotated Sorted Array", "Medium", "Binary Search", "find-minimum-in-rotated-sorted-array"),
    (4, "Median of Two Sorted Arrays", "Hard", "Binary Search", "median-of-two-sorted-arrays"),
    # 19. Heap (4)
    (215, "Kth Largest Element in an Array", "Medium", "Heap / Priority Queue", "kth-largest-element-in-an-array"),
    (502, "IPO", "Hard", "Heap / Priority Queue", "ipo"),
    (373, "Find K Pairs with Smallest Sums", "Medium", "Heap / Priority Queue", "find-k-pairs-with-smallest-sums"),
    (295, "Find Median from Data Stream", "Hard", "Heap / Priority Queue", "find-median-from-data-stream"),
    # 20. Bit Manipulation (6)
    (67, "Add Binary", "Easy", "Bit Manipulation", "add-binary"),
    (190, "Reverse Bits", "Easy", "Bit Manipulation", "reverse-bits"),
    (191, "Number of 1 Bits", "Easy", "Bit Manipulation", "number-of-1-bits"),
    (136, "Single Number", "Easy", "Bit Manipulation", "single-number"),
    (137, "Single Number II", "Medium", "Bit Manipulation", "single-number-ii"),
    (201, "Bitwise AND of Numbers Range", "Medium", "Bit Manipulation", "bitwise-and-of-numbers-range"),
    # 21. Math (6)
    (9, "Palindrome Number", "Easy", "Math", "palindrome-number"),
    (66, "Plus One", "Easy", "Math", "plus-one"),
    (172, "Factorial Trailing Zeroes", "Medium", "Math", "factorial-trailing-zeroes"),
    (69, "Sqrt(x)", "Easy", "Math", "sqrtx"),
    (50, "Pow(x, n)", "Medium", "Math", "powx-n"),
    (149, "Max Points on a Line", "Hard", "Math", "max-points-on-a-line"),
    # 22. 1D DP (5)
    (70, "Climbing Stairs", "Easy", "1D DP", "climbing-stairs"),
    (198, "House Robber", "Medium", "1D DP", "house-robber"),
    (139, "Word Break", "Medium", "1D DP", "word-break"),
    (322, "Coin Change", "Medium", "1D DP", "coin-change"),
    (300, "Longest Increasing Subsequence", "Medium", "1D DP", "longest-increasing-subsequence"),
    # 23. Multidimensional DP (9)
    (120, "Triangle", "Medium", "Multidimensional DP", "triangle"),
    (64, "Minimum Path Sum", "Medium", "Multidimensional DP", "minimum-path-sum"),
    (63, "Unique Paths II", "Medium", "Multidimensional DP", "unique-paths-ii"),
    (5, "Longest Palindromic Substring", "Medium", "Multidimensional DP", "longest-palindromic-substring"),
    (97, "Interleaving String", "Medium", "Multidimensional DP", "interleaving-string"),
    (72, "Edit Distance", "Medium", "Multidimensional DP", "edit-distance"),
    (123, "Best Time to Buy and Sell Stock III", "Hard", "Multidimensional DP", "best-time-to-buy-and-sell-stock-iii"),
    (188, "Best Time to Buy and Sell Stock IV", "Hard", "Multidimensional DP", "best-time-to-buy-and-sell-stock-iv"),
    (221, "Maximal Square", "Medium", "Multidimensional DP", "maximal-square"),
]

# Official LeetCode 75 (Exact 75 problems across 22 categories)
LC_75_RAW = [
    # 1. Array / String (9)
    (1768, "Merge Strings Alternately", "Easy", "Array / String", "merge-strings-alternately"),
    (1071, "Greatest Common Divisor of Strings", "Easy", "Array / String", "greatest-common-divisor-of-strings"),
    (1431, "Kids With the Greatest Number of Candies", "Easy", "Array / String", "kids-with-the-greatest-number-of-candies"),
    (605, "Can Place Flowers", "Easy", "Array / String", "can-place-flowers"),
    (345, "Reverse Vowels of a String", "Easy", "Array / String", "reverse-vowels-of-a-string"),
    (151, "Reverse Words in a String", "Medium", "Array / String", "reverse-words-in-a-string"),
    (238, "Product of Array Except Self", "Medium", "Array / String", "product-of-array-except-self"),
    (334, "Increasing Triplet Subsequence", "Medium", "Array / String", "increasing-triplet-subsequence"),
    (443, "String Compression", "Medium", "Array / String", "string-compression"),
    # 2. Two Pointers (4)
    (283, "Move Zeroes", "Easy", "Two Pointers", "move-zeroes"),
    (392, "Is Subsequence", "Easy", "Two Pointers", "is-subsequence"),
    (11, "Container With Most Water", "Medium", "Two Pointers", "container-with-most-water"),
    (1679, "Max Number of K-Sum Pairs", "Medium", "Two Pointers", "max-number-of-k-sum-pairs"),
    # 3. Sliding Window (4)
    (643, "Maximum Average Subarray I", "Easy", "Sliding Window", "maximum-average-subarray-i"),
    (1456, "Maximum Number of Vowels in a Substring of Given Length", "Medium", "Sliding Window", "maximum-number-of-vowels-in-a-substring-of-given-length"),
    (1004, "Max Consecutive Ones III", "Medium", "Sliding Window", "max-consecutive-ones-iii"),
    (1493, "Longest Subarray of 1's After Deleting One Element", "Medium", "Sliding Window", "longest-subarray-of-1s-after-deleting-one-element"),
    # 4. Prefix Sum (2)
    (1732, "Find the Highest Altitude", "Easy", "Prefix Sum", "find-the-highest-altitude"),
    (724, "Find Pivot Index", "Easy", "Prefix Sum", "find-pivot-index"),
    # 5. Hash Map / Set (4)
    (2215, "Find the Difference of Two Arrays", "Easy", "Hashmap / Set", "find-the-difference-of-two-arrays"),
    (1207, "Unique Number of Occurrences", "Easy", "Hashmap / Set", "unique-number-of-occurrences"),
    (1657, "Determine if Two Strings Are Close", "Medium", "Hashmap / Set", "determine-if-two-strings-are-close"),
    (2352, "Equal Row and Column Pairs", "Medium", "Hashmap / Set", "equal-row-and-column-pairs"),
    # 6. Stack (3)
    (2390, "Removing Stars From a String", "Medium", "Stack", "removing-stars-from-a-string"),
    (735, "Asteroid Collision", "Medium", "Stack", "asteroid-collision"),
    (394, "Decode String", "Medium", "Stack", "decode-string"),
    # 7. Queue (2)
    (933, "Number of Recent Calls", "Easy", "Queue", "number-of-recent-calls"),
    (649, "Dota2 Senate", "Medium", "Queue", "dota2-senate"),
    # 8. Linked List (4)
    (2095, "Delete the Middle Node of a Linked List", "Medium", "Linked List", "delete-the-middle-node-of-a-linked-list"),
    (328, "Odd Even Linked List", "Medium", "Linked List", "odd-even-linked-list"),
    (206, "Reverse Linked List", "Easy", "Linked List", "reverse-linked-list"),
    (2130, "Maximum Twin Sum of a Linked List", "Medium", "Linked List", "maximum-twin-sum-of-a-linked-list"),
    # 9. Binary Tree - DFS (6)
    (104, "Maximum Depth of Binary Tree", "Easy", "Binary Tree DFS", "maximum-depth-of-binary-tree"),
    (872, "Leaf-Similar Trees", "Easy", "Binary Tree DFS", "leaf-similar-trees"),
    (1448, "Count Good Nodes in Binary Tree", "Medium", "Binary Tree DFS", "count-good-nodes-in-binary-tree"),
    (437, "Path Sum III", "Medium", "Binary Tree DFS", "path-sum-iii"),
    (1372, "Longest ZigZag Path in a Binary Tree", "Medium", "Binary Tree DFS", "longest-zigzag-path-in-a-binary-tree"),
    (236, "Lowest Common Ancestor of a Binary Tree", "Medium", "Binary Tree DFS", "lowest-common-ancestor-of-a-binary-tree"),
    # 10. Binary Tree - BFS (2)
    (199, "Binary Tree Right Side View", "Medium", "Binary Tree BFS", "binary-tree-right-side-view"),
    (1161, "Maximum Level Sum of a Binary Tree", "Medium", "Binary Tree BFS", "maximum-level-sum-of-a-binary-tree"),
    # 11. Binary Search Tree (2)
    (700, "Search in a Binary Search Tree", "Easy", "Binary Search Tree", "search-in-a-binary-search-tree"),
    (450, "Delete Node in a BST", "Medium", "Binary Search Tree", "delete-node-in-a-bst"),
    # 12. Graphs - DFS (4)
    (841, "Keys and Rooms", "Medium", "Graph DFS", "keys-and-rooms"),
    (547, "Number of Provinces", "Medium", "Graph DFS", "number-of-provinces"),
    (1466, "Reorder Routes to Make All Paths Lead to the City Zero", "Medium", "Graph DFS", "reorder-routes-to-make-all-paths-lead-to-the-city-zero"),
    (399, "Evaluate Division", "Medium", "Graph DFS", "evaluate-division"),
    # 13. Graphs - BFS (2)
    (1926, "Nearest Exit from Entrance in Maze", "Medium", "Graph BFS", "nearest-exit-from-entrance-in-maze"),
    (994, "Rotting Oranges", "Medium", "Graph BFS", "rotting-oranges"),
    # 14. Heap / Priority Queue (4)
    (215, "Kth Largest Element in an Array", "Medium", "Heap / Priority Queue", "kth-largest-element-in-an-array"),
    (2336, "Smallest Number in Infinite Set", "Medium", "Heap / Priority Queue", "smallest-number-in-infinite-set"),
    (2542, "Maximum Subsequence Score", "Medium", "Heap / Priority Queue", "maximum-subsequence-score"),
    (2462, "Total Cost to Hire K Workers", "Medium", "Heap / Priority Queue", "total-cost-to-hire-k-workers"),
    # 15. Binary Search (4)
    (374, "Guess Number Higher or Lower", "Easy", "Binary Search", "guess-number-higher-or-lower"),
    (2300, "Successful Pairs of Spells and Potions", "Medium", "Binary Search", "successful-pairs-of-spells-and-potions"),
    (162, "Find Peak Element", "Medium", "Binary Search", "find-peak-element"),
    (875, "Koko Eating Bananas", "Medium", "Binary Search", "koko-eating-bananas"),
    # 16. Backtracking (2)
    (17, "Letter Combinations of a Phone Number", "Medium", "Backtracking", "letter-combinations-of-a-phone-number"),
    (216, "Combination Sum III", "Medium", "Backtracking", "combination-sum-iii"),
    # 17. DP - 1D (4)
    (1137, "N-th Tribonacci Number", "Easy", "1D DP", "n-th-tribonacci-number"),
    (746, "Min Cost Climbing Stairs", "Easy", "1D DP", "min-cost-climbing-stairs"),
    (198, "House Robber", "Medium", "1D DP", "house-robber"),
    (790, "Domino and Tromino Tiling", "Medium", "1D DP", "domino-and-tromino-tiling"),
    # 18. DP - Multidimensional (4)
    (62, "Unique Paths", "Medium", "Multidimensional DP", "unique-paths"),
    (1143, "Longest Common Subsequence", "Medium", "Multidimensional DP", "longest-common-subsequence"),
    (714, "Best Time to Buy and Sell Stock with Transaction Fee", "Medium", "Multidimensional DP", "best-time-to-buy-and-sell-stock-with-transaction-fee"),
    (72, "Edit Distance", "Medium", "Multidimensional DP", "edit-distance"),
    # 19. Bit Manipulation (3)
    (338, "Counting Bits", "Easy", "Bit Manipulation", "counting-bits"),
    (136, "Single Number", "Easy", "Bit Manipulation", "single-number"),
    (1318, "Minimum Flips to Make a OR b Equal to c", "Medium", "Bit Manipulation", "minimum-flips-to-make-a-or-b-equal-to-c"),
    # 20. Trie (2)
    (208, "Implement Trie (Prefix Tree)", "Medium", "Trie", "implement-trie-prefix-tree"),
    (1268, "Search Suggestions System", "Medium", "Trie", "search-suggestions-system"),
    # 21. Intervals (2)
    (435, "Non-overlapping Intervals", "Medium", "Intervals", "non-overlapping-intervals"),
    (452, "Minimum Number of Arrows to Burst Balloons", "Medium", "Intervals", "minimum-number-of-arrows-to-burst-balloons"),
    # 22. Monotonic Stack (2)
    (739, "Daily Temperatures", "Medium", "Monotonic Stack", "daily-temperatures"),
    (901, "Online Stock Span", "Medium", "Monotonic Stack", "online-stock-span"),
]


def parse_doc_metadata(rel_path: str, filename: str, content: str) -> dict:
    cat_raw = rel_path.split("/")[0] if "/" in rel_path else "Root"
    cat_info = CATEGORY_META.get(cat_raw, {"label": cat_raw, "order": 99, "icon": "📄"})

    m_title = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = m_title.group(1).strip() if m_title else filename

    m_num = re.match(r"^(\d+)_", filename)
    prefix_num = int(m_num.group(1)) if m_num else 9999

    m_lc_title = re.search(r"LeetCode\s+(\d+)", title, re.IGNORECASE)
    lc_number = int(m_lc_title.group(1)) if m_lc_title else None

    short_title = re.sub(r"^(?:LeetCode\s+\d+\s*[:\-–]\s*|\d+\.\s*)", "", title, flags=re.IGNORECASE).strip()

    m_diff = re.search(r"\*\*Difficulty:\*\*\s*(Easy|Medium|Hard)", content, re.IGNORECASE)
    if m_diff:
        difficulty = m_diff.group(1).capitalize()
    elif cat_raw == "cheat_sheets":
        difficulty = "Cheat Sheet"
    elif lc_number is not None:
        difficulty = "Easy"
    else:
        difficulty = "Concept"

    m_pat = re.search(r"\*\*Pattern:\*\*\s*([^\n|]+)", content)
    pattern = m_pat.group(1).strip() if m_pat else cat_info["label"]

    m_url = re.search(r"\((https://leetcode\.com/problems/[^)]+)\)", content)
    lc_url = m_url.group(1).strip() if m_url else ""

    summary = ""
    for line in content.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("```") or s.startswith("|") or s.startswith("---") or s.startswith("<"):
            continue
        clean_s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        clean_s = clean_s.replace("**", "").replace("`", "")
        if len(clean_s) > 20:
            summary = clean_s[:160] + ("..." if len(clean_s) > 160 else "")
            break

    if cat_raw == "cheat_sheets":
        doc_type = "cheat_sheet"
        sort_key = (2, prefix_num, short_title.lower())
    elif lc_number is not None:
        doc_type = "problem"
        sort_key = (1, lc_number, short_title.lower())
    else:
        doc_type = "concept"
        sort_key = (0, prefix_num, short_title.lower())

    return {
        "path": rel_path,
        "title": title,
        "shortTitle": short_title,
        "category": cat_raw,
        "categoryLabel": cat_info["label"],
        "categoryOrder": cat_info["order"],
        "categoryIcon": cat_info["icon"],
        "lcNumber": lc_number,
        "difficulty": difficulty,
        "pattern": pattern,
        "lcUrl": lc_url,
        "summary": summary,
        "docType": doc_type,
        "hasMermaid": "```mermaid" in content,
        "defaultSolved": lc_number in DEFAULT_SOLVED_NUMBERS,
        "sortOrder": sort_key,
        "content": content,
    }


raw_docs = []
for root, dirs, files in os.walk(ROOT_DIR):
    if any(x in root for x in (".git", "static", ".gemini", ".agents", "notes")):
        continue
    for f in sorted(files):
        if f.endswith(".md"):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, ROOT_DIR)
            with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
            raw_docs.append(parse_doc_metadata(rel_path, f, content))

raw_docs.sort(key=lambda d: (d["categoryOrder"], d["sortOrder"][0], d["sortOrder"][1], d["sortOrder"][2]))

docs = {}
lc_to_doc_path = {}
for idx, d in enumerate(raw_docs):
    d["index"] = idx
    del d["sortOrder"]
    docs[d["path"]] = d
    if d["lcNumber"] is not None:
        lc_to_doc_path[d["lcNumber"]] = d["path"]

# Also map concepts that cover specific LeetCode problems (e.g. LC 48, LC 54 in 00_matrix, LC 704/34 in 01_binary_search)
EXTRA_CONCEPT_DOC_MAP = {
    48: "01_arrays_and_pointers/00_matrix_2d_arrays_and_rotations.md",
    54: "01_arrays_and_pointers/00_matrix_2d_arrays_and_rotations.md",
    34: "05_binary_search/01_binary_search_fundamentals_and_occurrences.md",
    162: "05_binary_search/02_local_minima_and_peak_finding.md",
    33: "05_binary_search/04_search_in_rotated_sorted_array.md",
    153: "05_binary_search/04_search_in_rotated_sorted_array.md",
    875: "05_binary_search/06_binary_search_on_answer_greedy_predicates.md",
}
for lc_num, c_path in EXTRA_CONCEPT_DOC_MAP.items():
    if lc_num not in lc_to_doc_path and c_path in docs:
        lc_to_doc_path[lc_num] = c_path

# Build the Unified Problem Catalog (Top Interview 150 + LeetCode 75 + Repo Problems)
catalog_by_num = {}

for num, title, diff, topic, slug in TOP_150_RAW:
    doc_path = lc_to_doc_path.get(num, "")
    doc_obj = docs.get(doc_path)
    catalog_by_num[num] = {
        "number": num,
        "title": title,
        "difficulty": diff,
        "topic": topic,
        "pattern": doc_obj["pattern"] if doc_obj else topic,
        "url": f"https://leetcode.com/problems/{slug}/",
        "docPath": doc_path,
        "summary": doc_obj["summary"] if doc_obj else "",
        "in150": True,
        "in75": False,
        "defaultSolved": num in DEFAULT_SOLVED_NUMBERS,
    }

for num, title, diff, topic, slug in LC_75_RAW:
    if num in catalog_by_num:
        catalog_by_num[num]["in75"] = True
    else:
        doc_path = lc_to_doc_path.get(num, "")
        doc_obj = docs.get(doc_path)
        catalog_by_num[num] = {
            "number": num,
            "title": title,
            "difficulty": diff,
            "topic": topic,
            "pattern": doc_obj["pattern"] if doc_obj else topic,
            "url": f"https://leetcode.com/problems/{slug}/",
            "docPath": doc_path,
            "summary": doc_obj["summary"] if doc_obj else "",
            "in150": False,
            "in75": True,
            "defaultSolved": num in DEFAULT_SOLVED_NUMBERS,
        }

# Add any remaining Repo LeetCode problems not in Top 150 or LC 75 (e.g., LC 83, 678, 1290, 1721)
for path, d in docs.items():
    num = d["lcNumber"]
    if num is not None and num not in catalog_by_num:
        catalog_by_num[num] = {
            "number": num,
            "title": d["shortTitle"],
            "difficulty": d["difficulty"],
            "topic": d["categoryLabel"],
            "pattern": d["pattern"],
            "url": d["lcUrl"] or f"https://leetcode.com/problemset/?search={num}",
            "docPath": path,
            "summary": d["summary"],
            "in150": False,
            "in75": False,
            "defaultSolved": num in DEFAULT_SOLVED_NUMBERS,
        }

curated_problems = [catalog_by_num[k] for k in sorted(catalog_by_num.keys())]
c150 = sum(1 for p in curated_problems if p["in150"])
c75 = sum(1 for p in curated_problems if p["in75"])
print(f"Bundled {len(docs)} markdown documents and {len(curated_problems)} unique LeetCode problems (Top 150: {c150}, LC 75: {c75}).")

hl_css_path = os.path.join(ROOT_DIR, "static/vendor/highlight-github-dark.min.css")
hl_css = open(hl_css_path, "r", encoding="utf-8").read() if os.path.exists(hl_css_path) else ""

docs_json_str = json.dumps(docs)
problems_json_str = json.dumps(curated_problems)


def build_html(default_view: str = "concepts") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DSA Visual Study Hub & Focus Tracker</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="stylesheet" href="static/vendor/katex.min.css">
  <link rel="stylesheet" href="static/vendor/codemirror/codemirror.min.css">
  <script src="static/vendor/marked.min.js"></script>
  <script src="static/vendor/highlight.min.js"></script>
  <script src="static/vendor/katex.min.js"></script>
  <script src="static/vendor/auto-render.min.js"></script>
  <script src="static/vendor/mermaid.min.js"></script>
  <script src="static/vendor/skulpt.min.js"></script>
  <script src="static/vendor/skulpt-stdlib.js"></script>
  <script src="static/vendor/codemirror/codemirror.min.js"></script>
  <script src="static/vendor/codemirror/python.min.js"></script>
  <script src="static/vendor/codemirror/matchbrackets.min.js"></script>
  <script src="static/vendor/codemirror/closebrackets.min.js"></script>
  <style>
    {hl_css}

    /* DARK MODE (Claude.ai / Gemini Warm Charcoal Dark) */
    /* DARK MODE (LeetCode Official Dark Mode) */
    body.theme-dark {{
      --bg: #1a1a1a;
      --surface: #262626;
      --surface-card: #282828;
      --surface-hover: #323232;
      --border: #383838;
      --text: #eff2f6;
      --text-muted: #8c8c8c;
      --accent: #ffa116;
      --accent-text: #ffa116;
      --accent-fg: #1a1a1a;
      --accent-soft: rgba(255, 161, 22, 0.14);
      --accent-border: rgba(255, 161, 22, 0.35);
      --code-bg: #1e1e1e;
      --code-inline-bg: #2d2d2d;
      --code-inline-text: #ffa116;
      --heading-h1: #eff2f6;
      --heading-h2: #ffa116;
    }}

    /* LIGHT MODE (Clean Crisp Contrast) */
    body.theme-light {{
      --bg: #f7f8fa;
      --surface: #ffffff;
      --surface-card: #ffffff;
      --surface-hover: #f0f1f3;
      --border: #e2e4e8;
      --text: #262626;
      --text-muted: #6b7280;
      --accent: #ffa116;
      --accent-text: #c07800;
      --accent-fg: #ffffff;
      --accent-soft: rgba(255, 161, 22, 0.12);
      --accent-border: rgba(255, 161, 22, 0.35);
      --code-bg: #f8f9fa;
      --code-inline-bg: #f1f2f4;
      --code-inline-text: #b45309;
      --heading-h1: #1a1a1a;
      --heading-h2: #b45309;
    }}

    /* LeetCode VS Code Dark+ / Monaco Syntax Highlighting */
    body.theme-dark .hljs {{
      background: #1e1e1e !important;
      color: #d4d4d4 !important;
    }}
    body.theme-dark .hljs-keyword,
    body.theme-dark .hljs-operator {{
      color: #569cd6 !important;
    }}
    body.theme-dark .hljs-function,
    body.theme-dark .hljs-title.function_ {{
      color: #dcdcaa !important;
    }}
    body.theme-dark .hljs-string {{
      color: #ce9178 !important;
    }}
    body.theme-dark .hljs-comment {{
      color: #6a9955 !important;
      font-style: italic;
    }}
    body.theme-dark .hljs-number {{
      color: #b5cea8 !important;
    }}
    body.theme-dark .hljs-type,
    body.theme-dark .hljs-class,
    body.theme-dark .hljs-title.class_ {{
      color: #4ec9b0 !important;
    }}
    body.theme-dark .hljs-variable,
    body.theme-dark .hljs-params {{
      color: #9cdcfe !important;
    }}
    body.theme-dark .hljs-built_in {{
      color: #4ec9b0 !important;
    }}
    body.theme-dark .hljs-literal {{
      color: #569cd6 !important;
    }}

    /* CodeMirror LeetCode Theme */
    .cm-s-leetcode.CodeMirror {{
      height: 100% !important;
      width: 100% !important;
      background: #1e1e1e !important;
      color: #eff2f6 !important;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
      font-size: 13px !important;
      line-height: 1.6 !important;
      padding: 0 !important;
    }}
    .cm-s-leetcode .CodeMirror-scroll {{
      height: 100% !important;
      padding: 12px 0 !important;
      box-sizing: border-box !important;
    }}
    .cm-s-leetcode .CodeMirror-lines {{
      padding: 0 !important;
    }}
    .cm-s-leetcode .CodeMirror-gutters {{
      background: #1e1e1e !important;
      border-right: 1px solid #333333 !important;
      white-space: nowrap !important;
      padding-right: 2px !important;
    }}
    .cm-s-leetcode .CodeMirror-linenumber {{
      color: #858585 !important;
      font-size: 12px !important;
      min-width: 28px !important;
      padding: 0 8px 0 6px !important;
      text-align: right !important;
    }}
    .cm-s-leetcode .CodeMirror-cursor {{
      border-left: 2px solid #ffa116 !important;
    }}
    .cm-s-leetcode .CodeMirror-selected,
    .cm-s-leetcode.CodeMirror-focused .CodeMirror-selected {{
      background: rgba(38, 79, 120, 0.75) !important;
    }}
    .cm-s-leetcode .CodeMirror-line::selection,
    .cm-s-leetcode .CodeMirror-line > span::selection,
    .cm-s-leetcode .CodeMirror-line > span > span::selection {{
      background: rgba(38, 79, 120, 0.75) !important;
    }}
    .cm-s-leetcode .CodeMirror-matchingbracket {{
      color: #ffa116 !important;
      background: rgba(255, 161, 22, 0.25) !important;
      text-decoration: underline !important;
    }}

    /* CodeMirror Python Syntax Tokens (LeetCode / Monaco Dark+) */
    .cm-s-leetcode span.cm-keyword {{
      color: #569cd6 !important;
      font-weight: 600 !important;
    }}
    .cm-s-leetcode span.cm-def {{
      color: #dcdcaa !important;
      font-weight: 600 !important;
    }}
    .cm-s-leetcode span.cm-builtin {{
      color: #4ec9b0 !important;
    }}
    .cm-s-leetcode span.cm-string,
    .cm-s-leetcode span.cm-string-2 {{
      color: #ce9178 !important;
    }}
    .cm-s-leetcode span.cm-number {{
      color: #b5cea8 !important;
    }}
    .cm-s-leetcode span.cm-comment {{
      color: #6a9955 !important;
      font-style: italic !important;
    }}
    .cm-s-leetcode span.cm-variable,
    .cm-s-leetcode span.cm-variable-2 {{
      color: #9cdcfe !important;
    }}
    .cm-s-leetcode span.cm-variable-3 {{
      color: #4ec9b0 !important;
    }}
    .cm-s-leetcode span.cm-property {{
      color: #9cdcfe !important;
    }}
    .cm-s-leetcode span.cm-operator {{
      color: #d4d4d4 !important;
    }}
    .cm-s-leetcode span.cm-atom,
    .cm-s-leetcode span.cm-meta {{
      color: #569cd6 !important;
    }}

    /* Light mode CodeMirror */
    body.theme-light .cm-s-leetcode.CodeMirror {{
      background: #ffffff !important;
      color: #24292e !important;
    }}
    body.theme-light .cm-s-leetcode .CodeMirror-gutters {{
      background: #fafbfc !important;
      border-right: 1px solid #e1e4e8 !important;
    }}
    body.theme-light .cm-s-leetcode .CodeMirror-linenumber {{
      color: #959da5 !important;
    }}
    body.theme-light .cm-s-leetcode .CodeMirror-cursor {{
      border-left: 2px solid #0056b3 !important;
    }}
    body.theme-light .cm-s-leetcode .CodeMirror-selected,
    body.theme-light .cm-s-leetcode.CodeMirror-focused .CodeMirror-selected {{
      background: #c8e1ff !important;
    }}
    body.theme-light .cm-s-leetcode span.cm-keyword {{
      color: #d73a49 !important;
    }}
    body.theme-light .cm-s-leetcode span.cm-def {{
      color: #6f42c1 !important;
    }}
    body.theme-light .cm-s-leetcode span.cm-builtin {{
      color: #005cc5 !important;
    }}
    body.theme-light .cm-s-leetcode span.cm-string,
    body.theme-light .cm-s-leetcode span.cm-string-2 {{
      color: #032f62 !important;
    }}
    body.theme-light .cm-s-leetcode span.cm-number {{
      color: #005cc5 !important;
    }}
    body.theme-light .cm-s-leetcode span.cm-comment {{
      color: #6a737d !important;
      font-style: italic !important;
    }}
    body.theme-light .cm-s-leetcode span.cm-variable,
    body.theme-light .cm-s-leetcode span.cm-property {{
      color: #24292e !important;
    }}
    body.theme-light .cm-s-leetcode span.cm-operator {{
      color: #d73a49 !important;
    }}

    html, body {{
      height: 100%;
      width: 100%;
      margin: 0;
      padding: 0;
      overflow: hidden;
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, sans-serif;
      letter-spacing: -0.01em;
    }}

    .ui-bg {{ background-color: var(--bg); }}
    .ui-surface {{ background-color: var(--surface); border-color: var(--border); }}
    .ui-card {{ background-color: var(--surface-card); border-color: var(--border); }}
    .ui-text {{ color: var(--text); }}
    .ui-text-muted {{ color: var(--text-muted); }}
    .ui-border {{ border-color: var(--border); }}

    .ui-accent-btn {{
      background-color: var(--accent);
      color: var(--accent-fg);
    }}
    .ui-accent-soft {{
      background-color: var(--accent-soft);
      color: var(--accent-text);
      border-color: var(--accent-border);
    }}
    .ui-accent-text {{
      color: var(--accent-text);
    }}

    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 9999px; }}

    /* Markdown Reader Typography */
    .md-body {{
      color: var(--text);
      line-height: 1.75;
      font-size: 0.95rem;
    }}
    .md-body h1 {{
      font-size: 1.7rem;
      font-weight: 800;
      color: var(--heading-h1);
      margin-top: 0.25rem;
      margin-bottom: 1rem;
      padding-bottom: 0.6rem;
      border-bottom: 1px solid var(--border);
      letter-spacing: -0.02em;
    }}
    .md-body h2 {{
      font-size: 1.22rem;
      font-weight: 700;
      color: var(--heading-h2);
      margin-top: 1.85rem;
      margin-bottom: 0.65rem;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid var(--border);
      scroll-margin-top: 5rem;
    }}
    .md-body h3 {{
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--text);
      margin-top: 1.3rem;
      margin-bottom: 0.45rem;
      scroll-margin-top: 5rem;
    }}
    .md-body p {{ margin-bottom: 0.9rem; }}
    .md-body ul, .md-body ol {{ margin-bottom: 1rem; padding-left: 1.4rem; }}
    .md-body ul {{ list-style-type: disc; }}
    .md-body ol {{ list-style-type: decimal; }}
    .md-body li {{ margin-bottom: 0.35rem; }}
    .md-body blockquote {{
      border-left: 3px solid var(--accent);
      background: var(--accent-soft);
      padding: 0.65rem 1rem;
      border-radius: 0 0.6rem 0.6rem 0;
      margin-bottom: 1.1rem;
      font-size: 0.875rem;
    }}
    .md-body blockquote p {{ margin-bottom: 0.2rem; }}
    .md-body pre {{
      background: var(--code-bg) !important;
      color: #e2e8f0;
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      padding: 0.95rem 1.1rem;
      overflow-x: auto;
      margin-bottom: 1.1rem;
      font-size: 0.84rem;
      line-height: 1.55;
    }}
    .md-body code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.84em;
    }}
    .md-body :not(pre) > code {{
      background: var(--code-inline-bg);
      border: 1px solid var(--border);
      padding: 0.14rem 0.4rem;
      border-radius: 0.35rem;
      color: var(--code-inline-text);
      font-weight: 500;
    }}
    .md-body table {{
      display: block;
      width: 100%;
      overflow-x: auto;
      border-collapse: collapse;
      margin-bottom: 1.25rem;
      font-size: 0.85rem;
      border: 1px solid var(--border);
      border-radius: 0.5rem;
    }}
    .md-body th {{
      background: var(--surface);
      font-weight: 600;
      text-align: left;
      padding: 0.6rem 0.8rem;
      border-bottom: 1px solid var(--border);
    }}
    .md-body td {{
      padding: 0.55rem 0.8rem;
      border-bottom: 1px solid var(--border);
    }}
    .md-body a {{
      color: var(--accent-text);
      text-decoration: underline;
      text-underline-offset: 3px;
    }}
    .md-body details {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      padding: 0.7rem 1rem;
      margin-bottom: 1rem;
    }}
    .md-body summary {{
      cursor: pointer;
      font-weight: 600;
      color: var(--accent-text);
      user-select: none;
    }}
    .md-body details[open] summary {{
      margin-bottom: 0.75rem;
      padding-bottom: 0.45rem;
      border-bottom: 1px solid var(--border);
    }}

    .md-body.visual-focus-mode > p,
    .md-body.visual-focus-mode > ul,
    .md-body.visual-focus-mode > ol {{
      display: none;
    }}
    .md-body.hide-flowcharts-mode .mermaid-figure {{
      display: none;
    }}

    /* 7. Interactive Playthrough Widget */
    .playthrough-widget {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 1.25rem;
      padding: 1.25rem;
      margin: 1.5rem 0;
      box-shadow: 0 8px 30px -4px rgba(0,0,0,0.18);
      transition: all 0.3s ease;
    }}
    body.theme-dark .playthrough-widget {{
      background: #0b0f19;
      border-color: #1e293b;
    }}
    .pt-split-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 1.25rem;
      align-items: stretch;
    }}
    @media (min-width: 1024px) {{
      .pt-split-grid {{
        grid-template-columns: minmax(0, 1.05fr) minmax(0, 1.35fr);
      }}
    }}
    .pt-code-panel {{
      background: #080c14;
      border: 1px solid #1e293b;
      border-radius: 1rem;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      min-height: 380px;
      box-shadow: inset 0 1px 3px rgba(0,0,0,0.4);
    }}
    .pt-code-scroll {{
      flex: 1;
      overflow-y: auto;
      max-height: 480px;
      padding: 0.65rem 0.25rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.8rem;
      line-height: 1.55rem;
    }}
    .pt-code-line {{
      display: flex;
      align-items: center;
      padding: 0.08rem 0.5rem;
      border-left: 3px solid transparent;
      border-radius: 0.25rem;
      transition: all 0.15s ease;
    }}
    .pt-code-line.active {{
      background: rgba(16, 185, 129, 0.18) !important;
      border-left-color: #10b981 !important;
      box-shadow: inset 0 0 16px rgba(16, 185, 129, 0.1);
    }}
    .pt-code-num {{
      width: 2rem;
      text-align: right;
      padding-right: 0.75rem;
      color: #475569;
      user-select: none;
      font-size: 0.75rem;
    }}
    .pt-code-line.active .pt-code-num {{
      color: #34d399;
      font-weight: 700;
    }}
    .pt-code-text {{
      flex: 1;
      white-space: pre;
      color: #cbd5e1;
    }}
    .pt-code-line.active .pt-code-text {{
      color: #ffffff;
      font-weight: 600;
    }}
    /* Stage circular nodes */
    .pt-circle-node {{
      width: 3.25rem;
      height: 3.25rem;
      border-radius: 9999px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-weight: 700;
      font-size: 1.05rem;
      border: 2px solid #475569;
      background: #0f172a;
      color: #f8fafc;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      position: relative;
      user-select: none;
      flex-shrink: 0;
    }}
    @media (min-width: 640px) {{
      .pt-circle-node {{
        width: 3.6rem;
        height: 3.6rem;
        font-size: 1.15rem;
      }}
    }}
    .pt-circle-node.active {{
      border-color: #f59e0b !important;
      background: rgba(245, 158, 11, 0.2) !important;
      color: #fef3c7 !important;
      box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.35);
      transform: scale(1.08);
    }}
    .pt-circle-node.match-delete {{
      border-color: #ef4444 !important;
      background: rgba(239, 68, 68, 0.25) !important;
      color: #fca5a5 !important;
      box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.4);
    }}
    .pt-circle-node.dummy-node {{
      border-color: #a855f7 !important;
      background: rgba(168, 85, 247, 0.2) !important;
      color: #e9d5ff !important;
      box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.3);
    }}
    .pt-circle-node.bypassed-node {{
      opacity: 0.35;
      border-style: dashed !important;
      border-color: #ef4444 !important;
      text-decoration: line-through;
      transform: scale(0.9);
    }}
    /* Pointer pill badges */
    .pt-badge-head {{
      background: #06b6d4;
      color: #020617;
      font-weight: 800;
      font-size: 0.68rem;
      padding: 0.12rem 0.45rem;
      border-radius: 9999px;
      box-shadow: 0 2px 6px rgba(6, 182, 212, 0.45);
      white-space: nowrap;
    }}
    .pt-badge-next {{
      background: #f59e0b;
      color: #020617;
      font-weight: 800;
      font-size: 0.68rem;
      padding: 0.12rem 0.45rem;
      border-radius: 9999px;
      box-shadow: 0 2px 6px rgba(245, 158, 11, 0.45);
      white-space: nowrap;
    }}
    .pt-badge-prev {{
      background: #10b981;
      color: #020617;
      font-weight: 800;
      font-size: 0.68rem;
      padding: 0.12rem 0.45rem;
      border-radius: 9999px;
      box-shadow: 0 2px 6px rgba(16, 185, 129, 0.45);
      white-space: nowrap;
    }}
    .pt-badge-curr, .pt-badge-node {{
      background: #38bdf8;
      color: #020617;
      font-weight: 800;
      font-size: 0.68rem;
      padding: 0.12rem 0.45rem;
      border-radius: 9999px;
      box-shadow: 0 2px 6px rgba(56, 189, 248, 0.45);
      white-space: nowrap;
    }}
    .pt-badge-dummy {{
      background: #a855f7;
      color: #020617;
      font-weight: 800;
      font-size: 0.68rem;
      padding: 0.12rem 0.45rem;
      border-radius: 9999px;
      box-shadow: 0 2px 6px rgba(168, 85, 247, 0.45);
      white-space: nowrap;
    }}
    .pt-badge-curnext, .pt-badge-nodenext {{
      background: #f43f5e;
      color: #020617;
      font-weight: 800;
      font-size: 0.68rem;
      padding: 0.12rem 0.45rem;
      border-radius: 9999px;
      box-shadow: 0 2px 6px rgba(244, 63, 94, 0.45);
      white-space: nowrap;
    }}
    .pt-badge-default {{
      background: #64748b;
      color: #020617;
      font-weight: 800;
      font-size: 0.68rem;
      padding: 0.12rem 0.45rem;
      border-radius: 9999px;
      white-space: nowrap;
    }}
    .pt-cell {{
      min-width: 3.1rem;
      height: 3.6rem;
      border-radius: 0.75rem;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-weight: 700;
      font-size: 1.15rem;
      border: 1.5px solid var(--border);
      background: var(--surface-card);
      color: var(--text);
      transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      user-select: none;
    }}
    .pt-cell-active {{
      border-color: #ffa116 !important;
      background: rgba(255, 161, 22, 0.16) !important;
      color: #ffa116 !important;
      box-shadow: 0 0 0 3px rgba(255, 161, 22, 0.35);
      transform: translateY(-2px);
    }}
    body.theme-dark .pt-cell-active {{
      color: #ffa116 !important;
    }}
    .pt-cell-swapped {{
      border-color: #ff375f !important;
      background: rgba(255, 55, 95, 0.16) !important;
      color: #ff375f !important;
      box-shadow: 0 0 0 3px rgba(255, 55, 95, 0.32);
      transform: translateY(-3px) scale(1.04);
    }}
    .pt-cell-sorted {{
      border-color: #00b8a3 !important;
      background: rgba(0, 184, 163, 0.15) !important;
      color: #00b8a3 !important;
    }}
    body.theme-dark .pt-cell-sorted {{
      color: #00b8a3 !important;
    }}
    .pt-cell-dimmed {{
      opacity: 0.22;
      filter: grayscale(1);
    }}
    .pt-ptr-pill {{
      font-size: 0.68rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-weight: 700;
      padding: 0.1rem 0.35rem;
      border-radius: 0.35rem;
      background: rgba(255, 161, 22, 0.18);
      color: #ffa116;
      border: 1px solid rgba(255, 161, 22, 0.4);
      display: inline-flex;
      align-items: center;
      gap: 0.15rem;
      white-space: nowrap;
    }}
    body.theme-dark .pt-ptr-pill {{
      color: #ffa116;
    }}


    dialog::backdrop {{
      background: rgba(8, 10, 18, 0.75);
      backdrop-filter: blur(4px);
    }}
  </style>
</head>
<body class="theme-dark h-screen w-screen flex flex-col antialiased overflow-hidden">

  <!-- 1. UNIFIED TOP NAVIGATION BAR -->
  <header class="h-[53px] shrink-0 z-30 ui-surface border-b px-3 sm:px-5 flex items-center justify-between gap-2">
    <div class="flex items-center gap-2">
      <button type="button" id="toggle-left-sidebar-btn" onclick="toggleLeftSidebar()" class="p-1.5 rounded-lg ui-card border ui-text-muted hover:text-[var(--text)] transition-colors" title="Toggle Left Topic Sidebar (Shortcut: b)">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h10M4 18h16"/></svg>
      </button>

      <div class="flex items-center gap-2">
        <span class="text-base font-extrabold tracking-tight ui-accent-text whitespace-nowrap">DSA Hub</span>
        <button type="button" onclick="switchView('tracker')" id="global-progress-pill" class="hidden xl:inline-flex items-center gap-2 text-xs font-mono px-2.5 py-0.5 rounded-full ui-card border ui-text-muted hover:text-[var(--text)] transition-colors" title="Click to open Top 150 & LeetCode 75 Tracker">
          🔥 150: 0/150 • ⚡ 75: 0/75
        </button>
      </div>
    </div>

    <!-- 6 Primary Views -->
    <nav class="flex items-center gap-1 ui-card p-1 rounded-xl border overflow-x-auto" aria-label="Primary sections">
      <button type="button" onclick="switchView('concepts')" id="nav-btn-concepts" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">📘</span> Concepts
      </button>
      <button type="button" onclick="switchView('problems')" id="nav-btn-problems" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">🧩</span> LeetCode Guides
      </button>
      <button type="button" onclick="switchView('cheatsheets')" id="nav-btn-cheatsheets" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">⚡</span> Cheat Sheets
      </button>
      <button type="button" onclick="switchView('playground')" id="nav-btn-playground" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">🐍</span> Playground
      </button>
      <button type="button" onclick="switchView('tracker')" id="nav-btn-tracker" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">✅</span> 150 & 75 Tracker
      </button>
      <button type="button" onclick="switchView('pomodoro')" id="nav-btn-pomodoro" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">⏱️</span> <span id="nav-pomo-label">Pomodoro</span>
      </button>
      <button type="button" onclick="switchView('roadmap')" id="nav-btn-roadmap" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap">
        <span aria-hidden="true">🗺️</span> 12-Wk Plan
      </button>
    </nav>

    <!-- Right Controls -->
    <div class="flex items-center gap-1.5">
      <button type="button" id="open-cmdk-btn" class="px-2.5 py-1.5 rounded-lg ui-card border text-xs ui-text-muted hover:opacity-90 flex items-center gap-1.5 transition-colors" aria-label="Search all notes and problems">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <kbd class="px-1.5 py-0.5 text-xs font-mono ui-surface rounded border">⌘K</kbd>
      </button>

      <div class="flex items-center ui-card rounded-lg p-0.5 border text-xs" role="group" aria-label="Theme mode">
        <button type="button" onclick="setTheme('dark')" id="btn-theme-dark" class="px-2 py-1 rounded font-medium transition-all" title="Dark Mode">🌙 Dark</button>
        <button type="button" onclick="setTheme('light')" id="btn-theme-light" class="px-2 py-1 rounded font-medium transition-all" title="Light Mode">☀️ Light</button>
      </div>

      <button type="button" id="toggle-right-sidebar-btn" onclick="toggleRightSidebar()" class="p-1.5 rounded-lg ui-card border ui-text-muted hover:text-[var(--text)] transition-colors" title="Toggle Right 'On This Page' Column (Shortcut: o)">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7"/></svg>
      </button>
    </div>
  </header>

  <!-- ===================================================================== -->
  <!-- READER WORKSPACE (Used by both 📘 Concepts and 🧩 LeetCode Guides)    -->
  <!-- ===================================================================== -->
  <main id="view-reader" class="flex-1 min-h-0 flex overflow-hidden w-full">
    
    <aside id="reader-sidebar" class="w-[280px] min-w-[280px] max-w-[280px] shrink-0 ui-surface border-r flex flex-col h-full overflow-hidden">
      <div class="p-3 border-b ui-border space-y-2.5 shrink-0">
        <div class="flex items-center justify-between gap-2">
          <div class="grid grid-cols-3 gap-1 ui-card p-1 rounded-lg border text-xs flex-1" role="group" aria-label="Sidebar filter">
            <button type="button" onclick="setSidebarScope('concept')" id="sb-scope-concept" class="py-1 rounded font-semibold transition-colors">📘 Concepts</button>
            <button type="button" onclick="setSidebarScope('problem')" id="sb-scope-problem" class="py-1 rounded font-semibold transition-colors">🧩 Problems</button>
            <button type="button" onclick="setSidebarScope('all')" id="sb-scope-all" class="py-1 rounded font-semibold transition-colors">All (94)</button>
          </div>
          <button type="button" onclick="toggleLeftSidebar()" class="p-1.5 rounded-lg ui-card border ui-text-muted hover:text-[var(--text)]" title="Collapse left sidebar (b)">
            «
          </button>
        </div>

        <search>
          <input id="sidebar-filter-input" type="search" placeholder="Filter current list..." aria-label="Filter sidebar items" class="w-full ui-card border rounded-lg px-3 py-1.5 text-xs focus:outline-none">
        </search>

        <div class="flex items-center justify-between text-xs ui-text-muted px-1">
          <span id="sidebar-count-label">Showing items</span>
          <button type="button" id="toggle-all-cats-btn" class="hover:underline ui-accent-text">Collapse all</button>
        </div>
      </div>

      <div id="sidebar-tree" class="flex-1 min-h-0 overflow-y-auto p-2.5 space-y-2">
      </div>
    </aside>

    <div id="reader-scroll-container" class="flex-1 min-w-0 overflow-y-auto h-full px-4 sm:px-8 py-6">
      <div id="reader-inner-wrap" class="max-w-4xl mx-auto space-y-5 pb-16 transition-all">

        <div class="ui-card border rounded-xl p-3.5 flex flex-wrap items-center justify-between gap-3 shadow-sm">
          <div class="flex items-center gap-2 flex-wrap">
            <span id="doc-type-badge" class="text-xs font-semibold px-2.5 py-0.5 rounded-full border ui-accent-soft">Type</span>
            <span id="doc-cat-badge" class="text-xs font-medium px-2.5 py-0.5 rounded-full ui-surface border ui-text-muted">Module</span>
            <span id="doc-diff-badge" class="text-xs font-semibold px-2.5 py-0.5 rounded-full">Difficulty</span>
            <a id="doc-lc-link" href="#" target="_blank" rel="noopener noreferrer" class="hidden text-xs font-semibold ui-accent-text hover:underline flex items-center gap-1">
              LeetCode ↗
            </a>
          </div>

          <div class="flex items-center gap-2 flex-wrap">
            <div class="flex items-center ui-surface rounded-lg p-0.5 border text-xs" role="group" aria-label="Reading mode">
              <button type="button" onclick="setReaderMode('full')" id="mode-btn-full" class="px-2.5 py-1 rounded font-semibold ui-accent-soft border">
                Text + Diagrams
              </button>
              <button type="button" onclick="setReaderMode('visual')" id="mode-btn-visual" class="px-2.5 py-1 rounded font-medium ui-text-muted" title="Hide paragraphs and show only flowcharts, arrow traces, tables, and code">
                ⚡ Diagrams Only
              </button>
            </div>

            <button type="button" onclick="jumpToPlaythrough()" id="btn-open-playthrough" class="px-2.5 py-1 rounded-lg border ui-surface text-xs font-semibold hover:ui-accent-soft transition-colors flex items-center gap-1.5" title="Interactive step-by-step playthrough with Next/Prev">
              🎮 Interactive Playthrough
            </button>

            <button type="button" onclick="loadCurrentDocIntoPlayground()" id="btn-open-in-playground" class="px-2.5 py-1 rounded-lg border ui-surface text-xs font-semibold hover:ui-accent-soft transition-colors" title="Open and execute this guide's Python code in the browser playground">
              🐍 Run Code
            </button>

            <div class="flex items-center ui-surface rounded-lg p-0.5 border text-xs" role="group" aria-label="Study status">
              <button type="button" onclick="setCurrentDocStatus('todo')" id="status-btn-todo" class="px-2 py-1 rounded font-medium">○ Todo</button>
              <button type="button" onclick="setCurrentDocStatus('review')" id="status-btn-review" class="px-2 py-1 rounded font-medium">🔁 Review</button>
              <button type="button" onclick="setCurrentDocStatus('solved')" id="status-btn-solved" class="px-2 py-1 rounded font-medium">✓ Done</button>
            </div>
          </div>
        </div>

        <article id="rendered-content" class="md-body ui-card border rounded-2xl p-5 sm:p-8 shadow-sm">
        </article>

        <section class="ui-card border rounded-xl p-4 space-y-2" aria-label="Personal notes">
          <div class="flex items-center justify-between">
            <label for="doc-personal-note" class="text-xs font-bold uppercase tracking-wider ui-accent-text">📌 Personal Takeaway / Mistake to Remember</label>
            <span id="note-saved-indicator" class="text-xs ui-text-muted">Auto-saves locally</span>
          </div>
          <textarea id="doc-personal-note" rows="2" placeholder="Write your 1-sentence mental trigger or edge case for this topic..." class="w-full ui-surface border rounded-lg p-2.5 text-xs focus:outline-none"></textarea>
        </section>

        <nav class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2" aria-label="Document pagination">
          <button type="button" id="prev-doc-btn" class="ui-card border rounded-xl p-3.5 text-left hover:opacity-90 transition-all group">
            <div class="text-xs ui-text-muted">← Previous in List</div>
            <div id="prev-doc-title" class="text-sm font-semibold mt-0.5 ui-accent-text truncate">-</div>
          </button>
          <button type="button" id="next-doc-btn" class="ui-card border rounded-xl p-3.5 text-right hover:opacity-90 transition-all group">
            <div class="text-xs ui-text-muted">Next in List →</div>
            <div id="next-doc-title" class="text-sm font-semibold mt-0.5 ui-accent-text truncate">-</div>
          </button>
        </nav>

      </div>
    </div>

    <aside id="reader-toc-sidebar" class="w-[240px] min-w-[240px] max-w-[240px] shrink-0 ui-surface border-l p-4 h-full flex flex-col justify-between overflow-y-auto">
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold uppercase tracking-wider ui-text-muted">On This Page</span>
          <button type="button" onclick="toggleRightSidebar()" class="px-1.5 py-0.5 rounded ui-card border text-xs ui-text-muted hover:text-[var(--text)]" title="Collapse right sidebar (o)">
            »
          </button>
        </div>
        <nav id="toc-list" class="space-y-1.5 text-xs" aria-label="Table of contents">
        </nav>
      </div>
      <div class="ui-card border rounded-xl p-3 space-y-1.5 text-xs">
        <div class="font-semibold ui-accent-text">Keyboard Shortcuts</div>
        <div class="flex justify-between ui-text-muted"><span>Search all docs</span><kbd class="font-mono">⌘K / /</kbd></div>
        <div class="flex justify-between ui-text-muted"><span>Left / Right sidebar</span><kbd class="font-mono">b / o</kbd></div>
        <div class="flex justify-between ui-text-muted"><span>Prev / Next doc</span><kbd class="font-mono">[ / ]</kbd></div>
        <div class="flex justify-between ui-text-muted"><span>Diagrams Only</span><kbd class="font-mono">v</kbd></div>
      </div>
    </aside>

  </main>

  <!-- ===================================================================== -->
  <!-- VIEW 2: CHEAT SHEETS DECK (21 Quick-Reference Cards)                  -->
  <!-- ===================================================================== -->
  <section id="view-cheatsheets" class="hidden flex-1 min-h-0 overflow-y-auto h-full max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b ui-border pb-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold ui-accent-text">⚡ Pattern Cheat Sheets Deck (21)</h1>
        <p class="text-xs ui-text-muted mt-0.5">Quick-reference pattern triggers, decision flowcharts, and copy-paste templates.</p>
      </div>
      <search>
        <input id="cs-search-input" type="search" placeholder="Filter cheat sheets..." aria-label="Filter cheat sheets" class="ui-card border rounded-xl px-3.5 py-2 text-xs w-full sm:w-64 focus:outline-none">
      </search>
    </div>

    <div id="cheatsheets-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- VIEW: INTERACTIVE PYTHON 3 PLAYGROUND                                 -->
  <!-- ===================================================================== -->
  <section id="view-playground" class="hidden flex-1 min-h-0 overflow-y-auto h-full max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-4">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b ui-border pb-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold ui-accent-text flex items-center gap-2">
          <span>🐍</span> Python 3 Algorithm Playground
        </h1>
        <p class="text-xs ui-text-muted mt-0.5">Test sorting algorithms, two-pointer traces, and recursion trees in your browser. 100% client-side and offline.</p>
      </div>

      <div class="flex items-center gap-2 flex-wrap">
        <label for="playground-template-select" class="text-xs ui-text-muted font-medium">Template:</label>
        <select id="playground-template-select" onchange="onPlaygroundTemplateChange(this.value)" class="ui-card border rounded-lg px-2.5 py-1.5 text-xs font-semibold focus:outline-none">
          <optgroup label="Sorting Algorithms">
            <option value="bubble_sort">🫧 Bubble Sort (Step Trace)</option>
            <option value="selection_sort">🎯 Selection Sort</option>
            <option value="merge_sort">🌲 Merge Sort (Divide &amp; Conquer)</option>
            <option value="quick_sort">⚡ Quick Sort (Lomuto In-Place)</option>
            <option value="quickselect">🎯 Quickselect (LC 215 - O(N) Kth Largest)</option>
            <option value="bucket_sort">🪣 Bucket Sort (LC 347 - O(N) Frequency)</option>
            <option value="cyclic_sort">🔄 Cyclic Sort (LC 41 - O(N) In-Place [1..N])</option>
            <option value="heap_sort">🏔️ Heap Sort (In-Place Max Heapify)</option>
            <option value="sort_colors">🇳🇱 LC 75 Sort Colors (Dutch National Flag)</option>
          </optgroup>
          <optgroup label="Pointers &amp; Math">
            <option value="repeated_substring">🔁 LC 459 Repeated Substring Pattern</option>
            <option value="container_water">💧 LC 11 Container With Most Water</option>
          </optgroup>
          <optgroup label="Linked Lists">
            <option value="reverse_first_k">🔗 Reverse First K Nodes (Step Trace)</option>
            <option value="remove_elements">🗑️ LC 203 Remove Elements (3 Methods Compared)</option>
          </optgroup>
          <optgroup label="Recursion &amp; Backtracking">
            <option value="subsets">🌳 LC 78 Subsets (Backtracking)</option>
            <option value="n_queens">👑 LC 51 N-Queens (4x4 Board)</option>
            <option value="kth_grammar">🌲 LC 779 K-th Symbol in Grammar</option>
            <option value="diff_ways">🧮 LC 241 Different Ways to Add Parentheses</option>
          </optgroup>
          <option value="blank">📝 Blank Scratchpad</option>
        </select>
        <button type="button" onclick="loadCurrentDocIntoPlayground()" class="px-2.5 py-1.5 rounded-lg ui-card border text-xs font-semibold hover:ui-accent-soft transition-colors" title="Load solution code from the current note">
          📥 Load Current Note Code
        </button>
      </div>
    </div>

    <!-- Playground Controls Bar -->
    <div class="ui-card border rounded-xl p-3 flex flex-wrap items-center justify-between gap-3 shadow-sm">
      <div class="flex items-center gap-2">
        <button type="button" onclick="runPlaygroundCode()" id="playground-run-btn" class="ui-accent-btn px-4 py-1.5 rounded-lg font-bold text-xs flex items-center gap-1.5 shadow-sm hover:opacity-90 transition-all">
          <span aria-hidden="true">▶</span> Run Code <kbd class="opacity-75 font-mono text-[10px] ml-1">⌘↵</kbd>
        </button>
        <button type="button" onclick="clearPlaygroundConsole()" class="ui-surface border px-2.5 py-1.5 rounded-lg text-xs font-medium ui-text-muted hover:text-[var(--text)] transition-colors">
          Clear Console
        </button>
        <button type="button" onclick="resetPlaygroundCode()" class="ui-surface border px-2.5 py-1.5 rounded-lg text-xs font-medium ui-text-muted hover:text-[var(--text)] transition-colors">
          Reset Template
        </button>
      </div>

      <div class="flex items-center gap-2">
        <span id="playground-status-pill" class="px-2.5 py-0.5 rounded-full text-xs font-medium border ui-surface ui-text-muted">Ready</span>
        <span id="playground-time-pill" class="text-xs font-mono ui-text-muted"></span>
      </div>
    </div>

    <!-- Split Editor & Output Console -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div class="flex flex-col space-y-1.5">
        <div class="flex items-center justify-between text-xs px-1 ui-text-muted">
          <div class="flex items-center gap-2">
            <span class="font-bold uppercase tracking-wider text-[11px] flex items-center gap-1.5"><span class="text-[#00b8a3]">&lt;/&gt;</span> Python 3</span>
            <span id="editor-line-col-pill" class="text-[10px] font-mono px-1.5 py-0.5 rounded ui-surface border">Ln 1, Col 1</span>
          </div>
          <span class="text-[11px]">Auto-indent on ↵ • Tab 4 spaces</span>
        </div>
        
        <!-- LeetCode Monaco / CodeMirror Editor -->
        <div id="playground-editor-wrapper" class="relative w-full h-[520px] rounded-2xl border ui-border overflow-hidden bg-[#1e1e1e] shadow-inner font-mono text-xs focus-within:border-[var(--accent)] transition-colors">
          <textarea id="playground-code-input" spellcheck="false" class="hidden"></textarea>
        </div>
      </div>

      <div class="flex flex-col space-y-1.5">
        <div class="flex items-center justify-between text-xs px-1 ui-text-muted">
          <span class="font-bold uppercase tracking-wider text-[11px] flex items-center gap-1.5"><span class="text-sky-400">&gt;_</span> Test Result &amp; Console</span>
          <button type="button" onclick="copyPlaygroundOutput()" class="hover:underline ui-accent-text text-xs">Copy Output</button>
        </div>
        <div class="h-[520px] rounded-2xl border ui-border flex flex-col overflow-hidden shadow-inner bg-[#1e1e1e]">
          <pre id="playground-output" class="p-4 text-xs font-mono flex-1 overflow-y-auto whitespace-pre-wrap leading-relaxed select-text" style="color: #d4d4d4; background: #1e1e1e;">Click "▶ Run Code" or press ⌘+Enter to execute.</pre>
        </div>
      </div>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- VIEW 3: TOP INTERVIEW 150 & LEETCODE 75 PROBLEM TRACKER               -->
  <!-- ===================================================================== -->
  <section id="view-tracker" class="hidden flex-1 min-h-0 overflow-y-auto h-full max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
    
    <!-- Top Study Plan Progress Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
      <!-- Card 1: Top Interview 150 -->
      <div class="ui-card border rounded-2xl p-4 space-y-2">
        <div class="flex items-center justify-between text-xs">
          <span class="font-bold uppercase tracking-wider ui-accent-text">🔥 Top Interview 150</span>
          <span id="stat-150-pct" class="font-mono ui-text-muted">0%</span>
        </div>
        <div class="text-2xl font-black" id="stat-150-count">0 / 150</div>
        <div class="w-full ui-surface rounded-full h-2 overflow-hidden border">
          <div id="stat-150-bar" class="h-full transition-all duration-500" style="width: 0%; background-color: var(--accent);"></div>
        </div>
      </div>

      <!-- Card 2: LeetCode 75 -->
      <div class="ui-card border rounded-2xl p-4 space-y-2">
        <div class="flex items-center justify-between text-xs">
          <span class="font-bold uppercase tracking-wider text-sky-400">⚡ LeetCode 75</span>
          <span id="stat-75-pct" class="font-mono ui-text-muted">0%</span>
        </div>
        <div class="text-2xl font-black" id="stat-75-count">0 / 75</div>
        <div class="w-full ui-surface rounded-full h-2 overflow-hidden border">
          <div id="stat-75-bar" class="bg-sky-400 h-full transition-all duration-500" style="width: 0%;"></div>
        </div>
      </div>

      <!-- Card 3: Difficulty Breakdown -->
      <div class="ui-card border rounded-2xl p-4 flex flex-col justify-between">
        <div class="text-xs font-bold uppercase tracking-wider ui-text-muted">Total Solved Breakdown</div>
        <div class="flex items-baseline justify-between mt-1">
          <div class="text-2xl font-black ui-accent-text" id="stat-total-solved">0</div>
          <div class="flex items-center gap-2.5 text-xs font-mono">
            <span class="text-sky-400" id="stat-easy">0 E</span>
            <span class="text-amber-400" id="stat-medium">0 M</span>
            <span class="text-rose-400" id="stat-hard">0 H</span>
          </div>
        </div>
        <div class="text-xs ui-text-muted mt-1" id="stat-review-label">0 in review queue</div>
      </div>

      <!-- Card 4: Quick Actions -->
      <div class="ui-card border rounded-2xl p-4 flex flex-col justify-between">
        <div>
          <div class="text-xs font-bold uppercase tracking-wider ui-text-muted">Custom Problem Log</div>
          <p class="text-xs ui-text-muted mt-1">Solved an extra company-tagged problem?</p>
        </div>
        <button type="button" id="open-log-dialog-btn" class="mt-2 w-full py-2 px-3 rounded-xl ui-accent-btn font-semibold text-xs transition-all hover:opacity-90">
          + Log Custom Problem
        </button>
      </div>
    </div>

    <!-- Study Plan Tabs + Search + Category & Status Filters -->
    <div class="ui-card border rounded-2xl p-3.5 space-y-3">
      <!-- Row 1: Study Plan Selector Pills -->
      <div class="flex flex-wrap items-center justify-between gap-2 border-b ui-border pb-3">
        <div class="flex flex-wrap items-center gap-1.5 text-xs" role="group" aria-label="Study plan filter">
          <button type="button" onclick="setTrackerPlanFilter('ALL')" data-plan="ALL" class="trk-plan-btn px-3 py-1.5 rounded-xl font-semibold ui-accent-btn">
            All Curated (212)
          </button>
          <button type="button" onclick="setTrackerPlanFilter('150')" data-plan="150" class="trk-plan-btn px-3 py-1.5 rounded-xl font-medium ui-surface border ui-text-muted hover:text-[var(--text)]">
            🔥 Top Interview 150 (150)
          </button>
          <button type="button" onclick="setTrackerPlanFilter('75')" data-plan="75" class="trk-plan-btn px-3 py-1.5 rounded-xl font-medium ui-surface border ui-text-muted hover:text-[var(--text)]">
            ⚡ LeetCode 75 (75)
          </button>
          <button type="button" onclick="setTrackerPlanFilter('WITH_DOC')" data-plan="WITH_DOC" class="trk-plan-btn px-3 py-1.5 rounded-xl font-medium ui-surface border ui-text-muted hover:text-[var(--text)]">
            📖 Has Repo Study Guide
          </button>
        </div>

        <span id="tracker-showing-count" class="text-xs font-mono ui-text-muted">Showing 212 problems</span>
      </div>

      <!-- Row 2: Search Input + Topic Dropdown + Status Filter -->
      <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-2.5">
        <search class="flex-1">
          <input id="tracker-search-input" type="search" placeholder="Search by LC #, title, topic (e.g. Two Pointers, Graph, DP), or takeaway..." aria-label="Search tracker items" class="w-full ui-surface border rounded-xl px-3.5 py-1.5 text-xs focus:outline-none">
        </search>

        <div class="flex flex-wrap items-center gap-2">
          <select id="tracker-topic-filter" aria-label="Filter by topic" class="ui-surface border rounded-xl px-3 py-1.5 text-xs focus:outline-none">
            <option value="ALL">All 23 Topics</option>
          </select>

          <select id="tracker-diff-filter" aria-label="Filter by difficulty" class="ui-surface border rounded-xl px-2.5 py-1.5 text-xs focus:outline-none">
            <option value="ALL">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>

          <div class="flex items-center ui-surface rounded-xl p-0.5 border text-xs" role="group" aria-label="Filter by status">
            <button type="button" onclick="setTrackerStatusFilter('ALL')" data-status="ALL" class="tracker-status-btn px-2.5 py-1 rounded-lg font-semibold ui-accent-soft border">All</button>
            <button type="button" onclick="setTrackerStatusFilter('solved')" data-status="solved" class="tracker-status-btn px-2.5 py-1 rounded-lg font-medium ui-text-muted">✓ Solved</button>
            <button type="button" onclick="setTrackerStatusFilter('review')" data-status="review" class="tracker-status-btn px-2.5 py-1 rounded-lg font-medium ui-text-muted">🔁 Review</button>
            <button type="button" onclick="setTrackerStatusFilter('todo')" data-status="todo" class="tracker-status-btn px-2.5 py-1 rounded-lg font-medium ui-text-muted">○ Todo</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Problem Table -->
    <div class="ui-card border rounded-2xl overflow-hidden shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="ui-surface border-b ui-border ui-text-muted uppercase tracking-wider">
              <th class="py-3 px-3 w-28">Status</th>
              <th class="py-3 px-3">Problem</th>
              <th class="py-3 px-3 hidden sm:table-cell">Topic & Study Plans</th>
              <th class="py-3 px-3 hidden lg:table-cell">Your Takeaway / Core Trick</th>
              <th class="py-3 px-3 text-right w-44">Links</th>
            </tr>
          </thead>
          <tbody id="tracker-tbody" class="divide-y ui-border">
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- VIEW 4: POMODORO FOCUS TRACKER (With Smooth Harmonic Chime Alarm)     -->
  <!-- ===================================================================== -->
  <section id="view-pomodoro" class="hidden flex-1 min-h-0 overflow-y-auto h-full max-w-4xl w-full mx-auto px-4 sm:px-6 py-8 space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b ui-border pb-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold ui-accent-text">⏱️ Pomodoro & Interview Sprint Timer</h1>
        <p class="text-xs ui-text-muted mt-0.5">Runs in the background while you read notes • Plays a warm harmonic singing-bowl chime on completion.</p>
      </div>
      <div class="flex items-center gap-2">
        <select id="pomo-sound-select" aria-label="Alarm sound style" class="ui-card border rounded-lg px-2.5 py-1.5 text-xs focus:outline-none">
          <option value="chime">🔔 Warm Singing Bowl Chime</option>
          <option value="marimba">🎶 Soft Marimba Triad</option>
          <option value="crystal">✨ Crystal Bell Arpeggio</option>
        </select>
        <button type="button" onclick="playSmoothAlarm()" class="px-3 py-1.5 rounded-lg ui-card border text-xs font-semibold ui-accent-text hover:opacity-90">
          🔊 Test Chime
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
      <div class="md:col-span-3 ui-card border rounded-2xl p-6 flex flex-col items-center justify-between space-y-6 shadow-sm">
        <div class="flex flex-wrap items-center justify-center gap-1.5 ui-surface p-1.5 rounded-xl border text-xs w-full">
          <button type="button" onclick="setPomodoroPreset(25, 'Pomodoro Focus')" id="pomo-preset-25" class="pomo-preset-btn px-3 py-1.5 rounded-lg font-semibold ui-accent-btn">
            🍅 25m Focus
          </button>
          <button type="button" onclick="setPomodoroPreset(45, 'FAANG Mock Sprint')" id="pomo-preset-45" class="pomo-preset-btn px-3 py-1.5 rounded-lg font-medium ui-text-muted hover:text-[var(--text)]">
            ⚡ 45m FAANG Mock
          </button>
          <button type="button" onclick="setPomodoroPreset(5, 'Short Break')" id="pomo-preset-5" class="pomo-preset-btn px-3 py-1.5 rounded-lg font-medium ui-text-muted hover:text-[var(--text)]">
            ☕ 5m Break
          </button>
          <button type="button" onclick="setPomodoroPreset(15, 'Long Break')" id="pomo-preset-15" class="pomo-preset-btn px-3 py-1.5 rounded-lg font-medium ui-text-muted hover:text-[var(--text)]">
            🌿 15m Break
          </button>
        </div>

        <div class="relative w-56 h-56 flex items-center justify-center">
          <svg class="w-full h-full -rotate-90" viewBox="0 0 120 120" aria-hidden="true">
            <circle cx="60" cy="60" r="52" fill="none" stroke="var(--border)" stroke-width="6"></circle>
            <circle id="pomo-ring-circle" cx="60" cy="60" r="52" fill="none" stroke="var(--accent)" stroke-width="6" stroke-linecap="round" stroke-dasharray="326.7" stroke-dashoffset="0" class="transition-all duration-500"></circle>
          </svg>
          <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span id="pomo-mode-label" class="text-xs font-semibold uppercase tracking-wider ui-accent-text">Pomodoro Focus</span>
            <div id="pomo-time-display" class="text-5xl font-black font-mono tracking-tight my-1">25:00</div>
            <span id="pomo-status-sub" class="text-xs ui-text-muted">Ready to start</span>
          </div>
        </div>

        <div class="w-full space-y-1">
          <label for="pomo-task-input" class="text-xs ui-text-muted block">Focusing on topic / problem:</label>
          <input id="pomo-task-input" type="text" placeholder="e.g. 2D Matrices & Spiral Traversal (LC 54)" class="w-full ui-surface border rounded-xl px-3.5 py-2 text-xs focus:outline-none">
        </div>

        <div class="flex items-center justify-between gap-3 w-full pt-2 border-t ui-border">
          <div class="flex items-center gap-2">
            <button type="button" onclick="togglePomodoroStart()" id="pomo-start-btn" class="px-5 py-2 rounded-xl ui-accent-btn font-bold text-xs shadow-sm hover:opacity-90 transition-all">
              ▶ Start Focus
            </button>
            <button type="button" onclick="resetPomodoro()" class="px-3.5 py-2 rounded-xl ui-surface border text-xs font-semibold ui-text-muted hover:text-[var(--text)]">
              Reset
            </button>
          </div>

          <div class="flex items-center gap-1.5 text-xs">
            <label for="pomo-custom-min" class="ui-text-muted">Custom:</label>
            <input id="pomo-custom-min" type="number" min="1" max="180" value="25" class="w-14 ui-surface border rounded-lg px-2 py-1 text-center font-mono">
            <button type="button" onclick="applyCustomPomodoro()" class="px-2.5 py-1 rounded-lg ui-card border font-medium hover:opacity-90">Set</button>
          </div>
        </div>
      </div>

      <div class="md:col-span-2 flex flex-col justify-between space-y-4">
        <div class="grid grid-cols-2 gap-3">
          <div class="ui-card border rounded-2xl p-4">
            <div class="text-xs ui-text-muted">Sessions Today</div>
            <div id="pomo-stat-sessions" class="text-2xl font-black ui-accent-text mt-1">0</div>
            <div class="text-xs ui-text-muted mt-0.5">Completed blocks</div>
          </div>
          <div class="ui-card border rounded-2xl p-4">
            <div class="text-xs ui-text-muted">Focus Minutes</div>
            <div id="pomo-stat-minutes" class="text-2xl font-black text-sky-400 mt-1">0m</div>
            <div class="text-xs ui-text-muted mt-0.5">Deep work logged</div>
          </div>
        </div>

        <div class="ui-card border rounded-2xl p-4 flex-1 flex flex-col justify-between space-y-3">
          <div class="flex items-center justify-between border-b ui-border pb-2">
            <h2 class="text-xs font-bold uppercase tracking-wider ui-accent-text">Completed Focus Log</h2>
            <button type="button" onclick="clearPomodoroLog()" class="text-xs ui-text-muted hover:underline">Clear</button>
          </div>
          <div id="pomo-history-list" class="space-y-2 max-h-60 overflow-y-auto text-xs flex-1">
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ===================================================================== -->
  <!-- VIEW 5: 12-WEEK FAANG ROADMAP (With hidden="until-found" support)     -->
  <!-- ===================================================================== -->
  <section id="view-roadmap" class="hidden flex-1 min-h-0 overflow-y-auto h-full max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-5">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b ui-border pb-4">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold ui-accent-text">🗺️ 12-Week FAANG Preparation Roadmap</h1>
        <p class="text-xs ui-text-muted mt-0.5">2 problems/day on weekdays • 5/day on weekends • Click any topic to open its study note.</p>
      </div>
      <button type="button" onclick="openDocInReader('faang_preparation_plan.md')" class="px-3 py-1.5 rounded-lg ui-card border text-xs font-semibold ui-accent-text hover:opacity-90">
        Read Full Plan Doc →
      </button>
    </div>

    <div id="roadmap-accordion">
      <div class="flex items-center gap-2 overflow-x-auto pb-3" role="tablist">
        <button type="button" onclick="selectRoadmapPhase('rm-phase-1')" id="btn-rm-phase-1" aria-expanded="true" aria-controls="rm-phase-1" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-accent-soft border whitespace-nowrap">
          Phase 1: Arrays, Pointers & Windows (W1–3)
        </button>
        <button type="button" onclick="selectRoadmapPhase('rm-phase-2')" id="btn-rm-phase-2" aria-expanded="false" aria-controls="rm-phase-2" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap">
          Phase 2: Linked Lists, Stacks & Binary Search (W4–6)
        </button>
        <button type="button" onclick="selectRoadmapPhase('rm-phase-3')" id="btn-rm-phase-3" aria-expanded="false" aria-controls="rm-phase-3" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap">
          Phase 3: Pattern Cheat Sheets (W7–9)
        </button>
        <button type="button" onclick="selectRoadmapPhase('rm-phase-4')" id="btn-rm-phase-4" aria-expanded="false" aria-controls="rm-phase-4" class="rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap">
          Phase 4: System Design & Architecture (W10–12)
        </button>
      </div>

      <div id="rm-phase-1" class="rm-panel">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2" id="rm-phase-1-grid"></div>
      </div>
      <div id="rm-phase-2" class="rm-panel" hidden="until-found">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2" id="rm-phase-2-grid"></div>
      </div>
      <div id="rm-phase-3" class="rm-panel" hidden="until-found">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2" id="rm-phase-3-grid"></div>
      </div>
      <div id="rm-phase-4" class="rm-panel" hidden="until-found">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2" id="rm-phase-4-grid"></div>
      </div>
    </div>
  </section>

  <!-- NATIVE DIALOGS -->
  <dialog id="cmdk-dialog" closedby="any" class="ui-card border rounded-2xl w-full max-w-xl p-0 text-[var(--text)] shadow-2xl">
    <div class="p-3.5 border-b ui-border flex items-center gap-2.5">
      <svg class="w-4 h-4 ui-text-muted shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      <search class="flex-1">
        <input id="cmdk-input" type="search" placeholder="Search any concept, LC #, pattern, or keyword..." aria-label="Search all study guides" class="w-full bg-transparent text-sm focus:outline-none">
      </search>
      <form method="dialog">
        <button type="submit" class="px-2 py-0.5 rounded text-xs ui-surface border ui-text-muted">Esc</button>
      </form>
    </div>
    <div id="cmdk-results" class="max-h-96 overflow-y-auto p-2 space-y-1">
    </div>
  </dialog>

  <dialog id="peek-dialog" closedby="any" class="ui-card border rounded-2xl w-full max-w-3xl p-0 text-[var(--text)] shadow-2xl max-h-[88vh]">
    <div class="sticky top-0 z-10 ui-surface border-b px-5 py-3 flex items-center justify-between gap-3">
      <div class="flex items-center gap-2 truncate">
        <span id="peek-title" class="font-bold text-sm truncate">Study Guide</span>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <button type="button" id="peek-open-full-btn" class="px-3 py-1 rounded-lg ui-accent-btn font-semibold text-xs">
          Open Full Reader ↗
        </button>
        <form method="dialog">
          <button type="submit" class="px-2.5 py-1 rounded-lg ui-card border text-xs ui-text-muted">Close (Esc)</button>
        </form>
      </div>
    </div>
    <div id="peek-body" class="p-6 overflow-y-auto max-h-[calc(88vh-56px)] md-body">
    </div>
  </dialog>

  <dialog id="log-dialog" closedby="any" class="ui-card border rounded-2xl w-full max-w-md p-5 text-[var(--text)] shadow-2xl">
    <div class="flex items-center justify-between border-b ui-border pb-3 mb-4">
      <h2 class="text-base font-bold">Log Solved Problem</h2>
      <form method="dialog">
        <button type="submit" class="text-xs px-2 py-1 rounded ui-surface border ui-text-muted">Esc</button>
      </form>
    </div>
    <form id="custom-problem-form" class="space-y-3 text-xs">
      <div class="grid grid-cols-3 gap-2">
        <div>
          <label for="cp-num" class="block ui-text-muted mb-1">LC #</label>
          <input id="cp-num" type="number" required placeholder="42" class="w-full ui-surface border rounded-lg px-2.5 py-1.5">
        </div>
        <div class="col-span-2">
          <label for="cp-title" class="block ui-text-muted mb-1">Title</label>
          <input id="cp-title" type="text" required placeholder="Trapping Rain Water" class="w-full ui-surface border rounded-lg px-2.5 py-1.5">
        </div>
      </div>
      <div class="grid grid-cols-2 gap-2">
        <div>
          <label for="cp-diff" class="block ui-text-muted mb-1">Difficulty</label>
          <select id="cp-diff" class="w-full ui-surface border rounded-lg px-2.5 py-1.5">
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
        <div>
          <label for="cp-pattern" class="block ui-text-muted mb-1">Topic / Pattern</label>
          <input id="cp-pattern" type="text" required placeholder="Two Pointers" class="w-full ui-surface border rounded-lg px-2.5 py-1.5">
        </div>
      </div>
      <div>
        <label for="cp-note" class="block ui-text-muted mb-1">1-Line Takeaway</label>
        <textarea id="cp-note" rows="2" placeholder="Track left_max and right_max inward from the shorter wall." class="w-full ui-surface border rounded-lg px-2.5 py-1.5"></textarea>
      </div>
      <div class="flex justify-end gap-2 pt-2 border-t ui-border">
        <button type="button" onclick="document.getElementById('log-dialog').close()" class="px-3 py-1.5 rounded-lg ui-surface border">Cancel</button>
        <button type="submit" class="px-3.5 py-1.5 rounded-lg ui-accent-btn font-semibold">Save Problem</button>
      </div>
    </form>
  </dialog>

  <script>
    const DOCS_DATA = {docs_json_str};
    const DOC_KEYS = Object.keys(DOCS_DATA);
    const CURATED_CATALOG = {problems_json_str};
    const DEFAULT_INITIAL_VIEW = "{default_view}";

    const PROB_STATUS_KEY = 'dsa_hub_prob_status_v3';
    const DOC_STATUS_KEY = 'dsa_hub_status_v2';
    const NOTES_STORAGE_KEY = 'dsa_hub_notes_v2';
    const CUSTOM_PROBS_KEY = 'dsa_hub_custom_probs_v2';
    const THEME_KEY = 'dsa_hub_palette_v3';
    const LEFT_SB_KEY = 'dsa_hub_left_sb_open';
    const RIGHT_SB_KEY = 'dsa_hub_right_sb_open';
    const POMO_LOG_KEY = 'dsa_hub_pomo_log_v1';

    let probStatusMap = {{}}; // keyed by "lc-<number>"
    let docStatusMap = {{}};  // keyed by doc path
    let docNotesMap = {{}};
    let customProblems = [];
    let pomoHistory = [];
    let currentView = DEFAULT_INITIAL_VIEW;
    let sidebarScope = 'concept';
    let currentDocPath = "00_foundations/01_algorithms_correctness_efficiency.md";
    let readerMode = 'full';
    let showFlowcharts = true;
    let trackerPlanFilter = 'ALL'; // 'ALL' | '150' | '75' | 'WITH_DOC'
    let trackerStatusFilter = 'ALL';
    let isLeftSidebarOpen = true;
    let isRightSidebarOpen = true;

    // 1. Initialize Storage
    function initState() {{
      try {{
        const savedDocStatus = localStorage.getItem(DOC_STATUS_KEY);
        if (savedDocStatus) {{
          docStatusMap = JSON.parse(savedDocStatus);
        }} else {{
          DOC_KEYS.forEach(k => {{
            if (DOCS_DATA[k].defaultSolved) docStatusMap[k] = 'solved';
          }});
          localStorage.setItem(DOC_STATUS_KEY, JSON.stringify(docStatusMap));
        }}

        const savedProbStatus = localStorage.getItem(PROB_STATUS_KEY);
        if (savedProbStatus) {{
          probStatusMap = JSON.parse(savedProbStatus);
        }} else {{
          CURATED_CATALOG.forEach(p => {{
            if (p.defaultSolved || (p.docPath && docStatusMap[p.docPath] === 'solved')) {{
              probStatusMap['lc-' + p.number] = 'solved';
            }}
          }});
          localStorage.setItem(PROB_STATUS_KEY, JSON.stringify(probStatusMap));
        }}

        const savedNotes = localStorage.getItem(NOTES_STORAGE_KEY);
        if (savedNotes) docNotesMap = JSON.parse(savedNotes);

        const savedCustom = localStorage.getItem(CUSTOM_PROBS_KEY);
        if (savedCustom) customProblems = JSON.parse(savedCustom);

        const savedPomo = localStorage.getItem(POMO_LOG_KEY);
        if (savedPomo) pomoHistory = JSON.parse(savedPomo);

        const savedLeft = localStorage.getItem(LEFT_SB_KEY);
        if (savedLeft !== null) isLeftSidebarOpen = savedLeft === 'true';
        else isLeftSidebarOpen = window.innerWidth >= 900;

        const savedRight = localStorage.getItem(RIGHT_SB_KEY);
        if (savedRight !== null) isRightSidebarOpen = savedRight === 'true';
        else isRightSidebarOpen = window.innerWidth >= 1280;
      }} catch (e) {{
        console.warn(e);
      }}

      // Populate Topic filter dropdown in Tracker
      const topicSelect = document.getElementById('tracker-topic-filter');
      if (topicSelect) {{
        const topics = Array.from(new Set(CURATED_CATALOG.map(p => p.topic))).sort();
        topics.forEach(t => {{
          const opt = document.createElement('option');
          opt.value = t;
          opt.textContent = t;
          topicSelect.appendChild(opt);
        }});
      }}
    }}

    function getProbStatus(num) {{
      return probStatusMap['lc-' + num] || 'todo';
    }}

    function setProbStatus(num, status) {{
      probStatusMap['lc-' + num] = status;
      localStorage.setItem(PROB_STATUS_KEY, JSON.stringify(probStatusMap));
      // Sync with docStatusMap if problem has a local study doc
      const item = CURATED_CATALOG.find(p => p.number === num);
      if (item && item.docPath) {{
        docStatusMap[item.docPath] = status;
        localStorage.setItem(DOC_STATUS_KEY, JSON.stringify(docStatusMap));
      }}
      updateGlobalProgressPill();
      renderSidebarTree();
      if (currentView === 'tracker') renderTrackerTable();
      if (currentView === 'roadmap') renderRoadmapGrids();
      if (DOCS_DATA[currentDocPath]?.lcNumber === num) updateReaderStatusButtons();
    }}

    function getDocStatus(path) {{
      const d = DOCS_DATA[path];
      if (d && d.lcNumber) return getProbStatus(d.lcNumber);
      return docStatusMap[path] || 'todo';
    }}

    function setDocStatus(path, status) {{
      const d = DOCS_DATA[path];
      if (d && d.lcNumber) {{
        setProbStatus(d.lcNumber, status);
        return;
      }}
      docStatusMap[path] = status;
      localStorage.setItem(DOC_STATUS_KEY, JSON.stringify(docStatusMap));
      updateGlobalProgressPill();
      renderSidebarTree();
      if (currentDocPath === path) updateReaderStatusButtons();
      if (currentView === 'roadmap') renderRoadmapGrids();
    }}

    function updateGlobalProgressPill() {{
      const solved150 = CURATED_CATALOG.filter(p => p.in150 && getProbStatus(p.number) === 'solved').length;
      const solved75 = CURATED_CATALOG.filter(p => p.in75 && getProbStatus(p.number) === 'solved').length;
      const pill = document.getElementById('global-progress-pill');
      if (pill) pill.textContent = `🔥 Top 150: ${{solved150}}/150 • ⚡ LC 75: ${{solved75}}/75`;
    }}

    // 2. Collapsible Left & Right Sidebars
    function applySidebarVisibility() {{
      const leftSb = document.getElementById('reader-sidebar');
      const rightSb = document.getElementById('reader-toc-sidebar');
      const leftBtn = document.getElementById('toggle-left-sidebar-btn');
      const rightBtn = document.getElementById('toggle-right-sidebar-btn');
      const innerWrap = document.getElementById('reader-inner-wrap');

      if (leftSb) {{
        if (isLeftSidebarOpen) {{
          leftSb.classList.remove('hidden');
          leftBtn.classList.add('ui-accent-soft');
        }} else {{
          leftSb.classList.add('hidden');
          leftBtn.classList.remove('ui-accent-soft');
        }}
      }}

      if (rightSb) {{
        if (isRightSidebarOpen) {{
          rightSb.classList.remove('hidden');
          rightBtn.classList.add('ui-accent-soft');
        }} else {{
          rightSb.classList.add('hidden');
          rightBtn.classList.remove('ui-accent-soft');
        }}
      }}

      if (innerWrap) {{
        if (!isLeftSidebarOpen && !isRightSidebarOpen) {{
          innerWrap.className = 'max-w-4xl mx-auto space-y-5 pb-16 transition-all';
        }} else {{
          innerWrap.className = 'max-w-3xl mx-auto space-y-5 pb-16 transition-all';
        }}
      }}
    }}

    function toggleLeftSidebar() {{
      isLeftSidebarOpen = !isLeftSidebarOpen;
      localStorage.setItem(LEFT_SB_KEY, String(isLeftSidebarOpen));
      applySidebarVisibility();
    }}

    function toggleRightSidebar() {{
      isRightSidebarOpen = !isRightSidebarOpen;
      localStorage.setItem(RIGHT_SB_KEY, String(isRightSidebarOpen));
      applySidebarVisibility();
    }}

    // 3. Pomodoro Timer & Smooth Web Audio Harmonic Chime
    let pomoTotalSeconds = 25 * 60;
    let pomoRemainingSeconds = 25 * 60;
    let pomoModeTitle = 'Pomodoro Focus';
    let pomoInterval = null;
    let audioCtx = null;

    function playSmoothAlarm() {{
      try {{
        if (!audioCtx) {{
          const AudioContextClass = window.AudioContext || window.webkitAudioContext;
          audioCtx = new AudioContextClass();
        }}
        if (audioCtx.state === 'suspended') audioCtx.resume();

        const style = document.getElementById('pomo-sound-select')?.value || 'chime';
        const now = audioCtx.currentTime;

        const presets = {{
          chime:   {{ freqs: [523.25, 659.25, 783.99, 987.77, 1046.50], wave: 'sine',     gap: 0.22, dur: 2.4 }},
          marimba: {{ freqs: [440.00, 554.37, 659.25, 880.00],          wave: 'triangle', gap: 0.14, dur: 1.4 }},
          crystal: {{ freqs: [587.33, 880.00, 1174.66, 1479.98],        wave: 'sine',     gap: 0.18, dur: 2.0 }}
        }};
        const cfg = presets[style] || presets.chime;

        cfg.freqs.forEach((freq, idx) => {{
          const start = now + idx * cfg.gap;
          const osc = audioCtx.createOscillator();
          const overtone = audioCtx.createOscillator();
          const gain = audioCtx.createGain();

          osc.type = cfg.wave;
          osc.frequency.setValueAtTime(freq, start);

          overtone.type = 'sine';
          overtone.frequency.setValueAtTime(freq * 2, start);

          gain.gain.setValueAtTime(0.0001, start);
          gain.gain.linearRampToValueAtTime(0.16, start + 0.04);
          gain.gain.exponentialRampToValueAtTime(0.0001, start + cfg.dur);

          osc.connect(gain);
          overtone.connect(gain);
          gain.connect(audioCtx.destination);

          osc.start(start);
          overtone.start(start);
          osc.stop(start + cfg.dur + 0.05);
          overtone.stop(start + cfg.dur + 0.05);
        }});
      }} catch (e) {{
        console.warn('Audio chime error:', e);
      }}
    }}

    function formatMMSS(sec) {{
      const m = Math.floor(sec / 60);
      const s = sec % 60;
      return `${{String(m).padStart(2, '0')}}:${{String(s).padStart(2, '0')}}`;
    }}

    function updatePomodoroUI() {{
      const timeStr = formatMMSS(pomoRemainingSeconds);
      const disp = document.getElementById('pomo-time-display');
      if (disp) disp.textContent = timeStr;

      const modeLbl = document.getElementById('pomo-mode-label');
      if (modeLbl) modeLbl.textContent = pomoModeTitle;

      const ring = document.getElementById('pomo-ring-circle');
      if (ring && pomoTotalSeconds > 0) {{
        const fraction = 1 - (pomoRemainingSeconds / pomoTotalSeconds);
        ring.style.strokeDashoffset = String(326.7 * fraction);
      }}

      const navLbl = document.getElementById('nav-pomo-label');
      if (navLbl) {{
        if (pomoInterval) {{
          navLbl.textContent = timeStr;
        }} else if (pomoRemainingSeconds < pomoTotalSeconds && pomoRemainingSeconds > 0) {{
          navLbl.textContent = `${{timeStr}} (Paused)`;
        }} else {{
          navLbl.textContent = 'Pomodoro';
        }}
      }}
    }}

    function setPomodoroPreset(minutes, label) {{
      if (pomoInterval) {{
        clearInterval(pomoInterval);
        pomoInterval = null;
      }}
      pomoTotalSeconds = minutes * 60;
      pomoRemainingSeconds = pomoTotalSeconds;
      pomoModeTitle = label;
      document.getElementById('pomo-custom-min').value = minutes;
      document.getElementById('pomo-start-btn').textContent = '▶ Start Focus';
      document.getElementById('pomo-status-sub').textContent = 'Ready to start';

      [25, 45, 5, 15].forEach(m => {{
        const btn = document.getElementById(`pomo-preset-${{m}}`);
        if (!btn) return;
        if (m === minutes) {{
          btn.className = 'pomo-preset-btn px-3 py-1.5 rounded-lg font-semibold ui-accent-btn';
        }} else {{
          btn.className = 'pomo-preset-btn px-3 py-1.5 rounded-lg font-medium ui-text-muted hover:text-[var(--text)]';
        }}
      }});

      updatePomodoroUI();
    }}

    function applyCustomPomodoro() {{
      const mins = Math.max(1, Math.min(180, parseInt(document.getElementById('pomo-custom-min').value, 10) || 25));
      setPomodoroPreset(mins, `Custom ${{mins}}m Focus`);
    }}

    function togglePomodoroStart() {{
      const startBtn = document.getElementById('pomo-start-btn');
      const sub = document.getElementById('pomo-status-sub');

      if (!audioCtx) {{
        try {{
          const AudioContextClass = window.AudioContext || window.webkitAudioContext;
          audioCtx = new AudioContextClass();
        }} catch (e) {{}}
      }}

      if (pomoInterval) {{
        clearInterval(pomoInterval);
        pomoInterval = null;
        startBtn.textContent = '▶ Resume';
        sub.textContent = 'Paused';
        updatePomodoroUI();
        return;
      }}

      if (pomoRemainingSeconds <= 0) {{
        pomoRemainingSeconds = pomoTotalSeconds;
      }}

      startBtn.textContent = '⏸ Pause';
      sub.textContent = 'Focusing... (stays active across tabs)';

      pomoInterval = setInterval(() => {{
        pomoRemainingSeconds -= 1;
        updatePomodoroUI();

        if (pomoRemainingSeconds <= 0) {{
          clearInterval(pomoInterval);
          pomoInterval = null;
          startBtn.textContent = '▶ Start Again';
          sub.textContent = '🎉 Session Complete!';
          playSmoothAlarm();

          const minsCompleted = Math.round(pomoTotalSeconds / 60);
          const taskField = document.getElementById('pomo-task-input');
          const taskName = (taskField && taskField.value.trim()) || DOCS_DATA[currentDocPath]?.shortTitle || pomoModeTitle;
          pomoHistory.unshift({{
            id: 'pomo-' + Date.now(),
            title: taskName,
            minutes: minsCompleted,
            mode: pomoModeTitle,
            time: new Date().toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit' }})
          }});
          localStorage.setItem(POMO_LOG_KEY, JSON.stringify(pomoHistory));
          renderPomodoroHistory();
          updatePomodoroUI();
        }}
      }}, 1000);

      updatePomodoroUI();
    }}

    function resetPomodoro() {{
      if (pomoInterval) {{
        clearInterval(pomoInterval);
        pomoInterval = null;
      }}
      pomoRemainingSeconds = pomoTotalSeconds;
      document.getElementById('pomo-start-btn').textContent = '▶ Start Focus';
      document.getElementById('pomo-status-sub').textContent = 'Ready to start';
      updatePomodoroUI();
    }}

    function renderPomodoroHistory() {{
      const totalSessions = pomoHistory.length;
      const totalMins = pomoHistory.reduce((acc, s) => acc + (s.minutes || 0), 0);
      const sessEl = document.getElementById('pomo-stat-sessions');
      const minEl = document.getElementById('pomo-stat-minutes');
      const listEl = document.getElementById('pomo-history-list');

      if (sessEl) sessEl.textContent = totalSessions;
      if (minEl) minEl.textContent = `${{totalMins}}m`;
      if (!listEl) return;

      if (pomoHistory.length === 0) {{
        listEl.innerHTML = '<div class="ui-text-muted py-6 text-center">No completed sessions yet today. Start a 25m focus block above!</div>';
        return;
      }}

      listEl.innerHTML = pomoHistory.map(item => `
        <div class="ui-surface border rounded-xl p-2.5 flex items-center justify-between gap-2">
          <div class="truncate">
            <div class="font-semibold truncate">${{item.title}}</div>
            <div class="ui-text-muted">${{item.mode}} • ${{item.time}}</div>
          </div>
          <span class="px-2 py-0.5 rounded ui-accent-soft border font-mono shrink-0">+${{item.minutes}}m</span>
        </div>
      `).join('');
    }}

    // 3.5 Python Playground Controller (Client-Side Skulpt Runtime)
    const PLAYGROUND_TEMPLATES = {{
      bubble_sort: `# 🫧 Bubble Sort with Live Step Trace
def bubble_sort(arr):
    n = len(arr)
    print("Initial array:", arr)
    print()
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        print("Pass", i + 1, "(locked", arr[n - 1 - i], "at end):", arr)
        if not swapped:
            print(">> Early break: array is already sorted!")
            break
    return arr

nums = [64, 34, 25, 12, 22, 11, 90]
print("Final Sorted:", bubble_sort(nums))
`,
      selection_sort: `# 🎯 Selection Sort
def selection_sort(arr):
    n = len(arr)
    print("Initial array:", arr)
    print()
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        print("Pass", i + 1, "(placed", arr[i], "at idx", str(i) + "):", arr)
    return arr

nums = [29, 10, 14, 37, 13]
print("Final Sorted:", selection_sort(nums))
`,
      merge_sort: `# 🌲 Merge Sort with Divide & Conquer Trace
def merge_sort(arr, depth=0):
    indent = "  " * depth
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    print(indent + "Split -> Left:", arr[:mid], "| Right:", arr[mid:])

    left = merge_sort(arr[:mid], depth + 1)
    right = merge_sort(arr[mid:], depth + 1)

    merged = merge(left, right)
    print(indent + "Merged:", left, "+", right, "->", merged)
    return merged

def merge(left, right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

nums = [38, 27, 43, 3, 9, 82, 10]
print("Initial array:", nums)
print()
sorted_nums = merge_sort(nums)
print()
print("Final Sorted Array:", sorted_nums)
`,
      quick_sort: `# ⚡ Quick Sort (Lomuto In-Place Partition Trace)
def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    print("Partition range [" + str(low) + ".." + str(high) + "], Pivot:", pivot)
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            if i != j:
                print("  Swap arr[" + str(i) + "] with arr[" + str(j) + "] ->", arr)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    print("  Lock Pivot", pivot, "at index", i + 1, "->", arr)
    print()
    return i + 1

nums = [10, 80, 30, 90, 40, 50, 70]
print("Initial array:", nums)
print()
quick_sort(nums)
print("Final Sorted Array:", nums)
`,
      quickselect: `# 🎯 Quickselect: O(N) Average K-th Largest Element (LC 215 - MAANG Staple)
def find_kth_largest(nums, k):
    target_idx = len(nums) - k

    def quickselect(left, right):
        pivot = nums[right]
        i = left
        for j in range(left, right):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[right] = nums[right], nums[i]

        print("Pivot " + str(pivot) + " locked at index " + str(i) + " | Array: " + str(nums))

        if i == target_idx:
            return nums[i]
        elif i < target_idx:
            print("  Target is to the RIGHT (searching [" + str(i + 1) + ".." + str(right) + "])")
            return quickselect(i + 1, right)
        else:
            print("  Target is to the LEFT (searching [" + str(left) + ".." + str(i - 1) + "])")
            return quickselect(left, i - 1)

    print("Finding " + str(k) + "-th largest in " + str(nums) + " (Target sorted index: " + str(target_idx) + ")")
    print()
    return quickselect(0, len(nums) - 1)

arr = [3, 2, 1, 5, 6, 4]
ans = find_kth_largest(arr, k=2)
print()
print("Result: 2nd Largest Element is:", ans)
`,
      bucket_sort: `# 🪣 Bucket Sort: O(N) Linear Time (LC 347 Top K Frequent - Google/Meta Favorite)
def top_k_frequent(nums, k):
    # Step 1: Frequency map - O(N)
    counts = {{}}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    print("Frequency counts:", counts)

    # Step 2: Buckets where index = frequency - O(N)
    # At most, any number can appear len(nums) times
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in counts.items():
        buckets[freq].append(num)

    print("Frequency Buckets (idx = count):")
    for freq in range(len(buckets)):
        if buckets[freq]:
            print("  Freq " + str(freq) + ": " + str(buckets[freq]))

    # Step 3: Gather top k by scanning buckets backwards - O(N)
    res = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            res.append(num)
            if len(res) == k:
                return res
    return res

nums = [1, 1, 1, 2, 2, 3, 3, 3, 3, 4]
k = 2
print("Top " + str(k) + " frequent in:", nums)
print("Result:", top_k_frequent(nums, k))
`,
      cyclic_sort: `# 🔄 Cyclic Sort: O(N) Time, O(1) Space for [1..N] (LC 41 / LC 268 - FAANG Classic)
def first_missing_positive(nums):
    # Rule: Value x belongs at index x - 1
    n = len(nums)
    print("Initial array:", nums)
    print()

    i = 0
    while i < n:
        correct_idx = nums[i] - 1
        # Place nums[i] at correct_idx if in range [1..n] and not duplicate
        if 1 <= nums[i] <= n and nums[i] != nums[correct_idx]:
            val = nums[i]
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
            print("Swapped " + str(val) + " to index " + str(correct_idx) + " ->", nums)
        else:
            i += 1

    print()
    print("Array after cyclic placement:", nums)

    # First index where nums[i] != i + 1 is our missing answer
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1

nums = [3, 4, -1, 1]
ans = first_missing_positive(nums)
print("First Missing Positive:", ans)
`,
      heap_sort: `# 🏔️ In-Place Heap Sort (O(N log N) Time, O(1) Space)
def heap_sort(arr):
    n = len(arr)
    print("Initial array:", arr)
    print()

    # Step 1: Build max heap (sift down from last parent to root)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)
    print("Max Heap built:", arr)
    print()

    # Step 2: Extract elements one by one from end to front
    for i in range(n - 1, 0, -1):
        # Swap current max (arr[0]) with arr[i]
        arr[0], arr[i] = arr[i], arr[0]
        print("Locked max " + str(arr[i]) + " at index " + str(i) + " ->", arr)
        # Restore heap on reduced tree
        sift_down(arr, i, 0)
    return arr

def sift_down(arr, n, root):
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        sift_down(arr, n, largest)

nums = [12, 11, 13, 5, 6, 7]
print("Sorted Array:", heap_sort(nums))
`,
      sort_colors: `# 🇳🇱 LeetCode 75: Sort Colors (Dutch National Flag)
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    print("Initial:", nums)
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[high], nums[mid] = nums[mid], nums[high]
            high -= 1
        print("mid=" + str(mid) + ", low=" + str(low) + ", high=" + str(high) + " ->", nums)
    return nums

nums = [2, 0, 2, 1, 1, 0]
print("Sorted Colors:", sort_colors(nums))
`,
      repeated_substring: `# 🔁 LeetCode 459: Repeated Substring Pattern
def repeated_substring_pattern(s: str) -> bool:
    # Method 1: Doubling trick
    doubled_check = s in (s + s)[1:-1]

    # Method 2: Divisor chunking
    n = len(s)
    divisor_match = False
    for L in range(1, (n // 2) + 1):
        if n % L == 0:
            chunk = s[:L]
            if chunk * (n // L) == s:
                divisor_match = True
                print("Match found! Chunk '" + chunk + "' of size", L, "repeated", n // L, "times.")
                break
    return doubled_check

tests = ["abab", "aba", "abcabcabcabc"]
for t in tests:
    print("'" + t + "' ->", repeated_substring_pattern(t))
    print()
`,
      container_water: `# 💧 LeetCode 11: Container With Most Water
def max_area(height):
    l, r = 0, len(height) - 1
    max_w = 0
    while l < r:
        w = r - l
        h = min(height[l], height[r])
        area = w * h
        max_w = max(max_w, area)
        print("l=" + str(l) + " (h=" + str(height[l]) + "), r=" + str(r) + " (h=" + str(height[r]) + ") -> area=" + str(area))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return max_w

heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
print("Max Water Area:", max_area(heights))
`,
      n_queens: `# 👑 LeetCode 51: N-Queens Backtracking
def solve_n_queens(n):
    res = []
    board = [["."] * n for _ in range(n)]
    cols, diag, anti_diag = set(), set(), set()

    def backtrack(r):
        if r == n:
            res.append(["".join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti_diag:
                continue
            board[r][c] = "Q"
            cols.add(c); diag.add(r - c); anti_diag.add(r + c)
            backtrack(r + 1)
            board[r][c] = "."
            cols.remove(c); diag.remove(r - c); anti_diag.remove(r + c)

    backtrack(0)
    return res

solutions = solve_n_queens(4)
print("Found", len(solutions), "solutions for 4-Queens:")
print()
for i, sol in enumerate(solutions, 1):
    print("Solution #" + str(i) + ":")
    for row in sol:
        print("  " + " ".join(row))
    print()
`,
      subsets: `# 🌳 LeetCode 78: Subsets (Power Set)
def subsets(nums):
    res, path = [], []
    def backtrack(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    backtrack(0)
    return res

nums = [1, 2, 3]
print("All subsets of", nums, ":")
for s in subsets(nums):
    print(" ", s)
`,
      kth_grammar: `# 🌲 LeetCode 779: K-th Symbol in Grammar
def kth_grammar(n: int, k: int) -> int:
    if n == 1 and k == 1:
        return 0
    mid = 2 ** (n - 2)
    if k <= mid:
        return kth_grammar(n - 1, k)
    return 1 - kth_grammar(n - 1, k - mid)

for row in range(1, 5):
    line = [str(kth_grammar(row, col)) for col in range(1, 2 ** (row - 1) + 1)]
    print("Row " + str(row) + ": " + " ".join(line))
`,
      diff_ways: `# 🧮 LeetCode 241: Different Ways to Add Parentheses
def diff_ways(expression: str):
    res = []
    for i, ch in enumerate(expression):
        if ch in "+-*":
            left = diff_ways(expression[:i])
            right = diff_ways(expression[i + 1:])
            for l in left:
                for r in right:
                    if ch == "+": res.append(l + r)
                    elif ch == "-": res.append(l - r)
                    elif ch == "*": res.append(l * r)
    return res if res else [int(expression)]

expr = "2*3-4*5"
print("All parenthesizations of '" + expr + "':")
print(sorted(diff_ways(expr)))
`,
      reverse_first_k: `# 🔗 Reverse First K Nodes of a Linked List (In-Place Step Trace)
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_first_k(head, k):
    print("Initial Linked List:", to_list(head))
    print("Goal: reverse the first", k, "nodes in-place")
    print()
    if not head or k <= 1:
        return head

    prev = None
    cur = head

    # 1. Reverse first k nodes
    count = k
    while count > 0 and cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
        count -= 1
        print("Flipped Node " + str(prev.val) + " -> prev is at Node(" + str(prev.val) + "), cur is at Node(" + str(cur.val if cur else 'null') + ")")

    print()
    print("While loop finished!")
    print("  prev is at Node(" + str(prev.val) + ")  <-- FRONT of reversed chunk!")
    print("  head is at Node(" + str(head.val) + ")  <-- TAIL of reversed chunk!")
    print("  cur is at Node(" + str(cur.val if cur else 'null') + ")   <-- START of remaining list")

    # 2. The Bridge
    head.next = cur
    print()
    print("Bridge executed: head.next = cur")
    print("  Node(" + str(head.val) + ") is now glued to Node(" + str(cur.val if cur else 'null') + ")")

    # 3. Return prev
    print("Returning prev: the new head of the whole list is Node(" + str(prev.val) + ")!")
    return prev

def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

def to_list(head):
    res, curr = [], head
    while curr:
        res.append(curr.val)
        curr = curr.next
    return res

head = from_list([1, 2, 3, 4, 5, 6])
new_head = reverse_first_k(head, k=4)
print()
print("Final Result:", to_list(new_head))
`,
      remove_elements: `# 🗑️ LC 203: Remove Linked List Elements (3 Methods Compared)
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_list(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def to_list(head):
    res, cur = [], head
    while cur:
        res.append(cur.val)
        cur = cur.next
    return res

# Method 1: Sentinel Dummy Node (The Gold Standard)
def remove_elements_dummy(head, val):
    dummy = ListNode(0, head)
    cur = dummy
    while cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next  # Snip! Do NOT advance cur
        else:
            cur = cur.next            # Safe to advance cur
    return dummy.next

# Method 2: Without Dummy Node (Leading Head Trimming)
def remove_elements_no_dummy(head, val):
    # Step 1: Trim all matching nodes from the front
    while head and head.val == val:
        head = head.next
    
    # Step 2: Delete from the rest of the list
    cur = head
    while cur and cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head

# Method 3: Recursion (3-Line Functional Elegance)
def remove_elements_recursive(head, val):
    if not head:
        return None
    head.next = remove_elements_recursive(head.next, val)
    return head.next if head.val == val else head

# Testcase 1: All elements match (the user edge case: [7, 7, 7, 7], val = 7)
print("=== Testcase 1: [7, 7, 7, 7], target val = 7 ===")
t1_vals = [7, 7, 7, 7]
print("Input:          ", t1_vals)
print("Method 1 (Dummy):", to_list(remove_elements_dummy(build_list(t1_vals), 7)))
print("Method 2 (Trim): ", to_list(remove_elements_no_dummy(build_list(t1_vals), 7)))
print("Method 3 (Recur):", to_list(remove_elements_recursive(build_list(t1_vals), 7)))
print()

# Testcase 2: Multiple scattered matches [1, 2, 6, 3, 4, 5, 6], val = 6
print("=== Testcase 2: [1, 2, 6, 3, 4, 5, 6], target val = 6 ===")
t2_vals = [1, 2, 6, 3, 4, 5, 6]
print("Input:          ", t2_vals)
print("Method 1 (Dummy):", to_list(remove_elements_dummy(build_list(t2_vals), 6)))
print("Method 2 (Trim): ", to_list(remove_elements_no_dummy(build_list(t2_vals), 6)))
print("Method 3 (Recur):", to_list(remove_elements_recursive(build_list(t2_vals), 6)))
print()

# Testcase 3: Consecutive duplicates [1, 2, 2, 1], val = 2
print("=== Testcase 3: Consecutive matches [1, 2, 2, 1], target val = 2 ===")
t3_vals = [1, 2, 2, 1]
print("Input:          ", t3_vals)
print("Method 1 (Dummy):", to_list(remove_elements_dummy(build_list(t3_vals), 2)))
print("Method 2 (Trim): ", to_list(remove_elements_no_dummy(build_list(t3_vals), 2)))
print("Method 3 (Recur):", to_list(remove_elements_recursive(build_list(t3_vals), 2)))
`,
      blank: `# Python 3 Interactive Playground
# Sourced from your local DSA Hub

print("Hello from Python 3 Playground!")
`
    }};

    function builtinRead(x) {{
      if (typeof Sk === 'undefined' || Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined) {{
        throw "File not found: '" + x + "'";
      }}
      return Sk.builtinFiles["files"][x];
    }}

    function updateEditorLineCol() {{
      const pill = document.getElementById('editor-line-col-pill');
      if (!pill) return;
      if (window.playgroundEditor) {{
        const cursor = window.playgroundEditor.getCursor();
        pill.textContent = 'Ln ' + (cursor.line + 1) + ', Col ' + (cursor.ch + 1);
      }}
    }}

    let playgroundInitialized = false;
    function initPlayground() {{
      const input = document.getElementById('playground-code-input');
      const pill = document.getElementById('editor-line-col-pill');

      if (!playgroundInitialized) {{
        playgroundInitialized = true;
        let initialCode = input ? input.value : '';
        if (!initialCode.trim()) {{
          initialCode = PLAYGROUND_TEMPLATES['bubble_sort'];
        }}

        if (typeof CodeMirror !== 'undefined' && input) {{
          window.playgroundEditor = CodeMirror.fromTextArea(input, {{
            mode: {{ name: 'python', version: 3, singleLineStringErrors: false }},
            theme: 'leetcode',
            lineNumbers: true,
            indentUnit: 4,
            tabSize: 4,
            indentWithTabs: false,
            smartIndent: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            lineWrapping: false,
            extraKeys: {{
              "Tab": function(cm) {{
                if (cm.somethingSelected()) {{
                  cm.indentSelection("add");
                }} else {{
                  cm.replaceSelection("    ", "end");
                }}
              }},
              "Shift-Tab": function(cm) {{
                cm.indentSelection("subtract");
              }},
              "Cmd-Enter": function(cm) {{
                runPlaygroundCode();
              }},
              "Ctrl-Enter": function(cm) {{
                runPlaygroundCode();
              }}
            }}
          }});

          window.playgroundEditor.setValue(initialCode);

          window.playgroundEditor.on('cursorActivity', function(cm) {{
            if (pill) {{
              const cursor = cm.getCursor();
              pill.textContent = 'Ln ' + (cursor.line + 1) + ', Col ' + (cursor.ch + 1);
            }}
          }});

          setTimeout(() => {{
            if (window.playgroundEditor) window.playgroundEditor.refresh();
          }}, 50);
        }}
      }} else {{
        if (window.playgroundEditor) {{
          setTimeout(() => {{
            window.playgroundEditor.refresh();
          }}, 20);
        }}
      }}
    }}

    function onPlaygroundTemplateChange(val) {{
      const code = PLAYGROUND_TEMPLATES[val] || '';
      if (window.playgroundEditor) {{
        window.playgroundEditor.setValue(code);
        setTimeout(() => window.playgroundEditor.refresh(), 10);
      }} else {{
        const input = document.getElementById('playground-code-input');
        if (input) input.value = code;
      }}
      updateEditorLineCol();
      clearPlaygroundConsole();
    }}

    function resetPlaygroundCode() {{
      const sel = document.getElementById('playground-template-select');
      const val = (sel && sel.value) || 'bubble_sort';
      onPlaygroundTemplateChange(val);
    }}

    function clearPlaygroundConsole() {{
      const outEl = document.getElementById('playground-output');
      if (outEl) outEl.textContent = 'Console cleared. Click "▶ Run Code" or press ⌘+Enter to execute.';
      const statusEl = document.getElementById('playground-status-pill');
      if (statusEl) {{
        statusEl.textContent = 'Ready';
        statusEl.className = 'px-2.5 py-0.5 rounded-full text-xs font-medium border ui-surface ui-text-muted';
      }}
      const timerEl = document.getElementById('playground-time-pill');
      if (timerEl) timerEl.textContent = '';
    }}

    function copyPlaygroundOutput() {{
      const outEl = document.getElementById('playground-output');
      if (outEl && outEl.textContent) {{
        navigator.clipboard.writeText(outEl.textContent).then(() => {{
          showToast('Terminal output copied!');
        }}).catch(() => {{}});
      }}
    }}

    function loadCurrentDocIntoPlayground() {{
      const doc = DOCS_DATA[currentDocPath];
      if (!doc) return;
      
      const pyMatch = doc.content.match(/```python([\\s\\S]*?)```/);
      const code = pyMatch ? pyMatch[1].trim() : `# Could not find python block in ${{doc.title}}\\nprint("Write code here...")`;
      
      switchView('playground');
      const loadedCode = `# Loaded from: ${{doc.title}}\\n\\n` + code;
      if (window.playgroundEditor) {{
        window.playgroundEditor.setValue(loadedCode);
        setTimeout(() => window.playgroundEditor.refresh(), 20);
      }} else {{
        const input = document.getElementById('playground-code-input');
        if (input) input.value = loadedCode;
      }}
      const sel = document.getElementById('playground-template-select');
      if (sel) sel.value = 'blank';
      updateEditorLineCol();
      clearPlaygroundConsole();
    }}

    function runPlaygroundCode() {{
      const input = document.getElementById('playground-code-input');
      const outEl = document.getElementById('playground-output');
      const statusEl = document.getElementById('playground-status-pill');
      const timerEl = document.getElementById('playground-time-pill');
      const code = window.playgroundEditor ? window.playgroundEditor.getValue() : (input ? input.value : '');

      if (!code.trim()) {{
        outEl.textContent = 'Please enter some Python code to run.';
        return;
      }}

      if (typeof Sk === 'undefined') {{
        outEl.textContent = 'Skulpt Python runtime is still loading or not available.';
        return;
      }}

      outEl.textContent = '';
      statusEl.textContent = 'Running...';
      statusEl.className = 'px-2 py-0.5 rounded-full text-xs font-semibold border ui-accent-soft';
      timerEl.textContent = '';

      let output = '';
      Sk.pre = "output";
      Sk.configure({{
        output: function(text) {{
          output += text;
          outEl.textContent = output;
        }},
        read: builtinRead,
        __future__: Sk.python3
      }});

      const startTime = performance.now();
      const promise = Sk.misceval.asyncToPromise(function() {{
        return Sk.importMainWithBody("<stdin>", false, code, true);
      }});

      promise.then(function(mod) {{
        const elapsed = (performance.now() - startTime).toFixed(1);
        statusEl.textContent = '✓ Finished';
        statusEl.className = 'px-2 py-0.5 rounded-full text-xs font-semibold border bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        timerEl.textContent = `${{elapsed}}ms`;
        if (!output) {{
          outEl.textContent = '(Code executed successfully with no print output)';
        }}
      }}, function(err) {{
        const elapsed = (performance.now() - startTime).toFixed(1);
        statusEl.textContent = '✗ Error';
        statusEl.className = 'px-2 py-0.5 rounded-full text-xs font-semibold border bg-rose-500/10 text-rose-400 border-rose-500/30';
        timerEl.textContent = `${{elapsed}}ms`;
        outEl.textContent = (output ? output + '\\n' : '') + err.toString();
      }});
    }}

    // 4. Theme & Sidebar Scope
    function setTheme(theme) {{
      if (theme === 'daylight') theme = 'light';
      if (theme !== 'light' && theme !== 'dark') theme = 'dark';
      document.body.className = `theme-${{theme}} min-h-screen flex flex-col antialiased`;
      localStorage.setItem(THEME_KEY, theme);

      ['dark', 'light'].forEach(t => {{
        const btn = document.getElementById(`btn-theme-${{t}}`);
        if (!btn) return;
        if (t === theme) {{
          btn.className = 'px-2 py-1 rounded font-semibold transition-all ui-accent-soft border';
        }} else {{
          btn.className = 'px-2 py-1 rounded font-medium transition-all ui-text-muted hover:opacity-100';
        }}
      }});

      if (typeof mermaid !== 'undefined') {{
        mermaid.initialize({{
          startOnLoad: false,
          theme: theme === 'light' ? 'neutral' : 'dark',
          flowchart: {{ curve: 'basis', padding: 12 }},
          securityLevel: 'loose'
        }});
        if ((currentView === 'concepts' || currentView === 'problems') && currentDocPath) {{
          renderMermaidDiagrams(document.getElementById('rendered-content'));
        }}
      }}
    }}

    function setSidebarScope(scope) {{
      sidebarScope = scope;
      ['concept', 'problem', 'all'].forEach(s => {{
        const btn = document.getElementById(`sb-scope-${{s}}`);
        if (!btn) return;
        if (s === scope) {{
          btn.className = 'py-1 rounded font-semibold transition-colors ui-accent-btn shadow-sm';
        }} else {{
          btn.className = 'py-1 rounded font-medium transition-colors ui-text-muted hover:text-[var(--text)]';
        }}
      }});
      renderSidebarTree();
    }}

    // 5. Primary Navigation Switcher (7 Views)
    function switchView(view) {{
      currentView = view;
      ['concepts', 'problems', 'cheatsheets', 'playground', 'tracker', 'pomodoro', 'roadmap'].forEach(v => {{
        const btn = document.getElementById(`nav-btn-${{v}}`);
        if (!btn) return;
        if (v === view) {{
          btn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap ui-accent-btn shadow-sm';
        }} else {{
          btn.className = 'px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap ui-text-muted hover:text-[var(--text)]';
        }}
      }});

      const readerEl = document.getElementById('view-reader');
      const csEl = document.getElementById('view-cheatsheets');
      const playEl = document.getElementById('view-playground');
      const trkEl = document.getElementById('view-tracker');
      const pomoEl = document.getElementById('view-pomodoro');
      const rmEl = document.getElementById('view-roadmap');

      [readerEl, csEl, playEl, trkEl, pomoEl, rmEl].forEach(el => el && el.classList.add('hidden'));

      if (view === 'concepts') {{
        readerEl.classList.remove('hidden');
        setSidebarScope('concept');
        if (DOCS_DATA[currentDocPath]?.docType === 'problem') {{
          renderDoc("00_foundations/01_algorithms_correctness_efficiency.md");
        }}
      }} else if (view === 'problems') {{
        readerEl.classList.remove('hidden');
        setSidebarScope('problem');
        if (DOCS_DATA[currentDocPath]?.docType !== 'problem') {{
          renderDoc("01_arrays_and_pointers/3_longest_substring_without_repeating_characters.md");
        }}
      }} else if (view === 'cheatsheets') {{
        csEl.classList.remove('hidden');
        renderCheatSheetsGrid();
      }} else if (view === 'playground') {{
        playEl.classList.remove('hidden');
        initPlayground();
        if (window.playgroundEditor) {{
          setTimeout(() => window.playgroundEditor.refresh(), 20);
        }}
      }} else if (view === 'tracker') {{
        trkEl.classList.remove('hidden');
        renderTrackerTable();
      }} else if (view === 'pomodoro') {{
        pomoEl.classList.remove('hidden');
        const taskInput = document.getElementById('pomo-task-input');
        if (taskInput && !taskInput.value && DOCS_DATA[currentDocPath]) {{
          taskInput.value = DOCS_DATA[currentDocPath].title;
        }}
        renderPomodoroHistory();
      }} else if (view === 'roadmap') {{
        rmEl.classList.remove('hidden');
        renderRoadmapGrids();
      }}

      const url = new URL(window.location);
      url.searchParams.set('view', view);
      window.history.replaceState({{}}, '', url);
    }}

    function openDocInReader(docPath) {{
      const key = resolveDocKey(docPath);
      const doc = DOCS_DATA[key];
      const targetTab = doc?.docType === 'problem' ? 'problems' : 'concepts';
      currentDocPath = key;
      switchView(targetTab);
      if (doc?.docType === 'cheat_sheet') {{
        setSidebarScope('all');
      }}
      renderDoc(key);
    }}


    // 5.5 INTERACTIVE PLAYTHROUGH ENGINE
    const CONCEPT_PLAYTHROUGHS = {{
      '04_sorting/01_bubble_sort.md': {{ algorithm: 'bubble_sort', initial: [5, 1, 4, 2, 8] }},
      '04_sorting/02_selection_sort.md': {{ algorithm: 'selection_sort', initial: [64, 25, 12, 22, 11] }},
      '04_sorting/03_insertion_sort.md': {{ algorithm: 'insertion_sort', initial: [12, 11, 13, 5, 6] }},
      '04_sorting/04_merge_sort.md': {{ algorithm: 'merge_sort', initial: [38, 27, 43, 3, 9, 82, 10] }},
      '04_sorting/05_quick_sort.md': {{ algorithm: 'quick_sort', initial: [10, 80, 30, 90, 40, 50, 70] }},
      '04_sorting/06_quickselect.md': {{ algorithm: 'quick_sort', initial: [10, 80, 30, 90, 40, 50, 70] }},
      '04_sorting/07_counting_and_bucket_sort.md': {{ algorithm: 'selection_sort', initial: [4, 1, 3, 2, 3] }},
      '04_sorting/08_cyclic_sort.md': {{ algorithm: 'selection_sort', initial: [3, 4, -1, 1] }},
      '04_sorting/09_heap_sort.md': {{ algorithm: 'bubble_sort', initial: [12, 11, 13, 5, 6, 7] }},
      '05_binary_search/01_binary_search_fundamentals_and_occurrences.md': {{ algorithm: 'binary_search', initial: [2, 5, 8, 12, 16, 23, 38], target: 23 }},
      '05_binary_search/02_local_minima_and_peak_finding.md': {{ algorithm: 'peak_finding', initial: [1, 2, 1, 3, 5, 6, 4] }},
      '01_arrays_and_pointers/75_sort_colors.md': {{ algorithm: 'sort_colors', initial: [2, 0, 2, 1, 1, 0] }},
      '01_arrays_and_pointers/11_container_with_most_water.md': {{ algorithm: 'container_with_most_water', initial: [1, 8, 6, 2, 5, 4, 8, 3, 7] }},
      '01_arrays_and_pointers/53_maximum_subarray.md': {{ algorithm: 'kadanes', initial: [-2, 1, -3, 4, -1, 2, 1, -5, 4] }},
      '02_linked_lists/206_reverse_linked_list.md': {{ algorithm: 'reverse_linked_list', initial: [1, 2, 3, 4, 5] }},
      '02_linked_lists/02_reverse_first_k_nodes.md': {{ algorithm: 'reverse_first_k', initial: [1, 2, 3, 4, 5, 6], k: 4 }},
      '02_linked_lists/203_remove_linked_list_elements.md': {{ algorithm: 'remove_elements', initial: [1, 2, 6, 3, 4, 5, 6], target: 6 }}
    }};

    const PLAYTHROUGH_PRESETS = {{
      remove_elements: [
        {{ label: 'Default Example [1, 2, 6, 3, 4, 5, 6] (val=6)', val: [1, 2, 6, 3, 4, 5, 6], target: 6 }},
        {{ label: 'All Elements Match [7, 7, 7, 7] (val=7)', val: [7, 7, 7, 7], target: 7 }},
        {{ label: 'Consecutive Duplicates [1, 2, 2, 1] (val=2)', val: [1, 2, 2, 1], target: 2 }},
        {{ label: 'Target at Head [6, 1, 2, 3] (val=6)', val: [6, 1, 2, 3], target: 6 }},
        {{ label: 'Target at Tail [1, 2, 3, 6] (val=6)', val: [1, 2, 3, 6], target: 6 }}
      ],
      reverse_first_k: [
        {{ label: 'Notebook Example [1..6] (k=4)', val: [1, 2, 3, 4, 5, 6], k: 4 }},
        {{ label: 'Full Reversal [1, 2, 3, 4] (k=4)', val: [1, 2, 3, 4], k: 4 }},
        {{ label: 'First 2 of 5 [10, 20, 30, 40, 50] (k=2)', val: [10, 20, 30, 40, 50], k: 2 }}
      ],
      bubble_sort: [
        {{ label: 'Default [5, 1, 4, 2, 8]', val: [5, 1, 4, 2, 8] }},
        {{ label: 'Reversed [5, 4, 3, 2, 1]', val: [5, 4, 3, 2, 1] }},
        {{ label: 'Nearly Sorted [1, 2, 4, 3, 5]', val: [1, 2, 4, 3, 5] }},
        {{ label: 'Already Sorted [1, 2, 3, 4, 5]', val: [1, 2, 3, 4, 5] }}
      ],
      selection_sort: [
        {{ label: 'Default [64, 25, 12, 22, 11]', val: [64, 25, 12, 22, 11] }},
        {{ label: 'Reversed [5, 4, 3, 2, 1]', val: [5, 4, 3, 2, 1] }},
        {{ label: 'Small [3, 1, 2]', val: [3, 1, 2] }}
      ],
      insertion_sort: [
        {{ label: 'Default [12, 11, 13, 5, 6]', val: [12, 11, 13, 5, 6] }},
        {{ label: 'Reversed [5, 4, 3, 2, 1]', val: [5, 4, 3, 2, 1] }},
        {{ label: 'Already Sorted [1, 2, 3, 4, 5]', val: [1, 2, 3, 4, 5] }}
      ],
      binary_search: [
        {{ label: 'Target 23 (In list)', val: [2, 5, 8, 12, 16, 23, 38], target: 23 }},
        {{ label: 'Target 5 (Left side)', val: [2, 5, 8, 12, 16, 23, 38], target: 5 }},
        {{ label: 'Target 10 (Not found)', val: [2, 5, 8, 12, 16, 23, 38], target: 10 }}
      ],
      peak_finding: [
        {{ label: 'Default [1, 2, 1, 3, 5, 6, 4]', val: [1, 2, 1, 3, 5, 6, 4] }},
        {{ label: 'Single Peak [1, 3, 7, 4, 2]', val: [1, 3, 7, 4, 2] }}
      ],
      sort_colors: [
        {{ label: 'Default [2, 0, 2, 1, 1, 0]', val: [2, 0, 2, 1, 1, 0] }},
        {{ label: 'Alternating [1, 2, 0, 1, 2, 0]', val: [1, 2, 0, 1, 2, 0] }},
        {{ label: 'Reversed [2, 2, 1, 1, 0, 0]', val: [2, 2, 1, 1, 0, 0] }}
      ],
      container_with_most_water: [
        {{ label: 'Default [1, 8, 6, 2, 5, 4, 8, 3, 7]', val: [1, 8, 6, 2, 5, 4, 8, 3, 7] }},
        {{ label: 'Pyramid [1, 4, 8, 8, 4, 1]', val: [1, 4, 8, 8, 4, 1] }},
        {{ label: 'Descending [8, 6, 4, 2]', val: [8, 6, 4, 2] }}
      ],
      kadanes: [
        {{ label: 'Default [-2, 1, -3, 4, -1, 2, 1, -5, 4]', val: [-2, 1, -3, 4, -1, 2, 1, -5, 4] }},
        {{ label: 'All Negative [-5, -2, -8, -1]', val: [-5, -2, -8, -1] }},
        {{ label: 'All Positive [1, 2, 3, 4]', val: [1, 2, 3, 4] }}
      ],
      reverse_linked_list: [
        {{ label: 'Default [1, 2, 3, 4, 5]', val: [1, 2, 3, 4, 5] }},
        {{ label: 'Short [1, 2, 3]', val: [1, 2, 3] }}
      ]
    }};

    function generateBubbleSortSteps(initialArr) {{
      const arr = [...initialArr];
      const n = arr.length;
      const steps = [];

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{}},
        sorted: [],
        tag: 'Start',
        badge: 'Initial State',
        badgeColor: 'blue',
        desc: `Starting Bubble Sort with array [${{arr.join(', ')}}]. We make passes comparing adjacent pairs and bubbling the largest unsorted value right.`,
        vars: {{ n, pass: 0 }}
      }});

      for (let i = 0; i < n - 1; i++) {{
        let swapped = false;
        const locked = [];
        for (let k = n - i; k < n; k++) locked.push(k);

        for (let j = 0; j < n - 1 - i; j++) {{
          steps.push({{
            type: 'array',
            array: [...arr],
            active: [j, j + 1],
            pointers: {{ j, 'j+1': j + 1 }},
            sorted: [...locked],
            tag: `Pass ${{i + 1}} (i = ${{i}})`,
            badge: 'Compare',
            badgeColor: 'amber',
            desc: `Compare arr[${{j}}] (${{arr[j]}}) and arr[${{j + 1}}] (${{arr[j + 1]}}). ${{arr[j] > arr[j + 1] ? `Since ${{arr[j]}} > ${{arr[j + 1]}}, they are out of order!` : `Since ${{arr[j]}} ≤ ${{arr[j + 1]}}, they are in relative order.`}}`,
            vars: {{ i, j, 'arr[j]': arr[j], 'arr[j+1]': arr[j + 1], swapped }}
          }});

          if (arr[j] > arr[j + 1]) {{
            const tmp = arr[j];
            arr[j] = arr[j + 1];
            arr[j + 1] = tmp;
            swapped = true;

            steps.push({{
              type: 'array',
              array: [...arr],
              active: [j, j + 1],
              swapped: [j, j + 1],
              pointers: {{ j, 'j+1': j + 1 }},
              sorted: [...locked],
              tag: `Pass ${{i + 1}} (i = ${{i}})`,
              badge: 'Swap',
              badgeColor: 'rose',
              desc: `Swapped ${{arr[j + 1]}} and ${{arr[j]}}. Array is now [${{arr.join(', ')}}]. Marked swapped = True.`,
              vars: {{ i, j, 'arr[j]': arr[j], 'arr[j+1]': arr[j + 1], swapped: true }}
            }});
          }}
        }}

        locked.unshift(n - 1 - i);
        steps.push({{
          type: 'array',
          array: [...arr],
          active: [n - 1 - i],
          pointers: {{}},
          sorted: [...locked],
          tag: `Pass ${{i + 1}} Done`,
          badge: 'Locked',
          badgeColor: 'emerald',
          desc: `Pass ${{i + 1}} complete. Value ${{arr[n - 1 - i]}} is now permanently settled at index ${{n - 1 - i}}.`,
          vars: {{ i, sortedCount: locked.length, swapped }}
        }});

        if (!swapped) {{
          steps.push({{
            type: 'array',
            array: [...arr],
            active: [],
            pointers: {{}},
            sorted: arr.map((_, idx) => idx),
            tag: 'Early Exit',
            badge: 'Sorted!',
            badgeColor: 'emerald',
            desc: `Zero swaps occurred in Pass ${{i + 1}} (swapped == False). The array is fully sorted! Breaking early in O(n) time.`,
            vars: {{ status: 'Terminated early', passes: i + 1 }}
          }});
          return steps;
        }}
      }}

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{}},
        sorted: arr.map((_, idx) => idx),
        tag: 'Finished',
        badge: 'Sorted',
        badgeColor: 'emerald',
        desc: `Array is fully sorted: [${{arr.join(', ')}}].`,
        vars: {{ status: 'Complete' }}
      }});
      return steps;
    }}

    function generateSelectionSortSteps(initialArr) {{
      const arr = [...initialArr];
      const n = arr.length;
      const steps = [];

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{}},
        sorted: [],
        tag: 'Start',
        badge: 'Initial State',
        badgeColor: 'blue',
        desc: `Starting Selection Sort with array [${{arr.join(', ')}}]. We scan the unsorted suffix to find the minimum, then swap it into the sorted prefix.`,
        vars: {{ n }}
      }});

      for (let i = 0; i < n - 1; i++) {{
        let minIdx = i;
        const sorted = [];
        for (let k = 0; k < i; k++) sorted.push(k);

        steps.push({{
          type: 'array',
          array: [...arr],
          active: [i],
          pointers: {{ i, min_idx: minIdx }},
          sorted: [...sorted],
          tag: `Pass ${{i + 1}} (i = ${{i}})`,
          badge: 'Init Min',
          badgeColor: 'amber',
          desc: `Starting pass ${{i + 1}}. Assume minimum is at current index i = ${{i}} (value ${{arr[i]}}).`,
          vars: {{ i, min_idx: minIdx, min_val: arr[minIdx] }}
        }});

        for (let j = i + 1; j < n; j++) {{
          const isSmaller = arr[j] < arr[minIdx];
          steps.push({{
            type: 'array',
            array: [...arr],
            active: [j, minIdx],
            pointers: {{ i, j, min_idx: minIdx }},
            sorted: [...sorted],
            tag: `Scanning suffix`,
            badge: 'Compare',
            badgeColor: 'amber',
            desc: `Compare arr[j=${{j}}] (${{arr[j]}}) with current min arr[min_idx=${{minIdx}}] (${{arr[minIdx]}}). ${{isSmaller ? `Found smaller element! Update min_idx to ${{j}}.` : `arr[j] >= current min. Keep min_idx = ${{minIdx}}.`}}`,
            vars: {{ i, j, min_idx: isSmaller ? j : minIdx }}
          }});
          if (isSmaller) {{
            minIdx = j;
          }}
        }}

        if (minIdx !== i) {{
          const tmp = arr[i];
          arr[i] = arr[minIdx];
          arr[minIdx] = tmp;

          steps.push({{
            type: 'array',
            array: [...arr],
            active: [i, minIdx],
            swapped: [i, minIdx],
            pointers: {{ i, min_idx: minIdx }},
            sorted: [...sorted],
            tag: `Swap Minimum`,
            badge: 'Swap',
            badgeColor: 'rose',
            desc: `Swap minimum value ${{arr[i]}} at index ${{minIdx}} into slot i = ${{i}}. Array is now [${{arr.join(', ')}}].`,
            vars: {{ i, min_idx: minIdx, swapped: true }}
          }});
        }}

        sorted.push(i);
        steps.push({{
          type: 'array',
          array: [...arr],
          active: [i],
          pointers: {{}},
          sorted: [...sorted],
          tag: `Prefix Grown`,
          badge: 'Locked',
          badgeColor: 'emerald',
          desc: `Element at index ${{i}} (${{arr[i]}}) is now locked in its final sorted position.`,
          vars: {{ sortedCount: sorted.length }}
        }});
      }}

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{}},
        sorted: arr.map((_, idx) => idx),
        tag: 'Finished',
        badge: 'Sorted',
        badgeColor: 'emerald',
        desc: `Selection Sort complete! Array is sorted: [${{arr.join(', ')}}].`,
        vars: {{ status: 'Complete' }}
      }});
      return steps;
    }}

    function generateInsertionSortSteps(initialArr) {{
      const arr = [...initialArr];
      const n = arr.length;
      const steps = [];

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [0],
        pointers: {{ sorted: 0 }},
        sorted: [0],
        tag: 'Start',
        badge: 'Initial State',
        badgeColor: 'blue',
        desc: `Starting Insertion Sort with [${{arr.join(', ')}}]. Index 0 ([${{arr[0]}}]) forms the initial sorted hand of cards.`,
        vars: {{ n }}
      }});

      for (let i = 1; i < n; i++) {{
        const key = arr[i];
        let j = i - 1;
        const sorted = [];
        for (let k = 0; k < i; k++) sorted.push(k);

        steps.push({{
          type: 'array',
          array: [...arr],
          active: [i],
          pointers: {{ i, key: i }},
          sorted: [...sorted],
          tag: `Pick Key (i = ${{i}})`,
          badge: 'Pick Key',
          badgeColor: 'amber',
          desc: `Pick key = arr[${{i}}] (${{key}}). Scan sorted prefix left and shift larger elements right.`,
          vars: {{ i, key, j }}
        }});

        while (j >= 0 && arr[j] > key) {{
          steps.push({{
            type: 'array',
            array: [...arr],
            active: [j, j + 1],
            pointers: {{ j, 'j+1': j + 1, key: i }},
            sorted: [...sorted],
            tag: `Compare with key`,
            badge: 'Shift Right',
            badgeColor: 'rose',
            desc: `arr[${{j}}] (${{arr[j]}}) > key (${{key}}). Shift arr[${{j}}] right into index ${{j + 1}}.`,
            vars: {{ j, 'arr[j]': arr[j], key }}
          }});

          arr[j + 1] = arr[j];
          j -= 1;
        }}

        arr[j + 1] = key;
        sorted.push(i);

        steps.push({{
          type: 'array',
          array: [...arr],
          active: [j + 1],
          pointers: {{ inserted: j + 1 }},
          sorted: [...sorted],
          tag: `Insert Key`,
          badge: 'Inserted',
          badgeColor: 'emerald',
          desc: `Dropped key ${{key}} into sorted slot index ${{j + 1}}. Array is now [${{arr.join(', ')}}].`,
          vars: {{ insertedAt: j + 1, key }}
        }});
      }}

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{}},
        sorted: arr.map((_, idx) => idx),
        tag: 'Finished',
        badge: 'Sorted',
        badgeColor: 'emerald',
        desc: `Insertion Sort complete! Array is sorted: [${{arr.join(', ')}}].`,
        vars: {{ status: 'Complete' }}
      }});
      return steps;
    }}

    function generateBinarySearchSteps(initialArr, targetVal) {{
      const arr = [...initialArr];
      const target = targetVal !== undefined ? targetVal : 23;
      const n = arr.length;
      const steps = [];

      let lo = 0;
      let hi = n - 1;

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{ lo: 0, hi: n - 1 }},
        dimmed: [],
        tag: 'Start Search',
        badge: 'Initial State',
        badgeColor: 'blue',
        desc: `Searching for target = ${{target}} in sorted array [${{arr.join(', ')}}]. Active search interval is [lo=0, hi=${{n - 1}}].`,
        vars: {{ target, lo: 0, hi: n - 1 }}
      }});

      while (lo <= hi) {{
        const mid = Math.floor(lo + (hi - lo) / 2);
        const dimmed = [];
        for (let k = 0; k < lo; k++) dimmed.push(k);
        for (let k = hi + 1; k < n; k++) dimmed.push(k);

        steps.push({{
          type: 'array',
          array: [...arr],
          active: [mid],
          pointers: {{ lo, mid, hi }},
          dimmed: [...dimmed],
          tag: `Check Midpoint`,
          badge: 'Midpoint',
          badgeColor: 'amber',
          desc: `Compute mid = lo + (hi - lo) // 2 = ${{lo}} + (${{hi}} - ${{lo}}) // 2 = ${{mid}}. Comparing arr[mid] (${{arr[mid]}}) with target (${{target}}).`,
          vars: {{ lo, mid, hi, 'arr[mid]': arr[mid], target }}
        }});

        if (arr[mid] === target) {{
          steps.push({{
            type: 'array',
            array: [...arr],
            active: [mid],
            pointers: {{ MATCH: mid }},
            sorted: [mid],
            dimmed: [...dimmed],
            tag: `Target Found`,
            badge: 'Match!',
            badgeColor: 'emerald',
            desc: `arr[mid=${{mid}}] == ${{target}}! Target found at index ${{mid}} in O(log n) time.`,
            vars: {{ resultIndex: mid, target }}
          }});
          return steps;
        }} else if (arr[mid] < target) {{
          const nextLo = mid + 1;
          steps.push({{
            type: 'array',
            array: [...arr],
            active: [mid],
            pointers: {{ lo, mid, hi }},
            dimmed: [...dimmed],
            tag: `Steer Right`,
            badge: 'arr[mid] < target',
            badgeColor: 'rose',
            desc: `arr[mid] (${{arr[mid]}}) < target (${{target}}). Since array is sorted, target cannot exist in [lo...mid]. Discard left half: lo = mid + 1 = ${{nextLo}}.`,
            vars: {{ lo: nextLo, hi, action: 'lo = mid + 1' }}
          }});
          lo = nextLo;
        }} else {{
          const nextHi = mid - 1;
          steps.push({{
            type: 'array',
            array: [...arr],
            active: [mid],
            pointers: {{ lo, mid, hi }},
            dimmed: [...dimmed],
            tag: `Steer Left`,
            badge: 'arr[mid] > target',
            badgeColor: 'rose',
            desc: `arr[mid] (${{arr[mid]}}) > target (${{target}}). Target cannot exist in [mid...hi]. Discard right half: hi = mid - 1 = ${{nextHi}}.`,
            vars: {{ lo, hi: nextHi, action: 'hi = mid - 1' }}
          }});
          hi = nextHi;
        }}
      }}

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{}},
        dimmed: arr.map((_, i) => i),
        tag: 'Not Found',
        badge: 'Return -1',
        badgeColor: 'rose',
        desc: `lo > hi (interval exhausted). Target ${{target}} does not exist in the array. Return -1.`,
        vars: {{ lo, hi, result: -1 }}
      }});
      return steps;
    }}

    function generatePeakFindingSteps(initialArr) {{
      const arr = [...initialArr];
      const n = arr.length;
      const steps = [];

      let lo = 0;
      let hi = n - 1;

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{ lo: 0, hi: n - 1 }},
        tag: 'Start Peak Search',
        badge: 'Initial State',
        badgeColor: 'blue',
        desc: `Searching for any peak element where arr[i] > arr[i-1] and arr[i] > arr[i+1]. We climb the slope via binary search!`,
        vars: {{ lo: 0, hi: n - 1 }}
      }});

      while (lo < hi) {{
        const mid = Math.floor(lo + (hi - lo) / 2);
        const isUpward = arr[mid] < arr[mid + 1];

        steps.push({{
          type: 'array',
          array: [...arr],
          active: [mid, mid + 1],
          pointers: {{ lo, mid, 'mid+1': mid + 1, hi }},
          tag: `Inspect Slope at mid = ${{mid}}`,
          badge: isUpward ? 'Upward Slope' : 'Downward Slope',
          badgeColor: isUpward ? 'emerald' : 'rose',
          desc: `arr[mid=${{mid}}] = ${{arr[mid]}} vs arr[mid+1=${{mid+1}}] = ${{arr[mid+1]}}. ${{isUpward ? `Since arr[mid] < arr[mid+1], slope is rising to the right! A peak is guaranteed in [mid+1...hi]. Steer lo = mid + 1 = ${{mid + 1}}.` : `Since arr[mid] > arr[mid+1], slope is falling. A peak exists at or left of mid. Steer hi = mid = ${{mid}}.`}}`,
          vars: {{ lo, mid, hi, 'arr[mid]': arr[mid], 'arr[mid+1]': arr[mid+1] }}
        }});

        if (isUpward) {{
          lo = mid + 1;
        }} else {{
          hi = mid;
        }}
      }}

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [lo],
        pointers: {{ PEAK: lo }},
        sorted: [lo],
        tag: 'Peak Found',
        badge: `Peak = ${{arr[lo]}}`,
        badgeColor: 'emerald',
        desc: `lo == hi (${{lo}})! Peak element found at index ${{lo}} with value ${{arr[lo]}} in O(log n) time.`,
        vars: {{ peakIndex: lo, peakValue: arr[lo] }}
      }});
      return steps;
    }}

    function generateSortColorsSteps(initialArr) {{
      const arr = [...initialArr];
      const n = arr.length;
      const steps = [];

      let low = 0;
      let mid = 0;
      let high = n - 1;

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{ low: 0, mid: 0, high: n - 1 }},
        tag: 'Start Dutch Flag',
        badge: 'Initial State',
        badgeColor: 'blue',
        desc: `Sorting 0s (Red), 1s (White), and 2s (Blue) in a single O(n) pass. Invariant: [0...low-1] is 0, [low...mid-1] is 1, [high+1...n-1] is 2.`,
        vars: {{ low, mid, high }}
      }});

      while (mid <= high) {{
        const val = arr[mid];
        steps.push({{
          type: 'array',
          array: [...arr],
          active: [mid],
          pointers: {{ low, mid, high }},
          tag: `Inspect mid = ${{mid}}`,
          badge: `Val = ${{val}}`,
          badgeColor: val === 0 ? 'rose' : (val === 1 ? 'blue' : 'amber'),
          desc: `Inspecting nums[mid=${{mid}}] = ${{val}}. ${{val === 0 ? 'Value is 0: swap with low, advance both low and mid.' : (val === 1 ? 'Value is 1: already in middle region, advance mid.' : 'Value is 2: swap with high, decrement high. Do NOT advance mid!')}}`,
          vars: {{ low, mid, high, 'nums[mid]': val }}
        }});

        if (val === 0) {{
          const tmp = arr[low];
          arr[low] = arr[mid];
          arr[mid] = tmp;
          low += 1;
          mid += 1;
        }} else if (val === 1) {{
          mid += 1;
        }} else {{
          const tmp = arr[high];
          arr[high] = arr[mid];
          arr[mid] = tmp;
          high -= 1;
        }}
      }}

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [],
        pointers: {{}},
        sorted: arr.map((_, i) => i),
        tag: 'Partition Finished',
        badge: 'Sorted!',
        badgeColor: 'emerald',
        desc: `mid > high! Single-pass Dutch National Flag partition complete: [${{arr.join(', ')}}].`,
        vars: {{ status: 'Sorted' }}
      }});
      return steps;
    }}

    function generateContainerWaterSteps(initialArr) {{
      const arr = [...initialArr];
      const n = arr.length;
      const steps = [];

      let l = 0;
      let r = n - 1;
      let maxWater = 0;
      let bestL = 0;
      let bestR = n - 1;

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [l, r],
        pointers: {{ left: l, right: r }},
        tag: 'Start Two Pointers',
        badge: 'Max Width',
        badgeColor: 'blue',
        desc: `Initialize left = 0, right = ${{r}}. Start with maximum possible container width = ${{r - l}}.`,
        vars: {{ left: l, right: r, max_water: 0 }}
      }});

      while (l < r) {{
        const width = r - l;
        const hL = arr[l];
        const hR = arr[r];
        const minH = Math.min(hL, hR);
        const area = width * minH;
        const isNewMax = area > maxWater;
        if (isNewMax) {{
          maxWater = area;
          bestL = l;
          bestR = r;
        }}

        steps.push({{
          type: 'array',
          array: [...arr],
          active: [l, r],
          pointers: {{ left: l, right: r }},
          tag: `Evaluate Container`,
          badge: `Area = ${{area}}`,
          badgeColor: isNewMax ? 'emerald' : 'amber',
          desc: `left=${{l}} (h=${{hL}}), right=${{r}} (h=${{hR}}). Width = ${{width}}, limiting height = min(${{hL}}, ${{hR}}) = ${{minH}}. Area = ${{width}} × ${{minH}} = ${{area}}. ${{isNewMax ? `New maximum water = ${{maxWater}}!` : `Does not beat current best (${{maxWater}}).`}}`,
          vars: {{ left: l, right: r, width, min_height: minH, current_area: area, max_water: maxWater }}
        }});

        if (hL < hR) {{
          steps.push({{
            type: 'array',
            array: [...arr],
            active: [l],
            pointers: {{ left: l, right: r }},
            tag: `Shrink Left Wall`,
            badge: `h[left] < h[right]`,
            badgeColor: 'rose',
            desc: `Left wall (${{hL}}) is shorter than right wall (${{hR}}). Moving right cannot help since width shrinks and height is bottlenecked by the left wall. Advance left += 1 to look for a taller wall.`,
            vars: {{ left: l + 1, right: r, max_water: maxWater }}
          }});
          l += 1;
        }} else {{
          steps.push({{
            type: 'array',
            array: [...arr],
            active: [r],
            pointers: {{ left: l, right: r }},
            tag: `Shrink Right Wall`,
            badge: `h[right] <= h[left]`,
            badgeColor: 'rose',
            desc: `Right wall (${{hR}}) is the bottleneck (or equal). Decrement right -= 1.`,
            vars: {{ left: l, right: r - 1, max_water: maxWater }}
          }});
          r -= 1;
        }}
      }}

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [bestL, bestR],
        pointers: {{ best_left: bestL, best_right: bestR }},
        tag: 'Optimal Found',
        badge: `Max = ${{maxWater}}`,
        badgeColor: 'emerald',
        desc: `Pointers met! Maximum water capacity is ${{maxWater}} between index ${{bestL}} (height ${{arr[bestL]}}) and index ${{bestR}} (height ${{arr[bestR]}}).`,
        vars: {{ max_water: maxWater, best_left: bestL, best_right: bestR }}
      }});
      return steps;
    }}

    function generateKadanesSteps(initialArr) {{
      const arr = [...initialArr];
      const n = arr.length;
      const steps = [];

      let curSum = arr[0];
      let maxSum = arr[0];
      let start = 0;
      let bestStart = 0;
      let bestEnd = 0;

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [0],
        pointers: {{ i: 0 }},
        tag: 'Start Kadane',
        badge: `Init Sum = ${{arr[0]}}`,
        badgeColor: 'blue',
        desc: `Initialize running sum cur_sum = ${{arr[0]}} and max_sum = ${{arr[0]}}. At each element, decide: extend existing subarray or start fresh?`,
        vars: {{ cur_sum: curSum, max_sum: maxSum }}
      }});

      for (let i = 1; i < n; i++) {{
        const x = arr[i];
        const extendSum = curSum + x;
        const reset = x > extendSum;
        if (reset) {{
          curSum = x;
          start = i;
        }} else {{
          curSum = extendSum;
        }}

        const isNewMax = curSum > maxSum;
        if (isNewMax) {{
          maxSum = curSum;
          bestStart = start;
          bestEnd = i;
        }}

        const activeSubarray = [];
        for (let k = start; k <= i; k++) activeSubarray.push(k);

        steps.push({{
          type: 'array',
          array: [...arr],
          active: [...activeSubarray],
          pointers: {{ i }},
          tag: `Element ${{x}} (idx ${{i}})`,
          badge: reset ? 'Start Fresh' : 'Extend Subarray',
          badgeColor: isNewMax ? 'emerald' : 'amber',
          desc: `Evaluating arr[${{i}}] = ${{x}}. Extend sum (${{extendSum}}) vs start fresh (${{x}}) -> cur_sum = max(${{x}}, ${{extendSum}}) = ${{curSum}}. ${{reset ? `Previous sum was negative; starting fresh at index ${{i}}.` : `Extended previous subarray.`}} ${{isNewMax ? `New max_sum = ${{maxSum}}!` : `Global max_sum remains ${{maxSum}}.`}}`,
          vars: {{ i, 'arr[i]': x, cur_sum: curSum, max_sum: maxSum, start, end: i }}
        }});
      }}

      const finalSub = [];
      for (let k = bestStart; k <= bestEnd; k++) finalSub.push(k);

      steps.push({{
        type: 'array',
        array: [...arr],
        active: [...finalSub],
        pointers: {{ best_start: bestStart, best_end: bestEnd }},
        tag: 'Search Complete',
        badge: `Max Sum = ${{maxSum}}`,
        badgeColor: 'emerald',
        desc: `Kadane's algorithm complete! Maximum contiguous subarray sum is ${{maxSum}} (from index ${{bestStart}} to ${{bestEnd}}).`,
        vars: {{ max_sum: maxSum, start: bestStart, end: bestEnd }}
      }});
      return steps;
    }}

    function highlightPythonCode(lineStr) {{
      if (!lineStr) return ' ';
      let s = lineStr
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

      if (s.includes('#')) {{
        const parts = s.split('#');
        const codePart = parts[0];
        const commentPart = '#' + parts.slice(1).join('#');
        return highlightPythonCode(codePart) + '<span class="text-slate-500 italic">' + commentPart + '</span>';
      }}

      s = s.replace(/\b(class|def|return|if|else|elif|while|for|in|None|True|False|not|and|or|self|break|continue)\b/g, '<span class="text-pink-400 font-semibold">$1</span>');
      s = s.replace(/\b(Optional|ListNode|int|str|float|bool|Solution|List)\b/g, '<span class="text-cyan-300 font-semibold">$1</span>');
      s = s.replace(/\b(\\d+)\b/g, '<span class="text-emerald-400 font-semibold">$1</span>');
      s = s.replace(/\b(removeElements|reverseList|reverseFirstK|bubble_sort|selection_sort|insertion_sort|binary_search|peak_finding|sortColors|maxArea|maxSubArray|len|min|max|range)\b/g, '<span class="text-blue-300 font-semibold">$1</span>');
      s = s.replace(/\b(dummy|head|cur|prev|next_node|curr|node|val|nxt|low|mid|high|left|right)\b/g, '<span class="text-amber-200/90">$1</span>');
      return s;
    }}

    // REVERSE LINKED LIST: Iterative
    function generateReverseLinkedListIterativeSteps(initialArr) {{
      const vals = [...initialArr];
      const steps = [];

      // Step 0: Init
      steps.push({{
        type: 'linked_list',
        line: 4,
        tag: 'Step 0: Initialize Pointers',
        badge: 'prev=None, curr=head',
        badgeColor: 'blue',
        desc: `Initialize prev = None, curr = head (Node ${{vals[0]}}).`,
        nodes: vals.map((v, idx) => ({{
          val: v,
          topPtrs: idx === 0 ? ['head'] : [],
          bottomPtrs: idx === 0 ? ['curr'] : [],
          arrow: 'right'
        }}))
      }});

      let prevIdx = null;
      let currIdx = 0;
      let arrows = vals.map(() => 'right');

      while (currIdx < vals.length) {{
        const nextIdx = (currIdx + 1 < vals.length) ? currIdx + 1 : null;
        const nextVal = (nextIdx !== null) ? vals[nextIdx] : 'None';

        // Step A: Save next_node = curr.next
        steps.push({{
          type: 'linked_list',
          line: 6,
          tag: `Loop Node(${{vals[currIdx]}}): Save next_node`,
          badge: 'next_node = curr.next',
          badgeColor: 'amber',
          desc: `Save next pointer: next_node = curr.next (Node ${{nextVal}}). Bookmarks downstream list so it is not lost when pointer is reversed.`,
          nodes: vals.map((v, idx) => {{
            const top = [];
            const bot = [];
            if (idx === 0) top.push('head');
            if (idx === nextIdx) top.push('next');
            if (idx === prevIdx) bot.push('prev');
            if (idx === currIdx) bot.push('curr');
            return {{ val: v, topPtrs: top, bottomPtrs: bot, arrow: arrows[idx], isActive: idx === currIdx }};
          }})
        }});

        // Step B: Reverse curr.next = prev
        arrows[currIdx] = (prevIdx !== null) ? 'left' : 'null';
        steps.push({{
          type: 'linked_list',
          line: 7,
          tag: `Loop Node(${{vals[currIdx]}}): Reverse Pointer`,
          badge: 'curr.next = prev',
          badgeColor: 'rose',
          desc: `Reverse pointer: curr.next = prev (${{prevIdx !== null ? `Node ${{vals[prevIdx]}}` : 'None'}}). Arrow of Node(${{vals[currIdx]}}) now points backward!`,
          nodes: vals.map((v, idx) => {{
            const top = [];
            const bot = [];
            if (idx === 0) top.push('head');
            if (idx === nextIdx) top.push('next');
            if (idx === prevIdx) bot.push('prev');
            if (idx === currIdx) bot.push('curr');
            return {{ val: v, topPtrs: top, bottomPtrs: bot, arrow: arrows[idx], isActive: idx === currIdx }};
          }})
        }});

        // Step C: prev = curr
        prevIdx = currIdx;
        steps.push({{
          type: 'linked_list',
          line: 8,
          tag: `Loop Node(${{vals[prevIdx]}}): Advance prev`,
          badge: 'prev = curr',
          badgeColor: 'emerald',
          desc: `Move prev forward: prev = curr (Node ${{vals[prevIdx]}}). prev now stands on the front of the reversed chain.`,
          nodes: vals.map((v, idx) => {{
            const top = [];
            const bot = [];
            if (idx === 0) top.push('head');
            if (idx === nextIdx) top.push('next');
            if (idx === prevIdx) bot.push('prev');
            return {{ val: v, topPtrs: top, bottomPtrs: bot, arrow: arrows[idx] }};
          }})
        }});

        // Step D: curr = next_node
        currIdx = (nextIdx !== null) ? nextIdx : vals.length;
        steps.push({{
          type: 'linked_list',
          line: 9,
          tag: `Loop: Advance curr`,
          badge: 'curr = next_node',
          badgeColor: 'blue',
          desc: `Move curr forward: curr = next_node (${{currIdx < vals.length ? `Node ${{vals[currIdx]}}` : 'None'}}). Ready for next loop iteration.`,
          nodes: vals.map((v, idx) => {{
            const top = [];
            const bot = [];
            if (idx === 0) top.push('head');
            if (idx === prevIdx) bot.push('prev');
            if (idx === currIdx) bot.push('curr');
            return {{ val: v, topPtrs: top, bottomPtrs: bot, arrow: arrows[idx] }};
          }})
        }});
      }}

      // Final step: return prev
      steps.push({{
        type: 'linked_list',
        line: 10,
        tag: 'Complete: Return prev',
        badge: 'Finished',
        badgeColor: 'emerald',
        desc: `curr is None! while loop terminates. return prev (Node ${{vals[prevIdx]}}), which is now the head of the fully reversed list!`,
        nodes: vals.map((v, idx) => {{
          const top = [];
          if (idx === prevIdx) top.push('RETURN HEAD');
          return {{ val: v, topPtrs: top, bottomPtrs: [], arrow: arrows[idx] }};
        }})
      }});

      return steps;
    }}

    // REVERSE LINKED LIST: Recursive
    function generateReverseLinkedListRecursiveSteps(initialArr) {{
      const vals = [...initialArr];
      const steps = [];

      steps.push({{
        type: 'linked_list',
        line: 3,
        tag: '1. Base Case Check',
        badge: 'Call Stack Start',
        badgeColor: 'blue',
        desc: `Call reverseList(head = Node ${{vals[0]}}). Check base case: if not head or not head.next -> False. Recurse downstream.`,
        nodes: vals.map((v, idx) => ({{
          val: v,
          topPtrs: idx === 0 ? ['head'] : [],
          bottomPtrs: [],
          arrow: 'right'
        }}))
      }});

      for (let i = 1; i < vals.length; i++) {{
        const isTail = (i === vals.length - 1);
        steps.push({{
          type: 'linked_list',
          line: 5,
          tag: `2. Recurse downstream: Node(${{vals[i]}})`,
          badge: isTail ? 'Base Case Hit!' : 'Push Call Stack',
          badgeColor: isTail ? 'emerald' : 'amber',
          desc: isTail
            ? `Reaching tail Node(${{vals[i]}})! if not head or not head.next is True! Base case hit, returns new_head = Node(${{vals[i]}}). Call stack unwinds!`
            : `Recurse: new_head = self.reverseList(Node(${{vals[i]}})). Diving to the end of the list.`,
          nodes: vals.map((v, idx) => ({{
            val: v,
            topPtrs: idx === i ? ['head'] : (idx === vals.length - 1 && isTail ? ['new_head'] : []),
            bottomPtrs: [],
            arrow: 'right',
            isActive: idx === i
          }}))
        }});
      }}

      // Unwind: head.next.next = head
      let arrows = vals.map(() => 'right');
      for (let i = vals.length - 2; i >= 0; i--) {{
        arrows[i + 1] = 'left';
        arrows[i] = 'null';
        steps.push({{
          type: 'linked_list',
          line: 6,
          tag: `3. Unwind Node(${{vals[i]}}): head.next.next = head`,
          badge: 'Flip Arrow',
          badgeColor: 'rose',
          desc: `Unwinding to Node(${{vals[i]}}). Execute head.next.next = head! Node(${{vals[i + 1]}})'s next arrow flips backwards to point to Node(${{vals[i]}}). Then head.next = None breaks the cycle.`,
          nodes: vals.map((v, idx) => ({{
            val: v,
            topPtrs: idx === i ? ['head'] : (idx === vals.length - 1 ? ['new_head'] : []),
            bottomPtrs: [],
            arrow: arrows[idx],
            isActive: idx === i
          }}))
        }});
      }}

      steps.push({{
        type: 'linked_list',
        line: 8,
        tag: 'Complete: Return new_head',
        badge: 'Finished',
        badgeColor: 'emerald',
        desc: `Return new_head (Node ${{vals[vals.length - 1]}}). Entire linked list reversed via post-order recursion!`,
        nodes: vals.map((v, idx) => ({{
          val: v,
          topPtrs: idx === vals.length - 1 ? ['RETURN HEAD'] : [],
          bottomPtrs: [],
          arrow: arrows[idx]
        }}))
      }});

      return steps;
    }}

    function generateReverseLinkedListSteps(initialArr) {{
      return generateReverseLinkedListIterativeSteps(initialArr);
    }}

    // REVERSE FIRST K NODES
    function generateReverseFirstKSteps(initialArr, kVal) {{
      const vals = [...initialArr];
      const k = Math.min(kVal || 4, vals.length);
      const steps = [];

      steps.push({{
        type: 'linked_list',
        line: 2,
        tag: 'Step 0: Setup',
        badge: 'k = ' + k,
        badgeColor: 'blue',
        desc: `Target: reverse first k = ${{k}} nodes of [${{vals.join(' -> ')}} -> null]. Initialize prev = None, cur = head (Node ${{vals[0]}}).`,
        nodes: vals.map((v, i) => ({{
          val: v,
          topPtrs: i === 0 ? ['head'] : [],
          bottomPtrs: i === 0 ? ['cur'] : [],
          arrow: 'right',
          isActive: i < k
        }}))
      }});

      let prevVals = [];
      for (let i = 0; i < k; i++) {{
        const flippedVal = vals[i];
        prevVals.unshift(flippedVal);
        const remVals = vals.slice(i + 1);

        steps.push({{
          type: 'linked_list',
          line: 6,
          tag: `Flip ${{i + 1}} of ${{k}}: Node(${{flippedVal}})`,
          badge: `Flipped Node ${{flippedVal}}`,
          badgeColor: (i === k - 1) ? 'rose' : 'amber',
          desc: `1. nxt = cur.next. 2. cur.next = prev. 3. prev = cur (Node ${{prevVals[0]}}). 4. cur = nxt (${{remVals.length ? 'Node ' + remVals[0] : 'None'}}). ${{i === k - 1 ? 'Reversal loop finished! The reversed block is detached from remaining piece.' : 'Reversing piece from left.'}}`,
          nodes: vals.map((v, idx) => {{
            const top = [];
            const bot = [];
            if (v === vals[0]) top.push('head');
            if (v === prevVals[0]) bot.push('prev');
            if (remVals.length && v === remVals[0]) bot.push('cur');
            return {{ val: v, topPtrs: top, bottomPtrs: bot, arrow: idx < i ? 'left' : 'right', isActive: v === flippedVal }};
          }})
        }});
      }}

      // Step: The Bridge
      const nextTarget = (k < vals.length) ? `Node ${{vals[k]}}` : 'None';
      steps.push({{
        type: 'linked_list',
        line: 9,
        tag: 'The Bridge: head.next = cur',
        badge: 'Bridge Reconnected',
        badgeColor: 'emerald',
        desc: `Execute the bridge line: head.next = cur. Variable head was STILL pointing to Node(${{vals[0]}}), so head.next = cur connects Node(${{vals[0]}}) directly to ${{nextTarget}}! Detached pieces reunited!`,
        nodes: vals.map((v, idx) => {{
          const top = [];
          const bot = [];
          if (v === vals[0]) top.push('head');
          if (v === prevVals[0]) bot.push('prev');
          if (k < vals.length && v === vals[k]) bot.push('cur');
          return {{ val: v, topPtrs: top, bottomPtrs: bot, arrow: (idx === 0) ? 'right' : (idx < k ? 'left' : 'right') }};
        }})
      }});

      steps.push({{
        type: 'linked_list',
        line: 10,
        tag: 'Complete: Return prev',
        badge: 'Finished',
        badgeColor: 'emerald',
        desc: `return prev! Look at the front of the chain: it is Node(${{prevVals[0]}}). That is why we return prev!`,
        nodes: vals.map((v) => {{
          const top = [];
          if (v === prevVals[0]) top.push('RETURN HEAD');
          return {{ val: v, topPtrs: top, bottomPtrs: [], arrow: 'right' }};
        }})
      }});

      return steps;
    }}

    // REMOVE LINKED LIST ELEMENTS: Method 1 (Sentinel Dummy)
    function generateRemoveElementsSentinelSteps(initialArr, targetVal) {{
      const target = (targetVal !== undefined) ? targetVal : 6;
      const steps = [];
      let currentNodes = [
        {{ val: '0', isDummy: true }},
        ...initialArr.map(v => ({{ val: v, isDummy: false }}))
      ];
      let curPos = 0;

      // Step 0: Sentinel Setup
      steps.push({{
        type: 'linked_list',
        line: 4,
        tag: 'Step 0: Setup Sentinel Dummy Node',
        badge: 'Sentinel Setup',
        badgeColor: 'blue',
        desc: `Created sentinel dummy = ListNode(0, head) and set cur = dummy. Target to delete: val = ${{target}}. Dummy gives every single node (even original head) a predecessor!`,
        nodes: currentNodes.map((n, i) => ({{
          val: n.val,
          isDummy: n.isDummy,
          topPtrs: i === 1 ? ['head'] : [],
          bottomPtrs: i === 0 ? ['dummy', 'cur'] : [],
          arrow: 'right'
        }}))
      }});

      while (curPos < currentNodes.length - 1) {{
        const nextVal = currentNodes[curPos + 1].val;
        const isMatch = (nextVal === target);

        // Check cur.next.val == target
        steps.push({{
          type: 'linked_list',
          line: 6,
          tag: `Check: cur.next.val (${{nextVal}}) == ${{target}}?`,
          badge: isMatch ? 'Match Found!' : 'Keep Node',
          badgeColor: isMatch ? 'rose' : 'emerald',
          desc: isMatch
            ? `cur.next.val is ${{nextVal}}, which matches target ${{target}}! Prepare to bypass via cur.next = cur.next.next.`
            : `cur.next.val is ${{nextVal}}, which does not match target ${{target}}. Node is preserved; take else branch.`,
          nodes: currentNodes.map((n, i) => ({{
            val: n.val,
            isDummy: n.isDummy,
            topPtrs: i === 1 ? ['head'] : [],
            bottomPtrs: i === curPos ? ['cur'] : (i === curPos + 1 ? ['cur.next'] : []),
            arrow: 'right',
            isMatch: i === curPos + 1 && isMatch,
            isActive: i === curPos
          }}))
        }});

        if (isMatch) {{
          const bypassed = currentNodes.splice(curPos + 1, 1)[0];
          steps.push({{
            type: 'linked_list',
            line: 7,
            tag: `Bypass: Snip out Node(${{bypassed.val}})`,
            badge: 'cur.next = cur.next.next',
            badgeColor: 'amber',
            desc: `Rewired cur.next = cur.next.next! Node(${{bypassed.val}}) is snipped. CRUCIAL: Do NOT advance cur! Stay on cur to check the newly attached next node.`,
            bypassed: bypassed,
            nodes: currentNodes.map((n, i) => ({{
              val: n.val,
              isDummy: n.isDummy,
              topPtrs: i === 1 ? ['head'] : [],
              bottomPtrs: i === curPos ? ['cur'] : [],
              arrow: 'right',
              isActive: i === curPos
            }}))
          }});
        }} else {{
          curPos += 1;
          steps.push({{
            type: 'linked_list',
            line: 9,
            tag: `Advance: cur = cur.next`,
            badge: 'Slide Forward',
            badgeColor: 'blue',
            desc: `Safe to advance: cur = cur.next. cur now stands on Node(${{currentNodes[curPos].val}}).`,
            nodes: currentNodes.map((n, i) => ({{
              val: n.val,
              isDummy: n.isDummy,
              topPtrs: i === 1 ? ['head'] : [],
              bottomPtrs: i === curPos ? ['cur'] : [],
              arrow: 'right',
              isActive: i === curPos
            }}))
          }});
        }}
      }}

      // Final step: return dummy.next
      const finalRealNodes = currentNodes.slice(1);
      steps.push({{
        type: 'linked_list',
        line: 10,
        tag: 'Complete: Return dummy.next',
        badge: 'Finished',
        badgeColor: 'emerald',
        desc: `cur.next reached null! Loop terminates. return dummy.next, which returns ${{finalRealNodes.length ? `Node(${{finalRealNodes[0].val}})` : 'null'}} as the clean head (skipping fake dummy 0).`,
        nodes: currentNodes.map((n, i) => ({{
          val: n.val,
          isDummy: n.isDummy,
          topPtrs: i === 1 ? ['RETURN HEAD'] : [],
          bottomPtrs: i === curPos ? ['cur'] : [],
          arrow: 'right'
        }}))
      }});

      return steps;
    }}

    // REMOVE LINKED LIST ELEMENTS: Method 2 (Without Dummy / Two-Pass)
    function generateRemoveElementsNoDummySteps(initialArr, targetVal) {{
      const target = (targetVal !== undefined) ? targetVal : 6;
      const steps = [];
      let currentNodes = initialArr.map(v => ({{ val: v }}));

      if (!currentNodes.length) {{
        steps.push({{
          type: 'linked_list',
          line: 3,
          tag: 'Check Empty List',
          badge: 'List is None',
          badgeColor: 'blue',
          desc: 'head is None! Return head immediately.',
          nodes: []
        }});
        return steps;
      }}

      let nodePos = 0;
      steps.push({{
        type: 'linked_list',
        line: 5,
        tag: 'Step 1: Initialize node = head',
        badge: 'Pointer Setup',
        badgeColor: 'blue',
        desc: `Set node = head (Node ${{currentNodes[0].val}}). In this approach without a dummy node, we walk from head and delete from node.next onward!`,
        nodes: currentNodes.map((n, i) => ({{
          val: n.val,
          topPtrs: i === 0 ? ['head'] : [],
          bottomPtrs: i === 0 ? ['node'] : [],
          arrow: 'right'
        }}))
      }});

      while (nodePos < currentNodes.length - 1) {{
        const nextVal = currentNodes[nodePos + 1].val;
        const isMatch = (nextVal === target);

        steps.push({{
          type: 'linked_list',
          line: 7,
          tag: `Check: node.next.val (${{nextVal}}) == ${{target}}?`,
          badge: isMatch ? 'Match Found!' : 'Keep Node',
          badgeColor: isMatch ? 'rose' : 'emerald',
          desc: isMatch
            ? `node.next.val (${{nextVal}}) == ${{target}}! Prepare to bypass via node.next = node.next.next.`
            : `node.next.val (${{nextVal}}) != ${{target}}. Node preserved; advance node.`,
          nodes: currentNodes.map((n, i) => ({{
            val: n.val,
            topPtrs: i === 0 ? ['head'] : [],
            bottomPtrs: i === nodePos ? ['node'] : (i === nodePos + 1 ? ['node.next'] : []),
            arrow: 'right',
            isMatch: i === nodePos + 1 && isMatch,
            isActive: i === nodePos
          }}))
        }});

        if (isMatch) {{
          const bypassed = currentNodes.splice(nodePos + 1, 1)[0];
          steps.push({{
            type: 'linked_list',
            line: 8,
            tag: `Bypass: node.next = node.next.next`,
            badge: 'Bypassed Node',
            badgeColor: 'amber',
            desc: `Rewired node.next = node.next.next! Node(${{bypassed.val}}) snipped. Pointer node stays on current position.`,
            bypassed: bypassed,
            nodes: currentNodes.map((n, i) => ({{
              val: n.val,
              topPtrs: i === 0 ? ['head'] : [],
              bottomPtrs: i === nodePos ? ['node'] : [],
              arrow: 'right',
              isActive: i === nodePos
            }}))
          }});
        }} else {{
          nodePos += 1;
          steps.push({{
            type: 'linked_list',
            line: 10,
            tag: `Advance: node = node.next`,
            badge: 'Slide Forward',
            badgeColor: 'blue',
            desc: `Safe to advance: node = node.next to Node(${{currentNodes[nodePos].val}}).`,
            nodes: currentNodes.map((n, i) => ({{
              val: n.val,
              topPtrs: i === 0 ? ['head'] : [],
              bottomPtrs: i === nodePos ? ['node'] : [],
              arrow: 'right',
              isActive: i === nodePos
            }}))
          }});
        }}
      }}

      // Trailing check on head
      const headMatches = currentNodes.length > 0 && currentNodes[0].val === target;
      steps.push({{
        type: 'linked_list',
        line: 11,
        tag: `Trailing Check: head.val == ${{target}}?`,
        badge: headMatches ? 'Head Matches!' : 'Head Safe',
        badgeColor: headMatches ? 'rose' : 'emerald',
        desc: `While loop finished! NOTICE: Because the loop only inspected node.next, the original head node was NEVER checked during the loop! Now check: if head.val == ${{target}}. Result: ${{headMatches ? 'Matches! Need to chop head.' : 'Does not match. Head stays.'}}`,
        nodes: currentNodes.map((n, i) => ({{
          val: n.val,
          topPtrs: i === 0 ? ['head'] : [],
          bottomPtrs: i === nodePos ? ['node'] : [],
          arrow: 'right',
          isMatch: i === 0 && headMatches
        }}))
      }});

      if (headMatches) {{
        const poppedHead = currentNodes.splice(0, 1)[0];
        steps.push({{
          type: 'linked_list',
          line: 12,
          tag: `Chop head: head = head.next`,
          badge: 'Head Removed',
          badgeColor: 'rose',
          desc: `head.val matches target! Chop off the original head: head = head.next. Node(${{poppedHead.val}}) is discarded!`,
          bypassed: poppedHead,
          nodes: currentNodes.map((n, i) => ({{
            val: n.val,
            topPtrs: i === 0 ? ['head'] : [],
            bottomPtrs: [],
            arrow: 'right'
          }}))
        }});
      }}

      steps.push({{
        type: 'linked_list',
        line: 13,
        tag: 'Complete: Return head',
        badge: 'Finished',
        badgeColor: 'emerald',
        desc: `return head! All matching elements removed. Surviving list: [${{currentNodes.map(x => x.val).join(' -> ') || 'null'}}].`,
        nodes: currentNodes.map((n, i) => ({{
          val: n.val,
          topPtrs: i === 0 ? ['RETURN HEAD'] : [],
          bottomPtrs: [],
          arrow: 'right'
        }}))
      }});

      return steps;
    }}

    // REMOVE LINKED LIST ELEMENTS: Method 3 (Recursive)
    function generateRemoveElementsRecursiveSteps(initialArr, targetVal) {{
      const target = (targetVal !== undefined) ? targetVal : 6;
      const steps = [];
      const vals = [...initialArr];

      steps.push({{
        type: 'linked_list',
        line: 3,
        tag: '1. Call Stack Start',
        badge: 'Recurse',
        badgeColor: 'blue',
        desc: `Call removeElements(head = Node ${{vals[0]}}, val = ${{target}}). Dives downstream to clean remainder of list first.`,
        nodes: vals.map((v, i) => ({{
          val: v,
          topPtrs: i === 0 ? ['head'] : [],
          bottomPtrs: [],
          arrow: 'right'
        }}))
      }});

      for (let i = 1; i <= vals.length; i++) {{
        const isBase = (i === vals.length);
        steps.push({{
          type: 'linked_list',
          line: isBase ? 4 : 5,
          tag: isBase ? 'Base Case: Reached null' : `Recurse to Node(${{vals[i]}})`,
          badge: isBase ? 'Base Case' : 'Call Stack Push',
          badgeColor: isBase ? 'emerald' : 'amber',
          desc: isBase
            ? 'if not head: return None! Call stack reaches the bottom of list and begins unwinding upward.'
            : `head.next = self.removeElements(head.next, val). Descending to Node(${{vals[i]}}).`,
          nodes: vals.map((v, idx) => ({{
            val: v,
            topPtrs: idx === i ? ['head'] : [],
            bottomPtrs: [],
            arrow: 'right',
            isActive: idx === i
          }}))
        }});
      }}

      let surviving = [];
      for (let i = vals.length - 1; i >= 0; i--) {{
        const v = vals[i];
        const isMatch = (v === target);
        if (!isMatch) surviving.unshift(v);

        steps.push({{
          type: 'linked_list',
          line: 6,
          tag: `Unwind Node(${{v}}): ${{isMatch ? 'Delete' : 'Keep'}}`,
          badge: isMatch ? 'Skip Node' : 'Attach Node',
          badgeColor: isMatch ? 'rose' : 'emerald',
          desc: isMatch
            ? `head.val (${{v}}) == ${{target}}! Return head.next (skipping Node(${{v}})). Node is removed during unwind!`
            : `head.val (${{v}}) != ${{target}}. Return head. Node(${{v}}) is kept!`,
          bypassed: isMatch ? {{ val: v }} : null,
          nodes: surviving.map((sv, idx) => ({{
            val: sv,
            topPtrs: idx === 0 ? ['cur_head'] : [],
            bottomPtrs: [],
            arrow: 'right'
          }}))
        }});
      }}

      steps.push({{
        type: 'linked_list',
        line: 6,
        tag: 'Complete: Return Head',
        badge: 'Finished',
        badgeColor: 'emerald',
        desc: `Recursion fully unwound! Clean surviving head returned: [${{surviving.join(' -> ') || 'null'}}].`,
        nodes: surviving.map((sv, idx) => ({{
          val: sv,
          topPtrs: idx === 0 ? ['RETURN HEAD'] : [],
          bottomPtrs: [],
          arrow: 'right'
        }}))
      }});

      return steps;
    }}

    function generateRemoveElementsSteps(initialArr, targetVal) {{
      return generateRemoveElementsSentinelSteps(initialArr, targetVal);
    }}

    // MERGE SORT STEPS
    function generateMergeSortSteps(initialArr) {{
      const arr = [38, 27, 43, 3, 9, 82, 10];
      return [
        {{
          type: 'array',
          line: 5,
          array: [...arr],
          active: [],
          pointers: {{}},
          tag: '1. Divide Phase',
          badge: 'Full Array',
          badgeColor: 'blue',
          desc: 'Merge sort divides array recursively at mid = len // 2 into left and right halves until single elements are reached.',
          vars: {{ size: arr.length }}
        }},
        {{
          type: 'array',
          line: 7,
          array: [38, 27, 43, 3, 9, 82, 10],
          active: [0, 1, 2, 3],
          pointers: {{ left: 0, right: 4 }},
          tag: '2. Split Halves',
          badge: 'Halving',
          badgeColor: 'amber',
          desc: 'Left half: [38, 27, 43, 3] | Right half: [9, 82, 10]. Recurse down each half.',
          vars: {{ leftSize: 4, rightSize: 3 }}
        }},
        {{
          type: 'array',
          line: 12,
          array: [27, 38, 3, 43, 9, 82, 10],
          active: [0, 1, 2, 3],
          sorted: [0, 1, 2, 3],
          pointers: {{}},
          tag: '3. Merge Base Pairs',
          badge: 'Conquer',
          badgeColor: 'emerald',
          desc: 'Merged pairs: [38] and [27] -> [27, 38]. [43] and [3] -> [3, 43].',
          vars: {{ leftSubsorted: true }}
        }},
        {{
          type: 'array',
          line: 14,
          array: [3, 27, 38, 43, 9, 10, 82],
          active: [0, 1, 2, 3, 4, 5, 6],
          sorted: [0, 1, 2, 3, 4, 5, 6],
          pointers: {{}},
          tag: '4. Merge Quarter Arrays',
          badge: 'Two Pointers Merge',
          badgeColor: 'emerald',
          desc: 'Two pointers merge [27, 38] and [3, 43] -> [3, 27, 38, 43]. Right half merged -> [9, 10, 82].',
          vars: {{ leftQuarter: 4, rightQuarter: 3 }}
        }},
        {{
          type: 'array',
          line: 15,
          array: [3, 9, 10, 27, 38, 43, 82],
          active: [],
          pointers: {{}},
          sorted: [0, 1, 2, 3, 4, 5, 6],
          tag: '5. Final Combined Merge',
          badge: 'Sorted!',
          badgeColor: 'emerald',
          desc: 'Merged [3, 27, 38, 43] and [9, 10, 82] using two pointers in O(n) linear time! Array is sorted.',
          vars: {{ result: 'Fully sorted', complexity: 'O(n log n)' }}
        }}
      ];
    }}

    // QUICK SORT STEPS
    function generateQuickSortSteps(initialArr) {{
      const arr = [10, 80, 30, 90, 40, 50, 70];
      return [
        {{
          type: 'array',
          line: 4,
          array: [...arr],
          active: [6],
          pointers: {{ pivot: 6, i: -1, j: 0 }},
          tag: '1. Pivot Choice (Lomuto)',
          badge: 'Pivot = 70',
          badgeColor: 'blue',
          desc: 'Pivot chosen as last element arr[6] = 70. Pointer i tracks region <= 70, j scans indices 0 to 5.',
          vars: {{ pivot: 70, i: -1, j: 0 }}
        }},
        {{
          type: 'array',
          line: 6,
          array: [10, 80, 30, 90, 40, 50, 70],
          active: [0],
          pointers: {{ i: 0, j: 0, pivot: 6 }},
          tag: '2. Scan arr[0] = 10',
          badge: '10 <= 70',
          badgeColor: 'emerald',
          desc: 'arr[0] (10) <= 70. Increment i to 0, swap arr[0] with arr[0].',
          vars: {{ i: 0, j: 0 }}
        }},
        {{
          type: 'array',
          line: 7,
          array: [10, 30, 80, 90, 40, 50, 70],
          active: [1, 2],
          swapped: [1, 2],
          pointers: {{ i: 1, j: 2, pivot: 6 }},
          tag: '3. Scan arr[2] = 30',
          badge: 'Swap 80 and 30',
          badgeColor: 'rose',
          desc: 'arr[2] (30) <= 70. Increment i to 1, swap arr[1] (80) and arr[2] (30).',
          vars: {{ i: 1, j: 2 }}
        }},
        {{
          type: 'array',
          line: 7,
          array: [10, 30, 40, 90, 80, 50, 70],
          active: [2, 4],
          swapped: [2, 4],
          pointers: {{ i: 2, j: 4, pivot: 6 }},
          tag: '4. Scan arr[4] = 40',
          badge: 'Swap 90 and 40',
          badgeColor: 'rose',
          desc: 'arr[4] (40) <= 70. Increment i to 2, swap arr[2] (90) and arr[4] (40).',
          vars: {{ i: 2, j: 4 }}
        }},
        {{
          type: 'array',
          line: 7,
          array: [10, 30, 40, 50, 80, 90, 70],
          active: [3, 5],
          swapped: [3, 5],
          pointers: {{ i: 3, j: 5, pivot: 6 }},
          tag: '5. Scan arr[5] = 50',
          badge: 'Swap 80 and 50',
          badgeColor: 'rose',
          desc: 'arr[5] (50) <= 70. Increment i to 3, swap arr[3] (80) and arr[5] (50). Scanner j reaches end.',
          vars: {{ i: 3, j: 5 }}
        }},
        {{
          type: 'array',
          line: 9,
          array: [10, 30, 40, 50, 70, 90, 80],
          active: [4, 6],
          swapped: [4, 6],
          sorted: [4],
          pointers: {{ LOCKED_PIVOT: 4 }},
          tag: '6. Place Pivot into Slot',
          badge: 'Pivot Locked',
          badgeColor: 'emerald',
          desc: 'Swap pivot 70 with arr[i + 1] (arr[4] = 80). 70 is permanently settled at index 4!',
          vars: {{ pivotIndex: 4, value: 70 }}
        }},
        {{
          type: 'array',
          line: 11,
          array: [10, 30, 40, 50, 70, 80, 90],
          active: [],
          pointers: {{}},
          sorted: [0, 1, 2, 3, 4, 5, 6],
          tag: '7. Subarrays Sorted',
          badge: 'Done!',
          badgeColor: 'emerald',
          desc: 'Recurse on left [10, 30, 40, 50] and right [80, 90]. Entire array is sorted!',
          vars: {{ status: 'Sorted' }}
        }}
      ];
    }}

    // MASTER ALGORITHM CONFIGURATIONS
    const ALGO_CONFIGS = {{
      remove_elements: {{
        title: 'LeetCode 203: Remove Linked List Elements',
        defaultMethod: 'sentinel',
        methods: [
          {{
            id: 'sentinel',
            label: 'Sentinel Dummy',
            desc: 'Method 1: Sentinel Dummy (Recommended)',
            code: [
              'class Solution:',
              '    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:',
              '        dummy = ListNode(0, head)',
              '        cur = dummy',
              '        while cur.next:',
              '            if cur.next.val == val:',
              '                cur.next = cur.next.next  # Bypass matching node',
              '            else:',
              '                cur = cur.next            # Advance pointer',
              '        return dummy.next'
            ],
            generate: (arr, target) => generateRemoveElementsSentinelSteps(arr, target)
          }},
          {{
            id: 'no_dummy',
            label: 'Two-Pass (No Dummy)',
            desc: 'Method 2: Without Dummy (Head check + Pointer walk)',
            code: [
              'class Solution:',
              '    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:',
              '        if not head:',
              '            return head',
              '        node = head',
              '        while node and node.next:',
              '            if node.next.val == val:',
              '                node.next = node.next.next',
              '            else:',
              '                node = node.next',
              '        if head.val == val:',
              '            head = head.next',
              '        return head'
            ],
            generate: (arr, target) => generateRemoveElementsNoDummySteps(arr, target)
          }},
          {{
            id: 'recursive',
            label: 'Recursive',
            desc: 'Method 3: Recursive Downstream Cleanup',
            code: [
              'class Solution:',
              '    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:',
              '        if not head:',
              '            return None',
              '        head.next = self.removeElements(head.next, val)',
              '        return head.next if head.val == val else head'
            ],
            generate: (arr, target) => generateRemoveElementsRecursiveSteps(arr, target)
          }}
        ],
        presets: [
          {{ label: 'List 1 [1..6] (val=6)', val: [1, 2, 6, 3, 4, 5, 6], target: 6 }},
          {{ label: 'All 7s (val=7)', val: [7, 7, 7, 7], target: 7 }},
          {{ label: 'Duplicates [1,2,2,1] (val=2)', val: [1, 2, 2, 1], target: 2 }},
          {{ label: 'Head Match [6,1,2,3] (val=6)', val: [6, 1, 2, 3], target: 6 }},
          {{ label: 'Tail Match [1,2,3,6] (val=6)', val: [1, 2, 3, 6], target: 6 }}
        ]
      }},

      reverse_linked_list: {{
        title: 'LeetCode 206: Reverse Linked List',
        defaultMethod: 'iterative',
        methods: [
          {{
            id: 'iterative',
            label: 'Iterative (3 Pointers)',
            desc: 'Method 1: Three Pointers (prev, curr, next_node)',
            code: [
              'class Solution:',
              '    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:',
              '        prev = None',
              '        curr = head',
              '        while curr:',
              '            next_node = curr.next  # Save next node',
              '            curr.next = prev       # Reverse the pointer',
              '            prev = curr            # Move prev forward',
              '            curr = next_node       # Move curr forward',
              '        return prev'
            ],
            generate: (arr) => generateReverseLinkedListIterativeSteps(arr)
          }},
          {{
            id: 'recursive',
            label: 'Recursive',
            desc: 'Method 2: Post-order Call Stack Unwind',
            code: [
              'class Solution:',
              '    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:',
              '        if not head or not head.next:',
              '            return head',
              '        new_head = self.reverseList(head.next)',
              '        head.next.next = head',
              '        head.next = None',
              '        return new_head'
            ],
            generate: (arr) => generateReverseLinkedListRecursiveSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'List 1 [1, 2, 3, 4, 5]', val: [1, 2, 3, 4, 5] }},
          {{ label: 'List 2 [1, 2, 3]', val: [1, 2, 3] }},
          {{ label: 'Single Node [42]', val: [42] }},
          {{ label: 'Even Nodes [10, 20, 30, 40]', val: [10, 20, 30, 40] }}
        ]
      }},

      reverse_first_k: {{
        title: 'Reverse First K Nodes & Bridge',
        defaultMethod: 'iterative',
        methods: [
          {{
            id: 'iterative',
            label: 'Iterative (K Nodes)',
            desc: 'Reverse first K nodes and bridge head.next = cur',
            code: [
              'def reverseFirstK(head: ListNode, k: int) -> ListNode:',
              '    prev = None',
              '    cur = head',
              '    for _ in range(k):',
              '        nxt = cur.next',
              '        cur.next = prev',
              '        prev = cur',
              '        cur = nxt',
              '    head.next = cur  # The Bridge',
              '    return prev'
            ],
            generate: (arr, target, k) => generateReverseFirstKSteps(arr, k || 4)
          }}
        ],
        presets: [
          {{ label: 'Notebook [1..6] (k=4)', val: [1, 2, 3, 4, 5, 6], k: 4 }},
          {{ label: 'Full Reversal [1..4] (k=4)', val: [1, 2, 3, 4], k: 4 }},
          {{ label: 'First 2 of 5 (k=2)', val: [10, 20, 30, 40, 50], k: 2 }}
        ]
      }},

      bubble_sort: {{
        title: 'Bubble Sort Walkthrough',
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: 'Standard',
            desc: 'Adjacent swaps with early exit flag',
            code: [
              'def bubble_sort(arr):',
              '    n = len(arr)',
              '    for i in range(n):',
              '        swapped = False',
              '        for j in range(0, n - i - 1):',
              '            if arr[j] > arr[j + 1]:',
              '                arr[j], arr[j + 1] = arr[j + 1], arr[j]',
              '                swapped = True',
              '        if not swapped: break',
              '    return arr'
            ],
            generate: (arr) => generateBubbleSortSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'Default [5, 1, 4, 2, 8]', val: [5, 1, 4, 2, 8] }},
          {{ label: 'Reversed [5, 4, 3, 2, 1]', val: [5, 4, 3, 2, 1] }},
          {{ label: 'Nearly Sorted [1, 2, 4, 3, 5]', val: [1, 2, 4, 3, 5] }}
        ]
      }},

      binary_search: {{
        title: 'Binary Search Walkthrough',
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: 'Standard',
            desc: 'Classic while lo <= hi with mid calculation',
            code: [
              'def binary_search(nums, target):',
              '    lo, hi = 0, len(nums) - 1',
              '    while lo <= hi:',
              '        mid = lo + (hi - lo) // 2',
              '        if nums[mid] == target:',
              '            return mid',
              '        elif nums[mid] < target:',
              '            lo = mid + 1',
              '        else:',
              '            hi = mid - 1',
              '    return -1'
            ],
            generate: (arr, target) => generateBinarySearchSteps(arr, target)
          }}
        ],
        presets: [
          {{ label: 'Target 23 (In list)', val: [2, 5, 8, 12, 16, 23, 38], target: 23 }},
          {{ label: 'Target 5 (Left)', val: [2, 5, 8, 12, 16, 23, 38], target: 5 }},
          {{ label: 'Target 10 (Not found)', val: [2, 5, 8, 12, 16, 23, 38], target: 10 }}
        ]
      }},

      selection_sort: {{
        title: 'Selection Sort Walkthrough',
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: 'Standard',
            desc: 'Find minimum and swap into prefix',
            code: [
              'def selection_sort(arr):',
              '    n = len(arr)',
              '    for i in range(n):',
              '        min_idx = i',
              '        for j in range(i + 1, n):',
              '            if arr[j] < arr[min_idx]:',
              '                min_idx = j',
              '        arr[i], arr[min_idx] = arr[min_idx], arr[i]',
              '    return arr'
            ],
            generate: (arr) => generateSelectionSortSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'Default [64, 25, 12, 22, 11]', val: [64, 25, 12, 22, 11] }},
          {{ label: 'Reversed [5, 4, 3, 2, 1]', val: [5, 4, 3, 2, 1] }}
        ]
      }},

      insertion_sort: {{
        title: 'Insertion Sort Walkthrough',
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: 'Standard',
            desc: 'Shift elements to insert key in sorted prefix',
            code: [
              'def insertion_sort(arr):',
              '    for i in range(1, len(arr)):',
              '        key = arr[i]',
              '        j = i - 1',
              '        while j >= 0 and arr[j] > key:',
              '            arr[j + 1] = arr[j]',
              '            j -= 1',
              '        arr[j + 1] = key',
              '    return arr'
            ],
            generate: (arr) => generateInsertionSortSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'Default [12, 11, 13, 5, 6]', val: [12, 11, 13, 5, 6] }},
          {{ label: 'Reversed [5, 4, 3, 2, 1]', val: [5, 4, 3, 2, 1] }}
        ]
      }},

      peak_finding: {{
        title: 'Peak Finding Walkthrough',
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: 'Binary Search on Slope',
            desc: 'Compare mid with mid + 1',
            code: [
              'def findPeakElement(nums):',
              '    lo, hi = 0, len(nums) - 1',
              '    while lo < hi:',
              '        mid = (lo + hi) // 2',
              '        if nums[mid] < nums[mid + 1]:',
              '            lo = mid + 1',
              '        else:',
              '            hi = mid',
              '    return lo'
            ],
            generate: (arr) => generatePeakFindingSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'Default [1, 2, 1, 3, 5, 6, 4]', val: [1, 2, 1, 3, 5, 6, 4] }},
          {{ label: 'Single Peak [1, 3, 7, 4, 2]', val: [1, 3, 7, 4, 2] }}
        ]
      }},

      sort_colors: {{
        title: 'Dutch National Flag (Sort Colors)',
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: '3 Pointers',
            desc: 'low, mid, high pointers partition 0, 1, 2',
            code: [
              'def sortColors(nums):',
              '    low, mid, high = 0, 0, len(nums) - 1',
              '    while mid <= high:',
              '        if nums[mid] == 0:',
              '            nums[low], nums[mid] = nums[mid], nums[low]',
              '            low += 1; mid += 1',
              '        elif nums[mid] == 1:',
              '            mid += 1',
              '        else:',
              '            nums[mid], nums[high] = nums[high], nums[mid]',
              '            high -= 1'
            ],
            generate: (arr) => generateSortColorsSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'Default [2, 0, 2, 1, 1, 0]', val: [2, 0, 2, 1, 1, 0] }},
          {{ label: 'Alternating [1, 2, 0, 1, 2, 0]', val: [1, 2, 0, 1, 2, 0] }}
        ]
      }},

      container_with_most_water: {{
        title: 'Container With Most Water',
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: 'Two Pointers',
            desc: 'Squeeze pointers from outer edges inward',
            code: [
              'def maxArea(height):',
              '    left, right = 0, len(height) - 1',
              '    max_water = 0',
              '    while left < right:',
              '        h = min(height[left], height[right])',
              '        max_water = max(max_water, h * (right - left))',
              '        if height[left] < height[right]: left += 1',
              '        else: right -= 1',
              '    return max_water'
            ],
            generate: (arr) => generateContainerWaterSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'Default [1, 8, 6, 2, 5, 4, 8, 3, 7]', val: [1, 8, 6, 2, 5, 4, 8, 3, 7] }},
          {{ label: 'Pyramid [1, 4, 8, 8, 4, 1]', val: [1, 4, 8, 8, 4, 1] }}
        ]
      }},

      kadanes: {{
        title: "Kadane's Algorithm",
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: "Kadane's DP",
            desc: 'cur_sum = max(x, cur_sum + x)',
            code: [
              'def maxSubArray(nums):',
              '    max_sum = cur_sum = nums[0]',
              '    for x in nums[1:]:',
              '        cur_sum = max(x, cur_sum + x)',
              '        max_sum = max(max_sum, cur_sum)',
              '    return max_sum'
            ],
            generate: (arr) => generateKadanesSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'Default [-2, 1, -3, 4, -1, 2, 1, -5, 4]', val: [-2, 1, -3, 4, -1, 2, 1, -5, 4] }},
          {{ label: 'All Negative [-5, -2, -8, -1]', val: [-5, -2, -8, -1] }}
        ]
      }},

      merge_sort: {{
        title: 'Merge Sort Walkthrough',
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: 'Divide & Conquer',
            desc: 'Recursive split then two-pointer merge',
            code: [
              'def merge_sort(arr):',
              '    if len(arr) <= 1: return arr',
              '    mid = len(arr) // 2',
              '    left = merge_sort(arr[:mid])',
              '    right = merge_sort(arr[mid:])',
              '    return merge(left, right)'
            ],
            generate: (arr) => generateMergeSortSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'Default [38, 27, 43, 3, 9, 82, 10]', val: [38, 27, 43, 3, 9, 82, 10] }}
        ]
      }},

      quick_sort: {{
        title: 'Quick Sort (Lomuto Partition)',
        defaultMethod: 'standard',
        methods: [
          {{
            id: 'standard',
            label: 'Lomuto Partition',
            desc: 'Last element as pivot, i tracks <= pivot',
            code: [
              'def quick_sort(arr, lo, hi):',
              '    if lo < hi:',
              '        p = partition(arr, lo, hi)',
              '        quick_sort(arr, lo, p - 1)',
              '        quick_sort(arr, p + 1, hi)'
            ],
            generate: (arr) => generateQuickSortSteps(arr)
          }}
        ],
        presets: [
          {{ label: 'Default [10, 80, 30, 90, 40, 50, 70]', val: [10, 80, 30, 90, 40, 50, 70] }}
        ]
      }}
    }};

    // CREATE PLAYTHROUGH WIDGET: AlgoMaster Split-Screen Engine
    function createPlaythroughWidget(spec) {{
      const widget = document.createElement('div');
      widget.className = 'playthrough-widget not-prose';

      const algo = spec.algorithm || 'remove_elements';
      const config = ALGO_CONFIGS[algo] || ALGO_CONFIGS['remove_elements'];

      let currentMethodId = spec.method || config.defaultMethod || config.methods[0].id;
      let currentArr = spec.initial ? [...spec.initial] : [...config.presets[0].val];
      let targetVal = spec.target !== undefined ? spec.target : (config.presets[0].target !== undefined ? config.presets[0].target : 6);
      let kVal = spec.k !== undefined ? spec.k : (config.presets[0].k !== undefined ? config.presets[0].k : 4);

      let steps = [];
      function computeSteps() {{
        const method = config.methods.find(m => m.id === currentMethodId) || config.methods[0];
        if (spec.steps) {{
          steps = spec.steps;
        }} else {{
          steps = method.generate(currentArr, targetVal, kVal);
        }}
        if (stepIdx >= steps.length) stepIdx = 0;
      }}

      let stepIdx = 0;
      let playInterval = null;
      let currentSpeed = 1.0;

      computeSteps();

      widget.innerHTML = `
        <div class="flex flex-col gap-3">
          <!-- Top Bar: Title & Method Tabs -->
          <div class="flex flex-wrap items-center justify-between gap-3 border-b ui-border pb-3">
            <div class="flex items-center gap-2">
              <span class="text-sm font-bold ui-accent-text flex items-center gap-2">
                <span>⚡</span>
                <span class="pt-title">${{config.title}}</span>
              </span>
            </div>
            <!-- Method Tabs Switcher -->
            <div class="pt-methods-container flex items-center gap-1.5 p-1 rounded-xl ui-card border">
            </div>
          </div>

          <!-- Split Screen Grid -->
          <div class="pt-split-grid">
            <!-- Left Column: Code Panel -->
            <div class="pt-code-panel">
              <div class="flex items-center justify-between px-3.5 py-2 border-b ui-border bg-slate-950/70 text-xs">
                <div class="flex items-center gap-2">
                  <span class="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 font-semibold font-mono text-[11px] flex items-center gap-1">
                    <span>🐍</span> Python 3
                  </span>
                  <span class="ui-text-muted font-mono text-[11px] pt-method-desc"></span>
                </div>
                <div class="flex items-center gap-2">
                  <button type="button" class="btn-copy-code px-2 py-0.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition-colors text-xs font-mono" title="Copy Python Solution">📋 Copy</button>
                </div>
              </div>
              <div class="pt-code-scroll">
              </div>
            </div>

            <!-- Right Column: Visual Stage & Step Info -->
            <div class="flex flex-col gap-3 min-w-0">
              <!-- Input Card -->
              <div class="rounded-xl border ui-border bg-slate-900/50 p-3">
                <div class="flex items-center justify-between gap-2 flex-wrap mb-2">
                  <span class="text-xs font-bold ui-text-muted uppercase tracking-wider font-mono">Input</span>
                  <div class="pt-presets-row flex items-center gap-1.5 flex-wrap">
                  </div>
                </div>
                <div class="pt-values-display px-3 py-1.5 rounded-lg bg-slate-950/80 border ui-border font-mono text-xs text-emerald-300">
                  values = [...]
                </div>
                <!-- Custom Input Bar -->
                <div class="pt-custom-form hidden mt-2 pt-2 border-t ui-border flex items-center gap-2 flex-wrap text-xs">
                  <input type="text" class="pt-custom-arr px-2.5 py-1 rounded bg-slate-950 border ui-border font-mono text-white flex-1 min-w-[140px]" placeholder="e.g. 1, 2, 6, 3, 4, 5, 6">
                  <input type="number" class="pt-custom-target px-2.5 py-1 rounded bg-slate-950 border ui-border font-mono text-white w-24" placeholder="val = 6">
                  <button type="button" class="btn-apply-custom px-3 py-1 rounded ui-accent-btn font-bold transition-all">Apply</button>
                  <button type="button" class="btn-cancel-custom px-2 py-1 rounded ui-text-muted hover:text-white">Cancel</button>
                </div>
              </div>

              <!-- Animation Stage -->
              <div class="pt-stage min-h-[220px] rounded-2xl border ui-border bg-slate-950/60 p-4 flex flex-col items-center justify-center relative overflow-x-auto shadow-inner">
              </div>

              <!-- Step Description Banner -->
              <div class="pt-desc-box rounded-xl border ui-border bg-slate-900/80 p-3.5 shadow-sm border-l-4 border-l-emerald-400">
              </div>
            </div>
          </div>

          <!-- Bottom Playback Controller Bar -->
          <div class="rounded-xl border ui-border bg-slate-950/80 px-4 py-2.5 flex flex-wrap items-center justify-between gap-3 shadow-md">
            <div class="flex items-center gap-2">
              <button type="button" class="btn-pt-reset px-2.5 py-1 rounded-lg border ui-border bg-slate-800/80 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-all flex items-center gap-1" title="Reset to Start">↺ Reset</button>
              <button type="button" class="btn-pt-prev px-3 py-1 rounded-lg border ui-border bg-slate-800/80 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all flex items-center gap-1" title="Previous Step (Left Arrow)">◀</button>
              <button type="button" class="btn-pt-play px-3.5 py-1 rounded-lg ui-accent-btn text-xs font-bold transition-all flex items-center gap-1.5 shadow-sm" title="Play / Pause (Spacebar)">▶ Play</button>
              <button type="button" class="btn-pt-next px-3 py-1 rounded-lg border ui-border bg-slate-800/80 hover:bg-slate-700 text-slate-200 text-xs font-bold transition-all flex items-center gap-1" title="Next Step (Right Arrow)">▶</button>
            </div>

            <!-- Scrubber Slider -->
            <div class="flex-1 min-w-[160px] flex items-center gap-3">
              <input type="range" class="pt-slider w-full accent-emerald-400 cursor-pointer h-1.5 rounded-lg bg-slate-800" min="0" max="${{Math.max(0, steps.length - 1)}}" value="0">
              <span class="pt-step-counter text-xs font-mono font-bold text-slate-300 whitespace-nowrap min-w-[70px] text-right">Step 1 / ${{steps.length}}</span>
            </div>

            <div class="flex items-center gap-2">
              <!-- Speed selector -->
              <select class="pt-speed-select text-xs font-mono bg-slate-900 border ui-border text-slate-300 rounded px-2 py-1 cursor-pointer">
                <option value="0.5">0.5x</option>
                <option value="1" selected>1x</option>
                <option value="1.5">1.5x</option>
                <option value="2">2x</option>
              </select>
              <button type="button" class="btn-pt-fullscreen p-1.5 rounded border ui-border text-slate-400 hover:text-white hover:bg-slate-800 transition-colors text-xs" title="Toggle Fullscreen">⛶</button>
            </div>
          </div>
        </div>
      `;

      const methodsContainer = widget.querySelector('.pt-methods-container');
      const methodDescEl = widget.querySelector('.pt-method-desc');
      const codeScrollEl = widget.querySelector('.pt-code-scroll');
      const presetsRow = widget.querySelector('.pt-presets-row');
      const valuesDisplayEl = widget.querySelector('.pt-values-display');
      const customForm = widget.querySelector('.pt-custom-form');
      const customArrInput = widget.querySelector('.pt-custom-arr');
      const customTargetInput = widget.querySelector('.pt-custom-target');
      const btnApplyCustom = widget.querySelector('.btn-apply-custom');
      const btnCancelCustom = widget.querySelector('.btn-cancel-custom');
      const stageEl = widget.querySelector('.pt-stage');
      const descBox = widget.querySelector('.pt-desc-box');
      const slider = widget.querySelector('.pt-slider');
      const stepCounter = widget.querySelector('.pt-step-counter');
      const speedSelect = widget.querySelector('.pt-speed-select');
      const btnPlay = widget.querySelector('.btn-pt-play');
      const btnPrev = widget.querySelector('.btn-pt-prev');
      const btnNext = widget.querySelector('.btn-pt-next');
      const btnReset = widget.querySelector('.btn-pt-reset');
      const btnFullscreen = widget.querySelector('.btn-pt-fullscreen');
      const btnCopyCode = widget.querySelector('.btn-copy-code');

      // Speed selection
      speedSelect.addEventListener('change', () => {{
        currentSpeed = parseFloat(speedSelect.value);
        if (playInterval) {{
          stopPlay();
          startPlay();
        }}
      }});

      // Copy Code Button
      btnCopyCode.addEventListener('click', () => {{
        const method = config.methods.find(m => m.id === currentMethodId) || config.methods[0];
        navigator.clipboard.writeText(method.code.join('\\n')).then(() => {{
          btnCopyCode.textContent = '✓ Copied!';
          setTimeout(() => btnCopyCode.textContent = '📋 Copy', 1500);
        }});
      }});

      // Fullscreen Toggle
      btnFullscreen.addEventListener('click', () => {{
        if (!document.fullscreenElement) {{
          widget.requestFullscreen?.().catch(() => {{}});
        }} else {{
          document.exitFullscreen?.().catch(() => {{}});
        }}
      }});

      // Render Method Tabs
      function renderMethods() {{
        methodsContainer.innerHTML = '';
        if (!config.methods || config.methods.length <= 1) {{
          methodsContainer.classList.add('hidden');
          return;
        }}
        methodsContainer.classList.remove('hidden');

        config.methods.forEach(m => {{
          const isAct = (m.id === currentMethodId);
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = `px-3.5 py-1 rounded-lg text-xs font-semibold transition-all ${{
            isAct 
              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 shadow-sm' 
              : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
          }}`;
          btn.textContent = m.label;
          btn.onclick = () => {{
            stopPlay();
            currentMethodId = m.id;
            computeSteps();
            stepIdx = 0;
            slider.max = Math.max(0, steps.length - 1);
            renderMethods();
            renderCode();
            renderStep();
          }};
          methodsContainer.appendChild(btn);
        }});
      }}

      // Render Code View
      function renderCode() {{
        const method = config.methods.find(m => m.id === currentMethodId) || config.methods[0];
        methodDescEl.textContent = method.desc || '';
        codeScrollEl.innerHTML = method.code.map((line, idx) => {{
          const lineNum = idx + 1;
          return `
            <div class="pt-code-line" data-line="${{lineNum}}">
              <span class="pt-code-num">${{lineNum}}</span>
              <span class="pt-code-text">${{highlightPythonCode(line)}}</span>
            </div>
          `;
        }}).join('');
      }}

      // Render Presets
      function renderPresets() {{
        presetsRow.innerHTML = '';
        if (!config.presets) return;

        config.presets.forEach((p) => {{
          const isSel = JSON.stringify(p.val) === JSON.stringify(currentArr) && (p.target === undefined || p.target === targetVal);
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = `px-2.5 py-0.5 rounded text-xs font-semibold border transition-all ${{
            isSel
              ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 shadow-xs'
              : 'border-slate-800 bg-slate-950/60 text-slate-400 hover:text-white hover:border-slate-700'
          }}`;
          btn.textContent = (isSel ? '✓ ' : '') + p.label;
          btn.onclick = () => {{
            stopPlay();
            currentArr = [...p.val];
            if (p.target !== undefined) targetVal = p.target;
            if (p.k !== undefined) kVal = p.k;
            computeSteps();
            stepIdx = 0;
            slider.max = Math.max(0, steps.length - 1);
            renderPresets();
            updateValuesBar();
            renderStep();
          }};
          presetsRow.appendChild(btn);
        }});

        // Custom Button
        const btnCustom = document.createElement('button');
        btnCustom.type = 'button';
        btnCustom.className = 'px-2 py-0.5 rounded text-xs font-semibold border border-dashed border-slate-700 text-slate-400 hover:text-white hover:border-slate-500 flex items-center gap-1';
        btnCustom.innerHTML = '<span>✎</span> Custom';
        btnCustom.onclick = () => {{
          customForm.classList.toggle('hidden');
          if (!customForm.classList.contains('hidden')) {{
            customArrInput.value = currentArr.join(', ');
            customTargetInput.value = targetVal !== undefined ? targetVal : 6;
            customArrInput.focus();
          }}
        }};
        presetsRow.appendChild(btnCustom);
      }}

      // Custom Form Handlers
      btnApplyCustom.onclick = () => {{
        const raw = customArrInput.value.trim();
        const parsed = raw.split(/[\\s,]+/).map(x => parseInt(x)).filter(x => !isNaN(x));
        if (parsed.length) {{
          stopPlay();
          currentArr = parsed;
          if (customTargetInput.value !== '') {{
            targetVal = parseInt(customTargetInput.value) || 0;
          }}
          customForm.classList.add('hidden');
          computeSteps();
          stepIdx = 0;
          slider.max = Math.max(0, steps.length - 1);
          renderPresets();
          updateValuesBar();
          renderStep();
        }}
      }};

      btnCancelCustom.onclick = () => {{
        customForm.classList.add('hidden');
      }};

      function updateValuesBar() {{
        let txt = `values = [${{currentArr.join(', ')}}]`;
        if (targetVal !== undefined && (algo === 'remove_elements' || algo === 'binary_search')) {{
          txt += `, val = ${{targetVal}}`;
        }}
        if (kVal !== undefined && algo === 'reverse_first_k') {{
          txt += `, k = ${{kVal}}`;
        }}
        valuesDisplayEl.textContent = txt;
      }}

      // Playback Controls
      function stopPlay() {{
        if (playInterval) {{
          clearInterval(playInterval);
          playInterval = null;
          btnPlay.innerHTML = '▶ Play';
        }}
      }}

      function startPlay() {{
        stopPlay();
        btnPlay.innerHTML = '⏸ Pause';
        const delay = Math.max(350, Math.round(1100 / currentSpeed));
        playInterval = setInterval(() => {{
          if (stepIdx < steps.length - 1) {{
            stepIdx += 1;
            renderStep();
          }} else {{
            stopPlay();
          }}
        }}, delay);
      }}

      function togglePlay() {{
        if (playInterval) {{
          stopPlay();
        }} else {{
          if (stepIdx >= steps.length - 1) stepIdx = 0;
          startPlay();
        }}
      }}

      // Render Active Step
      function renderStep() {{
        const step = steps[stepIdx] || steps[0];
        stepCounter.textContent = `Step ${{stepIdx + 1}} / ${{steps.length}}`;
        slider.value = stepIdx;
        btnPrev.disabled = (stepIdx === 0);
        btnNext.disabled = (stepIdx === steps.length - 1);
        btnPrev.style.opacity = (stepIdx === 0) ? '0.4' : '1';
        btnNext.style.opacity = (stepIdx === steps.length - 1) ? '0.4' : '1';

        // Synchronize Active Line in Code Panel
        codeScrollEl.querySelectorAll('.pt-code-line').forEach(el => {{
          const lineNum = parseInt(el.getAttribute('data-line'));
          if (lineNum === step.line) {{
            el.classList.add('active');
            el.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
          }} else {{
            el.classList.remove('active');
          }}
        }});

        // Render Stage
        if (step.type === 'linked_list') {{
          const nodes = step.nodes || [];
          let html = `<div class="flex flex-col items-center justify-center w-full py-2">`;
          html += `<div class="flex items-center justify-center flex-wrap gap-1 sm:gap-2 max-w-full">`;

          nodes.forEach((n, idx) => {{
            // Top pointer badge
            let topPillHtml = '';
            if (n.topPtrs && n.topPtrs.length) {{
              const pType = n.topPtrs[0].toLowerCase();
              let badgeCls = 'pt-badge-head';
              if (pType.includes('next')) badgeCls = 'pt-badge-next';
              else if (pType.includes('return') || pType.includes('new_head')) badgeCls = 'pt-badge-prev';
              topPillHtml = `
                <div class="flex flex-col items-center">
                  <span class="${{badgeCls}}">${{n.topPtrs.join(', ')}}</span>
                  <span class="text-[10px] leading-none text-slate-400 font-bold">↓</span>
                </div>
              `;
            }}

            // Bottom pointer badge
            let botPillHtml = '';
            if (n.bottomPtrs && n.bottomPtrs.length) {{
              const pType = n.bottomPtrs[0].toLowerCase();
              let badgeCls = 'pt-badge-curr';
              if (pType.includes('prev')) badgeCls = 'pt-badge-prev';
              else if (pType.includes('dummy')) badgeCls = 'pt-badge-dummy';
              else if (pType.includes('curnext') || pType.includes('next')) badgeCls = 'pt-badge-curnext';
              botPillHtml = `
                <div class="flex flex-col items-center">
                  <span class="text-[10px] leading-none text-slate-400 font-bold">↑</span>
                  <span class="${{badgeCls}}">${{n.bottomPtrs.join(', ')}}</span>
                </div>
              `;
            }}

            // Node Circle Classes
            let nodeCls = 'pt-circle-node';
            if (n.isDummy) nodeCls += ' dummy-node';
            else if (n.isMatch) nodeCls += ' match-delete';
            else if (n.isActive) nodeCls += ' active';
            else if (n.isBypassed) nodeCls += ' bypassed-node';

            // Arrow
            let arrowSymbol = '──►';
            let arrowCls = 'text-slate-500 font-mono text-sm sm:text-base font-bold select-none px-1';
            if (n.arrow === 'left') {{
              arrowSymbol = '◄──';
              arrowCls = 'text-emerald-400 font-mono text-sm sm:text-base font-bold select-none px-1 animate-pulse';
            }} else if (n.arrow === 'null' || idx === nodes.length - 1) {{
              arrowSymbol = '──►';
            }}

            html += `
              <div class="flex items-center">
                <div class="flex flex-col items-center flex-shrink-0">
                  <div class="h-7 flex items-end justify-center mb-1">${{topPillHtml}}</div>
                  <div class="${{nodeCls}}">
                    <span>${{n.val}}</span>
                  </div>
                  <div class="h-7 flex items-start justify-center mt-1">${{botPillHtml}}</div>
                </div>
                ${{n.arrow !== 'none' ? `<span class="${{arrowCls}}">${{arrowSymbol}}</span>` : ''}}
              </div>
            `;
          }});

          // Null terminator
          html += `
            <div class="flex flex-col items-center flex-shrink-0">
              <div class="h-7"></div>
              <div class="px-2.5 py-1.5 rounded-lg border ui-border bg-slate-900 text-slate-400 font-mono text-xs font-semibold">null</div>
              <div class="h-7"></div>
            </div>
          `;

          html += `</div>`;

          // Bypassed Node Chip if applicable
          if (step.bypassed) {{
            html += `
              <div class="mt-3 flex items-center gap-2 px-3 py-1.5 rounded-lg bg-rose-950/40 border border-rose-500/30 text-rose-300 text-xs font-mono">
                <span>🗑️ Bypassed / Snipped:</span>
                <span class="line-through px-2 py-0.5 rounded-full bg-rose-900/60 border border-rose-500 font-bold text-white">Node ${{step.bypassed.val}}</span>
                <span class="text-slate-400 text-[11px] font-sans">Disconnected from chain</span>
              </div>
            `;
          }}

          html += `</div>`;
          stageEl.innerHTML = html;
        }} else {{
          // Array Stage
          const arr = step.array || [];
          const active = step.active || [];
          const swapped = step.swapped || [];
          const sorted = step.sorted || [];
          const dimmed = step.dimmed || [];
          const ptrs = step.pointers || {{}};

          let html = `
            <div class="flex flex-col items-center justify-center gap-1 overflow-x-auto py-1 max-w-full">
              <!-- Pointers Row -->
              <div class="flex items-center gap-2 mb-1 min-h-[22px]">
                ${{arr.map((_, i) => {{
                  const activePtrs = Object.entries(ptrs).filter(([_, v]) => v === i).map(([k]) => k);
                  return `<div class="w-11 sm:w-13 h-5 flex items-center justify-center">
                    ${{activePtrs.length ? `<span class="pt-ptr-pill">${{activePtrs.join(', ')}} ↓</span>` : ''}}
                  </div>`;
                }}).join('')}}
              </div>

              <!-- Cells Row -->
              <div class="flex items-center gap-2">
                ${{arr.map((val, i) => {{
                  const isAct = active.includes(i);
                  const isSwap = swapped.includes(i);
                  const isSort = sorted.includes(i);
                  const isDim = dimmed.includes(i);

                  let cls = 'pt-cell w-11 sm:w-13 h-13 sm:h-15 text-base sm:text-lg ';
                  if (isDim) cls += 'pt-cell-dimmed ';
                  else if (isSwap) cls += 'pt-cell-swapped ';
                  else if (isAct) cls += 'pt-cell-active ';
                  else if (isSort) cls += 'pt-cell-sorted ';

                  return `
                    <div class="${{cls}}">
                      <span>${{val}}</span>
                      ${{isSort ? '<span class="absolute top-1 right-1 text-[9px] text-emerald-500 font-bold">✓</span>' : ''}}
                    </div>
                  `;
                }}).join('')}}
              </div>

              <!-- Indices Row -->
              <div class="flex items-center gap-2 mt-1">
                ${{arr.map((_, i) => `<div class="w-11 sm:w-13 text-center text-[10px] font-mono ui-text-muted">${{i}}</div>`).join('')}}
              </div>
            </div>
          `;
          stageEl.innerHTML = html;
        }}

        // Render Description Banner
        let badgeColorClass = 'bg-amber-500/15 text-amber-500 border border-amber-500/30';
        if (step.badgeColor === 'emerald') badgeColorClass = 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30';
        else if (step.badgeColor === 'rose') badgeColorClass = 'bg-rose-500/15 text-rose-400 border border-rose-500/30';
        else if (step.badgeColor === 'blue') badgeColorClass = 'bg-sky-500/15 text-sky-400 border border-sky-500/30';

        descBox.innerHTML = `
          <div class="flex items-start gap-3">
            <div class="w-1.5 self-stretch bg-emerald-400 rounded-full flex-shrink-0"></div>
            <div class="flex-1 space-y-1">
              <div class="flex items-center justify-between gap-2 flex-wrap">
                <span class="text-xs font-bold uppercase tracking-wider text-emerald-400 font-mono">${{step.tag || 'Step ' + (stepIdx + 1)}}</span>
                <span class="text-[11px] px-2 py-0.5 rounded font-mono font-semibold ${{badgeColorClass}}">${{step.badge || 'Action'}}</span>
              </div>
              <p class="text-xs sm:text-sm text-slate-200 leading-relaxed font-sans">${{step.desc || ''}}</p>
            </div>
          </div>
        `;
      }}

      // Button Handlers
      btnPrev.onclick = () => {{
        stopPlay();
        if (stepIdx > 0) {{
          stepIdx -= 1;
          renderStep();
        }}
      }};

      btnNext.onclick = () => {{
        stopPlay();
        if (stepIdx < steps.length - 1) {{
          stepIdx += 1;
          renderStep();
        }}
      }};

      btnReset.onclick = () => {{
        stopPlay();
        stepIdx = 0;
        renderStep();
      }};

      btnPlay.onclick = () => {{
        togglePlay();
      }};

      slider.oninput = (e) => {{
        stopPlay();
        stepIdx = parseInt(e.target.value);
        renderStep();
      }};

      // Initial Mount
      renderMethods();
      renderCode();
      renderPresets();
      updateValuesBar();
      renderStep();

      return widget;
    }}

        function jumpToPlaythrough() {{
      let widget = document.querySelector('#rendered-content .playthrough-widget');
      if (!widget) {{
        const spec = CONCEPT_PLAYTHROUGHS[currentDocPath];
        if (spec) {{
          widget = createPlaythroughWidget(spec);
          const contentEl = document.getElementById('rendered-content');
          contentEl.insertBefore(widget, contentEl.firstChild);
        }}
      }}
      if (widget) {{
        widget.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        widget.classList.add('ring-2', 'ring-[var(--accent)]');
        setTimeout(() => widget.classList.remove('ring-2', 'ring-[var(--accent)]'), 1200);
      }}
    }}


    // Keyboard navigation for active Playthrough
    window.addEventListener('keydown', (e) => {{
      const tag = document.activeElement ? document.activeElement.tagName : '';
      if (tag === 'INPUT' || tag === 'TEXTAREA' || document.activeElement?.isContentEditable) return;

      const widget = document.querySelector('#rendered-content .playthrough-widget');
      if (!widget) return;

      if (e.key === 'ArrowLeft') {{
        const btnPrev = widget.querySelector('.btn-pt-prev');
        if (btnPrev && !btnPrev.disabled) {{
          e.preventDefault();
          btnPrev.click();
        }}
      }} else if (e.key === 'ArrowRight') {{
        const btnNext = widget.querySelector('.btn-pt-next');
        if (btnNext && !btnNext.disabled) {{
          e.preventDefault();
          btnNext.click();
        }}
      }} else if (e.key === ' ' && !e.repeat) {{
        const btnPlay = widget.querySelector('.btn-pt-play');
        if (btnPlay) {{
          e.preventDefault();
          btnPlay.click();
        }}
      }}
    }});


    // 6. Markdown + KaTeX + Mermaid Pipeline
    function renderMarkdownInto(containerEl, markdownText, basePath) {{
      if (typeof marked !== 'undefined') {{
        containerEl.innerHTML = marked.parse(markdownText, {{ breaks: true, gfm: true }});
      }} else {{
        containerEl.innerHTML = '<pre><code>' + markdownText + '</code></pre>';
      }}

      // Mount interactive playthrough widgets from ```playthrough blocks
      containerEl.querySelectorAll('pre code.language-playthrough').forEach((codeEl) => {{
        const pre = codeEl.parentElement;
        const text = codeEl.textContent.trim();
        let spec = {{}};
        try {{
          spec = JSON.parse(text);
        }} catch (e) {{
          spec = {{ algorithm: text || 'bubble_sort' }};
        }}
        const widget = createPlaythroughWidget(spec);
        pre.replaceWith(widget);
      }});

      containerEl.querySelectorAll('pre code.language-mermaid').forEach((codeEl) => {{
        const pre = codeEl.parentElement;
        const graphDef = codeEl.textContent;
        const fig = document.createElement('figure');
        fig.className = 'mermaid-figure my-4 ui-surface border rounded-xl p-4 overflow-x-auto';
        fig.innerHTML = `
          <figcaption class="flex items-center justify-between text-xs ui-text-muted mb-2 pb-1.5 border-b ui-border">
            <span class="font-semibold ui-accent-text flex items-center gap-1.5">📊 Decision Flowchart</span>
            <span>Follow arrows step-by-step</span>
          </figcaption>
          <div class="mermaid-render flex justify-center py-1" data-graph="${{encodeURIComponent(graphDef)}}"></div>
        `;
        pre.replaceWith(fig);
      }});

      containerEl.querySelectorAll('pre').forEach(pre => {{
        pre.setAttribute('tabindex', '0');
        if (typeof hljs !== 'undefined') {{
          const code = pre.querySelector('code');
          if (code) hljs.highlightElement(code);
        }}
      }});

      if (typeof renderMathInElement !== 'undefined') {{
        try {{
          renderMathInElement(containerEl, {{
            delimiters: [
              {{ left: '$$', right: '$$', display: true }},
              {{ left: '$', right: '$', display: false }},
              {{ left: '\\\\(', right: '\\\\)', display: false }},
              {{ left: '\\\\[', right: '\\\\]', display: true }}
            ],
            throwOnError: false
          }});
        }} catch (e) {{}}
      }}

      renderMermaidDiagrams(containerEl);

      containerEl.querySelectorAll('a').forEach(anchor => {{
        const href = anchor.getAttribute('href');
        if (href && (href.endsWith('.md') || href.includes('.md#'))) {{
          anchor.addEventListener('click', (e) => {{
            e.preventDefault();
            const cleanHref = href.split('#')[0];
            let currentDir = basePath.includes('/') ? basePath.substring(0, basePath.lastIndexOf('/')) : '';
            let resolved = cleanHref.replace(/^(\\.\\/)/, '');
            if (cleanHref.startsWith('../')) {{
              resolved = cleanHref.replace(/^(\\.\\.\\/)+/, '');
            }} else if (currentDir && !cleanHref.startsWith('/')) {{
              resolved = currentDir + '/' + resolved;
            }}
            document.getElementById('peek-dialog').close();
            openDocInReader(resolved);
          }});
        }}
      }});
    }}

    async function renderMermaidDiagrams(containerEl) {{
      if (typeof mermaid === 'undefined' || !containerEl) return;
      const nodes = containerEl.querySelectorAll('.mermaid-render');
      for (let i = 0; i < nodes.length; i++) {{
        const el = nodes[i];
        const rawGraph = decodeURIComponent(el.dataset.graph || '');
        if (!rawGraph.trim()) continue;
        try {{
          const id = 'mmd-' + Date.now() + '-' + Math.random().toString(36).substring(2, 7);
          const {{ svg }} = await mermaid.render(id, rawGraph);
          el.innerHTML = svg;
        }} catch (err) {{
          el.innerHTML = `<pre class="text-xs p-2 rounded ui-card border"><code>${{rawGraph}}</code></pre>`;
        }}
      }}
    }}

    // 7. Render Active Document in Reader
    function resolveDocKey(docPath) {{
      if (!docPath) return "00_foundations/01_algorithms_correctness_efficiency.md";
      const clean = docPath.replace(/^(\\.\\/|\\/)/, '');
      if (DOCS_DATA[clean]) return clean;
      const match = DOC_KEYS.find(k => k.endsWith(clean) || clean.endsWith(k));
      return match || "00_foundations/01_algorithms_correctness_efficiency.md";
    }}

    function getFilteredSidebarDocs() {{
      return DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => {{
        if (sidebarScope === 'concept') return d.docType === 'concept';
        if (sidebarScope === 'problem') return d.docType === 'problem';
        return true;
      }});
    }}

    function renderDoc(docPath) {{
      const targetKey = resolveDocKey(docPath);
      currentDocPath = targetKey;
      const doc = DOCS_DATA[targetKey];
      if (!doc) return;

      const url = new URL(window.location);
      url.searchParams.set('doc', targetKey);
      window.history.replaceState({{}}, '', url);

      document.title = `${{doc.title}} | DSA Study Hub`;
      document.getElementById('doc-type-badge').textContent = doc.docType === 'problem' ? '🧩 LeetCode Walkthrough' : (doc.docType === 'cheat_sheet' ? '⚡ Cheat Sheet' : '📘 Concept Guide');
      document.getElementById('doc-cat-badge').textContent = `${{doc.categoryIcon}} ${{doc.categoryLabel}}`;

      const diffBadge = document.getElementById('doc-diff-badge');
      diffBadge.textContent = doc.difficulty;
      if (doc.difficulty === 'Easy') {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-sky-500/15 text-sky-400 border border-sky-500/30';
      }} else if (doc.difficulty === 'Medium') {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30';
      }} else if (doc.difficulty === 'Hard') {{
        diffBadge.className = 'text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30';
      }} else {{
        diffBadge.className = 'hidden';
      }}

      const lcLink = document.getElementById('doc-lc-link');
      if (doc.lcUrl) {{
        lcLink.href = doc.lcUrl;
        lcLink.classList.remove('hidden');
      }} else {{
        lcLink.classList.add('hidden');
      }}

      updateReaderStatusButtons();

      const contentEl = document.getElementById('rendered-content');
      renderMarkdownInto(contentEl, doc.content, targetKey);
      buildTableOfContents(contentEl);

      const noteInput = document.getElementById('doc-personal-note');
      noteInput.value = docNotesMap[targetKey] || doc.summary || '';

      const scopedList = getFilteredSidebarDocs();
      const curIdx = scopedList.findIndex(d => d.path === targetKey);
      const prevDoc = curIdx > 0 ? scopedList[curIdx - 1] : scopedList[scopedList.length - 1] || doc;
      const nextDoc = curIdx >= 0 && curIdx < scopedList.length - 1 ? scopedList[curIdx + 1] : scopedList[0] || doc;

      document.getElementById('prev-doc-title').textContent = prevDoc.title;
      document.getElementById('prev-doc-btn').onclick = () => renderDoc(prevDoc.path);
      document.getElementById('next-doc-title').textContent = nextDoc.title;
      document.getElementById('next-doc-btn').onclick = () => renderDoc(nextDoc.path);

      document.querySelectorAll('.sidebar-doc-link').forEach(el => {{
        if (el.dataset.path === targetKey) {{
          el.className = 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs font-semibold ui-accent-soft border';
        }} else {{
          el.className = 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs ui-text-muted hover:text-[var(--text)] hover:bg-[var(--surface-hover)] transition-colors';
        }}
      }});

      document.getElementById('reader-scroll-container').scrollTo(0, 0);
    }}

    function buildTableOfContents(contentEl) {{
      const tocList = document.getElementById('toc-list');
      tocList.innerHTML = '';
      const headings = contentEl.querySelectorAll('h2, h3');
      headings.forEach((h, i) => {{
        const id = 'sec-' + i;
        h.id = id;
        const a = document.createElement('a');
        a.href = '#' + id;
        a.textContent = h.textContent;
        a.className = h.tagName === 'H3'
          ? 'block pl-3 py-1 ui-text-muted hover:text-[var(--accent-text)] truncate transition-colors'
          : 'block py-1 font-medium ui-text-muted hover:text-[var(--accent-text)] truncate transition-colors';
        a.addEventListener('click', (e) => {{
          e.preventDefault();
          h.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }});
        tocList.appendChild(a);
      }});
    }}

    function setReaderMode(mode) {{
      readerMode = mode;
      const contentEl = document.getElementById('rendered-content');
      const btnFull = document.getElementById('mode-btn-full');
      const btnVis = document.getElementById('mode-btn-visual');

      if (mode === 'visual') {{
        contentEl.classList.add('visual-focus-mode');
        btnVis.className = 'px-2.5 py-1 rounded font-semibold ui-accent-soft border';
        btnFull.className = 'px-2.5 py-1 rounded font-medium ui-text-muted';
      }} else {{
        contentEl.classList.remove('visual-focus-mode');
        btnFull.className = 'px-2.5 py-1 rounded font-semibold ui-accent-soft border';
        btnVis.className = 'px-2.5 py-1 rounded font-medium ui-text-muted';
      }}
    }}

    function toggleFlowcharts() {{
      showFlowcharts = !showFlowcharts;
      const contentEl = document.getElementById('rendered-content');
      const btn = document.getElementById('btn-toggle-flowcharts');
      if (showFlowcharts) {{
        contentEl.classList.remove('hide-flowcharts-mode');
        btn.textContent = '📊 Flowcharts: ON';
        btn.className = 'px-2.5 py-1 rounded-lg border ui-accent-soft text-xs font-semibold';
      }} else {{
        contentEl.classList.add('hide-flowcharts-mode');
        btn.textContent = '📊 Flowcharts: OFF';
        btn.className = 'px-2.5 py-1 rounded-lg border ui-surface text-xs font-medium ui-text-muted';
      }}
    }}

    function updateReaderStatusButtons() {{
      const st = getDocStatus(currentDocPath);
      const map = {{
        todo: document.getElementById('status-btn-todo'),
        review: document.getElementById('status-btn-review'),
        solved: document.getElementById('status-btn-solved')
      }};
      Object.keys(map).forEach(k => {{
        if (k === st) {{
          const activeColor = k === 'solved' ? 'ui-accent-soft border' : (k === 'review' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'ui-card text-[var(--text)] border');
          map[k].className = `px-2 py-1 rounded font-semibold ${{activeColor}}`;
        }} else {{
          map[k].className = 'px-2 py-1 rounded font-medium ui-text-muted hover:opacity-100';
        }}
      }});
    }}

    function setCurrentDocStatus(status) {{
      setDocStatus(currentDocPath, status);
    }}

    function renderSidebarTree() {{
      const container = document.getElementById('sidebar-tree');
      const q = (document.getElementById('sidebar-filter-input')?.value || '').toLowerCase().trim();
      container.innerHTML = '';

      const scopedDocs = getFilteredSidebarDocs().filter(d => {{
        if (!q) return true;
        return d.title.toLowerCase().includes(q) || d.pattern.toLowerCase().includes(q) || d.path.toLowerCase().includes(q);
      }});

      const scopeLabel = sidebarScope === 'concept' ? 'Concept Guides' : (sidebarScope === 'problem' ? 'Repo Problem Guides' : 'Total Docs');
      document.getElementById('sidebar-count-label').textContent = `${{scopedDocs.length}} ${{scopeLabel}}`;

      const groups = {{}};
      scopedDocs.forEach(d => {{
        if (!groups[d.category]) groups[d.category] = [];
        groups[d.category].push(d);
      }});

      Object.keys(groups).forEach(cat => {{
        const items = groups[cat];
        const first = items[0];
        const doneCount = items.filter(i => getDocStatus(i.path) === 'solved').length;

        const details = document.createElement('details');
        details.open = true;
        details.className = 'group';

        const summary = document.createElement('summary');
        summary.className = 'flex items-center justify-between px-2 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider ui-text-muted hover:text-[var(--text)] cursor-pointer select-none';
        summary.innerHTML = `
          <span>${{first.categoryIcon}} ${{first.categoryLabel}}</span>
          <span class="font-mono text-xs px-1.5 py-0.5 rounded ui-card border">${{doneCount}}/${{items.length}}</span>
        `;
        details.appendChild(summary);

        const listDiv = document.createElement('div');
        listDiv.className = 'mt-1 space-y-0.5 pl-1';

        items.forEach(item => {{
          const a = document.createElement('a');
          a.href = `?doc=${{encodeURIComponent(item.path)}}`;
          a.dataset.path = item.path;
          const isCurrent = item.path === currentDocPath;
          a.className = isCurrent
            ? 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs font-semibold ui-accent-soft border'
            : 'sidebar-doc-link flex items-center justify-between gap-2 px-2.5 py-1.5 rounded-lg text-xs ui-text-muted hover:text-[var(--text)] hover:bg-[var(--surface-hover)] transition-colors';

          const st = getDocStatus(item.path);
          const statusIcon = st === 'solved'
            ? '<span class="ui-accent-text font-bold shrink-0">✓</span>'
            : (st === 'review' ? '<span class="text-amber-400 shrink-0">🔁</span>' : '');

          const shortLabel = item.lcNumber
            ? `<span class="truncate"><span class="font-mono opacity-60 mr-1.5">#${{item.lcNumber}}</span>${{item.shortTitle}}</span>`
            : `<span class="truncate">${{item.shortTitle}}</span>`;

          a.innerHTML = `${{shortLabel}}${{statusIcon}}`;
          a.addEventListener('click', (e) => {{
            e.preventDefault();
            renderDoc(item.path);
          }});
          listDiv.appendChild(a);
        }});

        details.appendChild(listDiv);
        container.appendChild(details);
      }});
    }}

    function renderCheatSheetsGrid() {{
      const grid = document.getElementById('cheatsheets-grid');
      const q = (document.getElementById('cs-search-input')?.value || '').toLowerCase().trim();
      const sheets = DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => d.category === 'cheat_sheets' || d.path === 'dsa_patterns_study_guide.md');

      const filtered = sheets.filter(d => !q || d.title.toLowerCase().includes(q) || d.summary.toLowerCase().includes(q));
      grid.innerHTML = filtered.map(d => `
        <div class="ui-card border rounded-2xl p-4 flex flex-col justify-between gap-3 hover:border-[var(--accent)] transition-all">
          <div class="space-y-2">
            <div class="flex items-center justify-between gap-2">
              <span class="text-xs font-mono px-2 py-0.5 rounded ui-surface border ui-accent-text">${{d.categoryIcon}} ${{d.categoryLabel}}</span>
              ${{d.hasMermaid ? '<span class="text-xs px-2 py-0.5 rounded ui-accent-soft border">📊 Flowchart</span>' : ''}}
            </div>
            <h2 class="text-base font-bold">${{d.title}}</h2>
            <p class="text-xs ui-text-muted leading-relaxed">${{d.summary || 'Complete pattern triggers, visual arrows, and Python templates.'}}</p>
          </div>
          <div class="pt-3 border-t ui-border flex items-center justify-between">
            <button type="button" onclick="openPeekDialog('${{d.path}}')" class="text-xs ui-text-muted hover:text-[var(--text)]">Quick Peek</button>
            <button type="button" onclick="openDocInReader('${{d.path}}')" class="px-3 py-1.5 rounded-lg ui-accent-soft border text-xs font-semibold hover:opacity-90 transition-all">
              Open Sheet →
            </button>
          </div>
        </div>
      `).join('');
    }}

    // 8. Top Interview 150 & LeetCode 75 Tracker Logic
    function setTrackerPlanFilter(plan) {{
      trackerPlanFilter = plan;
      document.querySelectorAll('.trk-plan-btn').forEach(btn => {{
        if (btn.dataset.plan === plan) {{
          btn.className = 'trk-plan-btn px-3 py-1.5 rounded-xl font-semibold ui-accent-btn';
        }} else {{
          btn.className = 'trk-plan-btn px-3 py-1.5 rounded-xl font-medium ui-surface border ui-text-muted hover:text-[var(--text)]';
        }}
      }});
      renderTrackerTable();
    }}

    function setTrackerStatusFilter(st) {{
      trackerStatusFilter = st;
      document.querySelectorAll('.tracker-status-btn').forEach(btn => {{
        if (btn.dataset.status === st) {{
          btn.className = 'tracker-status-btn px-2.5 py-1 rounded-lg font-semibold ui-accent-soft border';
        }} else {{
          btn.className = 'tracker-status-btn px-2.5 py-1 rounded-lg font-medium ui-text-muted';
        }}
      }});
      renderTrackerTable();
    }}

    function cycleProbStatus(num) {{
      const cur = getProbStatus(num);
      const next = cur === 'todo' ? 'solved' : (cur === 'solved' ? 'review' : 'todo');
      setProbStatus(num, next);
    }}

    function renderTrackerTable() {{
      const tbody = document.getElementById('tracker-tbody');
      const q = (document.getElementById('tracker-search-input')?.value || '').toLowerCase().trim();
      const topicFilter = document.getElementById('tracker-topic-filter')?.value || 'ALL';
      const diffFilter = document.getElementById('tracker-diff-filter')?.value || 'ALL';

      // Top Progress Cards (Top 150 & LC 75)
      const list150 = CURATED_CATALOG.filter(p => p.in150);
      const solved150 = list150.filter(p => getProbStatus(p.number) === 'solved').length;
      const pct150 = Math.round((solved150 / list150.length) * 100);
      document.getElementById('stat-150-count').textContent = `${{solved150}} / ${{list150.length}}`;
      document.getElementById('stat-150-pct').textContent = `${{pct150}}%`;
      document.getElementById('stat-150-bar').style.width = `${{pct150}}%`;

      const list75 = CURATED_CATALOG.filter(p => p.in75);
      const solved75 = list75.filter(p => getProbStatus(p.number) === 'solved').length;
      const pct75 = Math.round((solved75 / list75.length) * 100);
      document.getElementById('stat-75-count').textContent = `${{solved75}} / ${{list75.length}}`;
      document.getElementById('stat-75-pct').textContent = `${{pct75}}%`;
      document.getElementById('stat-75-bar').style.width = `${{pct75}}%`;

      const allSolved = CURATED_CATALOG.filter(p => getProbStatus(p.number) === 'solved');
      const allReview = CURATED_CATALOG.filter(p => getProbStatus(p.number) === 'review');
      const easySolved = allSolved.filter(p => p.difficulty === 'Easy').length;
      const medSolved = allSolved.filter(p => p.difficulty === 'Medium').length;
      const hardSolved = allSolved.filter(p => p.difficulty === 'Hard').length;

      document.getElementById('stat-total-solved').textContent = `${{allSolved.length}} / ${{CURATED_CATALOG.length}}`;
      document.getElementById('stat-easy').textContent = `${{easySolved}} E`;
      document.getElementById('stat-medium').textContent = `${{medSolved}} M`;
      document.getElementById('stat-hard').textContent = `${{hardSolved}} H`;
      document.getElementById('stat-review-label').textContent = `${{allReview.length}} problems in review queue`;

      // Filter rows
      const rows = CURATED_CATALOG.filter(p => {{
        if (trackerPlanFilter === '150' && !p.in150) return false;
        if (trackerPlanFilter === '75' && !p.in75) return false;
        if (trackerPlanFilter === 'WITH_DOC' && !p.docPath) return false;
        if (topicFilter !== 'ALL' && p.topic !== topicFilter) return false;
        if (diffFilter !== 'ALL' && p.difficulty !== diffFilter) return false;
        const st = getProbStatus(p.number);
        if (trackerStatusFilter !== 'ALL' && st !== trackerStatusFilter) return false;
        if (q) {{
          const note = (p.docPath && docNotesMap[p.docPath]) || docNotesMap['lc-' + p.number] || p.summary || '';
          return p.title.toLowerCase().includes(q) ||
                 p.topic.toLowerCase().includes(q) ||
                 p.pattern.toLowerCase().includes(q) ||
                 p.number.toString().includes(q) ||
                 note.toLowerCase().includes(q);
        }}
        return true;
      }});

      document.getElementById('tracker-showing-count').textContent = `Showing ${{rows.length}} problems`;

      tbody.innerHTML = rows.map(p => {{
        const st = getProbStatus(p.number);
        const stBadge = st === 'solved'
          ? '<span class="px-2.5 py-1 rounded-lg font-semibold ui-accent-soft border">✓ Solved</span>'
          : (st === 'review'
            ? '<span class="px-2.5 py-1 rounded-lg font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30">🔁 Review</span>'
            : '<span class="px-2.5 py-1 rounded-lg font-medium ui-surface border ui-text-muted">○ Todo</span>');

        const diffColor = p.difficulty === 'Easy' ? 'text-sky-400' : (p.difficulty === 'Medium' ? 'text-amber-400' : 'text-rose-400');
        const noteText = (p.docPath && docNotesMap[p.docPath]) || docNotesMap['lc-' + p.number] || p.summary || 'Click Study or LeetCode ↗ to solve';

        const planBadges = [
          p.in150 ? '<span class="px-1.5 py-0.5 rounded text-xs ui-accent-soft border">🔥 150</span>' : '',
          p.in75 ? '<span class="px-1.5 py-0.5 rounded text-xs bg-sky-500/15 text-sky-400 border border-sky-500/30">⚡ 75</span>' : '',
        ].filter(Boolean).join(' ');

        return `
          <tr class="hover:bg-[var(--surface-hover)] transition-colors">
            <td class="py-3 px-3 whitespace-nowrap">
              <button type="button" onclick="cycleProbStatus(${{p.number}})" title="Click to cycle Todo -> Solved -> Review">
                ${{stBadge}}
              </button>
            </td>
            <td class="py-3 px-3">
              <div class="font-semibold text-sm flex items-center gap-2">
                <span class="font-mono text-xs px-1.5 py-0.5 rounded ui-surface border ui-accent-text">#${{p.number}}</span>
                ${{p.docPath
                  ? `<button type="button" onclick="openPeekDialog('${{p.docPath}}')" class="text-left hover:underline transition-colors">${{p.title}}</button>`
                  : `<a href="${{p.url}}" target="_blank" rel="noopener noreferrer" class="hover:underline transition-colors">${{p.title}}</a>`
                }}
              </div>
              <div class="text-xs ${{diffColor}} mt-0.5">${{p.difficulty}} ${{p.docPath ? '• 📖 Has Visual Study Note' : ''}}</div>
            </td>
            <td class="py-3 px-3 hidden sm:table-cell">
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="px-2 py-0.5 rounded ui-surface border text-xs">${{p.topic}}</span>
                ${{planBadges}}
              </div>
            </td>
            <td class="py-3 px-3 hidden lg:table-cell max-w-md">
              <p class="text-xs ui-text-muted line-clamp-2">${{noteText}}</p>
            </td>
            <td class="py-3 px-3 text-right whitespace-nowrap space-x-1.5">
              <a href="${{p.url}}" target="_blank" rel="noopener noreferrer" class="inline-block px-2.5 py-1 rounded-lg ui-surface border text-xs ui-text-muted hover:text-[var(--text)]">
                LC ↗
              </a>
              ${{p.docPath ? `
                <button type="button" onclick="openPeekDialog('${{p.docPath}}')" class="px-2 py-1 rounded-lg ui-surface border text-xs hover:opacity-80">
                  Peek
                </button>
                <button type="button" onclick="openDocInReader('${{p.docPath}}')" class="px-2.5 py-1 rounded-lg ui-accent-soft border text-xs font-semibold hover:opacity-90">
                  Note →
                </button>
              ` : ''}}
            </td>
          </tr>
        `;
      }}).join('');
    }}

    function openPeekDialog(docPath) {{
      const key = resolveDocKey(docPath);
      const doc = DOCS_DATA[key];
      if (!doc) return;
      const dialog = document.getElementById('peek-dialog');
      document.getElementById('peek-title').textContent = doc.title;
      document.getElementById('peek-open-full-btn').onclick = () => {{
        dialog.close();
        openDocInReader(key);
      }};
      const bodyEl = document.getElementById('peek-body');
      dialog.showModal();
      renderMarkdownInto(bodyEl, doc.content, key);
    }}

    function selectRoadmapPhase(panelId) {{
      document.querySelectorAll('.rm-panel').forEach(panel => {{
        if (panel.id === panelId) {{
          panel.removeAttribute('hidden');
        }} else {{
          panel.setAttribute('hidden', 'until-found');
        }}
      }});
      document.querySelectorAll('.rm-tab-btn').forEach(btn => {{
        const isMatch = btn.getAttribute('aria-controls') === panelId;
        btn.setAttribute('aria-expanded', isMatch ? 'true' : 'false');
        btn.className = isMatch
          ? 'rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-accent-soft border whitespace-nowrap'
          : 'rm-tab-btn px-3.5 py-2 rounded-xl text-xs font-semibold ui-card border ui-text-muted whitespace-nowrap';
      }});
    }}

    function renderRoadmapGrids() {{
      const phaseMapping = {{
        'rm-phase-1-grid': ['00_foundations', '01_arrays_and_pointers'],
        'rm-phase-2-grid': ['02_linked_lists', '03_stacks_and_queues', '04_sorting', '05_binary_search'],
        'rm-phase-3-grid': ['cheat_sheets'],
        'rm-phase-4-grid': ['system_design']
      }};

      Object.keys(phaseMapping).forEach(gridId => {{
        const gridEl = document.getElementById(gridId);
        if (!gridEl) return;
        const cats = phaseMapping[gridId];
        const items = DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => cats.includes(d.category));
        gridEl.innerHTML = items.map(d => {{
          const st = getDocStatus(d.path);
          const isSolved = st === 'solved';
          return `
            <div class="ui-card border rounded-xl p-3 flex items-center justify-between gap-2">
              <div class="truncate">
                <button type="button" onclick="openDocInReader('${{d.path}}')" class="text-xs font-semibold hover:underline truncate block text-left">
                  ${{d.lcNumber ? '#' + d.lcNumber + ' ' + d.shortTitle : d.shortTitle}}
                </button>
                <span class="text-xs ui-text-muted">${{d.docType === 'problem' ? '🧩 Problem' : '📘 Concept'}} • ${{d.categoryLabel}}</span>
              </div>
              <button type="button" onclick="setDocStatus('${{d.path}}', '${{isSolved ? 'todo' : 'solved'}}')" class="shrink-0 text-xs px-2 py-1 rounded border ${{isSolved ? 'ui-accent-soft' : 'ui-surface ui-text-muted'}}">
                ${{isSolved ? '✓ Done' : '○ Todo'}}
              </button>
            </div>
          `;
        }}).join('');
      }});
    }}

    const cmdkDialog = document.getElementById('cmdk-dialog');
    const cmdkInput = document.getElementById('cmdk-input');
    const cmdkResults = document.getElementById('cmdk-results');

    function openCmdK() {{
      cmdkDialog.showModal();
      cmdkInput.value = '';
      renderCmdKResults('');
      cmdkInput.focus();
    }}

    function renderCmdKResults(query) {{
      const q = query.toLowerCase().trim();
      const matches = DOC_KEYS.map(k => DOCS_DATA[k]).filter(d => {{
        if (!q) return true;
        return d.title.toLowerCase().includes(q) ||
               d.pattern.toLowerCase().includes(q) ||
               d.categoryLabel.toLowerCase().includes(q) ||
               d.content.toLowerCase().includes(q);
      }}).slice(0, 25);

      cmdkResults.innerHTML = matches.map(d => `
        <button type="button" onclick="cmdkDialog.close(); openDocInReader('${{d.path}}')" class="w-full text-left px-3 py-2 rounded-xl hover:bg-[var(--surface-hover)] flex items-center justify-between gap-3 transition-colors">
          <div class="truncate">
            <div class="text-xs font-semibold">${{d.title}}</div>
            <div class="text-xs ui-text-muted truncate">${{d.categoryLabel}} • ${{d.pattern}}</div>
          </div>
          <span class="text-xs font-mono px-2 py-0.5 rounded ui-surface border shrink-0">${{d.docType === 'problem' ? '🧩 Problem' : (d.docType === 'cheat_sheet' ? '⚡ Sheet' : '📘 Concept')}}</span>
        </button>
      `).join('');
    }}

    document.getElementById('open-cmdk-btn').addEventListener('click', openCmdK);
    cmdkInput.addEventListener('input', (e) => renderCmdKResults(e.target.value));

    window.addEventListener('keydown', (e) => {{
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {{
        e.preventDefault();
        openCmdK();
      }} else if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {{
        e.preventDefault();
        openCmdK();
      }} else if ((currentView === 'concepts' || currentView === 'problems') && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {{
        if (e.key === '[') document.getElementById('prev-doc-btn').click();
        if (e.key === ']') document.getElementById('next-doc-btn').click();
        if (e.key === 'v') setReaderMode(readerMode === 'full' ? 'visual' : 'full');
        if (e.key === 'b') toggleLeftSidebar();
        if (e.key === 'o') toggleRightSidebar();
      }}
    }});

    document.getElementById('doc-personal-note').addEventListener('input', (e) => {{
      docNotesMap[currentDocPath] = e.target.value;
      localStorage.setItem(NOTES_STORAGE_KEY, JSON.stringify(docNotesMap));
      const ind = document.getElementById('note-saved-indicator');
      ind.textContent = 'Saved ✓';
      setTimeout(() => {{ ind.textContent = 'Auto-saves locally'; }}, 1200);
    }});

    document.getElementById('sidebar-filter-input').addEventListener('input', renderSidebarTree);
    document.getElementById('toggle-all-cats-btn').addEventListener('click', (e) => {{
      const detailsList = document.querySelectorAll('#sidebar-tree details');
      const anyOpen = Array.from(detailsList).some(d => d.open);
      detailsList.forEach(d => {{ d.open = !anyOpen; }});
      e.target.textContent = anyOpen ? 'Expand all' : 'Collapse all';
    }});

    document.getElementById('cs-search-input').addEventListener('input', renderCheatSheetsGrid);
    document.getElementById('tracker-search-input').addEventListener('input', renderTrackerTable);
    document.getElementById('tracker-topic-filter').addEventListener('change', renderTrackerTable);
    document.getElementById('tracker-diff-filter').addEventListener('change', renderTrackerTable);

    document.getElementById('open-log-dialog-btn').addEventListener('click', () => {{
      document.getElementById('log-dialog').showModal();
    }});
    document.getElementById('custom-problem-form').addEventListener('submit', (e) => {{
      e.preventDefault();
      const num = parseInt(document.getElementById('cp-num').value, 10);
      const title = document.getElementById('cp-title').value.trim();
      const diff = document.getElementById('cp-diff').value;
      const pattern = document.getElementById('cp-pattern').value.trim();
      const notes = document.getElementById('cp-note').value.trim();

      let existing = CURATED_CATALOG.find(p => p.number === num);
      if (!existing) {{
        CURATED_CATALOG.unshift({{
          number: num,
          title: title,
          difficulty: diff,
          topic: pattern,
          pattern: pattern,
          url: `https://leetcode.com/problemset/?search=${{num}}`,
          docPath: '',
          summary: notes,
          in150: false,
          in75: false,
          defaultSolved: true
        }});
      }}
      if (notes) {{
        docNotesMap['lc-' + num] = notes;
        localStorage.setItem(NOTES_STORAGE_KEY, JSON.stringify(docNotesMap));
      }}
      setProbStatus(num, 'solved');
      document.getElementById('custom-problem-form').reset();
      document.getElementById('log-dialog').close();
      renderTrackerTable();
    }});

    const rmAccordion = document.getElementById('roadmap-accordion');
    if (rmAccordion) {{
      rmAccordion.addEventListener('beforematch', (e) => {{
        const matchedPanel = e.target.closest('.rm-panel');
        if (matchedPanel) selectRoadmapPhase(matchedPanel.id);
      }});
    }}
    if (!('onbeforematch' in HTMLElement.prototype)) {{
      document.querySelectorAll('[hidden="until-found"]').forEach((el) => {{
        el.removeAttribute('hidden');
      }});
    }}

    // Boot Application
    initState();
    const savedTheme = localStorage.getItem(THEME_KEY) || 'dark';
    setTheme(savedTheme);
    applySidebarVisibility();
    updateGlobalProgressPill();
    updatePomodoroUI();

    const params = new URLSearchParams(window.location.search);
    const paramDoc = params.get('doc');
    const paramView = params.get('view');

    if (paramDoc) {{
      openDocInReader(paramDoc);
    }} else if (paramView && ['concepts', 'problems', 'cheatsheets', 'playground', 'tracker', 'pomodoro', 'roadmap'].includes(paramView)) {{
      renderDoc(currentDocPath);
      switchView(paramView);
    }} else {{
      renderDoc(currentDocPath);
      switchView(DEFAULT_INITIAL_VIEW);
    }}
  </script>
</body>
</html>
"""


for filename, default_view in [
    ("viewer.html", "concepts"),
    ("tracker.html", "tracker"),
    ("faang_plan.html", "roadmap"),
]:
    out_path = os.path.join(ROOT_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(build_html(default_view))
    print(f"Generated {out_path} (default_view={default_view})")
