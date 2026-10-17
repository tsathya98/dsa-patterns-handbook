# Two Pointers Cheat Sheet

Replace $\mathcal{O}(n^2)$ nested loops with two coordinated index pointers that cross the data in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space.

## 1. When to use Two Pointers
Use this pattern when:
1. Element order is fixed or sorted.
2. Once a pointer moves past an element, you never need to backtrack to it.
3. You are searching for pairs, comparing two sequences, compacting an array in place, or expanding from a center.

---

## 2. The 6 Formations

```text
A. THE SQUEEZE (Inward)          B. SCOUT & WRITER (Same dir)     C. TWO CONVEYOR BELTS (2 arrays)
l ───►           ◄─── r          slow (writer)                    p1 ───► [ .  .  . ]
[ .  .  .  .  .  .  . ]          [ .  .  .  .  . ]                p2 ──────► [ .  .  .  . ]
                                      ▲
                                     fast (scout) ───►

D. ANCHOR & SCOUT (Chunks)       E. TAIL-BUFFER (Backwards)       F. FLASHLIGHT BEAM (Outward)
anchor                           p1 ◄──      p (write) ◄──        ◄─── l  r ───►
  ▼                              [ 2, 5, 6,  0, 0, 0 ]            [ .  .  c  .  . ]
[ 0, 1, 2,  4, 5,  7 ]           [ 1, 3, 4 ] (p2 ◄──)
  └─────┘ (scout)
```

### Formation A: The Squeeze (`l = 0, r = n - 1`)
Pointers start at opposite ends and walk inward until `l < r` fails.
- **Use for:** Palindrome checks ([LC 125](../01_arrays_and_pointers/125_valid_palindrome.md)), sorted pair sums ([LC 167](../01_arrays_and_pointers/167_two_sum_ii_input_array_is_sorted.md), [LC 15](../01_arrays_and_pointers/15_3sum.md)), container bounds ([LC 11](../01_arrays_and_pointers/11_container_with_most_water.md)), array reversal ([LC 189](../01_arrays_and_pointers/189_rotate_array.md)).
- **Which pointer moves?** In a sorted array, `l += 1` increases the sum; `r -= 1` decreases the sum. In container problems, move whichever wall is shorter.

```python
l, r = 0, len(arr) - 1
while l < r:
    if need_larger(arr[l], arr[r]):
        l += 1
    else:
        r -= 1
```

### Formation B: Scout & Writer (`slow = 0, fast = 0`)
Both start at index `0`. `fast` scans every element; `slow` marks the next write slot for valid items.
- **Use for:** In-place filtering or compaction ([LC 283](../01_arrays_and_pointers/283_move_zeroes.md), [LC 27](../01_arrays_and_pointers/27_remove_element.md), [LC 26](../01_arrays_and_pointers/26_remove_duplicates_from_sorted_array.md), [LC 80](../01_arrays_and_pointers/80_remove_duplicates_from_sorted_array_ii.md)).

```python
slow = 0
for fast in range(len(nums)):
    if is_valid(nums[fast]):
        nums[slow] = nums[fast]
        slow += 1
```

### Formation C: Two Conveyor Belts (`p1 = 0, p2 = 0`)
One pointer per sequence, advancing independently on matches.
- **Use for:** Subsequence checks ([LC 392](../01_arrays_and_pointers/392_is_subsequence.md)), merging two separate lists ([LC 21](../02_linked_lists/21_merge_two_sorted_lists.md)).

```python
p1 = p2 = 0
while p1 < len(s) and p2 < len(t):
    if s[p1] == t[p2]:
        p1 += 1
    p2 += 1
```

### Formation D: Anchor & Scout (Disjoint Chunks)
`start` marks the beginning of a contiguous run; an inner `while` loop advances `i` until the run breaks.
- **Use for:** Grouping consecutive runs ([LC 228](../01_arrays_and_pointers/228_summary_ranges.md)), run-length encoding (LC 443).
- **How this differs from Sliding Window:** Sliding windows overlap (one element belongs to many candidate windows, like [LC 3](../01_arrays_and_pointers/3_longest_substring_without_repeating_characters.md)). Anchor & Scout slices the array into disjoint, non-overlapping chunks where each element belongs to exactly one chunk.

```python
i = 0
while i < len(nums):
    start = nums[i]
    while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
        i += 1
    res.append(f"{start}->{nums[i]}" if start != nums[i] else str(start))
    i += 1
```

### Formation E: Tail-Buffer (Right-to-Left Placement)
When modifying an array in place that has empty buffer slots at the end, going left-to-right overwrites unread values. Work backward from the tail and place the largest values first.
- **Use for:** [LC 88: Merge Sorted Array](../01_arrays_and_pointers/88_merge_sorted_array.md), LC 977: Squares of a Sorted Array.

```python
p1, p2, p = m - 1, n - 1, m + n - 1
while p1 >= 0 and p2 >= 0:
    if nums1[p1] > nums2[p2]:
        nums1[p] = nums1[p1]
        p1 -= 1
    else:
        nums1[p] = nums2[p2]
        p2 -= 1
    p -= 1
while p2 >= 0:
    nums1[p] = nums2[p2]
    p2 -= 1
    p -= 1
```

### Formation F: Outward Expand Around Center (Flashlight Beam)
Start `l` and `r` at a center and expand outward (`l -= 1, r += 1`) while characters match.
- **Use for:** Finding palindromic substrings inside a string ([LC 5](../01_arrays_and_pointers/5_longest_palindromic_substring.md), LC 647).
- **Odd vs. even centers:** Always check both `(i, i)` for odd-length palindromes and `(i, i + 1)` for even-length palindromes. When the loop stops, `l` and `r` have stepped one index too far, so the valid slice is `s[l + 1 : r]`.

---

## 3. Quick Decision Table

| Goal | Formation | Initial Pointers | Example |
| :--- | :--- | :--- | :--- |
| Pair sum in sorted array | A: Squeeze | `l = 0, r = n - 1` | LC 167, LC 15 |
| Check if whole string is palindrome | A: Squeeze | `l = 0, r = n - 1` | LC 125 |
| Find longest palindrome inside string | F: Outward Expand | `(i, i)` and `(i, i + 1)` | LC 5, LC 647 |
| Max container area | A: Squeeze | `l = 0, r = n - 1` | LC 11 |
| Filter / compact array in place | B: Scout & Writer | `slow = 0, fast = 0` | LC 26, 27, 80, 283 |
| Match subsequence across 2 strings | C: Conveyor Belts | `p1 = 0, p2 = 0` | LC 392 |
| Group consecutive streaks | D: Anchor & Scout | `i = 0`, inner `while` | LC 228 |
| In-place merge into trailing buffer | E: Tail-Buffer | `p1 = m-1, p2 = n-1, p = m+n-1` | LC 88 |
