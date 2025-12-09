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
        self.args_parser.add_argument(
            "--interior-only",
            action=argparse.BooleanOptionalAction,
            default=False,
            dest="interior_only",
        )
        self.add_args(run_args)
        self.red_tiles = []
        self.green_tiles = []
        self.colored_tiles = []


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
            rect = self._rect(pair)
            if self.interior_only and any([x not in self.colored_tiles for x in rect]):
                #debug_print(f"P {pair} OUTSIDE")
                continue
            dr, dc = self._tile_span(pair)
            #debug_print(f"P {pair} OK {dr * dc}")
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

        outline_tiles = self.red_tiles + self.green_tiles
        debug_print("DONE OUTLINE")

        b = self._bounds()
        debug_print(f"{b[0][0], b[2][0] + 1}")
        for r in range(b[0][0], b[2][0] + 1):
            #debug_if(f"{r}", "", "", not r % 100, include_time=True)
            # outline tiles in this row
            outline_row = [x for x in outline_tiles if x[0] == r]
            mn = min(x[1] for x in outline_row)
            mx = max(x[1] for x in outline_row)
            debug_if(f"{outline_row}", "", "", False, include_time=True)
            # all tiles in this row between the outline tiles
            #col_coords = [(r, c) for c in range(b[0][1], b[3][1] + 1)]
            col_coords = [(r, c) for c in range(mn, mx + 1)]
            
            
            tiles_in_rows = [x for x in col_coords if x in outline_row]
            debug_if(f"GOT TILES NUM OUTLINE {len(outline_row)}", "", "", False, include_time=True)
            first = tiles_in_rows[0][1]
            last = tiles_in_rows[-1][1]
            i_t = [x for x in col_coords if x[1] > first and x[1] < last]
            debug_if(f"GOT INTERNAL", "", "", False, include_time=True)
            self.green_tiles.extend(i_t)
            debug_if(f"EXTENDED", "", "", not r % 100, include_time=True)

        self.colored_tiles = self.red_tiles + self.green_tiles
        #self._print_tiles()


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


    def _rect(self, pair):

        rect = []
        min_r = min(pair[0][0], pair[1][0])
        max_r = max(pair[0][0], pair[1][0])
        min_c = min(pair[0][1], pair[1][1])
        max_c = max(pair[0][1], pair[1][1])
        for r in range(min_r, max_r + 1):
            rect.extend([(r, c) for c in range(min_c, max_c + 1)])
        return rect


    def _tile_span(self, tile_pair, signed=False):
        dr = tile_pair[0][0] - tile_pair[1][0]
        dc = tile_pair[0][1] - tile_pair[1][1]
        return (dr, dc) if signed else (abs(dr) + 1, abs(dc) + 1 )
        