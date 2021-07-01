from typing import Counter


def find_single(nums):
    for key in nums:
        counter = 0
        for num in nums:
            if num == key:
                counter += 1
        if counter == 1:
            return key
            


print(find_single([2,1,1,3,3]))