import Day
from utils.debug import debug_print, debug_if
from utils import mathutils
from utils import collectionutils
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

    RED = "#"

    GREEN = "X"

    NONE = "."

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 9)
        self.add_args(run_args)
        self.red_tiles = []
        self.green_tiles = []


    def run(self):
        n = 0
        self._parse()
        n = self._max_area()
        debug_print(f"A {n}")
        return n
 

    def _max_area(self):
        import itertools

        max_area = 0
        for pair in itertools.combinations(self.red_tiles, 2):
            # add one to get the length instead of the distance
            dr, dc = self._tile_span(pair)
            max_area = max(max_area, dr * dc)
        return max_area


    def _bounds(self):
        r = [x[0] for x in self.red_tiles]
        c = [x[1] for x in self.red_tiles]
        return (min(r), min(c)), (min(r), max(c)), (max(r), min(c)), (max(r), max(c))


    def _parse(self):

        for line in self.input:
            c = re.findall(r"\d+", line)
            self.red_tiles.append((int(c[0]), int(c[1])))

        for i, t in enumerate(self.red_tiles):
            pair = (self.red_tiles[(i + 1) % len(self.red_tiles)], t)
            dr, dc = self._tile_span(pair, signed=True)
            # changes are always in one direction at a time
            if dr:
                self.green_tiles.extend([(t[0] + mathutils.sign(dr) * x, t[1]) for x in range(1, abs(dr))])
            else:
                self.green_tiles.extend([(t[0], t[1] + mathutils.sign(dc) * x) for x in range(1, abs(dc))])
        #debug_print(self.green_tiles)

        interior_tiles = []
        outline_tiles = self.red_tiles + self.green_tiles
        b = self._bounds()
        for r in range(b[0][0], b[2][0] + 1):
            coords = [(r, c) for c in range(b[0][1], b[3][1] + 1)]
            tiles_in_rows = [x for x in coords if x in outline_tiles]
            first = tiles_in_rows[0]
            last = tiles_in_rows[-1]
            i_t = [x for x in coords if x[1] > first[1] and x[1] < last[1]]
            debug_print(i_t)
            interior_tiles.append(i_t)
            self.green_tiles.extend(i_t)

        #self.green_tiles.extend()
        #debug_print(self._bounds())
        self._print_tiles()


    def _print_tiles(self, padding=2):
        b = self._bounds()
        num_cols = b[1][1] - b[0][1] + 1
        empty_row = (2 * padding + num_cols) * AdventDay.NONE
        for _ in range(padding):
            debug_print(empty_row)
        for r in range(b[0][0], b[2][0] + 1):
            debug_print(padding * AdventDay.NONE, end="")
            for c in range(b[0][1], b[3][1] + 1):
                coord = (r, c)
                s = AdventDay.NONE
                if coord in self.red_tiles:
                    s = AdventDay.RED
                elif coord in self.green_tiles:
                    s = AdventDay.GREEN
                debug_print(s, end="")
            debug_print(padding * AdventDay.NONE)
        for _ in range(padding):
            debug_print(empty_row)

    def _tile_span(self, tile_pair, signed=False):
        dr = tile_pair[0][0] - tile_pair[1][0]
        dc = tile_pair[0][1] - tile_pair[1][1]
        return (dr, dc) if signed else (abs(dr) + 1, abs(dc) + 1 )
        