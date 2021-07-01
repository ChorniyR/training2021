def find_pairs(numbers, target):
    pairs = [[numbers.index(num1), numbers.index(num2)] for num1 in nums for num2 in nums
             if num1 + num2 == target]
    return pairs


def display(pairs, target):
    for pair in pairs:
        print(f" nums[{pair[0]}] + nums[{pair[1]}] gives {target}")


if __name__ == '__main__':
    nums = [1, 3, 4, 5, 7, 2]
    target = 8

    pairs = find_pairs(nums, target)
    display(pairs, target)
