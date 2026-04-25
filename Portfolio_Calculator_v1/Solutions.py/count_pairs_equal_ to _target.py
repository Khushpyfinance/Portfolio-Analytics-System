class Solution(object):
    def equal_pairs(self, nums):
        seen = {}
        target = 6
        count = 0

        for i in range(len(nums)):
            num = nums[i]
            needed = target - num

            if needed in seen:
                count += seen[needed]

            if num in seen:
                seen[num] += 1
            else:
                seen[num] = 1

        return count
            
solution = Solution()
result = solution.equal_pairs([1,2,3,4,5])
print(result)  