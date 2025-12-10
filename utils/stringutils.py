from utils.debug import debug_print
import utils.mathutils

# get the given number of characters from an array of strings,
# starting at the index and crossing elements if need be
def get_chars(arr, index=0, offset=0, num_chars=1):
    if not arr or num_chars <= 0:
        return None, None, None

    arr_str = "".join(arr)
    start = utils.mathutils.sum([len(x) for x in arr[:index]]) + offset
    end = start + num_chars
    if end > len(arr_str):
        return None, None, None

    r = num_chars - len(arr[index]) + offset
    while index < len(arr) and r >= 0:
        index += 1
        r -= len(arr[index]) if index < len(arr) else 0
    if index >= len(arr):
        index = None
        offset = None
    else:
        offset = len(arr[index]) + r

    return arr_str[start:end], index, offset


def indices(element, collection):
    if element not in collection:
        return []
    
    if isinstance(collection, str):
        i = -1
        s = []
        while True:
            try:
                i = collection.index(element, i + 1)
                s.append(i)
            except ValueError:
                break
        return s
    
    return [i for i, x in enumerate(collection) if x == element]


def print_str_arr(arr):
    for r in arr:
        debug_print(r)


def re_indices(r, txt):
    import re

    s = []
    q = 0
    t = txt
    m = re.search(r, t)
    while m:
        p = m.span()[0]
        q += p
        s.append(q)
        t = t[p + 1:]
        q += 1
        m = re.search(r, t)
    return s

