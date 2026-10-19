# LeetCode 160: Intersection of Two Linked Lists

> **Pattern:** Two Pointers (Length Offset & Track Switch) / Hash Set  
> **Difficulty:** Easy  
> **Link:** [LeetCode 160](https://leetcode.com/problems/intersection-of-two-linked-lists/)

## The problem

Given the heads of two singly linked lists `headA` and `headB`, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return `None`.

The intersection must be determined by reference equality (the exact same memory object), not by node values (`.val`). The lists must retain their original structure after the function runs.

```text
List A:          [4] ──► [1] ──┐
                               ▼
                              [8] ──► [4] ──► [5] ──► None
                               ▲
List B:   [5] ──► [6] ──► [1] ──┘

Output: Intersected at '8' (node reference, not value 1 or 8)
```

## Why value comparison fails

Two completely unrelated nodes in different lists can hold the exact same value. In the example above, both lists contain a node with value `1` before the intersection, but they reside at different memory addresses. We only care when two pointers refer to the exact same physical node (`pA is pB` or `pA == pB`).

---

## Approach 1: Hash set of node references

Walk list A and add each node reference into a hash set. Then walk list B and check if any node is already in the set.

### Algorithm steps:
* **1. Store List A:** Walk `cur = headA` and insert each node into `seen = set()`.
* **2. Lookup in List B:** Walk `cur = headB`. If `cur in seen`, return `cur` immediately.
* **3. No intersection:** If the loop ends without a match, return `None`.

* **Time Complexity:** $\mathcal{O}(m + n)$
* **Space Complexity:** $\mathcal{O}(m)$

---

## Approach 2: Length difference offset (Optimal O(1) space)

If List A has length $m$ and List B has length $n$, the difference in lengths is $d = |m - n|$. Since the shared intersection tail has the exact same number of nodes in both lists, any difference in total length must come entirely from the prefix before the intersection.

### Algorithm steps:
* **1. Measure lengths:** Count nodes in list A (`lenA`) and list B (`lenB`).
* **2. Align starting points:** Advance the pointer on the longer list by $|lenA - lenB|$ steps so both pointers are equidistant from the end.
* **3. Walk together:** Advance both pointers one node at a time. The moment `curA == curB`, that node is the intersection.
* **4. Return result:** If both reach `None`, there is no intersection.

* **Time Complexity:** $\mathcal{O}(m + n)$
* **Space Complexity:** $\mathcal{O}(1)$

---

## Approach 3: Two-pointer track switch (Cleanest O(1) space)

Instead of explicitly counting lengths and writing separate alignment branches, let two pointers switch tracks when they reach the end:
* When pointer `pA` hits the end of List A (`None`), redirect it to `headB`.
* When pointer `pB` hits the end of List B (`None`), redirect it to `headA`.

```text
Path of pA: [List A prefix] + [Shared Tail] + [List B prefix] + [Shared Tail]
Path of pB: [List B prefix] + [Shared Tail] + [List A prefix] + [Shared Tail]
```

Because both pointers travel exactly $m + n$ total steps:
* **If they intersect:** They will collide at the intersection node at the start of their second pass.
* **If they do not intersect:** Both will hit `None` simultaneously after traversing $m + n$ steps, terminating the loop (`pA == pB == None`).

### Algorithm steps:
* **1. Initialize runners:** Set `pA = headA` and `pB = headB`.
* **2. Traverse and switch:** While `pA != pB`:
  * If `pA` is not `None`: `pA = pA.next`, else `pA = headB`.
  * If `pB` is not `None`: `pB = pB.next`, else `pB = headA`.
* **3. Return collision:** Return `pA` (either the shared intersection node or `None`).

---

## Solutions

### Approach 2: Length difference offset

<details>
<summary>Spoiler: Solution Code (Approach 2)</summary>

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode | None:
        lenA, lenB = 0, 0
        curA, curB = headA, headB

        while curA:
            lenA += 1
            curA = curA.next

        while curB:
            lenB += 1
            curB = curB.next

        curA, curB = headA, headB

        if lenA > lenB:
            for _ in range(lenA - lenB):
                curA = curA.next
        else:
            for _ in range(lenB - lenA):
                curB = curB.next

        while curA and curB:
            if curA == curB:
                return curA
            curA = curA.next
            curB = curB.next

        return None
```

</details>

### Approach 3: Track switch

<details>
<summary>Spoiler: Solution Code (Approach 3)</summary>

```python
class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode | None:
        pA, pB = headA, headB

        while pA != pB:
            pA = pA.next if pA else headB
            pB = pB.next if pB else headA

        return pA
```

</details>

## Complexity comparison

| Approach | Time Complexity | Space Complexity | Description |
| :--- | :--- | :--- | :--- |
| **1. Hash Set** | $\mathcal{O}(m + n)$ | $\mathcal{O}(m)$ | Stores references of List A in a set |
| **2. Length Offset** | $\mathcal{O}(m + n)$ | $\mathcal{O}(1)$ | Counts lengths, skips offset $d$, walks together |
| **3. Track Switch** | $\mathcal{O}(m + n)$ | $\mathcal{O}(1)$ | Switches heads on reaching `None`, collides in $\le 2$ passes |
