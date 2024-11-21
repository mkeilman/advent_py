import functools

def sum(arr, init_val=0):
    return functools.reduce((lambda x, y: x + y), arr, init_val)

