# Sorting Algorithms Cheat Sheet

> Guides: [01. Bubble](../04_sorting/01_bubble_sort.md) | [02. Selection](../04_sorting/02_selection_sort.md) | [03. Insertion](../04_sorting/03_insertion_sort.md) | [04. Merge](../04_sorting/04_merge_sort.md) | [05. Quick](../04_sorting/05_quick_sort.md)

## 1. Comparison Table

| Algorithm | Best Time | Avg Time | Worst Time | Space | In-Place? | Stable? | When to Use |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Bubble Sort** | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Yes | Yes | Detecting already-sorted input (`swapped` flag) |
| **Selection Sort** | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Yes | No | Minimizing memory writes (at most $n$ swaps) |
| **Insertion Sort** | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Yes | Yes | Tiny arrays ($n \le 32$) or nearly sorted streams |
| **Merge Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | No | Yes | Linked lists ($\mathcal{O}(1)$ space), external disk sort, counting inversions |
| **Quick Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(\log n)$ | Yes | No | Fast in-memory array sorting (cache-friendly) |
| **Heap Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(1)$ | Yes | No | Guaranteed $\mathcal{O}(n \log n)$ time with $\mathcal{O}(1)$ space |
| **Counting / Bucket** | $\mathcal{O}(n + k)$ | $\mathcal{O}(n + k)$ | $\mathcal{O}(n + k)$ | $\mathcal{O}(k)$ | No | Yes | Small integer range $[0..k]$ (e.g., [LC 274 H-Index](../01_arrays_and_pointers/274_h_index.md)) |
| **Timsort** | $\mathcal{O}(n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | No | Yes | Python `sorted()` / `.sort()` (hybrid Insertion + Merge) |

---

## 2. How to Pick in Interviews

```text
Need to sort data?
 ├── Sorting a Linked List? ──────────────────────► Merge Sort (O(n log n) time, O(1) pointer splice)
 ├── Values are integers bounded by small range K? ► Counting / Bucket Sort (O(n + k) linear time)
 ├── Need kth largest/smallest without full sort? ─► Quickselect (O(n) avg) or Min-Heap (O(n log k))
 └── General array sorting:
      ├── Need stability + worst-case O(n log n)? ─► Merge Sort / Timsort
      ├── Strict O(1) extra space required? ───────► Heap Sort
      └── Fastest average in-place cache speed? ───► Quick Sort (with random/median pivot)
```
