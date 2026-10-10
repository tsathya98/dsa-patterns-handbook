# ⛰️ Priority Queues & Heaps Master Cheat Sheet & Decision Guide

> **Pattern:** Binary Heap / Priority Queue  
> **Audience:** Complete Beginner / 1st-Year CS Student  
> **Analogy:** Hospital Emergency Room (ER) Triage

---

## 💡 1. What is a Heap / Priority Queue?

* A regular **Queue (FIFO)** = A line at a ticket counter. First person to arrive is the first person served.
* A **Priority Queue** = A hospital Emergency Room. Patients don't get seen by arrival time — the person with the **most critical condition** (highest priority) gets seen first!

A **Binary Heap** is the specialized data structure behind a Priority Queue:
* **Instant minimum (or maximum) lookup:** You can see the top element in $\mathcal{O}(1)$ time.
* **Fast insert & remove:** Adding an element or removing the top element takes only **$\mathcal{O}(\log n)$** time.

---

## 🐍 2. Heaps in Python (`import heapq`)

Python's built-in `heapq` module creates a **Min-Heap by default**:
* The **smallest** number always sits at index 0 (`heap[0]`).
* `heapq.heappush(heap, val)` $\to$ Inserts `val` in $\mathcal{O}(\log n)$.
* `heapq.heappop(heap)` $\to$ Pops and returns the **smallest** item in $\mathcal{O}(\log n)$.

```python
import heapq

min_heap = []
heapq.heappush(min_heap, 10)
heapq.heappush(min_heap, 2)
heapq.heappush(min_heap, 8)

print(min_heap[0])  # Output: 2 (Always the smallest!)
print(heapq.heappop(min_heap))  # Returns 2, and heap re-balances!
```

### 💡 Trick: How to make a Max-Heap in Python?
Since Python only has a min-heap, multiply numbers by `-1` before pushing, and multiply by `-1` when popping:
```python
heapq.heappush(max_heap, -num)
largest = -heapq.heappop(max_heap)
```

---

## 🏆 3. The Classic "Top K Elements" Pattern

### Why not just sort the array?
* Sorting the whole array takes $\mathcal{O}(n \log n)$ time.
* Using a Heap of size $K$ takes only **$\mathcal{O}(n \log k)$** time and $\mathcal{O}(k)$ space. When $k \ll n$ (e.g., finding Top 10 out of 1,000,000 items), a heap is thousands of times faster!

---

### 🔑 The Counter-Intuitive Rule:
> * **To find the $K$ LARGEST elements:** Keep a **MIN-HEAP** of size $K$.  
>   *(The smallest of your top candidates sits at the top. Whenever a bigger number comes along, you pop the top loser off!)*
> * **To find the $K$ SMALLEST elements:** Keep a **MAX-HEAP** of size $K$.

#### ⚙️ Top K Largest Template (e.g. *Kth Largest Element in an Array* - LC 215)
```python
import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    min_heap = []
    
    for num in nums:
        heapq.heappush(min_heap, num)
        
        # If heap exceeds size k, evict the smallest element!
        if len(min_heap) > k:
            heapq.heappop(min_heap)
            
    # The top of the heap is now the Kth largest element!
    return min_heap[0]
```

---

## 🎯 4. When to Use a Heap (Cheat Sheet Triggers)

Ask yourself:
1. Does the problem ask for **"Top K elements"**, **"Kth smallest/largest"**, or **"K closest points"**?
2. Are you merging multiple sorted lists into one (*Merge K Sorted Lists* - LC 23)?
3. Do you need to continuously calculate the **Median** of a dynamic stream of numbers (*Find Median from Data Stream* - LC 295)?

👉 Use a **Heap**!
