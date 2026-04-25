class Solution(object):
    def missing_number(self, nums):
        for i in range(len(nums)+ 1):
            if i not in nums:
                return i
            
solution = Solution() 
result = solution.missing_number([1, 0, 3]) 
print(result)