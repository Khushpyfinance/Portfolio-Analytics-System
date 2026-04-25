class Solution(object):
    def group_anagrams(self, strs):
        groups = {}

        for word in strs:
            key = tuple(sorted(word))

            if key not in groups:
                groups[key] = []

            groups[key].append(word)
            
        return list(groups.values())
        
solution = Solution()
result = solution.group_anagrams(["eat","tea","tan","ate","nat","bat"])
print(result)    