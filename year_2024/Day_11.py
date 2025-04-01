import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug
    
class AdventDay(Day.Base):

    SMALL = [
        "125 17",
    ]

    TEST = [
         "0 1 10 99 999",
    ]

    def __init__(self, year, day, run_args):
        import argparse
        super(AdventDay, self).__init__(
            year,
            day,
        )
        self.args_parser.add_argument(
            "--num-blinks",
            type=int,
            help="number of blinks",
            default=25,
            dest="num_blinks",
        )
        self.add_args(run_args)
        self.set_num_blinks(self.args["num_blinks"])


    def blink(self, stones):
        
        lookup_table = {}
        self._fill_lookup_table(stones, lookup_table)

        if self.num_blinks < 1:
            return lookup_table
        
        for n in range(self.num_blinks):
            pd = {}
            for s in lookup_table:
                self._fill_lookup_table(self._next_stones(s), pd, num_stones=lookup_table[s])
            lookup_table = pd
        return lookup_table


    def num_stones(self, lookup_table):
        return mathutils.sum(lookup_table.values())


    def run(self):
        # single line
        stones = [int(x) for x in re.findall(r"\d+", self.input[0])]
        s = self.blink(stones)
        debug(f"stones {stones} {self.num_blinks} blinks -> {self.num_stones(s)} total")
        return self.num_stones(s)


    def set_num_blinks(self, num_blinks):
        self.num_blinks = num_blinks


    def _fill_lookup_table(self, st, lookup_table, num_stones=1):
        for s in st:
            if s not in lookup_table:
                lookup_table[s] = 0
            lookup_table[s] += num_stones

    def _next_stones(self, s):
        def _num_digits(n):
            return int(math.log10(n)) + 1
        
        def _split(s):
            f = math.pow(10,  _num_digits(s) // 2)
            return [int(s // f), int(s % f)]
        
        if s == 0:
            return [1]
        if not _num_digits(s) % 2:
            return _split(s)
        return [s * 2024]
    

def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
