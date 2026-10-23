# LeetCode 142: Linked List Cycle II

> **Pattern:** Floyd's cycle detection (Two-phase collision)  
> **Difficulty:** Medium  
> **Access:** Free  
> **Link:** [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/)

## The problem

Given the `head` of a linked list, return the node where the cycle begins. If there is no cycle, return `None`.

Do not modify the linked list. Solve it using $\mathcal{O}(1)$ memory.

```text
Input:  head = [ 3, 2, 0, -4 ], pos = 1 (tail connects to node index 1)
[ 3 ] ──► [ 2 ] ──► [ 0 ] ──► [ -4 ]
            ▲                     │
            └─────────────────────┘
Output: Node with value 2
```

## The core trick

Floyd's Tortoise and Hare algorithm runs in two distinct phases:

### Phase 1: Detect cycle and find meeting point
Start `slow` and `fast` at `head`. Move `slow` by 1 step and `fast` by 2 steps. If `fast` or `fast.next` hits `None`, there is no cycle. If they collide (`slow == fast`), a cycle exists, and they are sitting at the **Meeting Point (MP)**.

### Phase 2: Find cycle entrance via mathematical alignment
Leave `fast` at the meeting point. Reset `slow` back to `head`. Move **both pointers 1 step at a time at the same speed**. The node where they collide is guaranteed to be the cycle start node.

### The mathematical proof:
Let $a$ be the distance from `head` to cycle start, $b$ be distance from cycle start to meeting point, and $l$ be the cycle loop length.

When they meet in Phase 1:
$$\text{Distance}(\text{slow}) = a + b + c_1 \cdot l$$
$$\text{Distance}(\text{fast}) = a + b + c_2 \cdot l$$

Since $\text{Distance}(\text{fast}) = 2 \cdot \text{Distance}(\text{slow})$:
$$a + b + c_2 \cdot l = 2a + 2b + 2c_1 \cdot l$$
$$a = (c_2 - 2c_1 - 1) \cdot l + (l - b)$$

Because $(c_2 - 2c_1 - 1)$ is an integer number of full loops $k \ge 0$:
$$a = k \cdot l + (l - b)$$

Walking $a$ steps from `head` equals walking $(l - b)$ steps from the meeting point. Therefore, both pointers stepping at 1 node per iteration will meet at the cycle entrance.

### Algorithm steps:
* **1. Phase 1 (Find meeting point):** Initialize `slow = fast = head`. Advance `slow = slow.next`, `fast = fast.next.next`. If `fast` reaches None, return None. Break when `slow == fast`.
* **2. Phase 2 (Find cycle entrance):** Reset `slow = head`.
* **3. Advance at equal speed:** While `slow != fast`, advance `slow = slow.next` and `fast = fast.next`.
* **4. Return:** Return `slow`.

## Traps to watch for

* **Advancing fast by 2 in Phase 2:** In Phase 2, **both pointers must advance by exactly 1 step**. Advancing at different speeds breaks the mathematical distance alignment.
* **Returning None if head is None:** Handled automatically if checking `while fast and fast.next:`.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
class Solution:
    def detectCycle(self, head: ListNode | None) -> ListNode | None:
        slow = fast = head

        # Phase 1: Find collision point
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return None  # No cycle found

        # Phase 2: Find cycle start
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next

        return slow
```

</details>

## Complexity

* **Time:** $\mathcal{O}(n)$ total. Phase 1 takes at most $\mathcal{O}(n)$ steps; Phase 2 takes at most $\mathcal{O}(n)$ steps.
* **Space:** $\mathcal{O}(1)$ auxiliary memory (only pointer references).
