import re
import Day
from utils import math
from utils.debug import debug

class AdventDay(Day.Base):

    def _get_muls(self, v, respect_enables=True):
        if not respect_enables:
            return [re.findall(r"mul\(\d+,\d+\)", x) for x in v]
        e = [re.findall(r"[(do\(\)) | (don\'t\(\))]", x) for x in v]
        debug(f"E {e}")
        return []


    def _do_muls(self, arr):
        s = 0
        for m in arr:
            s += math.product([int(x) for x in re.findall(r"\d+", m)])
        return s


    def mul_sum(self, v):
        s = 0
        for m in self._get_muls(v):
            s += self._do_muls(m)
        return s

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            3,
            [
                "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))",
            ]
        )
        self.args_parser.add_argument(
            "--respect-enables",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="respect_enables",
        )
        self.respect_enables = self.args_parser.parse_args(run_args).respect_enables

    def run(self, v):
        debug(f"M {self.mul_sum(v)}")


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
