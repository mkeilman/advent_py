from functools import reduce
import re
import Day

class AdventDay01(Day.AdventDay):

    def __init__(self):
        super(AdventDay01, self).__init__(1)
        self.test_strings = [
            "1abc2",
            "pqr3stu8vwx",
            "a1b2c3d4e5f",
            "treb7uchet",
        ]

    def run(self, v):
        return _get_calibrations(v)


nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
re_nums = r"|".join(nums + [str(d + 1) for d in range(9)])


def _cal_test():
    return _get_calibrations(
        [
            "1abc2",
            "pqr3stu8vwx",
            "a1b2c3d4e5f",
            "treb7uchet",
        ]
    )


def _cumulative_cal(curr, line):
    return curr + _get_calibration(line)


def _get_calibration(line):
    # digits only
    #d = [x for x in line if x.isdigit()]
    # digits and words
    d = [_to_digit(x) for x in re.findall(fr'(?=({re_nums}))', line)]
    cal = (10 * int(d[0]) + int(d[-1])) if d else 0
    #print(f"S {line.strip()} CAL {cal}")
    return cal  #(10 * int(d[0]) + int(d[-1])) if d else 0


def _get_calibrations(lines):
    return reduce(_cumulative_cal, lines, 0)


def _cal_test():
    return _get_calibrations(
        [
            "1abc2",
            "pqr3stu8vwx",
            "a1b2c3d4e5f",
            "treb7uchet",
        ]
    )

def _num_test():
    return _get_calibrations([
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ])


def _to_digit(txt):
    return txt if txt.isdigit() else str(nums.index(txt.lower()) + 1)


def main():
    #with open("input_day_01.txt", "r") as f:
    #    s = _get_calibrations(f.readlines())
    #print(s)
    #print("TEST {}".format(_cal_test()))
    #print("N TEST {}".format(_num_test()))
    d = AdventDay01()
    print(f"TEST {d.run_from_test_strings()}")
    print(f"CALS {d.run_from_file()}")


if __name__ == '__main__':
    main()
