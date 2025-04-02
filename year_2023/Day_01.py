from functools import reduce
import re
import Day
from utils.debug import debug_print


class AdventDay(Day.Base):

    nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    re_nums = r"|".join(nums + [str(d + 1) for d in range(9)])

    @classmethod
    def _cumulative_cal(cls, curr, line):
        return curr + cls._get_calibration(line)

    @classmethod
    def _get_calibration(cls, line):
        d = [cls._to_digit(x) for x in re.findall(fr'(?=({cls.re_nums}))', line)]
        return (10 * int(d[0]) + int(d[-1])) if d else 0

    @classmethod
    def _get_calibrations(cls, lines):
        return reduce(cls._cumulative_cal, lines, 0)

    @classmethod
    def _to_digit(cls, txt):
        return txt if txt.isdigit() else str(cls.nums.index(txt.lower()) + 1)

    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2023,
            1,
            [
                "two1nine",
                "eightwothree",
                "abcone2threexyz",
                "xtwone3four",
                "4nineeightseven2",
                "zoneight234",
                "7pqrstsixteen",
            ]
        )

    def run(self, v):
        debug_print(f"CALS {AdventDay._get_calibrations(v)}")


def main():
    d = AdventDay()

    debug_print(f"TEST NUMS ONLY:")
    d.run_from_test_input(
        [
            "1abc2",
            "pqr3stu8vwx",
            "a1b2c3d4e5f",
            "treb7uchet",
        ]
    )
    debug_print("TEST:")
    d.run_from_test_input()
    debug_print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
