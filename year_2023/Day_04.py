import Day
import re
from utils import math
from utils.debug import debug

class Deck:

    @classmethod
    def _card_numbers(cls, card):
        cid = re.match(r"Card\s*(\d+):", card).group(1)
        w, m = [re.findall(r"\D*(\d+)\D*", s) for s in card.split("|")]
        return cid, len([int(c) for c in m if c in w[1:]])

    def __init__(self, cards):
        self.cards = cards
        self.copies = self._card_copies()
        self.c_sum = self._copies_sum()
        self.sum = self._cards_sum()

    def _card_copies(self):
        lc = len(self.cards)
        r = range(lc)
        copies = {str(k + 1): 1 for k in r}
        for i in r:
            cid, num_winners = Deck._card_numbers(self.cards[i])
            for j in range(i + 1, min(i + 1 + num_winners, lc)):
                copies[Deck._card_numbers(self.cards[j])[0]] += copies[cid]
        return copies

    def _cards_sum(self):
        n = 0
        for c in self.cards:
            cid, num_winners = Deck._card_numbers(c)
            n += (2 ** (num_winners - 1)) if num_winners else 0
        return n

    def _copies_sum(self):
        return math.sum(self.copies.values())


class AdventDay(Day.Base):

    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2023,
            4,
            [
                "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
                "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
                "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
                "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
                "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
                "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
            ]
        )

    def run(self, v):
        deck = Deck(v)
        debug(f"SUM {deck.sum}")
        debug(f"COPIES SUM {deck.c_sum}")


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
