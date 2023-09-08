def twoSum(num, target: int):
    for i in range (0,len(num)-1):
        for j in range (i+1,len(num)):
            if num[i]+num[j]==target:
                return [i,j]
print(twoSum([2,7,11,15],9))

def twoSum2(self, nums, target):
        seen = {}
        for i, v in enumerate(nums):
            remaining = target - v
            if remaining in seen:
                return [seen[remaining], i]
            seen[v] = i
        return []