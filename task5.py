def find_single(nums):
    counts = {}
    for key in nums:
        counts[key] = nums.count(key)
    return min(counts, key=counts.get)


print(find_single([2, 2, 2, 1, 1, 3, 3, 7]))
