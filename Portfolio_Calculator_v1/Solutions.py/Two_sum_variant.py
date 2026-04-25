class Solution(object):
    def Two_sum_varient(self, nums):
        seen = set()
        target = 9
        for i in range(len(nums)):
            num = nums[i]
            needed = target - num
            if needed in seen:
                return [needed, num]
            
            seen.add(num)

        return []
    
solution = Solution() 
result = solution.Two_sum_varient([2, 7, 11, 15]) 
print(result)