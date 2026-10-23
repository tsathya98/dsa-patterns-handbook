# Cyclic sort

> **Source reference:** [AlgoMaster.io, Cyclic Sort Pattern](https://algomaster.io/learn/dsa/cycle-sort)  
> **LeetCode targets:** [LC 41. First Missing Positive](https://leetcode.com/problems/first-missing-positive/), [LC 268. Missing Number](https://leetcode.com/problems/missing-number/), [LC 287. Find Duplicate](https://leetcode.com/problems/find-the-duplicate-number/), [LC 448. Find All Disappeared Numbers](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)  
> **Category:** In-place index mapping  
> **Difficulty:** Hard / Medium

## 1. Why MAANG asks cyclic sort

Cyclic Sort is one of the highest-yield patterns in FAANG coding rounds. Whenever an interview problem states:
1. The array has length $n$.
2. The values belong to the range $[1..n]$ or $[0..n]$.
3. You must find the missing, duplicate, or first positive integer in **$\mathcal{O}(n)$ time** and strictly **$\mathcal{O}(1)$ auxiliary space**.

The key insight: **an array of size $n$ can serve as its own hashmap!**

Every integer $x \in [1..n]$ belongs at index $x - 1$:
* Value `1` belongs at `nums[0]`
* Value `2` belongs at `nums[1]`
* Value `x` belongs at `nums[x - 1]`

Instead of allocating an extra hash set (which costs $\mathcal{O}(n)$ memory), we iterate through the array and repeatedly swap each number $x$ into its designated home index `x - 1` until either:
* The current slot has the correct number (`nums[i] == i + 1`).
* The value is out of range ($x \le 0$ or $x > n$).
* The destination already contains the correct number (`nums[i] == nums[nums[i] - 1]`, detecting a duplicate).

---

## 2. Algorithm steps (LC 41 First Missing Positive)

* **1. Initialize pointer:** Set $i = 0$.
* **2. Check home position:** While $i < n$:
  * Determine destination index `correct_idx = nums[i] - 1`.
  * If $1 \le nums[i] \le n$ and $nums[i] \ne nums[correct\_idx]$, swap $nums[i]$ with $nums[correct\_idx]$. Do not increment $i$ yet; inspect the newly swapped element.
  * Otherwise (number is out of range, already placed, or a duplicate), increment $i += 1$.
* **3. Locate mismatch:** Scan from index $0$ to $n - 1$. The first index where $nums[i] \ne i + 1$ reveals the missing positive integer `i + 1`.
* **4. Edge case:** If all indices $0..n-1$ match, the answer is $n + 1$.

---

## 3. Python 3 implementation

<details>
<summary>Spoiler: Solution Code</summary>

```python
def first_missing_positive(nums: list[int]) -> int:
    n = len(nums)
    i = 0
    
    # Step 1: Place each positive number x in the range [1..n] at index x - 1
    while i < n:
        correct_idx = nums[i] - 1
        if 1 <= nums[i] <= n and nums[i] != nums[correct_idx]:
            # Swap nums[i] to its correct slot
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
        else:
            i += 1
            
    # Step 2: Find the first index that does not hold value i + 1
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
            
    return n + 1
```

</details>

---

## 4. Complexity and interview proof

* **Time complexity:** $\mathcal{O}(n)$ linear.
  * It looks like an inner loop because of the `while` without an automatic `i += 1`, but **each swap places at least one number into its permanent correct position**.
  * Since there are $n$ positions, there can be at most $n$ swaps throughout the entire execution. The outer index $i$ advances at most $n$ times.
  * Total loop iterations $\le 2n = \mathcal{O}(n)$.
* **Space complexity:** $\mathcal{O}(1)$ strictly in-place memory.
* **Why interviewers love this question:** LC 41 is a Hard question because candidates instinctively reach for sorting ($\mathcal{O}(n \log n)$) or a Hash Set ($\mathcal{O}(n)$ memory). Being able to explain why cyclic swapping runs in linear time proves deep intuition for amortized complexity analysis.
