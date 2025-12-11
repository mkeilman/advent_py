import Day
from utils.debug import debug_print, debug_if
from utils import mathutils
import re

class AdventDay(Day.Base):

    TEST = [
        "aaa: you hhh",
        "you: bbb ccc",
        "bbb: ddd eee",
        "ccc: ddd eee fff",
        "ddd: ggg",
        "eee: out",
        "fff: out",
        "ggg: out",
        "hhh: ccc fff iii",
        "iii: out",
    ]

    YOU = "you"
    OUT = "out"


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 11)
        self.add_args(run_args)
        self.rack = {}


    def run(self):
        n = 0
        self._parse()
        #debug_print(f"R {self.rack}")
        n = self._num_paths()
        debug_print(f"N {n}")
        return n
 

    def _num_paths(self, key=None, depth=0):
        n = 0
        k = key or AdventDay.YOU
        debug_print(f"KEY {k}")
        for d in self.rack[k]:
            debug_print(f"{k}: DDEVS {d}")
            if d == AdventDay.OUT:
                n += 1
            else:
                n += mathutils.sum([self._num_paths(key=d, depth=depth+1) for x in d])
        return n


    def _parse(self):
        for line in self.input:
            d = re.findall(r"[a-z]{3}", line)
            self.rack[d[0]] = d[1:]
