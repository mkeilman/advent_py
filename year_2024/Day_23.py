import re
import Day
from utils import mathutils
from utils.debug import debug_print, debug_if

class AdventDay(Day.Base):

    TEST = [
        "kh-tc",
        "qp-kh",
        "de-cg",
        "ka-co",
        "yn-aq",
        "qp-ub",
        "cg-tb",
        "vc-aq",
        "tb-ka",
        "wh-tc",
        "yn-cg",
        "kh-ub",
        "ta-co",
        "de-co",
        "tc-td",
        "tb-wq",
        "wh-td",
        "ta-ka",
        "td-qp",
        "aq-cg",
        "wq-ub",
        "ub-vc",
        "de-ta",
        "wq-aq",
        "wq-vc",
        "wh-yn",
        "ka-de",
        "kh-ta",
        "co-tc",
        "wh-qp",
        "tb-vc",
        "td-yn",
    ]

    def __init__(self, run_args):
        super(AdventDay, self).__init__(2024, 23)
        #self.args_parser.add_argument(
        #    "--num-iterations",
        #    type=int,
        #    help="number of iterations",
        #    default=1,
        #    dest="num_iterations",
        #)
        #self.add_args(run_args)


    def run(self):
        debug_print(f"RUN")
        return 0
    

    def _parse(self, grid):
        return [int(x) for x in grid]




