"""Debugging utilities
"""

def debug_print(txt, include_time=False, **kwargs):
    """A wrapper to avoid "naked prints"

    Args:
        txt (any): something to print
    """

    import time
    if include_time:
        txt = f"[{int(time.time())}] " + txt
    print(txt, **kwargs)


def debug_if(txt, alt_txt="", final_txt="", condition=None, include_time=False, **kwargs):
    if condition:
        debug_print(txt + final_txt, include_time=include_time, **kwargs)
    elif alt_txt:
        debug_print(alt_txt + final_txt, include_time=include_time, **kwargs)

