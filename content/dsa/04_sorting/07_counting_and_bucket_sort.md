# Counting sort and bucket sort

> **Source reference:** [AlgoMaster.io, Bucket Sort](https://algomaster.io/learn/dsa/bucket-sort)  
> **LeetCode targets:** [LC 347. Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/), [LC 451. Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency/), [LC 164. Maximum Gap](https://leetcode.com/problems/maximum-gap/)  
> **Category:** Non-comparison linear sorting  
> **Difficulty:** Medium

## 1. Why MAANG asks bucket and counting sort

Comparison-based sorting (Merge sort, Quick sort, Heap sort) has a mathematical lower bound of $\Omega(n \log n)$. You cannot beat this lower bound by comparing elements.

However, when elements have a bounded range or when sorting by frequencies, we can bypass comparisons entirely:
* **Counting sort:** When values are integers in a known small range $[0..k]$, we count frequencies in an array of size $k + 1$. Time is $\mathcal{O}(n + k)$. If $k = \mathcal{O}(n)$, the total time is strictly linear $\mathcal{O}(n)$.
* **Bucket sort:** We distribute elements into an array of buckets. When solving LC 347 (Top K Frequent Elements), the maximum frequency any element can have is $n$ (the length of the array). By creating $n + 1$ buckets where `bucket[freq]` holds all elements appearing `freq` times, we group frequencies in $\mathcal{O}(n)$ time and traverse backward from $n$ to $1$ to grab the top $k$ items.

At companies like Google and Meta, solving LC 347 using Bucket Sort instead of a min-heap ($\mathcal{O}(n \log k)$) demonstrates that you understand how to break the $\mathcal{O}(n \log n)$ comparison barrier.

---

## 2. Algorithm steps (LC 347 bucket sort pattern)

* **1. Count frequencies:** Build a hashmap of `{element: count}` in $\mathcal{O}(n)$ time.
* **2. Initialize buckets:** Create a list of $n + 1$ empty lists, where index $i$ corresponds to frequency $i$.
* **3. Distribute into buckets:** For each `(num, freq)` pair, append `num` to `buckets[freq]`.
* **4. Collect top $k$:** Iterate from index $n$ down to $1$. Append elements from non-empty buckets to the result list until the result length reaches $k$.

---

## 3. Python 3 implementation

<details>
<summary>Spoiler: Solution Code</summary>

```python
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    # Step 1: Count element frequencies - O(n)
    counts = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
        
    # Step 2: Create buckets where index = frequency - O(n)
    # At most, an element can appear len(nums) times
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in counts.items():
        buckets[freq].append(num)
        
    # Step 3: Traverse buckets from highest frequency to lowest - O(n)
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
                
    return result
```

</details>

---

## 4. Complexity and characteristics

* **Time complexity:** $\mathcal{O}(n)$ total.
  * Frequency map construction: $\mathcal{O}(n)$.
  * Bucketing: $\mathcal{O}(n)$ unique keys distributed across $n$ buckets.
  * Gathering top $k$: Scanning $n$ buckets visits at most $n$ total elements.
* **Space complexity:** $\mathcal{O}(n)$ auxiliary memory for the frequency map and the bucket lists.
* **Stability:** Counting sort can be made stable by computing prefix sums of counts and iterating backward over the input array.
* **When to pick in an interview:** Whenever problem constraints show a small discrete range ($k \le 10^5$), character counts (ASCII $0..127$ or alphabet $26$), or frequency groupings bounded by array length $n$.
