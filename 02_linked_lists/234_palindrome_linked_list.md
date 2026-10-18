# LeetCode 234: Palindrome Linked List

> **Pattern:** Fast/slow midpoint + in-place reversal + inward comparison  
> **Difficulty:** Easy (with Medium $\mathcal{O}(1)$ space follow-up)  
> **Link:** [LeetCode 234](https://leetcode.com/problems/palindrome-linked-list/)

## The problem

Given the `head` of a singly linked list, return `True` if it reads the same forward and backward, or `False` otherwise.

```text
Input:  1 -> 2 -> 2 -> 1 -> None  => Output: True
Input:  1 -> 2 -> None            => Output: False
```

## Why the naive way fails the follow-up

Dumping node values into a Python list `vals` and squeezing two indices (`l = 0, r = len(vals) - 1`) takes $\mathcal{O}(n)$ time and works well as a quick first pass. (If you do use an array, prefer the two-pointer `l < r` loop over `vals == vals[::-1]` so you avoid allocating a second copy of the array and can exit early on the first mismatch.)

However, copying values into an array uses $\mathcal{O}(n)$ extra memory. The standard follow-up asks for $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space, which means you have to check the list in-place.

## The core trick

Since you cannot walk backward from the tail of a singly linked list, reverse the second half in-place so its arrows point inward toward the middle:

1. **Find the end of the first half (tortoise and hare):** Start `slow = head` and `fast = head`. Loop while `fast.next and fast.next.next:` so `slow` stops on the last node of the first half (or the exact middle node on odd-length lists).
2. **Reverse the second half in-place:** Starting at `slow.next`, run the standard 4-step pointer flip ([LC 206](./206_reverse_linked_list.md)). At the end, `prev` points to the original tail.
3. **Compare both halves inward:** Walk `first = head` and `second = prev` together while `second` is not `None`. If `first.val != second.val`, return `False`.
4. **Optional cleanup:** If the caller still needs the input list intact after the check, reverse the second half a second time and reattach it to `slow.next`.

### Algorithm steps:
* **1. Find end of first half:** Advance `slow = head` and `fast = head` while `fast.next` and `fast.next.next` exist, leaving `slow` at the midpoint.
* **2. Reverse second half in-place:** Reverse the sublist starting from `slow.next` using a 3-pointer flip (`prev = None`, `cur = slow.next`), yielding new head `prev`.
* **3. Compare values inward:** Set `first = head` and `second = prev`. While `second` is not None:
  * If `first.val != second.val`, return `False`.
  * Advance `first = first.next` and `second = second.next`.
* **4. Terminate and return:** When `second` reaches None without any mismatch, return `True` (optionally re-reverse the second half to restore original list structure).

## Step-by-step trace

### 1. Find midpoint (`while fast.next and fast.next.next:`):
```text
Original: [ 1 ] ──► [ 2 ] ──► [ 2 ] ──► [ 1 ] ──► None
                      ▲         ▲
                     slow      fast
```
* `slow` stops on the first middle node `[ 2 ]`.
* The sublist to reverse is `cur = slow.next` (`[ 2 ] -> [ 1 ] -> None`).

### 2. Frame-by-frame second half reversal (`while cur:`):

**Frame 0: Initial setup**
```text
First half:          [ 1 ] ──► [ 2 ] (slow)
Second half:                   [ 2 ] ──────► [ 1 ] ──────► None
                                 ▲
                                cur
prev = None
```

**Frame 1: Iteration 1 (reversing the first node of second half)**
```text
Step 1 (nn = cur.next):       [ 2 ] ──────► [ 1 ] ──────► None
                                ▲             ▲
                               cur            nn

Step 2 (cur.next = prev):    None ◄──── [ 2 ]        [ 1 ] ──────► None
                               ▲          ▲            ▲
                              prev       cur           nn

Steps 3 & 4 (slide forward): None ◄──── [ 2 ]        [ 1 ] ──────► None
                                          ▲            ▲
                                         prev         cur
```

**Frame 2: Iteration 2 (reversing the last node)**
```text
Step 1 (nn = cur.next):      None ◄──── [ 2 ]        [ 1 ] ──────► None
                                          ▲            ▲             ▲
                                         prev         cur            nn

Step 2 (cur.next = prev):    None ◄──── [ 2 ] ◄────── [ 1 ]
                                          ▲             ▲
                                         prev          cur

Steps 3 & 4 (slide forward): None ◄──── [ 2 ] ◄────── [ 1 ]       (cur = None -> loop ends)
                                                        ▲
                                                       prev
```

### 3. Comparison inward (`first = head, second = prev`):
```text
First half:                 [ 1 ] ──► [ 2 ]
                             ▲
                            first

Reversed second half:       None ◄── [ 2 ] ◄── [ 1 ]
                                                ▲
                                              second
```
* **Step 1:** `first.val` (1) == `second.val` (1). Advance `first = first.next`, `second = second.next`.
* **Step 2:** `first.val` (2) == `second.val` (2). Advance both.
* **Step 3:** `second` is `None` -> All paired nodes matched! Return `True`.

*(On odd lists like `[1, 2, 3, 2, 1]`, `slow` stops on `3`, and `slow.next` (`[2, 1]`) reverses to `None <- 2 <- 1`. Driving the comparison loop with `while second:` compares the two outer pairs and stops right before the shared middle node `3`.)*

## Traps to watch for

- **Reversing the entire list in-place:** Flipping the whole list mutates the original nodes in-place, leaving you with only the reversed list and nothing left to compare against.
- **Wrong fast-pointer condition:** Using `while fast and fast.next:` advances `slow` one node too far on even-length lists. Use `while fast.next and fast.next.next:` so `slow.next` is always the clean start of the second half.

## Solution

<details>
<summary>Spoiler: Solution Code (Both Approaches)</summary>

```python
# Approach 1: Array conversion + Two-pointer squeeze (Intuitive, O(N) space)
class Solution:
    def isPalindrome(self, head: ListNode | None) -> bool:
        lst = []
        cur = head
        while cur:
            lst.append(cur.val)
            cur = cur.next

        l, r = 0, len(lst) - 1
        while l < r:
            if lst[l] != lst[r]:
                return False
            l += 1
            r -= 1
        return True


# Approach 2: Fast/slow midpoint + In-place reversal (Optimal follow-up, O(1) space)
class SolutionOptimal:
    def isPalindrome(self, head: ListNode | None) -> bool:
        if not head or not head.next:
            return True

        # 1. Stop slow at the end of the first half
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2. Reverse the second half in-place
        prev = None
        cur = slow.next
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt

        # 3. Compare both halves inward
        first, second = head, prev
        while second:
            if first.val != second.val:
                return False
            first = first.next
            second = second.next

        return True
```

</details>

## Complexity

- **Time:** $\mathcal{O}(n)$ ($\mathcal{O}(n/2)$ to find the middle, $\mathcal{O}(n/2)$ to reverse, and $\mathcal{O}(n/2)$ to compare).
- **Space:** $\mathcal{O}(1)$ auxiliary memory.
