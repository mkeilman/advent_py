import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print

class WordGrid:

    def __init__(self, grid, valid_words=None):
        self.valid_words = valid_words or []
        self.max_word_len = max([len(x) for x in self.valid_words])
        self.min_word_len = min([len(x) for x in self.valid_words])
        self.rows = grid
        self.cols = self._get_cols()
        self.diags = self._get_diags()


    def get_num_matches(self):
        n = 0
        for m in (self.rows, self.cols, self.diags):
            n += len(self._get_word_indices(m))
        return n
    
    def get_num_subgrid_matches(self, sub_grid):
        return 0

    def _get_cols(self):
        c = []
        nr = len(self.rows)
        nc = len(self.rows[0])
        for i in range(nc):
            s = ""
            for j in range(nr):
                s = s + self.rows[j][i]
            c.append(s)
        return c
    
    def _get_diags(self):
        d = []
        nr = len(self.rows)
        nc = len(self.rows[0])

        # build the lower half
        bottom = []
        for i in range(nr):
            c = []
            for j in range(nc):
                k = i + j
                if k < nr:
                    c.append((k, j))
            bottom.append(c)

        # add the top half by symmetry
        top = []
        for c in bottom:
            a = [(j, i) for i, j in c if i != j and j < nr and i < nc]
            if a:
                top.append(a)

        diags = top + bottom

        # flip top and bottom across cols
        rev = []
        for c in diags:
            rev.append([(i, nc - j - 1) for i, j in c])

        diags = diags + rev

        for c in diags:
            s = ""
            for ij in c:
                s += self.rows[ij[0]][ij[1]]
            d.append(s)
        return d

    def _get_word_indices(self, arr):
        w = []
        for i, txt in enumerate(arr):
            for v in self.valid_words:
                w.extend([(i, x) for x in string.indices(v, txt)])
        return w
    
    def _get_subgrid_indices(self, sub_grid):
        w = []
        nr = len(self.rows) - len(sub_grid) + 1
        nc = len(self.rows[0])
        for i in range(nr):
            p = [string.re_indices(x, self.rows[i + j]) for j, x in enumerate(sub_grid)]
            p = [x for x in p if all([len(y) for y in p])]
            if not p:
                continue
            for j in set([x for y in p for x in y]):
                if all([j in x for x in p]):
                    w.append((i, j))
            #debug_print(f"{i} SG POS {p}")
                
            #for j in range(nc):
            #    m = True
            #    for k, r in enumerate(sub_grid):
            #        M = string.re_indices(r, self)
            #        
            #        debug_print(f"MATCH {(i, j)} {r} in {self.rows[i + k][j:]}: {MM}")
            #        m = m and re.match(r, self.rows[i + k][j:])
            #    if m:
            #        w.append((i, j))
        return w
                    
            

class AdventDay(Day.Base):

    SMALL = [
        "SSS",
        "AAA",
        "MMM",
    ]

    SNAKE = [
        "..X...",
        ".SAMX.",
        ".A..A.",
        "XMAS.S",
        ".X....",
    ]

    TEST = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX",
    ]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 4)
        self.args_parser.add_argument(
            "--x-mas",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="x_mas",
        )
        self.add_args(run_args)
        self.x_mas = self.args["x_mas"]

    def run(self):
        g = WordGrid(self.input, valid_words=["XMAS", "SAMX"])
        if not self.x_mas:
            n = g.get_num_matches()
            debug_print(f"NUM MATCHES {n}")
            return n
        a = r".A."
        ms = r"M.S"
        sm = r"S.M"
        mm = r"M.M"
        ss = r"S.S"
        sg = [
            [ms, a, ms],
            [sm, a, sm],
            [mm, a, ss],
            [ss, a, mm],
        ]
        s = mathutils.sum(
            [len(x) for x in [g._get_subgrid_indices(y) for y in sg]]
        )
        debug_print(f"NUM X-MAS {s}")
        return s


