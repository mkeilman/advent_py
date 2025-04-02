import re
import Day
from utils import mathutils
from utils.debug import debug_print

class AdventDay(Day.Base):

    TEST = [
        "3   4",
        "4   3",
        "2   5",
        "1   3",
        "3   9",
        "3   3",
    ]

    def col_diff_sum(self):
        d = self._col_diffs(*self._get_cols(self.input))
        return mathutils.sum(d)
    

    def similarity_sum(self):
        c1, c2 = self._get_cols(self.input)
        return mathutils.sum([self._similarity(x, c2) for x in c1])

    def _col_diffs(self, c1, c2):
        return [abs(c1[i] - c2[i]) for i, _ in enumerate(c1)]
    

    def _get_cols(self, v):
        d = [re.findall(r"\d+", x) for x in v]
        c1 = sorted([int(x[0]) for x in d])
        c2 = sorted([int(x[1]) for x in d])
        return c1, c2

    def _similarity(self, val, arr):
        e = [int(val == x) for x in arr]
        return val * mathutils.sum([int(val == x) for x in arr])

    def __init__(self, run_args):
        super(AdventDay, self).__init__(2024, 1)
        self.args_parser.add_argument(
            "--calc",
            type=str,
            help="calculation",
            choices=["col-diffs", "similarity"],
            default="col-diffs",
            dest="calc",
        )
        self.add_args(run_args)
        self.calc = self.args["calc"]

    def run(self):
        c = self.col_diff_sum() if self.calc == 'col-diffs' else self.similarity_sum()
        debug_print(f"C {c}")
        return c
    



