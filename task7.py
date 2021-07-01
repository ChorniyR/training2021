def find_prefix(strs):
    prefix = strs[0][:1]
    i = 1
    while True:
        for str in strs:
            if len(prefix) > 1 and prefix != str[:i]:
                return prefix[:i - 1]
            if prefix != str[:i]:
                return 0
        i += 1
        prefix = str[:i]


print(find_prefix(["gfloower", "floow", "flwight"]))
