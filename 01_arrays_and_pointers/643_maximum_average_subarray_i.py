"""
LeetCode 643: Maximum Average Subarray I
Pattern: Fixed-Size Sliding Window (Running Differential / Add-New-Sub-Old)
Difficulty: Easy
Link: https://leetcode.com/problems/maximum-average-subarray-i/
"""

class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        """
        Time Complexity: O(n) - exactly 1 pass over nums
        Space Complexity: O(1) - tracks only running sums
        """
        # 1. Establish the baseline sum for the first window of size k
        tot = sum(nums[:k])
        max_tot = tot
        
        # 2. Slide the window from index k to the end
        # At each step:
        # - Add entering element: nums[i]
        # - Subtract leaving element: nums[i - k]
        for i in range(k, len(nums)):
            tot += nums[i] - nums[i - k]
            if tot > max_tot:
                max_tot = tot
                
        # 3. Divide by k once at the very end to maximize precision and avoid floating-point overhead in the loop
        return max_tot / k


if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ([1, 12, -5, -6, 50, 3], 4, 12.75),
        ([5], 1, 5.0),
        ([0, 4, 0, 3, 2], 1, 4.0),
        ([-1], 1, -1.0),
        ([4, 2, 1, 3, 3], 2, 3.0),
    ]
    
    for nums, k, expected in test_cases:
        actual = sol.findMaxAverage(nums, k)
        assert abs(actual - expected) < 1e-5, f"Failed for nums={nums}, k={k}: expected {expected}, got {actual}"
        print(f"✓ nums={nums}, k={k} -> max_avg = {actual}")
        
    print("\nAll test cases passed!")
