# LeetCode 1290: Convert Binary Number in a Linked List to Integer

> **Pattern:** Stream accumulation (Horner's rule / bit shifting)  
> **Difficulty:** Easy  
> **Link:** [LeetCode 1290](https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/)

## The problem

Given `head` of a singly linked list where each node holds `0` or `1`, return the decimal value of the binary number. The most significant bit sits at the `head` of the list.

```text
Input:  head = [1, 0, 1]
Output: 5
Explanation: (101) in base 2 is (1 * 4) + (0 * 2) + (1 * 1) = 5.
```

## Why the naive way fails

A common first attempt builds a string in one loop (`num += str(head.val)`) and computes powers of 2 in a second loop. Because strings in Python are immutable, `num += ...` allocates a new string and copies previous characters on each step, turning a linear problem into $\mathcal{O}(n^2)$ time and $\mathcal{O}(n)$ extra space. You also do not know the total length of the list upfront unless you waste an extra pass counting nodes.

## The core trick

Think about how you read a normal base-10 number like `"123"` from left to right when you do not know how many digits are left:
- Start with `ans = 0`.
- Read `1`: `ans = (0 * 10) + 1 = 1`
- Read `2`: `ans = (1 * 10) + 2 = 12`
- Read `3`: `ans = (12 * 10) + 3 = 123`

Every new digit shifts the running total one place to the left (multiplying by the base) and adds the new digit.

For base 2, do the exact same thing, except multiply by `2` instead of `10`:
- `ans = ans * 2 + head.val`
- Or using bitwise operators: shift all existing bits left by 1 (`ans << 1`) and drop the new bit into the ones place (`| head.val`).

### Algorithm steps:
* **1. Initialize accumulator:** Set `ans = 0`.
* **2. Traverse the list:** While `head` is not None:
  * Shift accumulator left and insert the current bit: `ans = (ans << 1) | head.val` (or `ans = ans * 2 + head.val`).
* **3. Advance pointer:** Move `head = head.next`.
* **4. Return result:** Once traversal reaches None, return `ans`.

## Step-by-step trace

Trace on `head = [1, 0, 1]`:

```text
Start:  ans = 0  (binary 0)
Node 1 (val = 1):  ans = (0 * 2) + 1 = 1  (binary 1)
Node 2 (val = 0):  ans = (1 * 2) + 0 = 2  (binary 10)
Node 3 (val = 1):  ans = (2 * 2) + 1 = 5  (binary 101)
```

## Traps to watch for

- **Operator precedence with bitwise shifts:** In Python, `+` has higher precedence than `<<` and `|`. If you mix them as `ans << 1 + head.val`, Python evaluates `1 + head.val` first and shifts by 2 bits. Always wrap `(ans << 1) | head.val` in parentheses, or stick to `ans = ans * 2 + head.val`.

## Solution

<details>
<summary>Spoiler: Solution Code (Both Approaches)</summary>

```python
# Approach 1: Array conversion + reverse indexing (Intuitive, O(N) space)
class Solution:
    def getDecimalValue(self, head: ListNode | None) -> int:
        lst = []
        cur = head
        while cur:
            lst.append(cur.val)
            cur = cur.next
        tot = 0
        for i in range(len(lst) - 1, -1, -1):
            tot += lst[len(lst) - i - 1] * (2 ** i)
        return tot


# Approach 2: Stream accumulation / Horner's rule (Optimal, O(1) space)
class SolutionOptimal:
    def getDecimalValue(self, head: ListNode | None) -> int:
        total = 0
        while head:
            total = total * 2 + head.val  # Or: (total << 1) | head.val
            head = head.next
        return total
```

</details>

## Complexity

- **Time:** $\mathcal{O}(n)$ single pass.
- **Space:** $\mathcal{O}(1)$ auxiliary memory.
