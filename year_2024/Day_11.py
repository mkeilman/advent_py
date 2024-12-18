import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

    
class AdventDay(Day.Base):

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            11,
            #[
            #    "0 1 10 99 999",
            #],
            [
                "125 17",
            ]
        )
        self.args_parser.add_argument(
            "--whole-files",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="whole_files",
        )
        self.whole_files = self.args_parser.parse_args(run_args).whole_files

    def run(self, v):
        # single line
        stones = [int(x) for x in re.findall(r"\d+", v[0])]
        n = 25
        new_stones = self.blink(stones, num_blinks=n)
        debug(f"{stones} BLINKS {n} -> N {len(new_stones)}")

    def blink(self, stones, num_blinks=1):
        new_stones = []
        for s in stones:
            if s == 0:
                new_stones.append(self._zero_to_one(s))
            elif not len(f"{s}") % 2:
                new_stones.extend(self._split(s))
            else:
                new_stones.append(self._mult(s))
        return new_stones if num_blinks == 1 else self.blink(new_stones, num_blinks=num_blinks - 1)

    def _zero_to_one(self, stone):
        return 1
    
    def _split(self, stone):
        s = f"{stone}"
        sz = len(s) // 2
        return [int(s[:sz]), int(s[sz:])]
    
    def _mult(self, stone):
        return stone * 2024



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
