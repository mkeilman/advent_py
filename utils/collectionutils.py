from debug import debug_print
import random


def flatten(arr):
    return [x for y in arr for x in y]


def random_base62(length):
    BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return "".join([random.choice(BASE62_CHARS) for _ in range(length)]) 


def random_exchanges(elements, inclusions=None, exclusions=None):
    """From the given list, retruns a list of pairs of random elements
    where each element appears in each position once and only once, and
    never in both positions of a single pair. Consider a gift exchange where each person draws a
    name not their own to give to.

    Args:
        elements (list): elements to pair
        inclusions (list): require these pairings
        exclusions (list): exclude these pairings
    """
    
    def _first(exchs):
        return [x[0] for x in exchs]
    
    def _second(exchs):
        return [x[1] for x in exchs]
    
    # an exchange is valid if:
    # - the first element differs from the second
    # - the second element has not been selected
    # - the exchange is not forbidden by the exclusions
    def _valid_exchanges(el, els, exchs, ex):
        return [x for x in els if x != el and x not in _second(exchs) and (el, x) not in ex]
    
    def _validate(exchs):
        i0 = _first(exchs)
        i1 = _second(exchs)
        return len(set(i0)) == len(i0) and len(set(i1)) == len(i1)
    
    
    n = len(elements)
    if n < 2:
        raise ValueError(f"cannot make pairs from {n} elements")

    incl = inclusions or []
    excl = exclusions or []

    # an element cannot exchange with itself
    if any([x[0] == x[1] for x in incl]):
        raise ValueError(f"an element cannot exchange with itself: {incl}")

    # an element can appear at most once in each position of the inclusions
    if not _validate(incl):
        raise ValueError(f"elements must appear at most once in each position: {incl}")
    #i0 = _first(incl)
    #i1 = _second(incl)
    #if len(set(i0)) != len(i0) or len(set(i1)) != len(i1):
    #     raise ValueError(f"elements must appear at most once in each position: {incl}")

    # naturally inclusions and exclusions may not share any elements
    intx = set(incl).intersection(set(flatten([[x, x[::-1]] for x in excl])))
    if intx:
        raise ValueError(f"inclusions and exclusions cannot share elements: {intx}")

    # there are n(n - 1) / 2 possible exchanges, and each exclusion removes 2, so
    # check if enough remain to pair (at least n pairings)
    if (n * (n - 1) // 2) - 2 * len(excl) < n:
        raise ValueError(f"can exclude no more than {n * (n - 2) // 2} pairs")

    # randomize the elements so any forced assignment is not always the same
    random.shuffle(elements)
    
    # accomodate the inclusions first, then exclusions, then the rest
    exchanges = incl[:]

    # unique excluded elements
    excluded_elements = list(set(_first(excl)))

    # go through exclusions first; otherwise they may not be pairable
    eeee = excluded_elements + [x for x in elements if x not in excluded_elements]
    for i, e in enumerate(eeee):
        # already added by inclusions
        if e in _first(incl):
            continue

        # if we're down to the last 2 elements and the last element has not
        # already been selected, select it now - otherwise it will not be paired
        if i == len(eeee) - 2 and eeee[-1] not in _second(exchanges):
            debug_print(f"NEXT TO LAST: {(e, eeee[-1])}")
            exchanges.append((e, eeee[-1]))
            continue

        v = _valid_exchanges(e, elements, exchanges, excl)
        x = (e, random.choice(v))
        debug_print(f"V {e}: {v} X {x}")
        exchanges.append(x)

    assert _validate(exchanges)
    return exchanges
    

def main():
    e = ["a", "b", "c", "d"]  #["Mike", "John", "Joe", "Thomb", "Patrick", "Jerry", "Sari", "Erin"]
    #exc = [("Jerry", "Sari"), ("Sari", "Jerry"), ("Erin", "Joe"), ("Joe", "Erin")]
    #inc = [("Erin", "Sari")]
    #r = random_exchanges(e, inclusions=inc, exclusions=exc)
    r = random_exchanges(e)
    debug_print(r)


if __name__ == "__main__":
    main()

