import math
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
            #[
            #    "0",
            #]
        )

    def run(self, v):
        # single line
        stones = [int(x) for x in re.findall(r"\d+", v[0])]
        n = 75
        s = self.blink(stones, num_blinks=n)
        debug(f"{n} -> {self.num_stones(s)}")


    def blink(self, stones, num_blinks=1):
        
        p_dict = {}
        self._fill_p_dict(stones, p_dict)

        if num_blinks < 1:
            return p_dict
        
        for n in range(num_blinks):
            pd = {}
            for s in p_dict:
                self._fill_p_dict(self._next_stones(s), pd, num_stones=p_dict[s])
            p_dict = pd
        return p_dict


    def num_stones(self, p_dict):
        return mathutils.sum(p_dict.values())


    def _fill_p_dict(self, st, p_dict, num_stones=1):
        for s in st:
            if s not in p_dict:
                p_dict[s] = 0
            p_dict[s] += num_stones

    def _next_stones(self, s):
        def _split(s):
            f = math.pow(10,  (int(math.log10(s)) + 1) // 2)
            return [int(s // f), int(s % f)]
        
        if s == 0:
            return [1]
        if not (int(math.log10(s)) + 1) % 2:
            return _split(s)
        return [s * 2024]


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
