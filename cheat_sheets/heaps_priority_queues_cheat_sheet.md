# Priority Queues & Heaps Cheat Sheet

A regular queue serves items in arrival order (FIFO). A **Priority Queue (Binary Heap)** always keeps the smallest (or largest) element at the top (`heap[0]`) for instant $\mathcal{O}(1)$ lookup and $\mathcal{O}(\log n)$ insertion/removal.

## 1. Python `heapq` Basics
Python's `heapq` module implements a **Min-Heap** on top of a regular list:
- `heap[0]` is always the smallest item ($\mathcal{O}(1)$).
- `heapq.heappush(heap, x)` inserts `x` in $\mathcal{O}(\log n)$.
- `heapq.heappop(heap)` pops and returns the smallest item in $\mathcal{O}(\log n)$.
- `heapq.heapify(nums)` converts an existing list into a valid heap in place in **$\mathcal{O}(n)$** time.

### How to do a Max-Heap in Python
Negate numbers on the way in and negate them back on the way out:
```python
heapq.heappush(max_heap, -val)
largest = -heapq.heappop(max_heap)
```

---

## 2. The "Top K" Pattern ($\mathcal{O}(n \log k)$ Time, $\mathcal{O}(k)$ Space)
Sorting the whole array takes $\mathcal{O}(n \log n)$ time. Maintaining a heap of size $K$ takes $\mathcal{O}(n \log k)$ time and $\mathcal{O}(k)$ memory.

**Which heap to use:**
- To keep the **$K$ largest** elements: use a **Min-Heap** of size $K$. Whenever the heap grows to $K + 1$, `heappop()` evicts the smallest loser, leaving the $K$ biggest champions inside.
- To keep the **$K$ smallest** elements: use a **Max-Heap** of size $K$.

### Template (LC 215: Kth Largest Element in an Array)
```python
import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
    return min_heap[0]  # Smallest of the top k = kth largest overall
```

---

## 3. When to reach for a Heap
1. **Top $K$ / $K$-th largest or smallest / $K$ closest points** (LC 215, LC 347, LC 973).
2. **Merging $K$ sorted lists or streams** (LC 23: push the head of each list into a min-heap of size $K$).
3. **Running median of a live stream** (LC 295: balance a Max-Heap for the lower half and a Min-Heap for the upper half).
