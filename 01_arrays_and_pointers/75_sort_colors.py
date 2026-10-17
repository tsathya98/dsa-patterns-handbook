"""
LeetCode 75: Sort Colors (Dutch National Flag Algorithm)
https://leetcode.com/problems/sort-colors/

Given an array nums with n objects colored red, white, or blue, sort them in-place
so that objects of the same color are adjacent, with the colors in the order red (0), white (1), and blue (2).
"""


class Solution:
    def sortColors(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        Three-pointer partitioning (Dijkstra's Dutch National Flag).
        Time Complexity: O(n) single pass
        Space Complexity: O(1) in-place
        """
        low = 0          # Boundary for 0s: nums[0...low-1] are 0s
        mid = 0          # Current inspection element
        high = len(nums) - 1  # Boundary for 2s: nums[high+1...end] are 2s

        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:  # nums[mid] == 2
                nums[high], nums[mid] = nums[mid], nums[high]
                high -= 1
                # Note: Do NOT increment mid here! The swapped element from high has not been inspected yet.


if __name__ == "__main__":
    sol = Solution()
    arr1 = [2, 0, 2, 1, 1, 0]
    sol.sortColors(arr1)
    assert arr1 == [0, 0, 1, 1, 2, 2]

    arr2 = [2, 0, 1]
    sol.sortColors(arr2)
    assert arr2 == [0, 1, 2]
    print("Sort Colors tests passed!")
