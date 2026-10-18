# Factors, primes, and iteration counting

> **Course reference:** CodeKerdos DSA, Class 3  
> **Core concept:** Deriving $\mathcal{O}(\sqrt{N})$ from symmetric factor pairs, primality testing, factor sum, sorted factor printing, and exact loop iteration formulas.

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

---

## 3. Homework 1: Sum of all factors of $N$ in $\mathcal{O}(\sqrt{N})$

**Problem:** Given a positive integer $N$, return the sum of all its positive factors in $\mathcal{O}(\sqrt{N})$ time.

### The core trick
Instead of adding `1` or `2` to a counter, add the actual factor values `i` and `n // i` to a running `total`. If `i * i == n` (a perfect square), only add `i` once so the square root isn't double-counted.

### Step-by-step trace (`N = 36`)

**Iteration 1 (`i = 1`, `1 * 1 <= 36`):**
`36 % 1 == 0` and `1 != 36`. Add both `1` and `36`:
```text
pair = (1, 36)   -> total = 0 + 1 + 36 = 37
```

**Iteration 2 (`i = 2`, `2 * 2 <= 36`):**
`36 % 2 == 0` and `2 != 18`. Add both `2` and `18`:
```text
pair = (2, 18)   -> total = 37 + 2 + 18 = 57
```

**Iteration 3 (`i = 3`, `3 * 3 <= 36`):**
`36 % 3 == 0` and `3 != 12`. Add both `3` and `12`:
```text
pair = (3, 12)   -> total = 57 + 3 + 12 = 72
```

**Iteration 4 (`i = 4`, `4 * 4 <= 36`):**
`36 % 4 == 0` and `4 != 9`. Add both `4` and `9`:
```text
pair = (4, 9)    -> total = 72 + 4 + 9 = 85
```

**Iteration 5 (`i = 5`, `5 * 5 <= 36`):**
`36 % 5 == 1 != 0`. Skip.

**Iteration 6 (`i = 6`, `6 * 6 <= 36`):**
`36 % 6 == 0` and `6 * 6 == 36` (perfect square!). Add `6` once:
```text
pair = (6, 6)    -> total = 85 + 6 = 91
```

Loop ends when `i = 7` (`49 > 36`). Final sum = `91`.

<details>
<summary>Spoiler: Solution Code</summary>

```python
def sum_of_factors(n: int) -> int:
    total = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            if i * i == n:
                total += i          # Perfect square root: add once
            else:
                total += i + (n // i)  # Add both partners
        i += 1
    return total
```

</details>

---

## 4. Homework 2: Print all factors in sorted order in $\mathcal{O}(\sqrt{N})$

**Problem:** Given an integer $N$, print or return all factors of $N$ in ascending sorted order in $\mathcal{O}(\sqrt{N})$ time without calling `.sort()`.

### Why naive collection fails
If you append both `i` and `n // i` to a single list as you go, the list comes out interleaved:
`[1, 24, 2, 12, 3, 8, 4, 6]`.

### The core trick
Notice how the two halves of each factor pair behave as `i` increases from $1$ to $\lfloor\sqrt{N}\rfloor$:
* The **small factors** (`i`) naturally grow in **ascending order**: `1, 2, 3, 4`.
* The **large factors** (`n // i`) naturally shrink in **descending order**: `24, 12, 8, 6`.

You can solve this in $\mathcal{O}(\sqrt{N})$ time in two ways:
1. **Two-list method ($\mathcal{O}(\sqrt{N})$ space):** Push `i` into `small` and `n // i` into `large`, then return `small + large[::-1]`.
2. **Two-pass method ($\mathcal{O}(1)$ extra space):**
   * Pass 1: Loop `i` from `1` up to $\lfloor\sqrt{N}\rfloor$ and print `i` whenever `n % i == 0`.
   * Pass 2: Loop `i` backward from $\lfloor\sqrt{N}\rfloor$ down to `1` and print `n // i` whenever `n % i == 0` (skipping `i * i == n` so you don't print the square root twice).

### Step-by-step trace (`N = 24`)

```text
i = 1:  small = [1]             large = [24]
i = 2:  small = [1, 2]          large = [24, 12]
i = 3:  small = [1, 2, 3]       large = [24, 12, 8]
i = 4:  small = [1, 2, 3, 4]    large = [24, 12, 8, 6]

Reverse large:  large[::-1] = [6, 8, 12, 24]
Concatenate:    [1, 2, 3, 4, 6, 8, 12, 24]
```

<details>
<summary>Spoiler: Solution Code</summary>

```python
# Method 1: Two lists (returns sorted list in O(sqrt(N)) time)
def factors_sorted(n: int) -> list[int]:
    small = []
    large = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            small.append(i)
            if i * i != n:
                large.append(n // i)
        i += 1
    return small + large[::-1]


# Method 2: Two passes (O(sqrt(N)) time, O(1) extra space)
def print_factors_sorted_o1_space(n: int) -> None:
    i = 1
    while i * i <= n:
        if n % i == 0:
            print(i, end=" ")
        i += 1

    i -= 1
    if i * i == n:
        i -= 1  # Skip perfect square root on the way back down

    while i >= 1:
        if n % i == 0:
            print(n // i, end=" ")
        i -= 1
```

</details>

---

## 5. Primality check in $\mathcal{O}(\sqrt{N})$

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

## 6. Exact loop iteration counts

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
