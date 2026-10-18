# LeetCode 203: Remove Linked List Elements

> **Pattern:** Sentinel dummy + pointer bypass  
> **Difficulty:** Easy  
> **Access:** Free  
> **Link:** [LeetCode 203](https://leetcode.com/problems/remove-linked-list-elements/)

## The problem

Given the `head` of a linked list and an integer `val`, remove all nodes in the list where `Node.val == val`, and return the new head.

```text
Example 1:
Input:  head = [ 1, 2, 6, 3, 4, 5, 6 ], val = 6
Output: [ 1, 2, 3, 4, 5 ]

Example 2 (The edge case that trips people up):
Input:  head = [ 7, 7, 7, 7 ], val = 7
Output: []
```

---

## Why this problem feels tricky

In a singly linked list, **a node cannot delete itself**.

If you are standing on `cur`, you have no backward pointer. You cannot reach behind yourself to tell the previous node to skip you. To delete a node, **you must stand on the node right before it**. That is why linked list deletion always inspects `cur.next.val == val` instead of `cur.val == val`.

```text
To delete [ 6 ]: your pointer MUST stand on [ 2 ]!
[ 1 ] ──► [ 2 ] ──► [ 6 ] ──► [ 3 ]
            ▲
           cur
Operation: cur.next = cur.next.next (wires [ 2 ] directly to [ 3 ])
```

The problem is: **what if the head itself needs to be deleted?** If `head.val == val`, who is standing before `head` to delete it?

---

## Three ways to solve this

### Method 1: Sentinel Dummy Node (The gold standard)

Instead of writing special checks for the head, attach a fake anchor node `dummy = ListNode(0, head)` in front of the list.

Now **every single node in the list (including the original head) has a predecessor standing behind it**. The exact same loop deletes nodes anywhere in the list without special cases.

#### Step-by-step trace on `[ 1, 2, 6, 3 ]`, `val = 6`:

```text
Setup:
dummy    head
  │       │
  ▼       ▼
[ 0 ] ──► [ 1 ] ──► [ 2 ] ──► [ 6 ] ──► [ 3 ] ──► null
  ▲
 cur

Iteration 1:
Inspect cur.next ([ 1 ]). Value 1 != 6. Safe to keep!
Action: cur = cur.next
dummy    head
[ 0 ] ──► [ 1 ] ──► [ 2 ] ──► [ 6 ] ──► [ 3 ] ──► null
            ▲
           cur

Iteration 2:
Inspect cur.next ([ 2 ]). Value 2 != 6. Safe to keep!
Action: cur = cur.next
dummy    head
[ 0 ] ──► [ 1 ] ──► [ 2 ] ──► [ 6 ] ──► [ 3 ] ──► null
                      ▲
                     cur

Iteration 3 (The Delete Step!):
Inspect cur.next ([ 6 ]). Value 6 == 6. MATCH FOUND!
Action: cur.next = cur.next.next (wire [ 2 ] directly to [ 3 ]).
IMPORTANT: Do NOT move cur! Stay on [ 2 ] to check the newly attached node.

After Snip:
dummy    head
[ 0 ] ──► [ 1 ] ──► [ 2 ] ────────► [ 3 ] ──► null
                      ▲
                     cur

Iteration 4:
Inspect cur.next ([ 3 ]). Value 3 != 6. Safe to keep!
Action: cur = cur.next
dummy    head
[ 0 ] ──► [ 1 ] ──► [ 2 ] ────────► [ 3 ] ──► null
                                      ▲
                                     cur

Loop ends: cur.next is null!
Return dummy.next -> skips fake [ 0 ] and returns real clean head [ 1 ].
```

#### What happens on `[ 7, 7, 7, 7 ]`, `val = 7`:

```text
Start:
dummy   head
[ 0 ] ──► [ 7 ] ──► [ 7 ] ──► [ 7 ] ──► [ 7 ] ──► null
  ▲
 cur

Round 1: cur.next is 7. Snip! cur.next = cur.next.next. Do NOT move cur!
[ 0 ] ────────────► [ 7 ] ──► [ 7 ] ──► [ 7 ] ──► null
  ▲
 cur

Round 2: cur.next is still 7! Snip again!
[ 0 ] ──────────────────────► [ 7 ] ──► [ 7 ] ──► null
  ▲
 cur

Round 3 & 4: Snip remaining 7s.
[ 0 ] ──────────────────────────────────────────► null
  ▲
 cur

Return dummy.next -> null (clean empty list in 1 uniform loop!)
```

#### Algorithm steps:
* **1. Anchor sentinel:** Create `dummy = ListNode(0, head)`, set `cur = dummy`.
* **2. Inspect cur.next:** While `cur.next` is not None:
  * If `cur.next.val == val`: snip out the node via `cur.next = cur.next.next`. **Do not advance cur**, because the newly attached node might also have value `val`!
  * Else: safe to advance `cur = cur.next`.
* **3. Return:** `dummy.next` (skips the dummy placeholder and returns the real head).

---

### Method 2: Without dummy node (Why the copied code worked)

Here is the exact code you copied from LeetCode:

```python
node = head
while node and node.next:
    if node.next.val == val:
        node.next = node.next.next
    else:
        node = node.next
if head.val == val:
    head = head.next
return head
```

#### Why this code felt weird and confusing:

In a singly linked list, `node` can only delete `node.next`. Because this code set `node = head` without a dummy in front, **the while loop only looked at nodes after the head**.

#### Step-by-step trace of that code on `[ 7, 7, 7, 7 ]`, `val = 7`:

```text
Start:
head, node
  │     │
  ▼     ▼
[ 7 ] ──► [ 7 ] ──► [ 7 ] ──► [ 7 ] ──► null

Iteration 1:
node is on the first [ 7 ]. node.next is [ 7 ] == 7.
Action: node.next = node.next.next (snip out 2nd node)
head, node
[ 7 ] ────────► [ 7 ] ──► [ 7 ] ──► null

Iteration 2:
node is STILL on first [ 7 ]. node.next is [ 7 ] == 7.
Action: node.next = node.next.next (snip out 3rd node)
head, node
[ 7 ] ──────────────────► [ 7 ] ──► null

Iteration 3:
Action: node.next = node.next.next (snip out 4th node)
head, node
[ 7 ] ────────────────────────────► null

The while loop ENDS here because node.next is now null!
Look at what is left in memory:
head
[ 7 ] ──► null

The first node was NEVER checked by the while loop!
That is why the author had to add this awkward trailing check:
if head.val == val:
    head = head.next   <-- chops off the last remaining 7!
```

This works, but having a trailing `if head.val == val` outside the loop is easy to forget in an interview. That is why **Method 1 (Sentinel Dummy)** is preferred.

---

### Method 3: Recursion (The 3-line functional way)

Think of recursion as asking: "Assume the rest of the list has already been completely cleaned up. Does my current node stay or go?"

```python
def removeElements_recursive(head, val):
    if not head:
        return None

    # 1. Clean up everything downstream first
    head.next = removeElements_recursive(head.next, val)

    # 2. If current node matches, skip it by returning head.next
    return head.next if head.val == val else head
```

The call stack dives to the end of the list and cleans nodes on the way back up. It is elegant to write, but costs $\mathcal{O}(n)$ call stack memory.

---

## Method comparison

| Method | Time | Space | Cleanliness & Traps |
| :--- | :--- | :--- | :--- |
| **1. Sentinel Dummy** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | **Best for interviews.** 1 loop, zero special cases for `head`. |
| **2. Two-Pass / Head Check** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Loop only checks `node.next`; requires trailing `if head.val == val`. |
| **3. Recursive** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Clean 3-liner, but risks stack overflow on lists with $> 1000$ nodes. |

---

## Traps to watch for

* **Advancing `cur` after deleting:** Never write `cur = cur.next` inside the deletion branch. If you delete node 6 from `[2, 6, 6, 3]` and advance `cur`, you land on `3` and skip checking the second `6`!
* **Empty list check:** In Method 2, always check `if not head: return None` upfront, otherwise `node.next` crashes on empty inputs.

---

## Solutions

<details>
<summary>Spoiler: Solution Code (Method 1: Sentinel Dummy - Recommended)</summary>

```python
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        cur = dummy

        while cur.next:
            if cur.next.val == val:
                cur.next = cur.next.next  # Snip! Do NOT advance cur
            else:
                cur = cur.next            # Safe to advance cur

        return dummy.next
```

</details>

<details>
<summary>Spoiler: Solution Code (Method 2: Without Dummy)</summary>

```python
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        if not head:
            return None

        node = head
        while node and node.next:
            if node.next.val == val:
                node.next = node.next.next
            else:
                node = node.next

        if head.val == val:
            head = head.next

        return head
```

</details>

<details>
<summary>Spoiler: Solution Code (Method 3: Recursive)</summary>

```python
class Solution:
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        if not head:
            return None
        head.next = self.removeElements(head.next, val)
        return head.next if head.val == val else head
```

</details>

## Complexity

* **Time:** $\mathcal{O}(n)$ single pass across all nodes.
* **Space:** $\mathcal{O}(1)$ auxiliary memory for Methods 1 and 2; $\mathcal{O}(n)$ call stack for Method 3.
