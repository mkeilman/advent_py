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
            #rect = self._rect(pair)
            #if self.interior_only and any([x not in self.colored_tiles for x in rect]):
            if self.interior_only and not self._is_interior(pair):
                debug_print(f"P {pair} OUTSIDE")
                continue
            dr, dc = self._tile_span(pair)
            #debug_print(f"P {pair} OK {dr * dc}")
            max_area = max(max_area, dr * dc)
        return max_area


    def _bounds(self):
        r = [x[0] for x in self.red_tiles]
        c = [x[1] for x in self.red_tiles]
        return (min(r), min(c)), (min(r), max(c)), (max(r), min(c)), (max(r), max(c))


    def _is_interior(self, pair):
        #rect = self._rect(pair)
        debug_print(f"CHECK P {pair}")
        min_row = min(pair[0][0], pair[1][0])
        max_row = max(pair[0][0], pair[1][0])
        min_col = min(pair[0][1], pair[1][1])
        max_col = max(pair[0][1], pair[1][1])
        for r in range(min_row, max_row + 1):
            #debug_print(r)
            # outline tiles in this row
            outline_tiles_in_row = [x for x in self.outline_tiles if x[0] == r]
            #debug_print(f"{r} OUTLINE {len(outline_tiles_in_row)}")
            min_outline_col = min(x[1] for x in outline_tiles_in_row)
            max_outline_col = max(x[1] for x in outline_tiles_in_row)
            #debug_print(f"MC {min_outline_col} MX {max_outline_col}")
            # all tiles in this row between the outline tiles
            #col_coords = [(r, c) for c in range(min_col, max_col + 1)]
            #debug_print(f"{r} COL COORDS DONE {len(col_coords)}", include_time=True)
            #if any([x not in col_coords for x in rect]):
            if min_col < min_outline_col or max_col > max_outline_col:
                debug_print(f"{r} OUTSIDE")
                return False
        debug_print("INSIDE")
        return True



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

        self.outline_tiles = self.red_tiles + self.green_tiles
        debug_print("DONE OUTLINE")
        return
        
        b = self._bounds()
        debug_print(f"{b[0][0], b[2][0] + 1}")
        for r in range(b[0][0], b[2][0] + 1):
            # outline tiles in this row
            outline_tiles_in_row = [x for x in outline_tiles if x[0] == r]
            mn = min(x[1] for x in outline_tiles_in_row)
            mx = max(x[1] for x in outline_tiles_in_row)
            # all tiles in this row between the outline tiles
            col_coords = [(r, c) for c in range(mn, mx + 1)]
            self.green_tiles.extend(col_coords)
            debug_if(f"{r} DONE", "", "", not r % 100, include_time=True)

        self.colored_tiles = self.red_tiles + self.green_tiles
        #self._print_tiles()


    def _print_tiles(self, padding=2, scale=1):
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
        