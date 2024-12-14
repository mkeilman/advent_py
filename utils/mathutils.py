import functools

def sign(val):
    return -1 if val < 0 else (1 if val > 0 else 0)
    
def sum(arr, init_val=0):
    return functools.reduce((lambda x, y: x + y), arr, init_val)

def product(arr, init_val=1):
    return functools.reduce((lambda x, y: x * y), arr, init_val)

