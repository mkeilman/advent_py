import re
from functools import reduce

re_part = r"\D*(\d+)\D*"
re_digit_or_dot = r"[.0-9]"
re_id = r"Card\s*(\d+):"

test_cards = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


def _cards_test():
    return _cards_sum(test_cards)


def _copies_file(filename):
    with open(filename, "r") as f:
        return _card_copies(f.readlines())


def _copies_test():
    return _card_copies(test_cards)


def _cards_file(filename):
    with open(filename, "r") as f:
        return  _cards_sum(f.readlines())


def _card_numbers(card):

    cid = re.match(re_id, card).group(1)
    w, m = [re.findall(re_part, s) for s in card.split("|")]
    return cid, len([int(c) for c in m if c in w[1:]])


def _cards_sum(cards):
    n = 0
    for c in cards:
        cid, num_winners = _card_numbers(c)
        print(cid, num_winners)
        n += (2 ** (num_winners - 1)) if num_winners else 0
    return n


def _card_copies(cards):
    lc = len(cards)
    r = range(lc)
    copies = {str(k + 1): 1 for k in r}
    for i in r:
        cid, num_winners = _card_numbers(cards[i])
        for j in range(i + 1, min(i + 1 + num_winners, lc)):
            copies[_card_numbers(cards[j])[0]] += copies[cid]
    return copies


def main():
    #n = _cards_test()
    #print(f"TEST {n}")
    #n = _cards_file("input_day_04.txt")
    #print(f"SUM {n}")
    #c = _copies_test()
    c = _copies_file("input_day_04.txt")
    n = reduce((lambda x, y: x + y), c.values(), 0)
    #print(f"TEST COPIES {c} N {n}")
    print(f"COPIES {c}")
    print(f"COPIES N {n}")


if __name__ == '__main__':
    main()
