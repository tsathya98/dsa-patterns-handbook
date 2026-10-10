# 🔗 Linked List Master Cheat Sheet: The Intuitive Guide

> **Target Audience:** Anyone who finds Linked Lists abstract or confusing.  
> **Philosophy:** A Linked List is NOT an array. It is a **treasure hunt of nested boxes**. Once you see the physical picture, the code writes itself.  
> 🗺️ **Full LeetCode Taxonomy:** Looking for the comprehensive 11-type classification of 90%+ of all interview questions? See **[The 90% Linked List Master Taxonomy Guide](./linked_list_90_percent_taxonomy.md)**.

---

## 📦 1. What IS a Linked List? (The Russian Nesting Doll)

In an **array** `[10, 20, 30]`, items sit side-by-side like a row of houses on the same street. That's why you can jump to `arr[2]` instantly ($\mathcal{O}(1)$).

A **Linked List** is completely different. It is a chain of **Russian nesting dolls**:

```python
# A linked list with values: 10 -> 20 -> 30 -> None
# In Python's memory, it is literally:
ListNode(val=10, next=ListNode(val=20, next=ListNode(val=30, next=None)))
```

```text
┌─────────────────┐
│     val: 10     │
│  next: ─────────┼──────► ┌─────────────────┐
└─────────────────┘        │     val: 20     │
                           │  next: ─────────┼──────► ┌─────────────────┐
                           └─────────────────┘        │     val: 30     │
                                                      │  next: None     │
                                                      └─────────────────┘
```

* Node `10` holds a pointer (`.next`) to Node `20`.
* Node `20` holds a pointer (`.next`) to Node `30`.
* Node `30` points to `None` (the end of the chain!).

> ⚠️ **The #1 Confusion:**  
> Why does `len(head)` crash?  
> Because a linked list node does **not** know how many nodes follow it! It only knows its own value and the next box. Finding the length requires walking every node ($\mathcal{O}(n)$).

---

## 🛡️ 2. The Anchor & Hand Pattern (`dummy` vs `cur`)

Whenever you build a new linked list, you will always see:
```python
dummy = ListNode()
cur = dummy
```

Here is the exact physical mental model to never get confused again:

```text
       [ DUMMY ] (The Coat Rack: fixed to the wall, never moves)
           │
           │ .next
           ▼
        [  1  ] ──► [  2  ] ──► [  4  ] ──► None
           ▲
          cur   (Your Hand: walks to the very end of the chain)
```

| Variable | What It Represents | Does It Move? | Why It Exists |
| :--- | :--- | :---: | :--- |
| **`dummy`** | **The Coat Rack** | ❌ **NEVER MOVES** | Glued to the start so you never lose the head of your list. |
| **`cur`** | **Your Hand** | ✅ **MOVES FORWARD** | Steps to the end of the chain (`cur = cur.next`) so the next item attaches to the tail, NOT the front! |
| **`dummy.next`**| **The First Real Item** | - | Skips the fake coat rack `[ 0 ]` and returns the true result! |

### 🎯 The 2-Second Return Rule: `return dummy.next` vs `return head`
Ask yourself **one simple question** at the end of your function:
> *"Is the starting node pointed to by this variable a **FAKE placeholder node I created**, or a **REAL node from the input**?"*

```text
Case A: You created a fake anchor          Case B: You modified an existing list
        dummy = ListNode(0)                         cur = head

            dummy                                       head
              │                                           │
              ▼                                           ▼
            [ 0 ] ──► [ 1 ] ──► [ 2 ]                   [ 1 ] ──► [ 2 ] ──► [ 3 ]
            (Fake)      ▲                                 ▲
                        │                                 │
           👉 return dummy.next                       👉 return head
         (Throw away the fake [0]!)                  (Keep the real starting node!)
```

* **Use `return dummy.next`** when: You constructed a new list or merged lists using `dummy = ListNode()`. Skipping `dummy` removes the fake `[0]` placeholder.
* **Use `return head`** when: You modified the list in-place (like `deleteDuplicates`) where `head` was already the first legitimate node. Returning `head.next` would accidentally chop off the first real number!

---

## 🎬 3. The 6 Universal Linked List Patterns

### 🔹 Pattern 1: The Zipper Merge (LC 21)
* **What it does:** Combines two sorted lines into one single sorted line.
* **Analogy:** Picking the shorter student at the front of two lines.

```text
list1: [ 1 ] ──► [ 4 ]
list2: [ 2 ] ──► [ 3 ]

dummy ──► [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ]
```

```python
def mergeTwoLists(list1, list2):
    dummy = ListNode()
    cur = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            cur.next = list1
            list1 = list1.next
        else:
            cur.next = list2
            list2 = list2.next
        cur = cur.next
        
    cur.next = list1 if list1 else list2
    return dummy.next
```

---

### 🔹 Pattern 2: In-Place Arrow Reversal (LC 206)
* **What it does:** Reverses every arrow in-place without allocating any new nodes ($\mathcal{O}(n)$ time, $\mathcal{O}(1)$ space).
* **The Analogy:** **The Preschool Children Conga Line** 🎒
  * A line of children holding each other's backpacks: `[ Alice ] ──► [ Bob ] ──► [ Charlie ] ──► None`.
  * The teacher says: *"Turn around! Charlie at the front, Alice at the back!"*
  * **The Danger:** If Bob lets go of Charlie without a spotter, **Charlie runs away and gets lost!**

#### The 3 Roles:
1. **`prev` (Person Behind You):** Starts at `None` (empty air behind Alice).
2. **`curr` (Person Turning Around):** Starts at `head` (Alice).
3. **`nxt` (Teacher's Spotter Hand):** Taps the child in front and says: *"Freeze! Hold on while the person behind you turns around!"*

```text
ROUND 1 (Alice turns around):
  prev     curr        nxt
   │        │           │
   ▼        ▼           ▼
  None   [ Alice ] ──► [ Bob ] ──► [ Charlie ]

Beat 1: nxt = curr.next    -> Teacher holds Bob!
Beat 2: curr.next = prev   -> Alice lets go of Bob and grabs None (behind her).
Beat 3: prev = curr        -> Slide prev to Alice.
Beat 4: curr = nxt         -> Slide curr to Bob.

None ◄── [ Alice ]   [ Bob ] ──► [ Charlie ]
           ▲           ▲
          prev        curr
```

```python
def reverseList(head: ListNode | None) -> ListNode | None:
    prev = None
    curr = head
    
    while curr:
        nxt = curr.next     # 1. SPOTTER: Hold child in front so they don't run away!
        curr.next = prev    # 2. TURN AROUND: Grab backpack of person behind you!
        prev = curr         # 3. ADVANCE PREV: You are now the person "behind" for next round!
        curr = nxt          # 4. ADVANCE CURR: Next child's turn to turn around!
        
    return prev             # prev is holding Charlie (the NEW FRONT of the line!)
```

#### ❓ Why `return prev`? Why not `return curr` or `curr.next`?
* **Why NOT `return curr`?** The loop only terminates when `curr` becomes **`None`**! Returning `curr` returns empty `[]`!
* **Why NOT `return curr.next`?** `None.next` raises `AttributeError: 'NoneType' has no attribute 'next'`! 💥
* **Why `return prev`?** When `curr` falls into `None`, `prev` is standing on the **very last node** (the new head of the line!).
* **Why `while curr:` instead of `while curr and curr.next:`?** `while curr.next` stops early on the last node, meaning the last node never turns around!

👉 *See full breakdown and visual comic in [`206_reverse_linked_list.md`](./206_reverse_linked_list.md).*

---

### 🔹 Pattern 3: Tortoise & Hare (Fast & Slow Pointers)
* **What it does:** Finds the middle node (LC 876) or detects cycles (LC 141) in a single pass without knowing the length!
* **Analogy:** Two runners on a track. Slow runs 1 step per second, Fast runs 2 steps per second.

```text
[ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None
            ▲                   ▲
           slow                fast (When fast hits end, slow is in the middle!)
```

```python
def findMiddle(head):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next          # 1 step
        fast = fast.next.next     # 2 steps
    return slow                   # Exact middle node!
```

---

### 🔹 Pattern 4: The 3-Step Palindrome / Reorder Triple Crown (LC 234, LC 143)
* **What it does:** Solves linked list symmetry/reordering in **$\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space** without converting to an array!
* **The 3 Steps:**
  1. **Find End of 1st Half:** Use `while fast.next and fast.next.next:` (so `slow` stops on the left of center).
  2. **Reverse 2nd Half:** Apply the Conga Line 4-beat dance starting at `slow.next`.
  3. **Compare Pointers:** Compare `head` and `reversed_2nd_half` side-by-side.
  4. *(Bonus)* **Restore:** Re-reverse the second half so the input list is not mutated!

```python
def isPalindrome(head: Optional[ListNode]) -> bool:
    if not head or not head.next:
        return True

    # 1. Find midpoint (Tortoise & Hare)
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    # 2. Reverse 2nd half (Conga Line Dance)
    prev, cur = None, slow.next
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    second_half = prev

    # 3. Compare 1st half vs reversed 2nd half
    p1, p2 = head, second_half
    is_pal = True
    while is_pal and p2:
        if p1.val != p2.val:
            is_pal = False
        p1 = p1.next
        p2 = p2.next

    # 4. Optional: Restore list
    prev, cur = None, second_half
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    slow.next = prev

    return is_pal
```

#### 🔬 Key Findings & Interview Trade-offs:
* **Array Dump + Two Pointers Squeeze:** Great initial baseline ($\mathcal{O}(n)$ time, $\mathcal{O}(n)$ space).
* **Two Pointers Squeeze vs `lst == lst[::-1]`:**
  * **Memory:** Two Pointers allocates **$0$ extra space** vs $\mathcal{O}(n)$ duplicate list copy for `[::-1]`.
  * **Short-circuiting:** Two Pointers quits in **$0.004$ ms ($1,685\times$ faster)** on early mismatch because it doesn't wait to reverse the entire list first.
* **Is Array Dump FAANG-worthy?**
  * As an initial solution: **Yes** (proves you write clean, bug-free code fast).
  * As the final solution: **No** (interviewers will prompt for the $\mathcal{O}(1)$ space in-place Triple Crown).

👉 *See full breakdown and benchmark in [`234_palindrome_linked_list.md`](./234_palindrome_linked_list.md).*

---

### 🔹 Pattern 5: The Measuring Stick / Offset Two Pointers (LC 19, LC 1721)
* **What it does:** Locates the $k$-th node from the end in a single pass without knowing list length and without an array!
* **Analogy:** A physical wooden ruler of fixed length $k$.
  * Front finger (`fast`) on the $k$-th node from start.
  * Back finger (`second`) at `head`.
  * Slide both forward together until `fast.next is None`.
  * When `fast` reaches the end, `second` is guaranteed to be standing on the $k$-th node from the end!

```text
head = [ 1,  2,  3,  4,  5 ], k = 2

Step 1: first walks k - 1 steps to [ 2 ]
Step 2: fast = first, second = head
Step 3: Slide both until fast.next is None:
        second lands on [ 4 ] (2nd from end!)
```

```python
def swapNodes(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    first = head
    second = head

    # 1. Walk first to k-th node from start (k - 1 steps!)
    for _ in range(k - 1):
        first = first.next

    # 2. Slide measuring stick to find k-th from end
    fast = first
    while fast.next:
        fast = fast.next
        second = second.next

    # 3. Swap values in-place
    first.val, second.val = second.val, first.val
    return head
```

#### 🔬 Key Findings & Pitfalls:
* **The "Fencepost" Step Rule:** Standing on Node 1 means reaching Node $k$ takes **`k - 1` steps**, not $k$! (Using `range(k)` takes 1 step too many and crashes on $k = \text{length}$).
* **Swapping Inside Reconstruction Loop (Direction-Dependent Bug):**  
  If you dump to an array and rebuild, never do `if i == k - 1: swap` inside the loop. If $k$ is in the back half (e.g. `[100, 90], k = 2`), index 0 is read before the swap happens, outputting duplicate values `[100, 100]`. Always swap *before* the loop!

👉 *See full breakdown in [`1721_swapping_nodes_in_a_linked_list.md`](./1721_swapping_nodes_in_a_linked_list.md).*

---

### 🔹 Pattern 6: The Positional Stream Accumulator / Horner's Rule (LC 1290)
* **What it does:** Converts a stream of incoming digits/bits in a linked list into a single integer in **$\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space** without string conversions or exponentiation!
* **The Analogy:** How you read digits in base-10:
  * See 1: `(0 * 10) + 1 = 1`
  * See 2: `(1 * 10) + 2 = 12`
  * See 3: `(12 * 10) + 3 = 123`
* **In Base-2 (Binary):** Multiply by 2 instead of 10:
  * `ans = ans * 2 + head.val`
  * Or with bitwise operations: `ans = (ans << 1) | head.val`

```python
def getDecimalValue(head: ListNode | None) -> int:
    ans = 0
    while head:
        ans = (ans << 1) | head.val  # Shift left, add bit
        head = head.next
    return ans
```

#### 🔬 Key Findings:
* **The String Concatenation Trap (`s += ...`):** Building a binary string with `s += str(head.val)` creates a brand new string on every node in Python, secretly degrading memory/time to $\mathcal{O}(n^2)$.
* **Hardware Shift Register Model:** `(ans << 1) | bit` mirrors how network packets and CPU registers accumulate bits across a serial wire.

👉 *See full breakdown in [`1290_convert_binary_number_in_a_linked_list_to_integer.md`](./1290_convert_binary_number_in_a_linked_list_to_integer.md).*

---

## ⚠️ 4. The 5 Golden Rules of Linked Lists

1. **Always stitch NODES, not numbers:**  
   `cur.next = list1` ✅  
   `cur.next = list1.val` ❌ (CRASH: integer has no `.next`).
2. **Never check `.val` on `None`:**  
   Always check `while list1 and list2:`. If you use `or`, the moment one list finishes, `list1.val` crashes with `AttributeError`.
3. **Always save `curr.next` before breaking it:**  
   In reversals: `nxt = curr.next` must happen **before** `curr.next = prev`. Otherwise, the rest of the chain floats away into void!
4. **`dummy` stays, `cur` walks:**  
   Never do `dummy = dummy.next`. Use `cur = cur.next` so `dummy` anchors the start!
5. **Restore mutated structures in production:**  
   If you reverse part of a list to inspect it (like in LC 234), re-reverse it before returning so you don't corrupt caller data in multi-threaded environments.

---

## 🗺️ 5. The Master Classification of Linked List Questions (The 90% Rule)

According to the famous LeetCode masterclass ([Post #2434752](https://leetcode.com/discuss/post/2434752/90-of-the-linked-list-questions-on-linke-4xc3/)), 90%+ of all Linked List interview questions fall into this clean hierarchy:

```text
├── # Fundamentals & Design (LC 707)
├── # Category I: Given 1 Linked List
│   ├── 1) Simple Recursion & Single-Pass (LC 1721, LC 369, LC 1290)
│   ├── 2) Modifying the LL (Node Count Same)
│   │   ├── A. Reversing the Linked List (LC 206, LC 92, LC 234, LC 25, LC 1265)
│   │   └── B. Reordering the Nodes (LC 86 IMP, LC 143, LC 24, LC 61, LC 328)
│   ├── 3) Delete Nodes (LC 19, LC 83, LC 82, LC 203)
│   ├── 4) Insert Node (LC 708 Circular)
│   └── 5) Fast & Slow Pointer / Cycles & Midpoint (LC 141, LC 876, LC 2095, LC 142)
├── # Category II: Given 2 or More Linked Lists (LC 2, LC 445, LC 21, LC 23 IMP, LC 160)
├── # Category III: Hash Table Augmented (LC 138 IMP, LC 1836)
├── # Category IV: Design Data Structures Using LL (LC 146 LRU, LC 706, LC 1472)
├── # Category V: Merge Sort on List (LC 148 IMP)
├── # Category VI: LL + Tree Hybrids (LC 426, LC 430, LC 2130, LC 237)
└── # Category VII: To Do (Hard Design Boss Challenges - LC 432, LC 460, LC 2296)
```

### 💡 The Crucial Duplicate Removal Rule:
* **Sorted List:** **NO extra memory needed!** Compare adjacent items: `cur.val == cur.next.val` $\rightarrow \mathcal{O}(1)$ space.
* **Unsorted List:** **You MUST use a Hash Table / HashSet!** Without sorting, duplicate values can appear anywhere in the list $\rightarrow \mathcal{O}(n)$ space.

👉 *For full visual diagrams, templates, and problem checklists, check out **[`linked_list_90_percent_taxonomy.md`](./linked_list_90_percent_taxonomy.md)**.*

