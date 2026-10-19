# 90% of linked list questions classified into types

> **Source:** [LeetCode Discuss: 90% of the Linked List questions classified into Types](https://leetcode.com/discuss/post/2434752/90-of-the-linked-list-questions-on-linke-4xc3/)

Instead of treating every linked list question as a new puzzle, map it to one of the standard pointer patterns below.

## The 10-second classifier

```text
                               [ Linked List Problem ]
                                          │
         ┌────────────────────────────────┼────────────────────────────────┐
         ▼                                ▼                                ▼
   [ GIVEN 1 LL ]                  [ 2 OR MORE LLs ]             [ DESIGN / HYBRID ]
         │                                │                                │
   ┌─────┴──────────────────┐      ┌──────┴──────────────┐          ┌──────┴──────────────┐
   │ 1. Single-Pass / Math  │      │ • Zipper Merge      │          │ • Hash Table Augment│
   │    (Stream/Horner/Swap)│      │ • Schoolbook Carry  │          │ • DLL + HashMap     │
   │ 2. Modify (Same Count) │      │ • Intersection      │          │   (LRU / LFU Cache) │
   │    - Reversing         │      │ • Merge k-Sorted    │          │ • Merge Sort on LL  │
   │    - Reordering        │      └─────────────────────┘          │ • LL + Tree Hybrids │
   │ 3. Delete Nodes        │                                       └─────────────────────┘
   │ 4. Insert Node         │
   │ 5. Fast/Slow Pointers  │
   └────────────────────────┘
```

### Algorithm steps (decision framework):
* **1. Categorize input size:** Determine whether the problem provides a single list, two or more lists, or asks for a hybrid data structure design.
* **2. Select pattern strategy:**
  * Single list: Apply in-place reversal (3-pointer flip), fixed-gap deletion with a dummy head, or fast and slow pointers (cycle detection, midpoint).
  * Multiple lists: Apply zipper merging, schoolbook carry traversal, or length-difference alignment.
  * Design and hybrid: Combine doubly linked lists with hash maps (LRU cache) or divide-and-conquer merge sort.
* **3. Initialize pointers and sentinels:** Set up a dummy anchor (`dummy.next = head`), boundary trackers (`prev`, `cur`, `nxt`), or two-speed runners (`slow`, `fast`).
* **4. Traverse and return:** Execute the pointer loop until reaching null terminators, returning either the new head or `dummy.next`.

## 0. Linked list fundamentals

- [Guide: Linked List Fundamentals](./01_linked_list_fundamentals.md)
- [Guide: Fast & Slow Pointers (Cycles, Midpoints & Reversals)](./03_fast_and_slow_pointers_cycle_detection_midpoints.md)
- [x] [LC 707: Design Linked List [Free]](./707_design_linked_list.md)
  - **Technique:** In doubly linked lists, initialize sentinel `head` and `tail` dummy nodes (`head.next = tail`, `tail.prev = head`) so insertions and deletions never hit null-boundary edge cases.

## I. Given 1 linked list

### 1. Single-pass and simple recursion
Nodes are inspected or accumulated without changing the list's structure or node count.

- [x] [LC 1721: Swapping Nodes in a Linked List [Free]](./1721_swapping_nodes_in_a_linked_list.md)
  - **Technique:** Fixed-gap pointers. Walk `first` `k - 1` steps, then slide `fast` (from `first`) and `second` (from `head`) until `fast.next` is `None`.
- [ ] [LC 369: Plus One Linked List [Paid / Premium]](https://leetcode.com/problems/plus-one-linked-list/) (Array cousin: [LC 66](../01_arrays_and_pointers/66_plus_one.md))
  - **Technique:** Post-order recursion bubbles the carry backward from the tail (`carry = add_carry(node.next)`).
- [x] [LC 1290: Convert Binary Number in a Linked List to Integer [Free]](./1290_convert_binary_number_in_a_linked_list_to_integer.md)
  - **Technique:** Horner's rule stream accumulator: `ans = (ans << 1) | head.val` in $\mathcal{O}(1)$ space.

### 2. Modifying the list (node count stays the same)

#### A. Reversing a linked list
Flips pointer directions in-place in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.

- [x] [LC 206: Reverse Linked List [Free]](./206_reverse_linked_list.md)
  - **Technique:** 4-step pointer flip (`nxt = cur.next`, `cur.next = prev`, `prev = cur`, `cur = nxt`).
- [x] [LC 92: Reverse Linked List II [Free]](./92_reverse_linked_list_ii.md)
  - **Technique:** Walk to `left - 1`, reverse the sub-segment of length `right - left + 1`, and stitch both ends.
- [x] [LC 234: Palindrome Linked List [Free]](./234_palindrome_linked_list.md)
  - **Technique:** Tortoise and hare midpoint, reverse the second half in-place, and compare pointers inward.
- [ ] [LC 25: Reverse Nodes in k-Group [Free]](https://leetcode.com/problems/reverse-nodes-in-k-group/)
  - **Technique:** Verify $k$ nodes remain, reverse those $k$ nodes, and connect the tail to the next group.
- [ ] [LC 1265: Print Immutable Linked List in Reverse [Paid / Premium]](https://leetcode.com/problems/print-immutable-linked-list-in-reverse/)
  - **Technique:** Recurse to the end first, then print as the call stack unwinds.

#### B. Reordering nodes
Rearranges existing nodes without allocating or deleting nodes.

- [ ] [LC 86: Partition List [Free]](https://leetcode.com/problems/partition-list/)
  - **Technique:** Two dummy heads (`small` for $< x$, `large` for $\ge x$). Walk the list, append each node to its belt, cap `large.next = None`, and stitch `small.next = large_dummy.next`.
- [x] [LC 143: Reorder List [Free]](./143_reorder_list.md)
  - **Technique:** Split at middle (`slow.next = None`), reverse second half, and zipper merge alternately.
- [ ] [LC 24: Swap Nodes in Pairs [Free]](https://leetcode.com/problems/swap-nodes-in-pairs/)
  - **Technique:** Dummy anchor + local pair swap (`first = cur.next`, `second = cur.next.next`).
- [ ] [LC 61: Rotate List [Free]](https://leetcode.com/problems/rotate-list/)
  - **Technique:** Count length $n$, link tail to head into a ring, and break the ring at $n - (k \bmod n)$.
- [ ] [LC 328: Odd Even Linked List [Free]](https://leetcode.com/problems/odd-even-linked-list/)
  - **Technique:** Maintain `odd` and `even` tails, leapfrog both forward, then attach `odd.next = even_head`.

### 3. Deleting nodes
Bypass unwanted nodes by rewiring `cur.next = cur.next.next`.

- [x] [LC 19: Remove Nth Node From End of List [Free]](./19_remove_nth_node_from_end.md)
  - **Technique:** Start `left` at `dummy` and `right` $n$ steps ahead of `head`. When `right` hits `None`, `left` sits right before the target node.
- [x] [LC 83: Remove Duplicates from Sorted List [Free]](./83_remove_duplicates_from_sorted_list.md)
  - **Technique:** Since the list is sorted, duplicates are adjacent. If `cur.val == cur.next.val`, snip `cur.next = cur.next.next` without advancing `cur`.
- [ ] [LC 82: Remove Duplicates from Sorted List II [Free]](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/)
  - **Technique:** Dummy head + inner loop skipping all copies of a duplicated value before reconnecting `prev.next`.
- [x] [LC 203: Remove Linked List Elements [Free]](./203_remove_linked_list_elements.md)
  - **Technique:** Dummy head + `if cur.next.val == val: cur.next = cur.next.next else: cur = cur.next`.

### 4. Inserting a node
- [ ] [LC 708: Insert into a Sorted Circular Linked List [Paid / Premium]](https://leetcode.com/problems/insert-into-a-sorted-circular-linked-list/)
  - **Technique:** Handle 3 cases: normal sorted gap (`prev <= val <= cur`), wrap-around cliff (`prev > cur` where `val >= prev` or `val <= cur`), or uniform ring (full loop completed).

### 5. Fast and slow pointers (cycles and midpoints)
Two pointers moving at 1x and 2x speed.

- [x] [LC 141: Linked List Cycle [Free]](./141_linked_list_cycle.md)
  - **Technique:** Floyd's tortoise and hare. If `slow == fast`, a cycle exists.
- [x] [LC 142: Linked List Cycle II [Free]](./142_linked_list_cycle_ii.md)
  - **Technique:** After `slow == fast`, start `slow2 = head` and step both by 1 until they meet at the cycle entrance.
- [x] [LC 876: Middle of the Linked List [Free]](./876_middle_of_the_linked_list.md)
  - **Technique:** While `fast and fast.next`, step `slow` by 1 and `fast` by 2.
- [x] [LC 2095: Delete the Middle Node of a Linked List [Free]](./2095_delete_the_middle_node_of_a_linked_list.md)
  - **Technique:** Start `fast = head.next.next` or dummy offset so `slow` stops one node before the middle, then snip `slow.next = slow.next.next`.

## II. Given 2 or more linked lists

- [x] [LC 2: Add Two Numbers](./2_add_two_numbers.md)
  - **Technique:** Walk `l1` and `l2` with `while l1 or l2 or carry:` and maintain `carry = total // 10`.
- [ ] [LC 445: Add Two Numbers II](https://leetcode.com/problems/add-two-numbers-ii/)
  - **Technique:** Most significant digit comes first; either push values onto two stacks or reverse both inputs first.
- [x] [LC 21: Merge Two Sorted Lists](./21_merge_two_sorted_lists.md)
  - **Technique:** Dummy anchor + `cur` builder. Attach smaller node, advance, then attach the leftover tail in one step.
- [ ] [LC 23: Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)
  - **Technique:** Min-heap of size $k$ ($\mathcal{O}(N \log k)$ time) or pairwise divide-and-conquer merges.
- [x] [LC 160: Intersection of Two Linked Lists](./160_intersection_of_two_linked_lists.md)
  - **Technique:** Track switch (`a = a.next if a else headB`, `b = b.next if b else headA`). Both traverse $A + B$ steps and meet at the intersection (or `None`).
- [ ] [LC 1634: Add Two Polynomials Represented as Linked Lists](https://leetcode.com/problems/add-two-polynomials-represented-as-linked-lists/)
  - **Technique:** Zipper merge comparing `p1.power` and `p2.power`.

## III. Hash table augmented

- [ ] [LC 138: Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/)
  - **Technique:** Pass 1 maps `{old_node: Node(old_node.val)}`. Pass 2 wires `.next` and `.random` via dictionary lookups (or interleave cloned nodes in $\mathcal{O}(1)$ space).
- [ ] [LC 1836: Remove Duplicates From an Unsorted Linked List](https://leetcode.com/problems/remove-duplicates-from-an-unsorted-linked-list/)
  - **Technique:** Pass 1 counts value frequencies in a hash map; Pass 2 uses a dummy head to skip nodes with `count[val] > 1`.

## IV. Design data structures using linked lists

Doubly linked lists give $\mathcal{O}(1)$ node removal and insertion when paired with a hash map of `{key: node}`.

- [ ] [LC 146: LRU Cache](https://leetcode.com/problems/lru-cache/) (Hash map + doubly linked list with dummy head and tail)
- [ ] [LC 460: LFU Cache](https://leetcode.com/problems/lfu-cache/) (Hash map of keys + frequency map of doubly linked lists)
- [ ] [LC 432: All O'one Data Structure](https://leetcode.com/problems/all-oone-data-structure/) (Doubly linked list of frequency buckets + hash maps)
- [ ] [LC 1472: Design Browser History](https://leetcode.com/problems/design-browser-history/)
- [ ] [LC 2296: Design a Text Editor](https://leetcode.com/problems/design-a-text-editor/)
- [ ] [LC 706: Design HashMap](https://leetcode.com/problems/design-hashmap/)
- [ ] [LC 705: Design HashSet](https://leetcode.com/problems/design-hashset/)
- [ ] [LC 716: Max Stack](https://leetcode.com/problems/max-stack/)
- [ ] [LC 622: Design Circular Queue](https://leetcode.com/problems/design-circular-queue/)

## V. Merge sort on a linked list

- [ ] [LC 148: Sort List](https://leetcode.com/problems/sort-list/)
  - **Technique:** Split at the midpoint (`slow.next = None`), recursively sort both halves, and zipper merge ([LC 21](./21_merge_two_sorted_lists.md)).

## VI. Linked list and tree hybrids

- [ ] [LC 426: Convert Binary Search Tree to Sorted Doubly Linked List](https://leetcode.com/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/)
- [ ] [LC 430: Flatten a Multilevel Doubly Linked List](https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/)
- [ ] [LC 2130: Maximum Twin Sum of a Linked List](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/)
- [ ] [LC 237: Delete Node in a Linked List](https://leetcode.com/problems/delete-node-in-a-linked-list/) (`node.val = node.next.val; node.next = node.next.next`)

## Study guides in this folder

| Problem | Category | Guide |
| :--- | :--- | :--- |
| Fundamentals | Node & pointer mechanics | [`01_linked_list_fundamentals.md`](./01_linked_list_fundamentals.md) |
| LC 2: Add Two Numbers | II (Two lists + carry) | [`2_add_two_numbers.md`](./2_add_two_numbers.md) |
| LC 19: Remove Nth Node From End | I.3 (Delete with fixed gap) | [`19_remove_nth_node_from_end.md`](./19_remove_nth_node_from_end.md) |
| LC 21: Merge Two Sorted Lists | II (Two lists zipper merge) | [`21_merge_two_sorted_lists.md`](./21_merge_two_sorted_lists.md) |
| LC 83: Remove Duplicates from Sorted List | I.3 (Delete nodes) | [`83_remove_duplicates_from_sorted_list.md`](./83_remove_duplicates_from_sorted_list.md) |
| LC 141 & 142: Linked List Cycle | I.5 (Fast & slow pointers) | [`141_linked_list_cycle.md`](./141_linked_list_cycle.md) |
| LC 143: Reorder List | I.2.B (Split + reverse + merge) | [`143_reorder_list.md`](./143_reorder_list.md) |
| LC 206: Reverse Linked List | I.2.A (In-place reversal) | [`206_reverse_linked_list.md`](./206_reverse_linked_list.md) |
| LC 234: Palindrome Linked List | I.2.A (Midpoint + reverse) | [`234_palindrome_linked_list.md`](./234_palindrome_linked_list.md) |
| LC 1290: Convert Binary in LL to Integer | I.1 (Single-pass stream) | [`1290_convert_binary_number_in_a_linked_list_to_integer.md`](./1290_convert_binary_number_in_a_linked_list_to_integer.md) |
| LC 1721: Swapping Nodes in a Linked List | I.1 (Fixed-gap pointers) | [`1721_swapping_nodes_in_a_linked_list.md`](./1721_swapping_nodes_in_a_linked_list.md) |
