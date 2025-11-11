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

    # there are n(n - 1) possible exchanges, and each exclusion removes 2, so
    # check if enough remain to pair (at least n pairings)
    # treat (a, b) and (b, a) as the same combination?
    if (n * (n - 1) // 2) - 2 * len(excl) < n:
        raise ValueError(f"can exclude no more than {n * (n - 2) // 2} pairs")


    exchanges = []
    # note this considers (a, b) and (b, a) as the same combination, but we do not
    all_pairs = itertools.combinations(elements, 2)
    #debug_print(list(all_pairs))
    # randomize the elements so any forced assignment is not always the same
    random.shuffle(elements)
    # accomodate the exclusions first
    pairs_less_exclusions = [x for x in all_pairs if not _has_exclusion(*x)]
    #if len(pairs_less_exclusions) < n:
    #    raise ValueError(f"")
    
    #debug_print(pairs_less_exclusions)

    excluded_elements = list(set(flatten(excl)))
    el_less_excl = [x for x in elements if x not in excluded_elements]



    #for i, e in enumerate(elements):
    eeee = excluded_elements + el_less_excl
    for i, e in enumerate(eeee):
        v = _valid_exchange(e, exchanges)
        #debug_print(f"VALID FOR {e} OUT OF {eeee}: {v}")

        # if we're down to the last 2 elements and the last element has not
        # already been selected, select it now - otherwise it will not be paired
        if i == len(eeee) - 2 and eeee[-1] not in exchanges:
            debug_print(f"{e} MUST CHOOSE {eeee[-1]}")
            exchanges.append(eeee[-1])
            debug_print(f"{_exchanges(eeee, exchanges)[-1]}")
            continue

        x = random.choice(v)
        exchanges.append(x)
        #debug_print(f"{_exchanges(eeee, exchanges)[-1]}")

    return _exchanges(eeee, exchanges)


def main():
    e = ["Mike", "John", "Joe", "Thomb", "Patrick", "Jerry", "Sari", "Erin"]
    ex = [("Jerry", "Sari"), ("Joe", "Erin")]
    #e = [1, 2, 3, 4]
    #ex = [(1, 2)]
    debug_print(random_exchanges(e, exclusions=ex))
    #x = random_exchanges(e)
    #for x in e:
    #    debug_print(f"{x} {random_base62(10)}")


if __name__ == "__main__":
    main()

