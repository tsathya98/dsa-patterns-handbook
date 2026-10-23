# LeetCode 19: Remove Nth Node From End of List

> **Pattern:** Two pointers with fixed offset + dummy node  
> **Difficulty:** Medium  
> **Access:** Free  
> **Link:** [LeetCode 19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

## The problem

Given the `head` of a linked list, remove the $n$-th node from the end of the list and return its head.

```text
Input:  head = [1, 2, 3, 4, 5], n = 2
Output: [1, 2, 3, 5] (Node 4 is removed)
```

---

## The two standard approaches

| Feature | Approach 1: Two-Pass | Approach 2: One-Pass (Optimal) |
| :--- | :--- | :--- |
| **Passes over list** | 2 passes | 1 single pass |
| **Mental model** | Count length $L$, walk to index $L - n$ | Fixed-gap ruler ($n$ steps) between two pointers |
| **Head removal handling** | Requires special check (`if k == 0: return head.next`) | Handled automatically by `dummy` sentinel |
| **Operations** | $\sim 2L$ node visits | Exactly $L$ node visits |
| **Time Complexity** | $\mathcal{O}(L)$ | $\mathcal{O}(L)$ |
| **Space Complexity** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ |

---

## Approach 1: Two-pass (Length counting)

This is the most intuitive approach and the one to articulate first in an interview.

### The core logic:
1. If the list has total length $L$, the $n$-th node from the end is at 0-based index $L - n$ from the start.
2. To delete the node at index $L - n$, you need to land on its **predecessor** at index $L - n - 1$.
3. If $L == n$, the node to remove is the original head, so you return `head.next`.

### Algorithm steps:
* **1. Pass 1 (Count length):** Traverse the list from `head` using `cur = cur.next` while incrementing `count`.
* **2. Check head deletion:** Compute $k = \text{count} - n$. If $k == 0$, return `head.next`.
* **3. Pass 2 (Walk to predecessor):** Reset `cur = head`. Walk forward $k - 1$ steps.
* **4. Bypass victim:** Set `cur.next = cur.next.next`.
* **5. Return:** Return `head`.

<details>
<summary>Spoiler: Approach 1 Solution Code (Two-Pass)</summary>

```python
class SolutionTwoPass:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        if not head:
            return None

        # Pass 1: Count total length
        count = 0
        cur = head
        while cur:
            count += 1
            cur = cur.next

        # If removing the head node
        k = count - n
        if k == 0:
            return head.next

        # Pass 2: Walk to predecessor (k - 1 hops)
        cur = head
        for _ in range(k - 1):
            cur = cur.next

        # Bypass victim node
        if cur and cur.next:
            cur.next = cur.next.next

        return head
```

</details>

---

## Approach 2: One-pass (Fixed-gap measuring stick)

When the interviewer asks: *"Can you do it in a single pass without counting the length first?"*, use the rigid measuring stick pattern.

Think of `left` and `right` as the two ends of a rigid ruler of length $n$:
1. Attach a `dummy` sentinel node before `head` (`dummy = ListNode(0, head)`).
2. Start `left` at `dummy` and `right` at `head`.
3. Advance `right` forward by $n$ steps. Now `left` and `right` have a fixed gap of $n$ nodes between them.
4. Slide both `left` and `right` forward one step at a time until `right` walks off the end into `None`.
5. Because the gap stayed fixed, `left` lands precisely on the **predecessor** of the victim node.
6. Bypass it with `left.next = left.next.next`.

```text
Trace on head = [1, 2, 3, 4, 5], n = 2:

1. Setup: left on dummy, right on head
   [dummy] ────► [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
      ▲            ▲
     left        right

2. Advance right by n = 2 steps:
   [dummy] ────► [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
      ▲                                    ▲
     left                                right

3. Slide both together until right is None:
   [dummy] ────► [ 1 ] ────► [ 2 ] ────► [ 3 ] ────► [ 4 ] ────► [ 5 ] ────► None
                                           ▲                                   ▲
                                          left                               right

4. Bypass target node (left.next = left.next.next):
   Node 3 skips Node 4 and points directly to Node 5.
```

### Algorithm steps:
* **1. Initialize sentinel:** Create `dummy = ListNode(0, head)`, set `left = dummy`, and set `right = head`.
* **2. Establish fixed gap:** Advance `right` forward $n$ steps.
* **3. Slide window until right reaches None:** While `right` is not None, advance both `left = left.next` and `right = right.next`.
* **4. Bypass target node:** Set `left.next = left.next.next`.
* **5. Return:** Return `dummy.next`.

<details>
<summary>Spoiler: Approach 2 Solution Code (One-Pass)</summary>

```python
class SolutionOnePass:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        dummy = ListNode(0, head)
        left = dummy
        right = head

        # Step 1: Create fixed window of n steps
        for _ in range(n):
            right = right.next

        # Step 2: Slide both pointers until right walks off list
        while right:
            left = left.next
            right = right.next

        # Step 3: Unlink victim node (left is at predecessor)
        left.next = left.next.next

        return dummy.next
```

</details>

---

## Why the dummy node eliminates all edge cases

Without `dummy`:
* Deleting the only node (`head = [1], n = 1`) crashes because there is no predecessor.
* Deleting the head of a list (`head = [1, 2], n = 2`) requires manual `if` branches.

With `dummy`:
* If $n$ equals the list length, `right` walks all the way to `None`, leaving `left` sitting on `dummy`.
* Running `left.next = left.next.next` unhooks the head node cleanly (`dummy.next` becomes `head.next`).
* Zero special-case branching needed.

---

## Complexity

* **Time Complexity:** $\mathcal{O}(L)$ where $L$ is the number of nodes. Approach 1 takes $\sim 2L$ operations; Approach 2 takes exactly $L$ operations.
* **Space Complexity:** $\mathcal{O}(1)$ auxiliary memory in both approaches.
