# Quickselect (Kth Order Statistic)

> **Source reference:** [AlgoMaster.io, Quickselect](https://algomaster.io/learn/dsa/quick-sort)  
> **LeetCode targets:** [LC 215. Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/), [LC 973. K Closest Points](https://leetcode.com/problems/k-closest-points-to-origin/), [LC 347. Top K Frequent](https://leetcode.com/problems/top-k-frequent-elements/)  
> **Category:** Divide and conquer (selection)  
> **Difficulty:** Medium

## 1. Why MAANG asks quickselect

In technical interviews at Meta, Google, and Amazon, finding the $k$-th smallest or largest element is a classic test of algorithmic trade-offs:
1. **Full sort:** Sort the array and return `nums[k]`. Time is $\mathcal{O}(n \log n)$. This does unnecessary work by ordering elements we do not care about.
2. **Min-heap of size $k$:** Push elements through a heap. Time is $\mathcal{O}(n \log k)$, auxiliary space is $\mathcal{O}(k)$.
3. **Quickselect:** Expected time is **$\mathcal{O}(n)$ linear** and auxiliary space is **$\mathcal{O}(1)$**.

Quickselect is based on Quick Sort's partition step. In Quick Sort, after partitioning around a pivot index $p$, we recursively sort **both** the left and right subarrays. In Quickselect, we check if $p$ matches our target index:
* If $p == \text{target}$, the pivot is already at its sorted position. Return `nums[p]`.
* If $p < \text{target}$, the target element must lie in the right subarray. Recurse only on the right.
* If $p > \text{target}$, the target element must lie in the left subarray. Recurse only on the left.

Because we discard half the search space at each step, the total work is:
$$n + \frac{n}{2} + \frac{n}{4} + \dots + 1 = 2n = \mathcal{O}(n)$$

---

## 2. Algorithm steps

* **1. Convert $k$ to 0-based target index:** To find the $k$-th largest element in an array of size $n$, its index in sorted ascending order is `target = n - k`.
* **2. Partition:** Pick a pivot (e.g., random index or `arr[high]`). Rearrange elements so that all values $\le$ pivot are to its left, and values $>$ pivot are to its right. Let $p$ be the final index of the pivot.
* **3. Check pivot position:**
  * If $p == \text{target}$, return `nums[p]`.
  * If $p < \text{target}$, continue searching in `low = p + 1` to `high`.
  * If $p > \text{target}$, continue searching in `low` to `high = p - 1`.
* **4. Repeat until found:** The partition guarantees that the element landing at `target` is the exact $k$-th order statistic.

```playthrough
{
  "algorithm": "quick_sort",
  "initial": [3, 2, 1, 5, 6, 4]
}
```

---

## 3. Python 3 implementation

<details>
<summary>Spoiler: Solution Code</summary>

```python
import random

def find_kth_largest(nums: list[int], k: int) -> int:
    target = len(nums) - k  # Convert k-th largest to 0-indexed position
    
    def quickselect(low: int, high: int) -> int:
        # Randomize pivot to prevent O(n^2) worst case on adversarial inputs
        rand_idx = random.randint(low, high)
        nums[rand_idx], nums[high] = nums[high], nums[rand_idx]
        
        pivot = nums[high]
        i = low
        for j in range(low, high):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[high] = nums[high], nums[i]
        
        if i == target:
            return nums[i]
        elif i < target:
            return quickselect(i + 1, high)
        else:
            return quickselect(low, i - 1)
            
    return quickselect(0, len(nums) - 1)
```

</details>

---

## 4. Complexity and interview notes

* **Time complexity:**
  * **Average:** $\mathcal{O}(n)$. The recurrence is $T(n) = T(n/2) + \mathcal{O}(n) = \mathcal{O}(n)$.
  * **Worst case:** $\mathcal{O}(n^2)$ if the pivot chosen is consistently the extreme element. Always mention random pivot selection or Introselect (fallback to median-of-medians) in interviews to eliminate this risk.
* **Space complexity:** $\mathcal{O}(1)$ auxiliary space if written iteratively, or $\mathcal{O}(\log n)$ stack frames recursively.
* **Interview tip:** When an interviewer asks LC 215, start by mentioning the $\mathcal{O}(n \log k)$ min-heap solution. Then say: *"We can optimize time to $\mathcal{O}(n)$ average using Quickselect with in-place Lomuto partitioning."* This demonstrates mastery of both heap and divide-and-conquer paradigms.
