# 🔁 LeetCode 141 & 142: Linked List Cycle Detection

> **Pattern:** Fast & Slow Pointers (Floyd's Tortoise and Hare)  
> **Difficulty:** Easy / Medium

---

## 📌 Problem Description
Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

---

## 💡 The Race Track Analogy
Imagine two runners on a running track:
- 🐢 **Slow runner:** Runs 1 meter/sec.
- 🐇 **Fast runner:** Runs 2 meters/sec.

1. **If the track is straight (no cycle):** The fast runner will reach the finish line (`None`).
2. **If the track is circular (has a cycle):** The fast runner will lap the slow runner and they will **inevitably crash into each other**.

---

## 🔍 Part 1: Does a cycle exist? (LeetCode 141)

```python
class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next          # 1 step
            fast = fast.next.next     # 2 steps
            
            if slow == fast:          # Crash detected! Cycle exists!
                return True
                
        return False  # Fast hit None -> No cycle!
```

---

## 🔍 Part 2: Where does the cycle begin? (LeetCode 142)

Once `slow` and `fast` meet:
1. Leave `slow` where it is.
2. Move a new pointer `slow2` to the `head`.
3. Move both `slow` and `slow2` at **1 step at a time**.
4. **The exact node where they collide is the start of the cycle!**

```python
class Solution:
    def detectCycle(self, head: ListNode) -> ListNode:
        slow = fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            return None  # No cycle
            
        # Mathematical convergence to cycle entry point:
        slow2 = head
        while slow != slow2:
            slow = slow.next
            slow2 = slow2.next
            
        return slow  # Start of cycle
```
