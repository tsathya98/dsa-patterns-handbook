# 📊 LeetCode 274: H-Index – Master Study Guide

> **Difficulty:** Medium | **Top Interview 150:** Arrays / Sorting  
> **Pattern:** Sorting + Linear Scan Rank Comparison  
> **Complexity:** Time: $\mathcal{O}(n \log n)$ | Space: $\mathcal{O}(1)$ (in-place sort)  
> **Source Code:** [`274_h_index.py`](./274_h_index.py)

---

## 📌 Problem in Plain English

Given an array of integers `citations` where `citations[i]` is the number of citations a researcher received for their $i$-th paper, compute the researcher's **H-Index**.

> **Definition:** A scientist has an index $h$ if $h$ of their $n$ papers have **at least $h$ citations each**, and the other $n - h$ papers have **no more than $h$ citations each**.

```text
Example 1:
Input: citations = [3, 0, 6, 1, 5]
Output: 3
Explanation:
Sorted descending: [6, 5, 3, 1, 0]
- 1st paper has 6 citations (6 >= 1) -> Valid
- 2nd paper has 5 citations (5 >= 2) -> Valid
- 3rd paper has 3 citations (3 >= 3) -> Valid
- 4th paper has 1 citation  (1 >= 4) -> Invalid!
Result: 3 papers meet the threshold -> H-Index = 3.

Example 2:
Input: citations = [100]
Output: 1
Explanation: 1st paper has 100 citations (100 >= 1). H-Index = 1.
```

---

## 🧠 Mental Model: The Runner Finish Line / Finger Count

Sort descending. Compare the paper's citations against its rank ($i + 1$):
* Does paper at rank $i + 1$ have $\ge i + 1$ citations?
* If **YES**, update $h = i + 1$.
* The very first time a paper fails ($c < i + 1$), **stop immediately** (`break`), because all subsequent papers have even fewer citations!

---

## 💻 Production Implementation

```python
from typing import List

class Solution:
    def hIndex(self, citations: List[int]) -> int:
        citations.sort(reverse=True)
        h_index = 0
        
        for i, c in enumerate(citations):
            if c >= i + 1:
                h_index = i + 1
            else:
                break
                
        return h_index
```

### ⚡ Complexity:
* **Time Complexity:** $\mathcal{O}(n \log n)$ due to sorting. The linear scan takes $\mathcal{O}(n)$.
* **Space Complexity:** $\mathcal{O}(1)$ auxiliary space (in-place sort).
