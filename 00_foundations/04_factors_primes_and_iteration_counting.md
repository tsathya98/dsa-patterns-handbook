# 🔢 Factors, Primes & Iteration Counting

> **Course Reference:** CodeKerdos DSA — Class 3  
> **Core Concept:** Deriving $\mathcal{O}(\sqrt{N})$ from the symmetric factor pair observation, prime validation, and exact loop iteration arithmetic.

---

## 1. Count of Factors in a Number

A factor of an integer $N$ is any integer $i$ that divides $N$ with zero remainder (`N % i == 0`).

```text
Factors of 24: {1, 2, 3, 4, 6, 8, 12, 24}  -> 8 factors
Factors of 12: {1, 2, 3, 4, 6, 12}          -> 6 factors
Factors of 36: {1, 2, 3, 4, 6, 9, 12, 18, 36} -> 9 factors (Notice 6 x 6)
```

### The $\mathcal{O}(N)$ Brute Force
Looping from $1$ to $N$ checks every candidate:
* If $N = 10^9$, this performs $10^9$ operations $\to$ **Time Limit Exceeded (TLE)**.

---

## 2. The $\mathcal{O}(\sqrt{N})$ Symmetric Pair Observation

Factors never appear in isolation; they always come in **symmetric pairs**:
$$\text{If } i \text{ divides } N, \text{ then } \frac{N}{i} \text{ MUST also divide } N.$$

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

### The Mathematical Invariant
* For any pair $(i, N/i)$, both terms cannot simultaneously be greater than $\sqrt{N}$.
* If $i > \sqrt{N}$, then $N/i < \sqrt{N}$ (meaning we already counted it when the loop examined the smaller number!).
* Therefore, the loop only needs to run while **$i \le \sqrt{N}$** (written in code as `i * i <= N` to avoid floating-point square root errors).

### The Perfect Square Trap
If $N = 36$ and $i = 6$:
* $i = 6$ and $N/i = 36/6 = 6$.
* Both halves of the pair are the same number!
* **Rule:** If $i == N/i$, add $1$ to factor count. Otherwise, add $2$.

```python
def count_factors(n: int) -> int:
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            if i * i == n:
                count += 1      # Perfect square root (e.g. 6 x 6 = 36)
            else:
                count += 2      # Both i and n // i
        i += 1
    return count
```

* **Time Complexity:** $\mathcal{O}(\sqrt{N})$ — For $N = 10^9$, runs $\approx 31,622$ iterations instead of $1,000,000,000$.
* **Space Complexity:** $\mathcal{O}(1)$.

---

## 3. Prime Number Checking in $\mathcal{O}(\sqrt{N})$

A prime number $N > 1$ has **exactly two factors**: $1$ and $N$.
* Numbers $\le 1$ are not prime.
* If any number between $2$ and $\lfloor\sqrt{N}\rfloor$ divides $N$, $N$ is composite.

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

---

## 4. Exact Loop Iteration Counting Matrix

In interview problem solving, loop analysis requires counting exact iterations before simplifying to Big-O:

| Loop Pattern | Code Example | Exact Iteration Formula | Big-O Class |
|---|---|---|---|
| **Fixed Range** | `for i in range(35, 87):` | $\text{stop} - \text{start} = 87 - 35 = 52$ | $\mathcal{O}(1)$ |
| **Linear Range** | `for i in range(1, n):` | $n - 1$ | $\mathcal{O}(N)$ |
| **Stepped Range** | `for i in range(0, n, 2):` | $\lceil n / 2 \rceil$ | $\mathcal{O}(N)$ |
| **Square Root Condition** | `while i * i <= n: i += 1` | $\lfloor\sqrt{n}\rfloor$ | $\mathcal{O}(\sqrt{N})$ |
| **Doubling / Halving** | `while i < n: i *= 2` | $\lceil\log_2 n\rceil$ | $\mathcal{O}(\log N)$ |
| **Triangular Nested** | `for i in range(n): for j in range(i, n):` | $\frac{n(n + 1)}{2}$ | $\mathcal{O}(N^2)$ |
| **Independent Nested** | `for i in range(n): for j in range(m):` | $n \times m$ | $\mathcal{O}(N \times M)$ |
