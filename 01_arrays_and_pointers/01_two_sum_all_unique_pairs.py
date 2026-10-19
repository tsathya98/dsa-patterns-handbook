def two_sum_unique_pairs_brute_force(arr: list[int], k: int) -> list[tuple[int, int]]:
    """
    Approach 1: Brute Force Nested Loops
    Time: O(N^2)
    Space: O(U) where U is the number of unique pairs
    """
    unique_pairs = set()
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == k:
                pair = (min(arr[i], arr[j]), max(arr[i], arr[j]))
                unique_pairs.add(pair)
    return sorted(list(unique_pairs))


def two_sum_unique_pairs_two_pointers(arr: list[int], k: int) -> list[tuple[int, int]]:
    """
    Approach 2: Semi-Optimized Sort + Two Pointers Squeeze
    Sorts array and walks left/right pointers, skipping adjacent duplicates.
    Time: O(N log N)
    Auxiliary Space: O(1) beyond the sort
    """
    sorted_arr = sorted(arr)
    left = 0
    right = len(sorted_arr) - 1
    result = []

    while left < right:
        curr_sum = sorted_arr[left] + sorted_arr[right]
        if curr_sum == k:
            result.append((sorted_arr[left], sorted_arr[right]))
            left += 1
            right -= 1
            # Skip duplicates on both sides
            while left < right and sorted_arr[left] == sorted_arr[left - 1]:
                left += 1
            while left < right and sorted_arr[right] == sorted_arr[right + 1]:
                right -= 1
        elif curr_sum < k:
            left += 1
        else:
            right -= 1

    return result


def two_sum_unique_pairs(arr: list[int], k: int) -> list[tuple[int, int]]:
    """
    Approach 3: Optimized Single-Pass Hash Set with Canonical Tuples
    Time: O(N)
    Space: O(N)
    """
    seen = set()
    used_pairs = set()
    result = []

    for x in arr:
        comp = k - x
        if comp in seen:
            pair = (min(x, comp), max(x, comp))
            if pair not in used_pairs:
                used_pairs.add(pair)
                result.append(pair)
        seen.add(x)

    return result


def test_two_sum_unique_pairs():
    approaches = [
        ("Brute Force", two_sum_unique_pairs_brute_force),
        ("Sort + Two Pointers", two_sum_unique_pairs_two_pointers),
        ("Hash Set Canonical", two_sum_unique_pairs),
    ]

    test_cases = [
        ([1, 5, 7, -1, 5], 6, [(-1, 7), (1, 5)]),
        ([3, 3, 3, 3], 6, [(3, 3)]),
        ([1, 2, 3, 4, 5], 10, []),
        ([2, 4, 3, 5, 7, 8, 9], 7, [(2, 5), (3, 4)]),
        ([0, 0, 0], 0, [(0, 0)]),
    ]

    for name, fn in approaches:
        for arr, k, expected in test_cases:
            res = fn(arr, k)
            assert sorted(res) == sorted(expected), f"{name} failed on {arr}, k={k}: got {res}, expected {expected}"

    print("All Two Sum unique pairs approaches passed successfully!")


if __name__ == "__main__":
    test_two_sum_unique_pairs()
