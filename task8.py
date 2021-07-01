def find_missing_number(nums):
    sorted_nums = sorted(nums)
    for indx, number in enumerate(sorted_nums):
        try:
            if number != sorted_nums[indx + 1] - 1:
                return number + 1
        except IndexError:
            return number + 1


print(find_missing_number([1, 2, -1]))
