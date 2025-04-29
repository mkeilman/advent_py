"""Debugging utilities
"""

def debug_print(txt, **kawrgs):
    """A wrapper to avoid "naked prints"

    Args:
        txt (any): something to print
    """
    print(txt, **kawrgs)


def debug_if(txt, condition=None, **kwargs):
    if condition:
        debug_print(txt, **kwargs)

