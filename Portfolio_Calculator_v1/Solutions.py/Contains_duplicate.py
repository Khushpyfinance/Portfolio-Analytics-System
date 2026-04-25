class Solution(object):
    def contains_duplicate(self, nums):
        seen = set()
        for num in nums:
            if num in seen:
                return True
            else:
                seen.add(num)
        
        return False
        
solution = Solution() 
result = solution.contains_duplicate([1, 2, 3, 1]) 
print(result)