import re
import Day
from utils import mathutils
from utils.debug import debug_print

class AdventDay(Day.Base):

    TEST = [
        "1",
        "10",
        "100",
        "2024",
    ]


    def __init__(self, run_args):
        super(AdventDay, self).__init__(2024, 22)
        self.args_parser.add_argument(
            "--num-iterations",
            type=int,
            help="number of iterations",
            default=1,
            dest="num_iterations",
        )
        self.add_args(run_args)


    def run(self):
        n = 0
        for s in self._parse(self.input):
            c = self._next(s)
            #debug_print(f"{s} -> {c}")
            n += c
        debug_print(f"N {n}")
        return n
    

    def _mix(self, val, secret):
        return val ^ secret


    def _next(self, secret):
        n = secret
        for _ in range(self.num_iterations):
            n = self._prune(self._mix(n, 64 * n))
            n = self._prune(self._mix(n, n // 32))
            n = self._prune(self._mix(n, 2048 * n))

        return n


    def _parse(self, grid):
        return [int(x) for x in grid]


    def _prune(self, secret):
        return secret % 16777216

