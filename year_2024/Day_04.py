import re
import Day
from utils import math
from utils import string
from utils.debug import debug

class WordGrid:

    def __init__(self, grid, valid_words=None):
        self.valid_words = valid_words or []
        self.max_word_len = max([len(x) for x in self.valid_words])
        self.min_word_len = min([len(x) for x in self.valid_words])
        self.rows = grid
        self.cols = self._get_cols(0)
        self.diags = self._get_diags()
        #debug(f"DIAGs {self.diags}")

        matches = []

    def get_num_matches(self):
        n = 0
        for m in (self.rows, self.cols, self.diags):
            n += len(self._get_word_indices(m))
        return n
    
    def _get_cols(self, direction):
        c = []
        d = math.sign(direction)
        nr = len(self.rows)
        nc = len(self.rows[0])
        for i in range(nc):
            s = ""
            #debug(f"COL {i}")
            for j in range(nr):
                #debug(f"ROW {j}")
                s = s + self.rows[j][i]
            c.append(s)
            #c.append("".join([self.rows[j][i] for j, _ in enumerate(self.rows)]))
        return c
    
    def _get_diags(self):
        d = []
        nr = len(self.rows)
        nc = len(self.rows[0])
        # build the lower half
        bottom = []
        for i in range(nr):
            #s = ""
            c = []
            for j in range(nc):
                k = i + j
                l = nc - k - 1
                if k < nr:
                    c.append((k, j))
                    #s = s + self.rows[k][j]
            #d.append(s)
            bottom.append(c)
        #debug(f"BOTTOM {bottom}")

        # add the top half by symmetry
        top = []
        for c in bottom:
            a = [(j, i) for i, j in c if i != j and j < nr and i < nc]
            if a:
                top.append(a)
        #debug(f"TOP {top}")

        diags = top + bottom

        # flip top and bottom across cols
        rev = []
        for c in diags:
            rev.append([(i, nc - j - 1) for i, j in c])
        #debug(f"REV {rev}")

        diags = diags + rev

        for c in diags:
            s = ""
            #debug(f"TC {c}")
            for cccc in c:
                s += self.rows[cccc[0]][cccc[1]]
            d.append(s)
        return d

    def _get_word_indices(self, arr):
        w = []
        for i, txt in enumerate(arr):
            for v in self.valid_words:
                #debug(f"FIND {v} IN {txt}")
                w.extend([(i, x) for x in string.indices(v, txt)])
        return w

class AdventDay(Day.Base):


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            4,
            #[    
            #    "..X...",
            #    ".SAMX.",
            #    ".A..A.",
            #    "XMAS.S",
            #    ".X....",
            #]
            [
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
        )
        self.args_parser.add_argument(
            "--x-mas",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="x_mas",
        )
        self.x_mas = self.args_parser.parse_args(run_args).x_mas

    def run(self, v):
        g = WordGrid(v, valid_words=["XMAS", "SAMX"])
        debug(f"NUM MATCHES {g.get_num_matches()}")


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
