from debug import debug_print
import random


def flatten(arr):
    return [x for y in arr for x in y]

def random_base62(length):
    BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return "".join([random.choice(BASE62_CHARS) for _ in range(length)]) 


def random_exchanges(elements, exclusions=None):
    """From the given list, retruns a list of pairs of random elements
    where each element appears in each position once and only once, and
    never in both positions of a single pair. Consider a gift exchange where each person draws a
    name not their own to give to.

    Args:
        elements (list): elements to pair
        exclusions (list): exclude these pairings (both to and from)
    """

    import itertools

    def _exchanges(el, exch):
        return [(el[i], x) for i, x in enumerate(exch)]

    def _has_exclusion(a, b):
        return (a, b) in excl or (b, a) in excl
    
    def _valid_exchange(el, exch):
        return [x for x in elements if x != el and x not in exch and not _has_exclusion(el, x)]
    
    n = len(elements)
    if n < 2:
        raise ValueError(f"cannot make pairs from {n} elements")

    excl = exclusions or []

    # there are n(n - 1) / 2 possible exchanges, and each exclusion removes 2, so
    # check if enough remain to pair (at least n pairings)
    if (n * (n - 1) // 2) - 2 * len(excl) < n:
        raise ValueError(f"can exclude no more than {n * (n - 2) // 2} pairs")

    # randomize the elements so any forced assignment is not always the same
    random.shuffle(elements)
    
    exchanges = []

    # unique excluded elements
    excluded_elements = list(set(flatten(excl)))
    # accomodate the exclusions first
    eeee = excluded_elements + [x for x in elements if x not in excluded_elements]
    for i, e in enumerate(eeee):
        v = _valid_exchange(e, exchanges)

        # if we're down to the last 2 elements and the last element has not
        # already been selected, select it now - otherwise it will not be paired
        if i == len(eeee) - 2 and eeee[-1] not in exchanges:
            exchanges.append(eeee[-1])
            continue

        exchanges.append(random.choice(v))

    return _exchanges(eeee, exchanges)


def main():
    e = ["Mike", "John", "Joe", "Thomb", "Patrick", "Jerry", "Sari", "Erin"]
    ex = [("Jerry", "Sari"), ("Joe", "Erin")]
    #e = [1, 2, 3]
    #ex = [(1, 2)]
    debug_print(random_exchanges(e, exclusions=ex))
    #x = random_exchanges(e)
    #for x in e:
    #    debug_print(f"{x} {random_base62(10)}")


if __name__ == "__main__":
    main()

