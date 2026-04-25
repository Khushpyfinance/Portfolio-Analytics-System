class Solution(object):
    def most_num(self, nums):
        count = {}
        max_count = 0
        result = None

        for num in nums:
            # Step 1: update frequency
            if num in count:
                count[num] += 1
            else:
                count[num] = 1

            # Step 2: check if this is new max
            if count[num] > max_count:
                max_count = count[num]
                result = num

        return result


solution = Solution()
result = solution.most_num([2,2,1,1,1,2,2])
print(result)