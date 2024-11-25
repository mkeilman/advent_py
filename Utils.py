import functools

class Math:

    def __init__(self):
        pass

    @staticmethod
    def sum(arr, init_val=0):
        return functools.reduce((lambda x, y: x + y), arr, init_val)

    def product(arr, init_val=1):
        return functools.reduce((lambda x, y: x * y), arr, init_val)
