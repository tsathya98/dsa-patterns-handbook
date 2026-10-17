# ⚡ Bit Manipulation Master Cheat Sheet & Decision Guide

> **Pattern:** Bit Manipulation & Bitwise Operations  
> **Target Audience:** Hardware, Systems (Nvidia, Qualcomm), and High-Performance Software Engineering.  
> **Philosophy:** Bits are the native language of the CPU. What takes loops and dictionaries in high-level code often takes **1 single clock cycle** with bitwise operators.

---

## 💡 1. The 6 Fundamental Bitwise Operators

| Operator | Name | What it Does | Silicon Rule | Example (a = 5 = 101₂, b = 3 = 011₂) |
| :---: | :--- | :--- | :--- | :--- |
| **`&`** | **AND** | `1` only if BOTH bits are 1 | Multiplies bits | `5 & 3` $\implies 001_2 = \mathbf{1}$ |
| **`\|`** | **OR** | `1` if AT LEAST ONE bit is 1 | Sets a bit | `5 \| 3` $\implies 111_2 = \mathbf{7}$ |
| **`^`** | **XOR** | `1` if bits are DIFFERENT (`0^1=1`, `1^1=0`) | Toggles a bit | `5 ^ 3` $\implies 110_2 = \mathbf{6}$ |
| **`~`** | **NOT** | Flips all bits (`~x = -(x + 1)`) | Inverts | `~5` $\implies \mathbf{-6}$ |
| **`<<`** | **Left Shift** | Shifts bits left, fills with 0 (Multiplies by $2^k$) | Shift left | `5 << 1` $\implies 1010_2 = \mathbf{10}$ |
| **`>>`** | **Right Shift** | Shifts bits right (Divides by $2^k$) | Shift right | `5 >> 1` $\implies 10_2 = \mathbf{2}$ |

---

## 🕹️ 2. The Stream Accumulation Pattern (Horner's Rule in Bits)

When reading an incoming stream of bits from left to right (like in a network packet or [LC 1290: Convert Binary in Linked List](../02_linked_lists/1290_convert_binary_number_in_a_linked_list_to_integer.md)):

```text
Bits arrive:  [ 1 ]  ──►  [ 0 ]  ──►  [ 1 ]   (Binary 101 = Decimal 5)

Step 1: Start ans = 0
Step 2: ans = (ans << 1) | 1  -> 0001 (1)
Step 3: ans = (ans << 1) | 0  -> 0010 (2)
Step 4: ans = (ans << 1) | 1  -> 0101 (5)
```

```python
ans = 0
while head:
    ans = (ans << 1) | head.val  # Shift left by 1 (multiply by 2), attach new bit!
    head = head.next
```

---

## 🏆 3. The 5 Essential "Power Hacks" (Interview Weapons)

### 🔹 Hack 1: Odd or Even Check
* **Normal Code:** `if n % 2 == 1:` (requires division/modulo).
* **Bitwise Hack:**
  ```python
  if n & 1:  # The least significant bit (LSB) is 1 for odd numbers!
      # n is Odd
  ```

---

### 🔹 Hack 2: Is `n` a Power of 2? (LC 231)
Powers of 2 have **exactly one bit set**:
* $4 = 100_2$
* $8 = 1000_2$
* $16 = 10000_2$

Notice what happens when you subtract 1:
* $8 - 1 = 7 = 0111_2$
* $8 \ \& \ 7 = 1000_2 \ \& \ 0111_2 = \mathbf{0}$!

```python
def isPowerOfTwo(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0
```

---

### 🔹 Hack 3: Clear the Lowest Set Bit (Brian Kernighan's Algorithm - LC 191)
`n & (n - 1)` always wipes out the **rightmost `1` bit** to `0`:

```text
  n     = 1 1 0 1 0 0
  n - 1 = 1 1 0 0 1 1
──────────────────────
  n & (n-1) = 1 1 0 0 0 0  (Lowest 1 bit wiped out!)
```

#### Count Number of Set Bits (Hamming Weight) in $\mathcal{O}(\text{bits})$ time:
```python
def hammingWeight(n: int) -> int:
    count = 0
    while n > 0:
        n = n & (n - 1)  # Strips 1 set bit per round!
        count += 1
    return count
```

---

### 🔹 Hack 4: Extract the Lowest Set Bit (LSB)
To isolate **only** the lowest set bit and turn everything else to `0`:
```python
lowest_bit = n & -n
```
* Example: $12 = 1100_2 \implies 12 \ \& \ (-12) = 0100_2 = \mathbf{4}$!
* *Why it works:* Two's complement negation `-n` inverts all bits and adds 1.

---

### 🔹 Hack 5: XOR Cancellation / The Duplicate Eraser (LC 136)
The 3 magical properties of XOR:
1. $x \oplus x = \mathbf{0}$ (Any number XORed with itself vanishes!).
2. $x \oplus 0 = \mathbf{x}$ (Any number XORed with 0 stays itself).
3. Order doesn't matter: $a \oplus b \oplus a = (a \oplus a) \oplus b = 0 \oplus b = \mathbf{b}$.

#### Find the Single Number in an array of duplicates:
```python
def singleNumber(nums: list[int]) -> int:
    res = 0
    for num in nums:
        res ^= num  # All duplicates destroy each other!
    return res
```

---

## 🎯 4. Quick Decision Matrix

| What is the problem asking? | Bitwise Formula | Classic Problem |
| :--- | :--- | :--- |
| Accumulate stream of bits | `(ans << 1) \| bit` | LC 1290: Convert Binary in Linked List |
| Find single non-duplicate | `res ^= num` | LC 136: Single Number |
| Check power of two | `n > 0 and (n & (n - 1)) == 0` | LC 231: Power of Two |
| Count number of 1-bits | `n = n & (n - 1)` loop | LC 191: Number of 1 Bits |
| Missing number in range `0..n` | XOR all indices and values | LC 268: Missing Number |
| Swap two numbers without temp | `a ^= b; b ^= a; a ^= b` | Bitwise Swap |
