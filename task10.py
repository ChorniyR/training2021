def get_index(nums, target):
    try:
        return nums.index(target)
    except ValueError:
        return abs(nums[0] - target)


print(get_index([-1, 0, 2, 3, 4, 5, 7], 1))
