"""Math utilities
"""

import functools

def sign(val):
    """Returns the sign of the given value. Similar to numpy

    Args:
        val (number): a numeric value

    Returns:
        (int): the sign of the value (-1, 1, or 0)
    """
    return -1 if val < 0 else (1 if val > 0 else 0)
    
def sum(arr, init_val=0):
    """Returns the sum of the values in the given array

    Args:
        arr (number[]): array of numeric values
        init_val (number): an initial value to begin the sum

    Returns:
        (number): the sum
    """
    return functools.reduce((lambda x, y: x + y), arr, init_val)

def product(arr, init_val=1):
    """Returns the product of the values in the given array

    Args:
        arr (number[]): array of numeric values
        init_val (number): an initial value to begin the product

    Returns:
        (number): the product
    """
    return functools.reduce((lambda x, y: x * y), arr, init_val)

