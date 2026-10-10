# 🗳️ 169. Majority Element

> **Difficulty:** Easy (LeetCode Label) / **Classic FAANG Follow-up**  
> **Pattern:** Boyer-Moore Voting Algorithm (The Mutual Cancellation Pattern)  
> **Constraints:** $\mathcal{O}(n)$ Time, strictly $\mathcal{O}(1)$ Auxiliary Space.

---

## 💡 1. The 3-Tier Interview Ladder

When an interviewer asks this problem, they want to observe your thought hierarchy:

```text
Tier 1: Hash Map / Counter       -> O(n) Time, O(n) Space  (Mention first!)
Tier 2: Sorting Middle Element   -> O(n log n) Time, O(1) Space
Tier 3: Boyer-Moore Voting       -> O(n) Time, O(1) Space  (The FAANG Gold Standard)
```

> 🎯 **Pro Interview Strategy:**  
> Start by stating: *"The straightforward solution is a HashMap/Counter to tally frequencies in $\mathcal{O}(n)$ time and $\mathcal{O}(n)$ space. But since the majority element appears more than $\lfloor n / 2 \rfloor$ times, we can optimize space to $\mathcal{O}(1)$ using Boyer-Moore Voting."*

---

## ⚔️ 2. The Mental Model: The Battle Royale Arena

The problem guarantees that the majority element appears **strictly more than 50% of the time**:

$$\text{Majority Count} > \frac{n}{2} \implies \text{Majority Count} - \text{All Opponents Combined} > 0$$

### The Analogy:
Imagine an arena where:
* The **Majority Clan** has $> 50\%$ of all warriors.
* All other minority clans combined have $< 50\%$ of the warriors.
* **The Rule:** Whenever two warriors from **different clans** fight, they eliminate each other (1-for-1 mutual cancellation).

Even if every single minority warrior teams up to eliminate a majority warrior, **the majority clan is mathematically guaranteed to have survivors left standing!**

---

## ❓ 3. Why is it Safe to Reset when `count == 0`?

```text
nums = [ 1 , 2 , 1 , 2 ,  3 , 3 , 3 ]
        └─────────────┘
       Two 1s and Two 2s
          (Count = 0)
```

In that prefix `[1, 2, 1, 2]`:
* `1` appeared 2 times (50%).
* Opponents appeared 2 times (50%).

> 🔑 **The Mathematical Miracle:**  
> If you discard a subsegment where elements cancelled each other out equally,  
> **the true majority element in the entire array STILL maintains a majority (> 50%) in the remaining subarray!**  
> Looking at the remainder: `[ 3 , 3 , 3 ]` $\implies$ `3` is still the majority!

---

## ⚡ 4. Python Bytecode Optimization: Why `elif` Beats Two `if` Checks

Many candidates write:
```python
# ⚠️ Redundant evaluation on reset!
if count == 0:
    candidate = num
if candidate == num:
    count += 1
else:
    count -= 1
```

When `count == 0`, you set `candidate = num`. Then Python immediately evaluates `if candidate == num:`, which is **guaranteed to be True**!

### The Faster `elif` Version:
When `count == 0`, settle `count = 1` immediately and skip all other checks:

```python
class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        candidate = None
        count = 0

        for num in nums:
            if count == 0:
                candidate = num
                count = 1
            elif candidate == num:
                count += 1
            else:
                count -= 1

        return candidate
```

*(This cuts out 6–8 CPU bytecode instructions on every reset, dropping runtime into the top percentile!)*

---

## 📊 5. Complexity Comparison

| Approach | Time Complexity | Auxiliary Space | Best Used For |
| :--- | :---: | :---: | :--- |
| **`Counter(nums)`** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Rapid prototyping, when $> 50\%$ constraint isn't guaranteed |
| **`nums.sort()`** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(1)$ | Quick 1-liner (`nums[len(nums) // 2]`) |
| **Boyer-Moore Voting** | **$\mathcal{O}(n)$** | **$\mathcal{O}(1)$** | **Strict $\mathcal{O}(1)$ space interview requirement** |
