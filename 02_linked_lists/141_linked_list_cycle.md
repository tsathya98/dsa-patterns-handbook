# LeetCode 141 & 142: Linked List Cycle

> **Pattern:** Fast and slow pointers (Floyd's tortoise and hare)  
> **Difficulty:** Easy (LC 141) / Medium (LC 142)  
> **Links:** [LeetCode 141](https://leetcode.com/problems/linked-list-cycle/) | [LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/)

## The problem

- **LC 141:** Given `head`, determine if the linked list has a cycle in it.
- **LC 142:** If a cycle exists, return the exact node where the cycle begins (otherwise return `None`).

## The core trick

A hash set of visited nodes takes $\mathcal{O}(n)$ extra memory. To detect a cycle in $\mathcal{O}(1)$ space, put two pointers on the track at different speeds:
- `slow` moves 1 step per turn (`slow = slow.next`).
- `fast` moves 2 steps per turn (`fast = fast.next.next`).

If the list has an end, `fast` reaches `None` and you return `False`. If the list loops back on itself, `fast` enters the loop first and closes the distance to `slow` by 1 node every turn until they land on the exact same node (`slow == fast`).

### Finding the cycle entrance (LC 142)
Suppose the straight path before the cycle has length $L$, the cycle has circumference $C$, and the pointers collide $K$ steps after the cycle entrance:
- `slow` traveled $L + K$ steps.
- `fast` traveled $2(L + K)$ steps, which is also $L + K + nC$ (some number of full laps $n$ around the cycle).
- Subtracting the two gives $L + K = nC$, or $L = nC - K$.

This equation means the distance from `head` to the cycle entrance ($L$) equals the remaining distance from the collision point forward to the cycle entrance ($C - K$, plus any full laps). If you leave `slow` at the collision spot, start a second pointer `slow2 = head`, and walk both 1 step at a time, they are guaranteed to meet at the cycle entrance.

## Traps to watch for

- **Loop condition order:** Always write `while fast and fast.next:`. Checking `fast.next` before verifying `fast` is non-null crashes with an `AttributeError` when `fast` steps onto `None` on an even-length list.
- **Checking `slow.val == fast.val`:** Different nodes can hold duplicate numbers. Always compare object identity (`slow == fast` or `slow is fast`).
- **Checking `if slow == fast:` before moving pointers:** Since both start at `head`, checking before stepping immediately triggers a false positive on turn 0.

## Solution

<details>
<summary>Spoiler: Solution Code</summary>

```python
# Part 1: LeetCode 141 - Does a cycle exist?
class Solution141:
    def hasCycle(self, head: ListNode | None) -> bool:
        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True

        return False


# Part 2: LeetCode 142 - Where does the cycle begin?
class Solution142:
    def detectCycle(self, head: ListNode | None) -> ListNode | None:
        slow = fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return None

        slow2 = head
        while slow != slow2:
            slow = slow.next
            slow2 = slow2.next

        return slow
```

</details>

## Complexity

- **Time:** $\mathcal{O}(n)$ since `fast` laps `slow` within at most one full cycle after `slow` enters the loop.
- **Space:** $\mathcal{O}(1)$ auxiliary memory.
