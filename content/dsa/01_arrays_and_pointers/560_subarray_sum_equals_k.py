class Solution:
    def subarraySum_brute_force(self, nums: list[int], k: int) -> int:
        """
        Approach 1: Brute Force
        Generate all subarrays and sum them.
        Time: O(N^2)
        Space: O(1)
        """
        count = 0
        n = len(nums)
        for i in range(n):
            curr_sum = 0
            for j in range(i, n):
                curr_sum += nums[j]
                if curr_sum == k:
                    count += 1
        return count

    def subarraySum_prefix_array(self, nums: list[int], k: int) -> int:
        """
        Approach 2: Semi-Optimized (Explicit Prefix Sum Array + Nested Loops)
        Computes prefix sum array, then checks prefix[j] - prefix[i] == k.
        Time: O(N^2)
        Space: O(N)
        """
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        count = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                if prefix[j] - prefix[i] == k:
                    count += 1
        return count

    def subarraySum(self, nums: list[int], k: int) -> int:
        """
        Approach 3: Optimized (Running Prefix Sum + Hash Map Frequency)
        If cur_sum - (earlier_prefix) == k, then earlier_prefix = cur_sum - k.
        Time: O(N)
        Space: O(N)
        """
        prefix_counts = {0: 1}
        cur_sum = 0
        count = 0

        for x in nums:
            cur_sum += x
            needed_cut = cur_sum - k
            count += prefix_counts.get(needed_cut, 0)
            prefix_counts[cur_sum] = prefix_counts.get(cur_sum, 0) + 1

        return count


def test_subarray_sum():
    sol = Solution()
    approaches = [
        ("Brute Force", sol.subarraySum_brute_force),
        ("Prefix Array Nested", sol.subarraySum_prefix_array),
        ("Optimized Running Hash Map", sol.subarraySum),
    ]

    test_cases = [
        ([1, 1, 1], 2, 2),
        ([1, 2, 3], 3, 2),
        ([1, -1, 0], 0, 3),
        ([1, 2, 1, -1, 2], 3, 3),
        ([3], 3, 1),
        ([3], 2, 0),
    ]

    for name, fn in approaches:
        for nums, k, expected in test_cases:
            res = fn(nums, k)
            assert res == expected, f"{name} failed on nums={nums}, k={k}: got {res}, expected {expected}"

    print("All 3 approaches for LC 560 passed successfully!")


if __name__ == "__main__":
    test_subarray_sum()
