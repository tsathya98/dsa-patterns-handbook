# 🗺️ 90% of Linked List Questions Classified into Types

> **Source:** [LeetCode Discuss: 90% of the Linked List questions on linked list classified into Types](https://leetcode.com/discuss/post/2434752/90-of-the-linked-list-questions-on-linke-4xc3/) (Post #2434752)  
> **Philosophy:** Stop treating every linked list problem like an isolated puzzle. Over 90% of all interview questions fall into these clean, predictable types.

---

## ⚡ The 10-Second Classifier Decision Tree

Before writing any code, identify your problem's category:

```text
                              [ Linked List Problem ]
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
  [ GIVEN 1 LL ]                  [ 2 OR MORE LLs ]             [ DESIGN / HYBRID ]
        │                                │                                │
  ┌─────┴──────────────────┐      ┌──────┴──────────────┐          ┌──────┴──────────────┐
  │ 1. Simple Recursion    │      │ • Zipper Merge      │          │ • Hash Table Augment│
  │    (Stream/Horner/Swap)│      │ • Schoolbook Carry  │          │ • DLL + HashMap     │
  │ 2. Modify (Same Count) │      │ • Intersection      │          │   (LRU Cache)       │
  │    - Reversing         │      │ • Merge k-Sorted    │          │ • Merge Sort on LL  │
  │    - Reordering        │      └─────────────────────┘          │ • LL + Tree Hybrids │
  │ 3. Delete Nodes        │                                       └─────────────────────┘
  │ 4. Insert Node         │
  │ 5. Fast/Slow Pointers  │
  └────────────────────────┘
```

---

## 📑 The Master Classification Breakdown

```text
├── # Linked List Fundamentals (Design)
├── # Category I: Given 1 Linked List
│   ├── 1) Simple Recursion & Single-Pass
│   ├── 2) Modifying the List (Node Count Remains Same)
│   │   ├── A. Reversing the Linked List
│   │   └── B. Reordering the Nodes
│   ├── 3) Delete Nodes
│   ├── 4) Insert Node
│   └── 5) Fast Pointer & Slow Pointer (Cycles & Midpoints)
├── # Category II: Given 2 or More Linked Lists
├── # Category III: Hash Table Augmented
├── # Category IV: Design Data Structures Using Linked Lists
├── # Category V: Merge Sort on List
├── # Category VI: Linked List + Tree Hybrids
└── # Category VII: To Do (Hard Design Boss Challenges)
```

---

## 🧱 0. Linked List Fundamentals

The building block: designing and understanding node connections from scratch.

* [ ] [LC 707: Design Linked List](https://leetcode.com/problems/design-linked-list/)

> 💡 **Design Superweapon (Sentinels):**  
> In doubly linked lists, always initialize dummy `head` and `tail` nodes (`head.next = tail`, `tail.prev = head`). This completely eliminates edge-case checks for inserting at the front or deleting at the back.

---

## 🏃 I. Given 1 Linked List

### 1) Simple Recursion & Single-Pass (Nothing Else)
Nodes are inspected or accumulated without changing the list structure or node count.

* [x] [LC 1721: Swapping Nodes in a Linked List](file:///Users/sathyat/Developer/projects/dsa/1721_swapping_nodes_in_a_linked_list.md) *(Solved in Repo)*
  * **Technique:** Measuring Stick / Offset Runners. Reaching node $k$ takes `k - 1` steps. Slide `fast` and `second` together.
* [ ] [LC 369: Plus One Linked List](https://leetcode.com/problems/plus-one-linked-list/) *(Array cousin: [LC 66](file:///Users/sathyat/Developer/projects/dsa/66_plus_one.md) in repo)*
  * **Technique:** Post-order recursion bubbles the carry backward: `carry = add_carry(node.next)`.
* [x] [LC 1290: Convert Binary Number in a Linked List to Integer](file:///Users/sathyat/Developer/projects/dsa/1290_convert_binary_number_in_a_linked_list_to_integer.md) *(Solved in Repo)*
  * **Technique:** Horner's Rule accumulator: `ans = (ans << 1) | head.val`. Pure $\mathcal{O}(1)$ space, no string copying.

---

### 2) Modifying the LL (Node Count Remains the Same)

#### A. Reversing the Linked List
Reverses the direction of pointers in-place ($\mathcal{O}(n)$ time, $\mathcal{O}(1)$ space).

* [x] [LC 206: Reverse Linked List](file:///Users/sathyat/Developer/projects/dsa/206_reverse_linked_list.md) *(Solved in Repo)*
  * **Mental Model:** Preschool Conga Line 4-beat dance (`nxt = curr.next`, `curr.next = prev`, `prev = curr`, `curr = nxt`).
* [ ] [LC 92: Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/)
  * **Technique:** Reverse only the sub-segment between `left` and `right`, stitch boundaries.
* [x] [LC 234: Palindrome Linked List](file:///Users/sathyat/Developer/projects/dsa/234_palindrome_linked_list.md) *(Solved in Repo)*
  * **Technique:** In-Place Triple Crown (Tortoise & Hare Midpoint $\to$ Reverse 2nd half $\to$ Compare pointers $\to$ Restore).
* [ ] [LC 25: Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) *(Hard)*
  * **Technique:** Check if $k$ nodes exist $\to$ reverse the group of $k$ $\to$ recursively reverse next group.
* [ ] [LC 1265: Print Immutable Linked List in Reverse](https://leetcode.com/problems/print-immutable-linked-list-in-reverse/)
  * **Technique:** Standard recursion call stack (`print_rev(head.getNext())`, then `head.printValue()`).

#### B. Reordering the Nodes
Rearranges the order of nodes without adding or removing any nodes.

* [ ] [LC 86: Partition List](https://leetcode.com/problems/partition-list/) ⭐ **IMP**
  * **Technique:** Multi-Track Conveyor Belts. Create two dummy heads (`small` for $< x$, `great` for $\ge x$). Walk list, attach to appropriate belt, set `great.next = None`, and stitch `small.next = dummy_great.next`.
* [ ] [LC 143: Reorder List](https://leetcode.com/problems/reorder-list/)
  * **Technique:** Find middle $\to$ reverse second half $\to$ zipper weave nodes alternately.
* [ ] [LC 24: Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/)
  * **Technique:** Pointer swapping with dummy anchor: `first = cur.next`, `second = cur.next.next`.
* [ ] [LC 61: Rotate List](https://leetcode.com/problems/rotate-list/)
  * **Technique:** Connect tail to head to form a ring, break ring at `len - (k % len)`.
* [ ] [LC 328: Odd Even Linked List](https://leetcode.com/problems/odd-even-linked-list/)
  * **Technique:** Two pointers (`odd` and `even`), walk simultaneously, link `odd.next = even_head`.

---

### 3) Delete Nodes
Bypassing unwanted nodes (`prev.next = cur.next`).

* [ ] [LC 19: Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)
  * **Technique:** Offset runners by $N + 1$ steps from `dummy` so `slow` lands right before the deletion target.
* [x] [LC 83: Remove Duplicates from Sorted List](file:///Users/sathyat/Developer/projects/dsa/83_remove_duplicates_from_sorted_list.md) *(Solved in Repo)*
  * **Golden Rule:** List is SORTED $\implies$ **No Hash Table needed!** Compare `cur.val == cur.next.val` in $\mathcal{O}(1)$ space.
* [ ] [LC 82: Remove Duplicates from Sorted List II](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/)
  * **Technique:** Remove *all* nodes with duplicate numbers. Use `dummy`, lookahead `while cur.next and cur.next.val == cur.next.next.val:`.
* [ ] [LC 203: Remove Linked List Elements](https://leetcode.com/problems/remove-linked-list-elements/)
  * **Technique:** Dummy head + skip target values: `if cur.next.val == val: cur.next = cur.next.next else: cur = cur.next`.

---

### 4) Insert Node
* [ ] [LC 708: Insert into a Sorted Circular Linked List](https://leetcode.com/problems/insert-into-a-sorted-circular-linked-list/)
  * **Technique:** 3 cases: (1) normal gap `prev <= val <= curr`, (2) wrap-around boundary `prev > curr` with `val >= prev` or `val <= curr`, (3) full 360° circle.

---

### 5) Fast Pointer & Slow Pointer (Cycle or Middle Element)
Two runners moving at different speeds (`slow = 1 step`, `fast = 2 steps`).

* [ ] [LC 141: Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)
  * **Technique:** Floyd's Cycle Finding. If `fast == slow`, cycle exists.
* [ ] [LC 876: Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/)
  * **Technique:** When `fast` reaches end, `slow` is at midpoint.
* [ ] [LC 2095: Delete the Middle Node of a Linked List](https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/)
  * **Technique:** Fast/slow with `dummy` or track `prev` before slow.
* [ ] [LC 142: Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/)
  * **Technique:** Collision meet point $\to$ reset `finder = head` $\to$ step both at 1x $\to$ meet at cycle start.

---

## ⚡ II. Given 2 or More Linked Lists

Synchronizing and merging multiple independent chains.

* [ ] [LC 2: Add Two Numbers](https://leetcode.com/problems/add-two-numbers/)
  * **Technique:** Simultaneous traversal + schoolbook carry: `carry, out = divmod(v1 + v2 + carry, 10)`.
* [ ] [LC 445: Add Two Numbers II](https://leetcode.com/problems/add-two-numbers-ii/)
  * **Technique:** Digits most significant first $\implies$ use two stacks or reverse both lists first.
* [x] [LC 21: Merge Two Sorted Lists](file:///Users/sathyat/Developer/projects/dsa/linked_list_master_cheat_sheet.md#pattern-1-the-zipper-merge-lc-21) *(Covered in Master Cheat Sheet)*
  * **Technique:** Zipper merge: pick smaller head, attach to `cur.next`, stitch remaining tail.
* [ ] [LC 23: Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) ⭐ **IMP**
  * **Technique:** Min-Heap (priority queue) of size $k$ $\implies \mathcal{O}(N \log k)$ time, or Divide & Conquer merge pairs.
* [ ] [LC 160: Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists/)
  * **Technique:** Track Switch: `pA = pA.next if pA else headB`. Equalizes path lengths $A + B = B + A$.
* [ ] [LC 1634: Add Two Polynomials Represented as Linked Lists](https://leetcode.com/problems/add-two-polynomials-represented-as-linked-lists/)
  * **Technique:** Merge by exponent power: compare `p1.power` vs `p2.power`.

---

## 🗄️ III. Hash Table Augmented

Used when pointer manipulation alone requires costly $\mathcal{O}(n^2)$ scans.

* [ ] [LC 138: Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) ⭐ **IMP**
  * **Technique:** Pass 1 creates `{old_node: Node(val)}`. Pass 2 wires `.next` and `.random` using dictionary lookups. (Can also be done in $\mathcal{O}(1)$ space by interweaving).
* [ ] [LC 1836: Remove Duplicates From an Unsorted Linked List](https://leetcode.com/problems/remove-duplicates-from-an-unsorted-linked-list/)
  * **Crucial Rule:** Unsorted list $\implies$ **Must use HashMap/Counter!** Pass 1 counts frequencies; Pass 2 deletes nodes where `count[val] > 1`.

---

## 🏛️ IV. Design Data Structures Using Linked Lists

Doubly Linked Lists provide $\mathcal{O}(1)$ node removal and insertion given a node pointer. Combining DLL + HashMap provides $\mathcal{O}(1)$ lookup AND $\mathcal{O}(1)$ updates.

* [ ] [LC 146: LRU Cache](https://leetcode.com/problems/lru-cache/) ⭐ **Top FAANG Question**
  * **Architecture:** `HashMap { key: Node }` + `Doubly Linked List (head dummy <-> tail dummy)`.
* [ ] [LC 706: Design HashMap](https://leetcode.com/problems/design-hashmap/) *(Chaining with bucket linked lists)*
* [ ] [LC 716: Max Stack](https://leetcode.com/problems/max-stack/) *(DLL + TreeMap / Doubly Linked List)*
* [ ] [LC 705: Design HashSet](https://leetcode.com/problems/design-hashset/)
* [ ] [LC 1472: Design Browser History](https://leetcode.com/problems/design-browser-history/) *(Doubly Linked List back/forward)*
* [ ] [LC 355: Design Twitter](https://leetcode.com/problems/design-twitter/) *(Note: Can use HashMaps + Min-Heap; no strict need for LL)*
* [ ] [LC 622: Design Circular Queue](https://leetcode.com/problems/design-circular-queue/) *(Fixed array or Singly/Doubly Linked List)*

---

## 🌲 V. Merge Sort on List

* [ ] [LC 148: Sort List](https://leetcode.com/problems/sort-list/) ⭐ **IMP**
  * **Why it's special:** Arrays need $\mathcal{O}(n)$ space to merge. Linked Lists do Merge Sort in **$\mathcal{O}(1)$ auxiliary space**!
  * **Steps:** Fast/Slow midpoint $\to$ cut `slow.next = None` $\to$ recurse left and right $\to$ zipper merge (LC 21).

---

## 🌳 VI. Linked List + Tree Hybrids

* [ ] [LC 426: Convert Binary Search Tree to Sorted Doubly Linked List](https://leetcode.com/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/)
  * **Technique:** In-order traversal visits BST in sorted order; wire `prev.right = cur` and `cur.left = prev`.
* [ ] [LC 430: Flatten a Multilevel Doubly Linked List](https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/)
  * **Technique:** Pre-order DFS traversal. Splice child chain between `cur` and `cur.next`.
* [ ] [LC 2130: Maximum Twin Sum of a Linked List](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/)
  * **Technique:** Find middle $\to$ reverse second half $\to$ iterate both halves simultaneously summing pairs.
* [ ] [LC 237: Delete Node in a Linked List](https://leetcode.com/problems/delete-node-in-a-linked-list/)
  * **The Trick Question:** You are only given the node to delete! Copy next value: `node.val = node.next.val`, bypass next: `node.next = node.next.next`.

---

## 🏔️ VII. To Do: Hard Design Boss Challenges

The ultimate trio of complex linked list system designs:

* [ ] [LC 432: All O`one Data Structure](https://leetcode.com/problems/all-oone-data-structure/) *(DLL of Frequency Buckets + Two HashMaps)*
* [ ] [LC 460: LFU Cache](https://leetcode.com/problems/lfu-cache/) *(Least Frequently Used: HashMap of Frequencies to Doubly Linked Lists)*
* [ ] [LC 2296: Design a Text Editor](https://leetcode.com/problems/design-a-text-editor/) *(Doubly Linked List cursor or two stacks)*

---

## 📊 Summary Mapping: Your Solved Problems

| Problem | Section in this Guide | Solved Guide |
| :--- | :--- | :--- |
| **LC 206: Reverse Linked List** | **I. 2. A (Reversing LL)** | [`206_reverse_linked_list.md`](file:///Users/sathyat/Developer/projects/dsa/206_reverse_linked_list.md) |
| **LC 234: Palindrome Linked List** | **I. 2. A (Reversing LL)** | [`234_palindrome_linked_list.md`](file:///Users/sathyat/Developer/projects/dsa/234_palindrome_linked_list.md) |
| **LC 1721: Swapping Nodes in a Linked List** | **I. 1 (Simple Recursion/Single Pass)** | [`1721_swapping_nodes_in_a_linked_list.md`](file:///Users/sathyat/Developer/projects/dsa/1721_swapping_nodes_in_a_linked_list.md) |
| **LC 1290: Convert Binary in LL to Integer** | **I. 1 (Simple Recursion/Single Pass)** | [`1290_convert_binary_number_in_a_linked_list_to_integer.md`](file:///Users/sathyat/Developer/projects/dsa/1290_convert_binary_number_in_a_linked_list_to_integer.md) |
| **LC 21: Merge Two Sorted Lists** | **II. Given 2 or More LLs** | [`linked_list_master_cheat_sheet.md`](file:///Users/sathyat/Developer/projects/dsa/linked_list_master_cheat_sheet.md#pattern-1-the-zipper-merge-lc-21) |
| **LC 83: Remove Duplicates from Sorted List** | **I. 3 (Delete Nodes)** | [`83_remove_duplicates_from_sorted_list.md`](file:///Users/sathyat/Developer/projects/dsa/83_remove_duplicates_from_sorted_list.md) |
| **LC 66: Plus One** | *(Array Cousin of LC 369 in I. 1)* | [`66_plus_one.md`](file:///Users/sathyat/Developer/projects/dsa/66_plus_one.md) |
