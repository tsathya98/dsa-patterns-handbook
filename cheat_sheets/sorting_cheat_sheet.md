# Sorting Algorithms Cheat Sheet

> Guides: [01. Bubble](../04_sorting/01_bubble_sort.md) | [02. Selection](../04_sorting/02_selection_sort.md) | [03. Insertion](../04_sorting/03_insertion_sort.md) | [04. Merge](../04_sorting/04_merge_sort.md) | [05. Quick](../04_sorting/05_quick_sort.md)  
> Sources: Airtribe DSA Core, Innoskrit Sorting Mastery, InterviewCoach Cohort

## 1. The Grand Sorting Taxonomy

```text
Sorting Algorithms
 ├── Comparison-Based (Lower bound: Ω(n log n))
 │    ├── Elementary: Bubble Sort, Selection Sort, Insertion Sort
 │    ├── Divide & Conquer: Merge Sort, 3-Way Merge Sort, Quick Sort
 │    └── Tree / Structural: Heap Sort, Cycle Sort
 ├── Non-Comparison Based (Can achieve O(n) with key constraints)
 │    └── Counting Sort, Radix Sort, Bucket Sort, Pigeonhole Sort
 └── Hybrid Engines (Real-world production standard)
      ├── Timsort: Insertion + Merge Sort (Python sorted(), Java Arrays.sort())
      └── Introsort: Quick + Heap + Insertion Sort (C++ std::sort)
```

---

## 2. In-Place vs Stable: The Two Core Interview Properties

### In-Place Sorting
An algorithm is **in-place** if it sorts the array using $\mathcal{O}(1)$ auxiliary memory (it mutates the input array without allocating a full copy).
- **In-place ($\mathcal{O}(1)$ auxiliary space):** Bubble, Selection, Insertion, Heap, Quick Sort (call stack is $\mathcal{O}(\log n)$).
- **Out-of-place:** Merge Sort ($\mathcal{O}(n)$ temp array allocations during merge).

### Stable Sorting
An algorithm is **stable** if elements with identical keys maintain their original relative order.

```text
Sort students by marks:
Original:    [(Alice, 80), (Bob, 90), (Charlie, 80)]

Stable sort:   [(Alice, 80), (Charlie, 80), (Bob, 90)]   <-- Alice stays before Charlie
Unstable sort: [(Charlie, 80), (Alice, 80), (Bob, 90)]   <-- Charlie jumped over Alice!
```

- **Why Selection Sort is Unstable:** Swapping the minimum across long distances jumps over duplicate keys:
  ```text
  nums = [4_a, 4_b, 2]
  Pass 1: min is 2 at index 2. Swap nums[0] (4_a) with nums[2] (2).
  Result: [2, 4_b, 4_a]   <-- 4_b now appears before 4_a! Unstable.
  ```

---

## 3. Master Comparison Table

| Algorithm | Best Time | Avg Time | Worst Time | Aux Space | In-Place? | Stable? | Core Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Bubble Sort** | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Yes | Yes | Sinks max element to end via adjacent swaps. Early break with `swapped` flag. |
| **Selection Sort** | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Yes | No | Finds min in unsorted subarray, swaps to front. Minimizes memory writes ($\le n$ swaps). |
| **Insertion Sort** | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Yes | Yes | Slides each element backward into sorted left prefix. Optimal for tiny or nearly sorted arrays. |
| **Merge Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | No | Yes | Divides array into halves, recursively sorts and merges. Standard for linked lists. |
| **Quick Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(\log n)$ | Yes | No | Partitions around pivot. Unmatched cache locality and constant factors in memory. |
| **Heap Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(1)$ | Yes | No | Builds max-heap in place, repeatedly pops root to end. Guaranteed $\mathcal{O}(n \log n)$ in $\mathcal{O}(1)$ space. |
| **Counting Sort** | $\mathcal{O}(n + k)$ | $\mathcal{O}(n + k)$ | $\mathcal{O}(n + k)$ | $\mathcal{O}(k)$ | No | Yes | Counts frequencies in range $[0..k]$. Linear time when $k = \mathcal{O}(n)$. |
| **Radix Sort** | $\mathcal{O}(d(n + b))$ | $\mathcal{O}(d(n + b))$ | $\mathcal{O}(d(n + b))$ | $\mathcal{O}(n + b)$ | No | Yes | Sorts digit by digit (LSD to MSD) using stable counting sort. |
| **Timsort** | $\mathcal{O}(n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | No | Yes | Finds natural sorted runs, sorts short runs with Insertion, merges with Merge Sort. |

---

## 4. Arithmetic Loop Bound Derivation (Airtribe Proof)

Why do Bubble Sort and Selection Sort inner loops run $N - 1 - i$ times?

```text
Let N = len(nums).
Pass i = 0: inner loop runs N - 1 times
Pass i = 1: inner loop runs N - 2 times
...
Pass i = N - 2: inner loop runs 1 time

Rule: In every pass, (i + j) = N - 1  ==>  j runs up to (N - 1 - i)
Total operations = (N - 1) + (N - 2) + ... + 2 + 1
                 = [N * (N - 1)] / 2
                 = O(N^2)
```

---

## 5. How to Pick in Interviews

### Decision rules:
* **1. Linked lists:** Use Merge Sort because slow/fast pointers split the list in $\mathcal{O}(n)$ time and merging requires only $\mathcal{O}(1)$ pointer reassignments without allocating array buffers.
* **2. Small integer ranges:** Use Counting Sort or Bucket Sort to achieve $\mathcal{O}(n + k)$ non-comparison linear time when maximum value $k$ is small.
* **3. Partial selection (Top K):** Maintain a Min-Heap of size $k$ running in $\mathcal{O}(n \log k)$ time, or use Quickselect to find the $k$-th order statistic in $\mathcal{O}(n)$ average time.
* **4. Stability with guaranteed $\mathcal{O}(n \log n)$:** Choose Merge Sort or Python's native Timsort when relative order of equal elements must be preserved.
* **5. Strict $\mathcal{O}(1)$ auxiliary space:** Choose Heap Sort for guaranteed $\mathcal{O}(n \log n)$ worst-case time with in-place heapification.
* **6. Average cache performance:** Choose Quick Sort with randomized or median-of-three pivot selection for optimal CPU cache locality.

