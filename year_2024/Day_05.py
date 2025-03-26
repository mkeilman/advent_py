import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Rule:
    def __init__(self, txt):
        self.page_order = re.findall(r"\d+", txt)



class Update:

    @classmethod
    def get_middle_page(cls, pages):
        return pages[len(pages) // 2]

    def __init__(self, txt, rules):
        self.pages = re.findall(r"\d+", txt)
        self.rules = []
        for r in rules:
            if r.page_order[0] in self.pages or r.page_order[1] in self.pages:
                self.rules.append(r)

    def is_in_order(self):
        if not self.rules:
            return True
        for r in self.rules:
            o = r.page_order
            # if this rule refernces only one page, ignore it
            if o[0] not in self.pages or o[1] not in self.pages:
                continue
            if self.pages.index(o[0]) > self.pages.index(o[1]):
                return False
        return True
    
    def reordered(self):
        import functools
        def _cmp(p1, p2):
            for r in self.rules:
                o = r.page_order
                if p1 not in o or p2 not in o:
                    continue
                return o.index(p1) - o.index(p2)

        if self.is_in_order():
            return self.pages

        return sorted(self.pages, key=functools.cmp_to_key(_cmp))
    
    def _get_middle_page(self):
        #return self.pages[len(self.pages) // 2]
        return Update.get_middle_page(self.pages)


class AdventDay(Day.Base):

    TEST = [
        "47|53",
        "97|13",
        "97|61",
        "97|47",
        "75|29",
        "61|13",
        "75|53",
        "29|13",
        "97|29",
        "53|29",
        "61|53",
        "97|53",
        "61|29",
        "47|13",
        "75|47",
        "97|75",
        "47|61",
        "75|61",
        "47|29",
        "75|13",
        "53|13",
        "",
        "75,47,61,53,29",
        "97,61,53,29,13",
        "75,29,13",
        "75,97,47,61,53",
        "61,13,29",
        "97,13,75,29,47",
    ]
    
    def get_updates(self, v):
        j = 0
        rules = []
        for i, r in enumerate(v):
            if not r:
                j = i + 1
                break
            rules.append(Rule(r))
        updates = [Update(r, rules) for r in v[j:]]
        return updates
            

    def __init__(self, year, day, run_args):
        import argparse
        super(AdventDay, self).__init__(
            year,
            day,
        )

    def run(self, v):
        u = self.get_updates(v)
        m = [x._get_middle_page() for x in [y for y in u if y.is_in_order()]]
        fb = [x.reordered() for x in [y for y in u if not y.is_in_order()]]
        fbm = [Update.get_middle_page(x) for x in fb]
        fbs = mathutils.sum([int(x) for x in fbm])
        s = mathutils.sum([int(x) for x in m])
        debug(f"SUM {s}")
        debug(f"FIXED BAD SUM {fbs}")


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
