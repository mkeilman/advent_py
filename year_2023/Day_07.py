from functools import reduce
import re
import Day


class CamelCard():
    labels = "23456789TJQKA"

    def __init__(self, label):
        self.label = label
        self.rank = {x:CamelCard.labels.index(x) for x in CamelCard.labels}[label]

    def cmp(self, other_card):
        return 1 if self.rank > other_card.rank else -1 if self.rank < other_card.rank else 0


class CamelHand():

    @classmethod
    def cmp(cls, h1, h2):
        return h1.cmp(h2)
        if h1.hand_type != h2.hand_type:
            return 1 if h1.hand_type > h2.hand_type else -1
        res = h1.cards[0].cmp(h2[0])
        if len(h2) == 1 or res != 0:
            return res
        #return h1.sub_hand().cmp(h2.sub_hand())
        return cls.cmp(h1.sub_hand(), h2.sub_hand())

    def __init__(self, hand_str):
        self.hand_str = hand_str
        self.cards = [CamelCard(x) for x in hand_str]
        self.cards_sorted = sorted(self.cards, key=lambda x: x.rank)
        self.card_groups = self._group_cards_by_rank()
        self.hand_type = self._type()
        self.ranks = [x.rank for x in self.cards]
        #print(self.hand_str, self.hand_type)
        #print("GRPS")
        #for g in self.card_groups:
        #    print([x.label for x in g])

    def sub_hand(self):
        return CamelHand(self.hand_str[1:])
    
    def cmp(self, other_hand):
        def _card_cmp(h1, h2):
            res = h1.cards[0].cmp(h2.cards[0])
            if len(h2.cards) == 1 or res != 0:
                return res
            return _card_cmp(h1.sub_hand(), h2.sub_hand())
        
        if self.hand_type != other_hand.hand_type:
            return 1 if self.hand_type > other_hand.hand_type else -1
        return _card_cmp(self, other_hand)
        #res = self.cards[0].cmp(other_hand.cards[0])
        #if len(other_hand.cards) == 1 or res != 0:
        #    return res
        #return self.sub_hand().cmp(other_hand.sub_hand())
    
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
        return sorted(card_groups, key=len, reverse=True)
	
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
        for i, f in enumerate([
            self._is_type_high_card,
            self._is_type_pair,
            self._is_type_two_pair,
            self._is_type_3_of_a_kind,
            self._is_type_full_house,
            self._is_type_4_of_a_kind,
            self._is_type_5_of_a_kind,
        ]):
            if f():
                return i
        return -1

class Play():
    @classmethod
    def cmp(cls, p1, p2):
        return CamelHand.cmp(p1.hand, p2.hand)
    
    def __init__(self, play_str):
        re_hand_bet = fr"([{CamelCard.labels}]+)\s?(\d+)"
        hb = re.match(re_hand_bet, play_str)
        self.hand = CamelHand(hb.group(1))
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
    

    def run(self, v):
        import functools
        plays = sorted([Play(x) for x in v], key=functools.cmp_to_key(Play.cmp))
        #print(f"PLAYS {[p.hand.hand_str for p in plays]}")
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
