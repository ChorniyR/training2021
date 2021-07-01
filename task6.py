def get_median(nums1, nums2):
    merged = list(set(nums1) ^ set(nums2))

    median_index = len(merged) // 2
    if len(merged) % 2 != 0:
        return merged[int(median_index)]
    return (merged[median_index] + merged[median_index-1]) / 2


print(get_median([1, 2], [5]))
