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

If you are standing on `cur`, you have no backward pointer. You cannot reach behind yourself to tell the previous node to skip you. To delete a node, **you must be standing on the node right before it**. That is why linked list deletion always checks `cur.next.val == val` instead of `cur.val == val`.

```text
To delete [ 6 ]: your pointer MUST be standing on [ 2 ]!
[ 1 ] ──► [ 2 ] ──► [ 6 ] ──► [ 3 ]
            ▲
           cur
Operation: cur.next = cur.next.next (wires [ 2 ] directly to [ 3 ])
```

The problem is: **what if the head itself needs to be deleted?** If `head.val == val`, who is standing before `head` to delete it?

---

## Three ways to solve this

### Method 1: Sentinel Dummy Node (The gold standard)

Instead of writing special checks for the head, hammer a fake anchor node `dummy = ListNode(0, head)` in front of the list.

Now **every single node in the list (including the original head) has a predecessor standing behind it**. The exact same loop deletes nodes anywhere in the list without a single edge-case `if` statement.

```text
Input: [ 7, 7, 7, 7 ], val = 7

Start:
[ dummy (0) ] ──► [ 7 ] ──► [ 7 ] ──► [ 7 ] ──► [ 7 ] ──► null
      ▲
     cur

Turn 1: cur.next is 7. Snip! cur.next = cur.next.next. Do NOT move cur!
[ dummy (0) ] ────────────► [ 7 ] ──► [ 7 ] ──► [ 7 ] ──► null
      ▲
     cur

Turn 2: cur.next is still 7! Snip again!
[ dummy (0) ] ──────────────────────► [ 7 ] ──► [ 7 ] ──► null
      ▲
     cur

Turn 3 & 4: Snip remaining 7s.
[ dummy (0) ] ──────────────────────────────────────────► null
      ▲
     cur

Return dummy.next -> null (clean empty list!)
```

```playthrough
{
  "algorithm": "remove_elements",
  "initial": [1, 2, 6, 3, 4, 5, 6],
  "target": 6
}
```

#### Algorithm steps:
* **1. Anchor sentinel:** Create `dummy = ListNode(0, head)`, set `cur = dummy`.
* **2. Inspect cur.next:** While `cur.next` is not None:
  * If `cur.next.val == val`: snip out the node via `cur.next = cur.next.next`. **Do not advance cur**, because the newly attached node might also have value `val`!
  * Else: safe to advance `cur = cur.next`.
* **3. Return:** `dummy.next` (skips the dummy placeholder and returns the real head).

---

### Method 2: Without dummy node (Leading head trimming)

If you do not want to use a dummy node, you must handle the head in two separate passes:

1. **Trim the front:** Use a `while` loop to advance `head` as long as `head.val == val`.
2. **Trim the rest:** Walk a pointer `cur = head` and delete from `cur.next` onward.

```python
def removeElements_no_dummy(head, val):
    # Pass 1: Chop off all matching heads from the front
    while head and head.val == val:
        head = head.next

    # Pass 2: Clean up the rest
    cur = head
    while cur and cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next

    return head
```

#### Why the code you copied worked (and why it felt weird):
In the solution you copied:
```python
node = head
while node and node.next:
    if node.next.val == val:
        node.next = node.next.next
    else:
        node = node.next
if head.val == val:
    head = head.next
```
That code started walking from `head` without trimming the front first. So on `[7, 7, 7, 7]`, `node` held onto the first `7` while the while loop deleted all the 7s *after* it. That left a single `[7]`. Then the trailing line `if head.val == val: head = head.next` finally chopped off that last remaining 7. It worked, but it is much easier to make a mistake with that ordering than with Method 1's dummy node.

---

### Method 3: Recursion (The 3-line functional way)

Think of recursion as asking: "Assume the rest of the list has already been completely cleaned up. Does my current node stay or go?"

```python
def removeElements_recursive(head, val):
    if not head:
        return None

    # Clean up everything downstream first
    head.next = removeElements_recursive(head.next, val)

    # If current node matches, skip it by returning head.next
    return head.next if head.val == val else head
```

The call stack dives to the end of the list and cleans nodes on the way back up. It is elegant to write, but costs $\mathcal{O}(n)$ call stack memory.

---

## Method comparison

| Method | Time | Space | Cleanliness & Traps |
| :--- | :--- | :--- | :--- |
| **1. Sentinel Dummy** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | **Best for interviews.** 1 loop, zero special cases for `head`. |
| **2. Two-Pass Trim** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Requires two separate loops; easy to forget the leading `while` check. |
| **3. Recursive** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Clean 3-liner, but risks stack overflow on lists with $> 1000$ nodes. |

---

## Traps to watch for

* **Advancing `cur` after deleting:** Never write `cur = cur.next` inside the deletion branch. If you delete node 6 from `[2, 6, 6, 3]` and advance `cur`, you land on `3` and skip checking the second `6`!
* **Using `while head.val == val:` without checking `head`:** In Method 2, always write `while head and head.val == val:`. If all nodes match, `head` becomes `None` and `head.val` crashes with an `AttributeError`.

---

## Solutions

<details>
<summary>Spoiler: Solution Code (Method 1: Sentinel Dummy - Recommended)</summary>

```python
class Solution:
    def removeElements(self, head: ListNode | None, val: int) -> ListNode | None:
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
    def removeElements(self, head: ListNode | None, val: int) -> ListNode | None:
        while head and head.val == val:
            head = head.next

        cur = head
        while cur and cur.next:
            if cur.next.val == val:
                cur.next = cur.next.next
            else:
                cur = cur.next

        return head
```

</details>

<details>
<summary>Spoiler: Solution Code (Method 3: Recursive)</summary>

```python
class Solution:
    def removeElements(self, head: ListNode | None, val: int) -> ListNode | None:
        if not head:
            return None
        head.next = self.removeElements(head.next, val)
        return head.next if head.val == val else head
```

</details>

## Complexity

* **Time:** $\mathcal{O}(n)$ single pass across all nodes.
* **Space:** $\mathcal{O}(1)$ auxiliary memory for Methods 1 and 2; $\mathcal{O}(n)$ call stack for Method 3.
