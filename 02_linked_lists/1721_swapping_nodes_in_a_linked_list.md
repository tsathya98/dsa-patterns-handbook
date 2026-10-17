# LeetCode 1721: Swapping Nodes in a Linked List

> **Pattern:** Two pointers with fixed offset  
> **Difficulty:** Medium  
> **Link:** [LeetCode 1721](https://leetcode.com/problems/swapping-nodes-in-a-linked-list/)

## The problem

Given the `head` of a 1-indexed linked list and an integer `k`, swap the values of the $k$-th node from the beginning and the $k$-th node from the end, then return the head.

```text
Input:  head = [1, 2, 3, 4, 5], k = 2
Output: [1, 4, 3, 2, 5]
Explanation: 2nd from start is 2; 2nd from end is 4.
```

## Why the naive way fails

Dumping the list into an array uses $\mathcal{O}(n)$ extra memory. Worse, if you try to swap array elements inside the same loop that writes values back into the linked list:
```python
for i in range(len(lst)):
    if i == k - 1:
        lst[k - 1], lst[len(lst) - k] = lst[len(lst) - k], lst[k - 1]
    cur.val = lst[i]
```
this breaks whenever `k` is in the second half of the list (like `[100, 90], k = 2`). Index `0` gets written to the list before the swap happens at `i = 1`, so both nodes end up with `100`.

## The core trick

You can find both target nodes in a single pass with $\mathcal{O}(1)$ space using a fixed gap between two pointers:
1. Start `first = head` and walk it `k - 1` steps forward. Now `first` sits on the $k$-th node from the beginning. Keep `first` parked there so you can swap its value at the end.
2. Create a runner `fast = first` and a follower `second = head`. They are now separated by `k - 1` steps.
3. Advance both `fast` and `second` together until `fast` lands on the final node (`while fast.next:`).
4. Because `fast` is at the end (1st node from the back) and `second` trails by `k - 1` steps, `second` is now sitting on the $k$-th node from the end. Swap `first.val` and `second.val`.

### Algorithm steps:
* **1. Locate k-th node from start:** Initialize `first = head` and walk forward `k - 1` times. Keep `first` parked on this node.
* **2. Initialize fixed-gap runner:** Set `fast = first` and follower `second = head` (preserving a gap of `k - 1` steps).
* **3. Slide window to tail:** While `fast.next` is not None, advance both `fast = fast.next` and `second = second.next`.
* **4. Swap values and return:** Swap the values `first.val, second.val = second.val, first.val`, then return `head`.

## Step-by-step trace

Trace on `head = [1, 2, 3, 4, 5]`, `k = 2`:

```text
Step 1: Walk first k - 1 = 1 step from head
  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None
              ▲
            first (2nd from start)

Step 2: Put second at head, fast at first
  second     fast
    │         │
    ▼         ▼
  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None

Step 3: Slide second and fast together while fast.next is not None
                                second     fast
                                  │         │
                                  ▼         ▼
  [ 1 ] ──► [ 2 ] ──► [ 3 ] ──► [ 4 ] ──► [ 5 ] ──► None
                                  ▲
                            2nd from end

Step 4: Swap first.val (2) and second.val (4)
  Result: [1, 4, 3, 2, 5]
```

## Traps to watch for

- **The fencepost error (`range(k)` instead of `range(k - 1)`):** `first` already starts on Node 1 (`head`). Reaching Node $k$ takes $k - 1$ steps. Using `range(k)` overshoots by one node and crashes with an `AttributeError` when $k$ equals the list length.
- **Looping `while fast:` instead of `while fast.next:`:** If `fast` walks all the way onto `None`, `second` also advances one step too far. Stop as soon as `fast` lands on the tail node (`fast.next is None`).

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def swapNodes(self, head: ListNode | None, k: int) -> ListNode | None:
        first = second = head

        for _ in range(k - 1):
            first = first.next

        fast = first
        while fast.next:
            fast = fast.next
            second = second.next

        first.val, second.val = second.val, first.val
        return head
```

</details>

## Complexity

- **Time:** $\mathcal{O}(n)$ single pass.
- **Space:** $\mathcal{O}(1)$ auxiliary memory.
