# 📊 The Ultimate Sorting Algorithms Comparison Cheat Sheet

> **Summary Reference:** Comparison of all 10 core sorting algorithms covering Time, Space, Stability, In-Place behavior, and Best Use Cases.

---

## 🏆 Master Comparison Table

| Algorithm | Best Time | Average Time | Worst Time | Space | In-Place? | Stable? | Best Used For |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Bubble Sort** | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Yes | Yes | Nearly sorted data, small inputs, teaching |
| **Selection Sort** | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Yes | No | Minimizing memory writes (at most $n$ swaps) |
| **Insertion Sort** | $\mathcal{O}(n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Yes | Yes | Small datasets ($N \le 32$), online data streams |
| **Merge Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | No | Yes | Guaranteed $\mathcal{O}(n \log n)$, Linked Lists, External Sort |
| **Quick Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(\log n)$ | Yes | No | General purpose, fast in-memory array sorting |
| **Heap Sort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(1)$ | Yes | No | Embedded systems where $\mathcal{O}(1)$ space and guaranteed $\mathcal{O}(n \log n)$ required |
| **Counting Sort** | $\mathcal{O}(n + k)$ | $\mathcal{O}(n + k)$ | $\mathcal{O}(n + k)$ | $\mathcal{O}(k)$ | No | Yes | Small integer keys in range $[0, k]$ |
| **Radix Sort** | $\mathcal{O}(d \cdot (n + b))$ | $\mathcal{O}(d \cdot (n + b))$ | $\mathcal{O}(d \cdot (n + b))$ | $\mathcal{O}(n + b)$ | No | Yes | Fixed-digit integers/strings |
| **Bucket Sort** | $\mathcal{O}(n + k)$ | $\mathcal{O}(n + k)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(n + k)$ | No | Yes | Uniformly distributed floating point numbers in $[0, 1)$ |
| **Timsort** | $\mathcal{O}(n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | No | Yes | Standard library default (Python `sorted()`, Java `Arrays.sort()`) |

---

## 🎯 Interview Decision Tree: "Which Sorting Algorithm Should I Pick?"

```text
                           [ Need to Sort Data ]
                                     │
           ┌─────────────────────────┴─────────────────────────┐
    [ Array / Contiguous ]                               [ Linked List ]
           │                                                   │
    Is elements range small integers?                    Merge Sort (O(N log N), O(1) space)
     ┌─────┴─────┐
   [Yes]        [No]
     │           │
Counting Sort  Need guaranteed O(N log N) & Stability?
 or Radix Sort   ┌─────────┴─────────┐
               [Yes]                [No]
                 │                    │
             Merge Sort         Need O(1) Space?
                                 ┌────┴────┐
                               [Yes]      [No]
                                 │          │
                             Heap Sort   Quick Sort (Fastest Average)
```
