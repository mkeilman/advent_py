import Day
from utils.debug import debug_print, debug_if
import re

class AdventDay(Day.Base):

    TEST = [
        "3-5",
        "10-14",
        "16-20",
        "12-18",
        "",
        "1",
        "5",
        "8",
        "11",
        "17",
        "32",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 5)
        self.add_args(run_args)
        self.fresh_ranges = []
        self.available_ingredients = []


    def run(self):
        n = 0
        self._parse()
        n = self._num_fresh_ingredients()
        debug_print(f"NUM FRESH {n}")
        return n
 

    def _num_fresh_ingredients(self):
        n = 0
        for i in self.available_ingredients:
            n += int(any([i in x for x in self.fresh_ranges]))
        return n

    def _parse(self):
        for line in self.input:
            if not line:
                continue
            if "-" in line:
                r = [int(x) for x in re.findall(r'\d+', line)]
                self.fresh_ranges.append(range(r[0], r[1] + 1))
            else:
                self.available_ingredients.append(int(line))
