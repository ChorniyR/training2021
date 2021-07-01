import statistics

def get_median(nums1,nums2):
    merged = list(set(nums1) ^ set(nums2))
    return statistics.median(merged)

print(get_median([1,3,5],[2,4]))


