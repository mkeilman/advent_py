from functools import reduce
import re
import Day


class CamelCard():
    labels = "23456789TJQKA"
    joker_labels = "J23456789TQKA"

    def __init__(self, label, jokers=True):
        self.label = label
        ll = CamelCard.joker_labels if jokers else CamelCard.labels
        self.rank = {x:ll.index(x) for x in ll}[label]

    def cmp(self, other_card):
        return 1 if self.rank > other_card.rank else -1 if self.rank < other_card.rank else 0


class CamelHand():

    @classmethod
    def cmp(cls, h1, h2):
        return h1.cmp(h2)

    def __init__(self, hand_str, jokers=True):
        self.hand_str = hand_str
        self.jokers = jokers
        self.cards = [CamelCard(x, jokers=jokers) for x in hand_str]
        self.cards_sorted = sorted(self.cards, key=lambda x: x.rank)
        self.card_groups = self._group_cards_by_rank()
        self.hand_type = self._type()
        self.ranks = [x.rank for x in self.cards]
    
    def cmp(self, other_hand):
        def _card_cmp(c1, c2):
            #print("CRD CMP", "".join([x.label for x in c1]), "".join([x.label for x in c2]))
            res = c1[0].cmp(c2[0])
            if len(c2) == 1 or res != 0:
                return res
            return _card_cmp(c1[1:], c2[1:])
        
        if self.hand_type != other_hand.hand_type:
            return 1 if self.hand_type > other_hand.hand_type else -1
        #print("CRD CMP", self.hand_str, other_hand.hand_str)
        return _card_cmp(self.cards, other_hand.cards)

    
    def _group_cards_by_rank(self):
        card_groups = []
        last_card = None
        card_group = []
    
        for card in self.cards_sorted:
            if last_card is None:
                card_group.append(card)
            else:
                if card.cmp(last_card):
                    card_groups.append(card_group)
                    card_group = []
                    card_group.append(card)
                else:
                    card_group.append(card)
            last_card = card
		
        card_groups.append(card_group)
        #return sorted(card_groups, key=len, reverse=True)
        return sorted(card_groups, key=lambda x: (len(x), x[0].rank), reverse=True)
	
    def _is_type_3_of_a_kind(self):
        return len(self.card_groups) >= 2 and len(self.card_groups[0]) == 3 and len(self.card_groups[1]) == 1

    def _is_type_4_of_a_kind(self):
        return len(self.card_groups[0]) == 4
    
    def _is_type_5_of_a_kind(self):
        return len(self.card_groups[0]) == 5
    
    def _is_type_full_house(self):
        return len(self.card_groups) == 2 and len(self.card_groups[0]) == 3 and len(self.card_groups[1]) == 2
    
    def _is_type_high_card(self):
        return len(self.card_groups[0]) == 1

    def _is_type_pair(self):
        return len(self.card_groups) >= 2 and len(self.card_groups[0]) == 2 and len(self.card_groups[1]) == 1

    def _is_type_two_pair(self):
        return len(self.card_groups) >= 2 and len(self.card_groups[0]) == 2 and len(self.card_groups[1]) == 2

    def _type(self):

        type_fns = [
            self._is_type_5_of_a_kind,
            self._is_type_4_of_a_kind,
            self._is_type_full_house,
            self._is_type_3_of_a_kind,
            self._is_type_two_pair,
            self._is_type_pair,
            self._is_type_high_card,
        ]
        n = len([x for x in self.hand_str if x == "J"])
        
        if self.jokers and n and len(self.card_groups) > 1:
            h = f"{self.hand_str}"
            for g in self.card_groups:
                if n <= 0:
                    break
                label = g[0].label
                if label == "J":
                    continue
                nr = min(n, 5 - len(g))
                h = h.replace("J", label, nr)
                n -= nr
            return CamelHand(h, jokers=False).hand_type

        for i, f in enumerate(type_fns):
            if f():
                return len(type_fns) - i - 1
        return -1

class Play():
    @classmethod
    def cmp(cls, p1, p2):
        return CamelHand.cmp(p1.hand, p2.hand)
    
    def __init__(self, play_str, jokers=True):
        re_hand_bet = fr"([{CamelCard.labels}]+)\s?(\d+)"
        hb = re.match(re_hand_bet, play_str)
        self.hand = CamelHand(hb.group(1), jokers=jokers)
        self.bet = int(hb.group(2))


class AdventDay(Day.Base):
     
    @classmethod
    def _parse_line(cls, line, preserve_spaces):
        return [int(reduce((lambda x, y: x + y), line, ""))]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2023,
            7,
            [
                "32T3K 765",
                "T55J5 684",
                "KK677 28",
                "KTJJT 220",
                "QQQJA 483",
            ]
        )
        self.args_parser.add_argument(
            "--jokers",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="jokers",
        )
        self.jokers = self.args_parser.parse_args(run_args).jokers

    def run(self, v):
        import functools
        plays = sorted([Play(x, jokers=self.jokers) for x in v], key=functools.cmp_to_key(Play.cmp))
        amts = [(i + 1) * x for (i, x) in enumerate([y.bet for y in plays])]
        winnings = reduce((lambda x, y: x + y), amts, 0)
        print(f"WIN {winnings}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
