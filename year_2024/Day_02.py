import re
import Day
from utils import mathutils
from utils.debug import debug_print


class AdventDay(Day.Base):

    TEST = [
        "7 6 4 2 1",
        "1 2 7 8 9",
        "9 7 6 2 1",
        "1 3 2 4 5",
        "8 6 4 4 1",
        "1 3 6 7 9",
    ]
    
    def safe_sum(self, dampen=True):
        d = [[int(y) for y in re.findall(r"\d+", x)] for x in self.input]
        s = [int(self._is_safe(x, dampen=dampen)) for x in d]
        return mathutils.sum(s)

    
    def _is_safe(self, arr, dampen=True):
        max_diff = 3
        min_diff = 1

        def _s(arr):
            d = [arr[i + 1] - arr[i] for i, _ in enumerate(arr[1:])]
            return all([mathutils.sign(x) == mathutils.sign(d[0]) for x in d]) and all([min_diff <= abs(x) <= max_diff for x in d])

        s = _s(arr)
        if not s and dampen:
            t = False
            for i in range(len(arr)):
                t = _s(arr[:i] + arr[i + 1:])
                if t:
                    return True
            return False
        return s

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 2)
        self.args_parser.add_argument(
            "--dampen",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="dampen",
        )
        self.add_args(run_args)
        self.dampen = self.args["dampen"]

    def run(self):
        n = self.safe_sum(dampen=self.dampen)
        debug_print(f"SAFE {n} D? {self.dampen}")
        return n

