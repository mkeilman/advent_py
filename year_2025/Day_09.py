import Day
from utils.debug import debug_print, debug_if
import re

class AdventDay(Day.Base):

    TEST = [
        "7,1",
        "11,1",
        "11,7",
        "9,7",
        "9,5",
        "2,5",
        "2,3",
        "7,3",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 9)
        self.add_args(run_args)
        self.red_tiles = []
        self.tile_pairs = []


    def run(self):
        n = 0
        self._parse()
        #debug_print(f"TILES {self.red_tiles} NUM {self.num_tiles} ROOM SIZE {self.size}")
        n = self._max_area()
        debug_print(f"A {n}")
        return n
 

    def _max_area(self):
        import itertools

        max_area = 0
        for pair in itertools.combinations(self.red_tiles, 2):
            dr = abs(pair[0][0] - pair[1][0]) + 1
            dc = abs(pair[0][1] - pair[1][1]) + 1
            max_area = max(max_area, dr * dc)
        return max_area


    def _parse(self):

        for line in self.input:
            c = re.findall(r"\d+", line)
            self.red_tiles.append((int(c[0]), int(c[1])))
        self.num_tiles = len(self.red_tiles)
        self.size = (max([x[0] for x in self.red_tiles]), max([x[1] for x in self.red_tiles]))
        
        