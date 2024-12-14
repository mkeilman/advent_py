import re
import Day
from utils import mathutils
from utils.debug import debug


class AdventDay(Day.Base):

    def safe_sum(self, v, dampen=True):
        d = [[int(y) for y in re.findall(r"\d+", x)] for x in v]
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
        super(AdventDay, self).__init__(
            2024,
            2,
            [
                "7 6 4 2 1",
                "1 2 7 8 9",
                "9 7 6 2 1",
                "1 3 2 4 5",
                "8 6 4 4 1",
                "1 3 6 7 9",
            ]
        )
        self.args_parser.add_argument(
            "--dampen",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="dampen",
        )
        self.dampen = self.args_parser.parse_args(run_args).dampen

    def run(self, v):
        debug(f"SAFE {self.safe_sum(v, dampen=self.dampen)} D? {self.dampen}")


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
