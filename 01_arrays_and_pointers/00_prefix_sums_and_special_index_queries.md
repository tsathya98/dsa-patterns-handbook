# ⚖️ Prefix Sums & Special Index Parity Queries

> **Course Reference:** CodeKerdos DSA — Class 5  
> **Core Concepts:** Range sum queries in $\mathcal{O}(1)$, equilibrium pivot indices, and index shifting parity analysis (Even/Odd prefix sums).

---

## 1. Range Sum Queries in $\mathcal{O}(1)$

Given an array of size $N$ and $Q$ range queries $[L, R]$, find the sum of elements from index $L$ to $R$.

* **Naive Approach:** Sum elements from $L$ to $R$ on each query $\to \mathcal{O}(Q \times N)$ (TLE when $Q, N = 10^5$).
* **Prefix Sum Array:** Precompute cumulative sums in $\mathcal{O}(N)$, then answer each query in $\mathcal{O}(1)$.

```text
Array:        ar = [ -3 ,  6 ,  2 ,  4 ,  5 ,  2 ,  8 , -1 ,  3 ,  1 ]
Index:               0    1    2    3    4    5    6    7    8    9
Prefix Sum:   pf = [ -3 ,  3 ,  5 ,  9 , 14 , 16 , 24 , 23 , 26 , 27 ]
```

### The Query Formula
$$\text{sum}(L, R) = \begin{cases} pf[R] & \text{if } L = 0 \\ pf[R] - pf[L - 1] & \text{if } L > 0 \end{cases}$$

```python
def build_prefix_sum(ar: list[int]) -> list[int]:
    n = len(ar)
    pf = [0] * n
    pf[0] = ar[0]
    for i in range(1, n):
        pf[i] = pf[i - 1] + ar[i]
    return pf

def query_range_sum(pf: list[int], L: int, R: int) -> int:
    if L == 0:
        return pf[R]
    return pf[R] - pf[L - 1]
```

---

## 2. Equilibrium Index (Pivot Point)

An index $i$ is an **Equilibrium Index** if:
$$\sum_{j=0}^{i-1} ar[j] == \sum_{j=i+1}^{N-1} ar[j]$$

### The Zero-Memory $\mathcal{O}(1)$ Auxiliary Space Optimization
Instead of storing an explicit `pf` array of size $N$, compute `total_sum` once, then maintain a running `left_sum`:
* $\text{left\_sum}$ starts at $0$.
* At index $i$, $\text{right\_sum} = \text{total\_sum} - \text{left\_sum} - ar[i]$.
* If $\text{left\_sum} == \text{right\_sum}$, index $i$ is an equilibrium point!
* Advance: $\text{left\_sum} \mathrel{+}= ar[i]$.

```python
def find_equilibrium_index(ar: list[int]) -> int:
    total_sum = sum(ar)
    left_sum = 0
    
    for i, val in enumerate(ar):
        right_sum = total_sum - left_sum - val
        if left_sum == right_sum:
            return i
        left_sum += val
        
    return -1
```

---

## 3. Special Indices: Parity Flip on Deletion

> **Problem:** Count how many indices $i$, when deleted from the array, cause the sum of elements at even indices to equal the sum of elements at odd indices.

```text
Original indices:   0    1    2    3    4    5
Elements:          [A ,  B ,  C ,  D ,  E ,  F ]

Delete index 2 (C):
Remaining array:   [A ,  B ,  D ,  E ,  F ]
New indices:        0    1    2    3    4
Parities:          even odd even odd even
```

### The Index Shifting Rule
When index $i$ is removed:
1. **Elements before index $i$ ($0 \le j < i$):** Indices do not change. Even indices stay even; odd indices stay odd.
2. **Elements after index $i$ ($i < j \le N-1$):** Every element shifts left by 1 position!
   * What was at an **even** index is now at an **odd** index.
   * What was at an **odd** index is now at an **even** index.

### The Formula
$$\text{new\_even} = \text{even\_sum}(0, i - 1) + \text{odd\_sum}(i + 1, N - 1)$$
$$\text{new\_odd} = \text{odd\_sum}(0, i - 1) + \text{even\_sum}(i + 1, N - 1)$$

```python
def count_special_indices(ar: list[int]) -> int:
    n = len(ar)
    if n <= 1:
        return n

    # 1. Build specialized even and odd prefix sums
    pf_even = [0] * n
    pf_odd = [0] * n

    pf_even[0] = ar[0]
    pf_odd[0] = 0

    for i in range(1, n):
        if i % 2 == 0:
            pf_even[i] = pf_even[i - 1] + ar[i]
            pf_odd[i] = pf_odd[i - 1]
        else:
            pf_odd[i] = pf_odd[i - 1] + ar[i]
            pf_even[i] = pf_even[i - 1]

    def get_range(pf: list[int], L: int, R: int) -> int:
        if L > R or R < 0 or L >= n:
            return 0
        return pf[R] if L == 0 else pf[R] - pf[L - 1]

    count = 0
    for i in range(n):
        # Even sum after deleting i
        even_sum = get_range(pf_even, 0, i - 1) + get_range(pf_odd, i + 1, n - 1)
        # Odd sum after deleting i
        odd_sum = get_range(pf_odd, 0, i - 1) + get_range(pf_even, i + 1, n - 1)

        if even_sum == odd_sum:
            count += 1

    return count
```
* **Time Complexity:** $\mathcal{O}(N)$ preprocessing + $\mathcal{O}(N)$ evaluation = $\mathcal{O}(N)$.
* **Auxiliary Space:** $\mathcal{O}(N)$ (for prefix arrays).
