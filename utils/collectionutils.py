from debug import debug_print


def random_element(elements):
    import random
    return elements[random.randint(0, len(elements) - 1)]


def random_exchanges(elements):
    """From the given list, retruns a list of pairs of random elements
    where each element appears in each position once and only once, and
    never in both positions of a single pair. Consider a gift exchange where each person draws a
    name not their own to give to.

    Args:
        elements (list): elements to pair
    """

    exchanges = []
    for e in elements:
        not_e = [x for x in elements if x != e and x not in exchanges]
        exchanges.append(random_element(not_e))

    return [(x, exchanges[i]) for i, x in enumerate(elements)]

def main():
    e = ("Mike", "John", "Joe", "Thomb", "Patrick", "Jerry", "Sari")
    x = random_exchanges(e)
    debug_print(x)


if __name__ == "__main__":
    main()

