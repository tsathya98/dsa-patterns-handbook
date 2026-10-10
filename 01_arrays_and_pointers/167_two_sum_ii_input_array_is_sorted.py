from typing import List

class Solution:
    def twoSum_two_pointers(self, numbers: List[int], target: int) -> List[int]:
        """
        Optimal FAANG Solution: Two Pointers Formation A (Inward Squeeze)
        
        Time Complexity: O(n)
        Auxiliary Space: O(1) - strictly constant space (meets problem constraints)
        """
        l, r = 0, len(numbers) - 1
        
        while l < r:
            cur_sum = numbers[l] + numbers[r]
            if cur_sum == target:
                return [l + 1, r + 1]  # 1-indexed
            elif cur_sum < target:
                # Sum too small -> squeeze left pointer forward to bigger numbers
                l += 1
            else:
                # Sum too large -> squeeze right pointer backward to smaller numbers
                r -= 1
                
        return []

    def twoSum_hashmap(self, numbers: List[int], target: int) -> List[int]:
        """
        HashMap Approach (LC 1 style)
        Time: O(n), Space: O(n)
        """
        dct = {}
        for i, num in enumerate(numbers):
            diff = target - num
            if diff in dct:
                return [dct[diff] + 1, i + 1]
            if num not in dct:
                dct[num] = i
        return []


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ([2, 7, 11, 15], 9, [1, 2]),
        ([2, 3, 4], 6, [1, 3]),
        ([-1, 0], -1, [1, 2]),
        ([0, 0, 3, 4], 0, [1, 2]),
    ]
    
    for nums, target, expected in test_cases:
        assert sol.twoSum_two_pointers(nums, target) == expected
        assert sol.twoSum_hashmap(nums, target) == expected
        
    print("All unit tests for LC 167 passed successfully!")
