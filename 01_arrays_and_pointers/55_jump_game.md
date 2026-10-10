# 🎮 LeetCode 55: Jump Game – Master Study Guide

> **Difficulty:** Medium | **Top Interview 150:** Arrays / Greedy  
> **Pattern:** Greedy (Archetype 2: The Horizon / Laser Reach)  
> **Complexity:** Time: $\mathcal{O}(n)$ | Space: $\mathcal{O}(1)$  
> **Source Code:** [`55_jump_game.py`](./55_jump_game.py)

---

## 📌 Problem in Plain English

You are given an integer array `nums` where each element represents your **maximum jump power** from that stone.
Starting at index `0`, determine if you can ever reach or land on the last stone (`len(nums) - 1`).

```text
Example 1:
Input: nums = [2, 3, 1, 1, 4]
Output: true (From 0 jump 1 to stone 1; from stone 1 jump 3 to stone 4)

Example 2:
Input: nums = [3, 2, 1, 0, 4]
Output: false (Every possible jump lands directly on the '0' quicksand at index 3)
```

---

## 🧠 Mental Model: The Flashlight / Laser Reach

Do not try to simulate individual hops. Simulating hops creates a massive decision tree in your head.

Instead, ask one question as you walk forward:
> **"What is the furthest stone illuminated by my flashlight beam?" (`max_reach`)**

```text
At each stone i:
The furthest stone you could launch yourself to is: i + nums[i]
```

### The 3 Golden Rules:
1. **Can I even stand here?**  
   If `i > max_reach`, you walked past the edge of illuminated ground. You ran out of momentum. Return `False`!
2. **Can I stretch my horizon?**  
   `max_reach = max(max_reach, i + nums[i])`
3. **Did I cross the finish line?**  
   If `max_reach >= len(nums) - 1`, return `True` immediately!

---

## 💻 Production Implementation

```python
from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_reach = 0
        target = len(nums) - 1
        
        for i, jump in enumerate(nums):
            # If current stone is beyond furthest reachable horizon, we are stuck!
            if i > max_reach:
                return False
                
            # Greedily stretch our reach as far as possible
            max_reach = max(max_reach, i + jump)
            
            # Early victory check
            if max_reach >= target:
                return True
                
        return True
```

* **Time Complexity:** $\mathcal{O}(n)$ — Single pass through `nums`.
* **Space Complexity:** $\mathcal{O}(1)$ — Only one scalar integer (`max_reach`).
