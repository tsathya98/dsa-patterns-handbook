# Print a Linked List in Reverse Order

> **Difficulty:** Easy | **Pattern:** LIFO Stack vs Call Stack / In-Place Reversal  
> **Source Code:** [`print_linked_list_in_reverse.py`](print_linked_list_in_reverse.py)

## The problem

Given the head of a singly linked list, print the node values from tail to head separated by spaces without destroying the input structure.

```text
Input:  head = [1, 2, 3, 4, 5]
Output: 5 4 3 2 1

Input:  head = []
Output: (empty)
```

---

## Why interviewers ask this (The 2 trap checks)

This problem is rarely given as a stand-alone challenge. Interviewers use it as an early filter to probe core software engineering principles:

### 1. Immutability and destructive side effects
A function named `printLinkedListInReverse` is fundamentally a read-only query.
Reversing the linked list in-place (`prev = None`) without restoring it mutates the caller's data structure. In production systems and FAANG hiring rubrics, modifying caller state in a read function violates API contracts. If you reverse the pointers for $\mathcal{O}(1)$ space, you **must reverse it back** before returning.

### 2. Stack overflow on large constraints ($N = 10^5$)
A common 3-line recursive approach places every node onto the system call stack.
- In Python, the default recursion limit is 1,000 frames (`RecursionError`).
- In Java/C++, thread stacks are 1 MB to 8 MB (`StackOverflowError`).
Using an **explicit heap-allocated stack** handles $10^5$ items safely without OS thread stack exhaustion.

---

## Visual walkthrough

```text
Input List:  (1) -> (2) -> (3) -> (4) -> (5) -> None

Traverse & push to explicit stack:
[ 1, 2, 3, 4, 5 ]  <-- Top is 5

Unpack / pop in LIFO order:
5 4 3 2 1
(Original list remains completely intact)
```

---

### Algorithm steps:

* **1. Guard empty input:** If `head` is `None`, return immediately with no output.
* **2. Collect values:** Traverse `curr = head` through `next`, pushing each `curr.val` onto `stack = []`.
* **3. Output in reverse:** Print the unpacked reversed elements `print(*reversed(stack))`.

---

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

def printLinkedListInReverse(head) -> None:
    if not head:
        return

    stack = []
    curr = head
    while curr:
        stack.append(curr.val)
        curr = curr.next

    print(*reversed(stack))
```

</details>

---

## The FAANG Follow-Up: $\mathcal{O}(1)$ Auxiliary Space

> *"What if memory is strictly constrained and you cannot allocate $\mathcal{O}(N)$ extra space, but the linked list must remain exactly as it was when the function returns?"*

<details>
<summary>Spoiler: Follow-up Code (Reverse, Print, Reverse Back)</summary>

```python
def printLinkedListInReverseO1(head) -> None:
    if not head:
        return

    def reverse(node):
        prev = None
        curr = node
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    # Step 1: Reverse in-place
    tail = reverse(head)

    # Step 2: Print reversed sequence
    curr = tail
    while curr:
        print(curr.val, end=" " if curr.next else "")
        curr = curr.next
    print()

    # Step 3: Reverse back to preserve caller immutability
    reverse(tail)
```

</details>

---

## Complexity

- **Standard Stack:**
  - **Time:** $\mathcal{O}(N)$ single pass forward, single pass output.
  - **Space:** $\mathcal{O}(N)$ heap memory (avoids call stack overflow).
- **Follow-up In-Place (Reverse-Print-Reverse):**
  - **Time:** $\mathcal{O}(N)$ across 3 linear passes.
  - **Space:** $\mathcal{O}(1)$ auxiliary memory while preserving list immutability.
