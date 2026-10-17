# Bit Manipulation Cheat Sheet

## 1. The 6 Bitwise Operators

| Operator | Name | Rule | Example (`5 = 101₂`, `3 = 011₂`) |
| :--- | :--- | :--- | :--- |
| `&` | AND | `1` only if both bits are `1` | `5 & 3` $\to 001_2 = 1$ |
| `\|` | OR | `1` if at least one bit is `1` | `5 \| 3` $\to 111_2 = 7$ |
| `^` | XOR | `1` if bits differ (`0^1 = 1`, `1^1 = 0`) | `5 ^ 3` $\to 110_2 = 6$ |
| `~` | NOT | Inverts all bits (`~x == -(x + 1)`) | `~5` $\to -6$ |
| `<<` | Left Shift | Shifts bits left, multiplies by $2^k$ | `5 << 1` $\to 1010_2 = 10$ |
| `>>` | Right Shift | Shifts bits right, floor-divides by $2^k$ | `5 >> 1` $\to 10_2 = 2$ |

---

## 2. Core Tricks

### Trick 1: Stream Accumulation / Horner's Rule ([LC 1290](../02_linked_lists/1290_convert_binary_number_in_a_linked_list_to_integer.md))
When reading bits from left to right, shift the running total left by 1 (multiply by 2) and attach the incoming bit:
```python
ans = 0
while head:
    ans = (ans << 1) | head.val
    head = head.next
```

### Trick 2: Odd or Even Check
Check the least significant bit (LSB):
```python
is_odd = (n & 1) == 1
```

### Trick 3: Clear the Lowest Set Bit (`n & (n - 1)`) (LC 191, LC 231)
Subtracting 1 flips the rightmost `1` bit to `0` and turns all trailing zeros after it to `1`. ANDing `n` with `n - 1` wipes out that lowest `1` bit in one operation:

```text
  n         = 110100
  n - 1     = 110011
  n & (n-1) = 110000  (rightmost 1 cleared)
```

- **Power of two check (LC 231):** Powers of two have a single `1` bit (`4 = 100₂`, `8 = 1000₂`).
  ```python
  def isPowerOfTwo(n: int) -> bool:
      return n > 0 and (n & (n - 1)) == 0
  ```
- **Count set bits / Hamming Weight (LC 191):** Loop only as many times as there are `1` bits.
  ```python
  def hammingWeight(n: int) -> int:
      count = 0
      while n > 0:
          n &= (n - 1)
          count += 1
      return count
  ```

### Trick 4: Isolate the Lowest Set Bit (`n & -n`)
Two's complement negation `-n` is `~n + 1`, so `n & -n` zeroes everything except the rightmost `1` bit (`12 & -12 == 4`). Used in Fenwick Trees (Binary Indexed Trees).

### Trick 5: XOR Duplicate Cancellation (LC 136, LC 268)
XOR obeys three rules:
1. $x \oplus x = 0$ (duplicates cancel out).
2. $x \oplus 0 = x$.
3. Order does not matter ($a \oplus b \oplus a = b$).

```python
def singleNumber(nums: list[int]) -> int:
    res = 0
    for num in nums:
        res ^= num
    return res
```

---

## 3. Quick Decision Table

| Problem Goal | Bitwise Expression | Classic Problem |
| :--- | :--- | :--- |
| Convert bit stream to int | `ans = (ans << 1) \| bit` | LC 1290 |
| Find single non-duplicate | `res ^= num` | LC 136 |
| Check power of two | `n > 0 and (n & (n - 1)) == 0` | LC 231 |
| Count set `1` bits | `n &= (n - 1)` in a `while n:` loop | LC 191 |
| Missing number in `0..n` | XOR all indices `0..n` with all values | LC 268 |
