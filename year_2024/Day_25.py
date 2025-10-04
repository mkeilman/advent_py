import re
import Day
from utils import mathutils
from utils.debug import debug_print, debug_if


class Schematic:
    
    FILLED = "#"
    EMPTY = "."

    TYPES = ["KEY", "LOCK"]

    def __init__(self, grid):
        self.num_rows = len(grid)
        self.num_cols = len(grid[0])
        self.channel_length = self.num_rows - 2

        self.is_lock = grid[0] == Schematic.FILLED * self.num_cols and grid[self.num_rows - 1] == Schematic.EMPTY * self.num_cols
        self.is_key = grid[self.num_rows - 1] == Schematic.FILLED * self.num_cols and grid[0] == Schematic.EMPTY * self.num_cols
        self.s_type = Schematic.TYPES[1 - self.is_lock]

        self.cols = self.num_cols * [""]
        for line in grid:
            for j, c in enumerate(line):
                self.cols[j] += c

        self.lengths = []
        for c in self.cols:
            self.lengths.append(len([x for x in c if x == Schematic.FILLED]) - 1)


    def __repr__(self):
        return f"{self.cols}"
    

    def fit(self, other_schematic):
        assert self.num_rows == other_schematic.num_rows and self.num_cols == other_schematic.num_cols
        if self.s_type == other_schematic.s_type:
            return False
        sums = [x + other_schematic.lengths[i] for i, x in enumerate(self.lengths)]
        #debug_print(f"S1 {self} S2 {other_schematic}: {sums}")
        return all([x <= self.channel_length for x in sums])


class Lock(Schematic):

    def __init__(self, grid):
        super(grid)
        assert grid[0] == self.__class__.FILLED * self.num_cols and grid[self.num_rows - 1] == self.__class__.EMPTY * self.num_cols
        

class Key(Schematic):

    def __init__(self, grid):
        super(grid)
        assert grid[self.num_rows - 1] == self.__class__.FILLED * self.num_cols and grid[0] == self.__class__.EMPTY * self.num_cols



class AdventDay(Day.Base):

    TEST = [
        "#####",
        ".####",
        ".####",
        ".####",
        ".#.#.",
        ".#...",
        ".....",
        "",
        "#####",
        "##.##",
        ".#.##",
        "...##",
        "...#.",
        "...#.",
        ".....",
        "",
        ".....",
        "#....",
        "#....",
        "#...#",
        "#.#.#",
        "#.###",
        "#####",
        "",
        ".....",
        ".....",
        "#.#..",
        "###..",
        "###.#",
        "###.#",
        "#####",
        "",
        ".....",
        ".....",
        ".....",
        "#....",
        "#.#..",
        "#.#.#",
        "#####",
    ]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 25)
        #self.args_parser.add_argument(
        #    "--validate-sum",
        #    action=argparse.BooleanOptionalAction,
        #    default=True,
        #    dest="validate_sum",
        #)
        #self.add_args(run_args)
    


    def run(self):
        debug_print("RUN")
        self._parse()
        #debug_print(f"K {self.keys} L {self.locks}")
        n = self._count_fits()
        debug_print(f"FITS {n}")
        return 0


    def _count_fits(self):
        n = 0
        #debug_print(f"NK {len(self.keys)} NL {len(self.locks)}")
        #return 0
        for k in self.keys:
            for l in self.locks:
                n += k.fit(l)
        return n


    def _parse(self):
        def _add_schematic(arr):
            sx = Schematic(arr)
            self.schematics.append(sx)
            if sx.is_key:
                self.keys.append(sx)
            else:
                self.locks.append(sx)

        self.schematics = []
        self.locks = []
        self.keys = []
        s = []
        for line in self.input:
            if not line:
                _add_schematic(s)
                s = []
                continue
            s.append(line)
        if s:
            _add_schematic(s)
        
