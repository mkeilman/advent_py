import re
import Day
import Utils


class AdventDay(Day.Base):

    def _get_muls(self, v):
        return [re.findall(r"mul\(\d+,\d+\)", x) for x in v]


    def _do_muls(self, arr):
        s = 0
        for m in arr:
            s += Utils.Math.product([int(x) for x in re.findall(r"\d+", m)])
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
            "--dampen",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="dampen",
        )
        self.dampen = self.args_parser.parse_args(run_args).dampen

    def run(self, v):
        Utils.Debug.debug(f"M {self.mul_sum(v)}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
