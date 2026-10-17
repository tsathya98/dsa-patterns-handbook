# Factors, primes, and iteration counting

> **Course reference:** CodeKerdos DSA, Class 3  
> **Core concept:** Deriving $\mathcal{O}(\sqrt{N})$ from symmetric factor pairs, primality testing, and exact loop iteration formulas.

## 1. Counting factors of a number

A factor of an integer $N$ is any integer $i$ that divides $N$ with zero remainder (`N % i == 0`).

```text
Factors of 24: {1, 2, 3, 4, 6, 8, 12, 24}      -> 8 factors
Factors of 12: {1, 2, 3, 4, 6, 12}             -> 6 factors
Factors of 36: {1, 2, 3, 4, 6, 9, 12, 18, 36}  -> 9 factors (6 * 6 pairs with itself)
```

### The $\mathcal{O}(N)$ brute-force scan
Looping from $1$ to $N$ checks every integer candidate. If $N = 10^9$, a linear scan runs $10^9$ operations and hits Time Limit Exceeded (TLE).

## 2. The $\mathcal{O}(\sqrt{N})$ symmetric pair observation

Factors always come in pairs:
$$\text{If } i \text{ divides } N, \text{ then } \frac{N}{i} \text{ also divides } N.$$

```text
Factor pairs of 24:
 1  x 24 = 24
 2  x 12 = 24
 3  x  8 = 24
 4  x  6 = 24
──────────────  <- Split line at √24 ≈ 4.899
 6  x  4 = 24   (Duplicate of 4 x 6)
 8  x  3 = 24   (Duplicate of 3 x 8)
12  x  2 = 24   (Duplicate of 2 x 12)
24  x  1 = 24   (Duplicate of 1 x 24)
```

### The invariant
* For any factor pair $(i, N/i)$, both values cannot exceed $\sqrt{N}$ at the same time.
* Once $i > \sqrt{N}$, its partner $N/i$ is strictly less than $\sqrt{N}$, which means we already counted that pair earlier in the loop.
* We only need to iterate while $i \le \sqrt{N}$, written as `i * i <= N` to avoid floating-point precision issues.

### Perfect squares
When $N = 36$ and $i = 6$, both $i$ and $N/i$ equal $6$. Count that factor once instead of twice:
* If `i * i == n`, add $1$ to the count.
* Otherwise, add $2$ (for both $i$ and $n // i$).

```python
def count_factors(n: int) -> int:
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            if i * i == n:
                count += 1      # Perfect square root (e.g. 6 * 6 = 36)
            else:
                count += 2      # Both i and n // i
        i += 1
    return count
```

* **Time complexity:** $\mathcal{O}(\sqrt{N})$. For $N = 10^9$, the loop runs $31,622$ times instead of $10^9$.
* **Space complexity:** $\mathcal{O}(1)$.

## 3. Primality check in $\mathcal{O}(\sqrt{N})$

A prime number $N > 1$ has exactly two factors: $1$ and $N$.
* Integers $\le 1$ are not prime.
* If any integer between $2$ and $\lfloor\sqrt{N}\rfloor$ divides $N$, then $N$ is composite.

```python
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
```

## 4. Exact loop iteration counts

Before simplifying to Big O, you can count the exact number of iterations a loop runs:

| Loop pattern | Code example | Exact iteration formula | Big O class |
|---|---|---|---|
| **Fixed range** | `for i in range(35, 87):` | $\text{stop} - \text{start} = 87 - 35 = 52$ | $\mathcal{O}(1)$ |
| **Linear range** | `for i in range(1, n):` | $n - 1$ | $\mathcal{O}(N)$ |
| **Stepped range** | `for i in range(0, n, 2):` | $\lceil n / 2 \rceil$ | $\mathcal{O}(N)$ |
| **Square root bound** | `while i * i <= n: i += 1` | $\lfloor\sqrt{n}\rfloor$ | $\mathcal{O}(\sqrt{N})$ |
| **Doubling / halving** | `while i < n: i *= 2` | $\lceil\log_2 n\rceil$ | $\mathcal{O}(\log N)$ |
| **Triangular nested** | `for i in range(n): for j in range(i, n):` | $\frac{n(n + 1)}{2}$ | $\mathcal{O}(N^2)$ |
| **Independent nested** | `for i in range(n): for j in range(m):` | $n \times m$ | $\mathcal{O}(N \times M)$ |
