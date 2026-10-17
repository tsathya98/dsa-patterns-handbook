# Prefix sums and special index parity queries

> **Course reference:** CodeKerdos DSA, Class 5
> **Core concepts:** Range sum queries in $\mathcal{O}(1)$, equilibrium pivot indices, and index parity flips on deletion.

## Range sum queries in $\mathcal{O}(1)$

Given an array of size $N$ and $Q$ range queries $[L, R]$, summing from $L$ to $R$ on each query takes $\mathcal{O}(Q \times N)$ time, which times out when $Q, N = 10^5$. Precomputing a prefix sum array `pf` in $\mathcal{O}(N)$ lets you answer any query in $\mathcal{O}(1)$:

$$\text{sum}(L, R) = \begin{cases} pf[R] & \text{if } L = 0 \\ pf[R] - pf[L - 1] & \text{if } L > 0 \end{cases}$$

```text
Index:        0    1    2    3    4    5    6    7    8    9
Array (ar): [ -3,   6,   2,   4,   5,   2,   8,  -1,   3,   1 ]
Prefix(pf): [ -3,   3,   5,   9,  14,  16,  24,  23,  26,  27 ]
```

## Equilibrium index in $\mathcal{O}(1)$ space

An index $i$ is an equilibrium index if the sum of elements strictly to its left equals the sum of elements strictly to its right:

$$\sum_{j=0}^{i-1} ar[j] == \sum_{j=i+1}^{N-1} ar[j]$$

Instead of allocating an $\mathcal{O}(N)$ prefix array, compute `total_sum = sum(ar)` upfront and track `left_sum = 0` as you iterate. At index $i$, the right sum is `total_sum - left_sum - ar[i]`.

<details>
<summary>Spoiler: Solution Code</summary>

```python
def find_equilibrium_index(ar: list[int]) -> int:
    total_sum = sum(ar)
    left_sum = 0

    for i, val in enumerate(ar):
        if left_sum == total_sum - left_sum - val:
            return i
        left_sum += val

    return -1
```

</details>

## Special indices: parity flip on deletion

Count how many indices $i$, when deleted from the array, make the sum of even-indexed elements equal the sum of odd-indexed elements.

```text
Original indices:   0    1    2    3    4    5
Elements:          [A,   B,   C,   D,   E,   F]

Delete index 2 (C):
Remaining array:   [A,   B,   D,   E,   F]
New indices:        0    1    2    3    4
Parities:          even odd  even odd  even
```

When index $i$ is removed:
1. Elements before $i$ ($0 \le j < i$) keep their original indices and parities.
2. Elements after $i$ ($i < j \le N - 1$) shift left by 1, flipping their index parity: old even indices become odd, and old odd indices become even.

$$\text{new\_even} = \text{even\_sum}(0, i - 1) + \text{odd\_sum}(i + 1, N - 1)$$
$$\text{new\_odd} = \text{odd\_sum}(0, i - 1) + \text{even\_sum}(i + 1, N - 1)$$

<details>
<summary>Spoiler: Solution Code</summary>

```python
def count_special_indices(ar: list[int]) -> int:
    n = len(ar)
    if n <= 1:
        return n

    pf_even = [0] * n
    pf_odd = [0] * n
    pf_even[0] = ar[0]

    for i in range(1, n):
        pf_even[i] = pf_even[i - 1] + (ar[i] if i % 2 == 0 else 0)
        pf_odd[i] = pf_odd[i - 1] + (ar[i] if i % 2 == 1 else 0)

    def get_range(pf: list[int], L: int, R: int) -> int:
        if L > R or R < 0 or L >= n:
            return 0
        return pf[R] if L == 0 else pf[R] - pf[L - 1]

    count = 0
    for i in range(n):
        even_sum = get_range(pf_even, 0, i - 1) + get_range(pf_odd, i + 1, n - 1)
        odd_sum = get_range(pf_odd, 0, i - 1) + get_range(pf_even, i + 1, n - 1)
        if even_sum == odd_sum:
            count += 1

    return count
```

</details>

* **Time complexity:** $\mathcal{O}(N)$ preprocessing and $\mathcal{O}(N)$ evaluation.
* **Space complexity:** $\mathcal{O}(N)$ for the even and odd prefix arrays.
