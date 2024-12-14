import re
import Day
from utils import mathutils
from utils.debug import debug

re_times = r"(?:Time:\s+)*(\d+)\s?"
re_dists = r"(?:Distance:\s+)*(\d+)\s?"


class AdventDay(Day.Base):

    @classmethod
    def _dist(cls, press_time, total_time):
        return press_time * (total_time - press_time)

    @classmethod
    def _get_wins_product(cls, lines, preserve_spaces=True):
        dists = []
        wins = []
        tp = cls._parse_line(re.findall(re_times, lines[0]), preserve_spaces)
        dp = cls._parse_line(re.findall(re_dists, lines[1]), preserve_spaces)
        for t in tp:
            dists.append([cls._dist(i, t) for i in range(t + 1)])
        #debug(f"D {dists}")
        record_dists = dp
        for (i, d) in enumerate(dists):
            w = 0
            o = len(d) % 2
            j = len(d) // 2 + o
            hd = d[:j]
            for (k, dd) in enumerate(hd):
                p = 1 if o and k == len(hd) - 1 else 0
                w += (2 - p if dd > record_dists[i] else 0)
            wins.append(w)
        #debug(f"W {wins}")
        return mathutils.product(wins)
        
    @classmethod
    def _parse_line(cls, line, preserve_spaces):
        if preserve_spaces:
            return [int(x) for x in line]
        return [int(mathutils.sum(line, ""))]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2023,
            6,
            [
                "Time:        7     15     30",
                "Distance:   9   40   200",
            ]
        )
        self.args_parser.add_argument(
            "--preserve-spaces",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="preserve_spaces",
        )
        self.args_parser.parse_args(run_args).preserve_spaces
        self.preserve_spaces = self.args_parser.parse_args(run_args).preserve_spaces
    

    def run(self, v):
        debug(f"DISTS {AdventDay._get_wins_product(v, self.preserve_spaces)}")


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
