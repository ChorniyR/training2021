def last_word_len(str):
    elements = str.split(" ")
    try:
        last_word = elements[-1]
    except IndexError:
        return None
    else:
        return len(last_word)


print(last_word_len("Hello World"))
