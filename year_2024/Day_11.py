import math
import re
import Day
from utils import mathutils
from utils.debug import debug_print
    
class AdventDay(Day.Base):

    SMALL = [
        "125 17",
    ]

    TEST = [
         "0 1 10 99 999",
    ]

    def __init__(self, year, day, run_args):
        super(AdventDay, self).__init__(
            year,
            day,
        )
        self.args_parser.add_argument(
            "--num-blinks",
            type=int,
            help="number of blinks",
            default=25,
            dest="num_blinks",
        )
        self.add_args(run_args)
        self.set_num_blinks(self.args["num_blinks"])


    def blink(self, stones):
        def _update_count_map(st, count_map, num_stones=1):
            for s in st:
                if s not in count_map:
                    count_map[s] = 0
                count_map[s] += num_stones


        count_map = {}
        _update_count_map(stones, count_map)

        if self.num_blinks < 1:
            return count_map
        
        for _ in range(self.num_blinks):
            m = {}
            for s in count_map:
                _update_count_map(self._next_stones(s), m, num_stones=count_map[s])
            count_map = m
        return count_map


    def num_stones(self, count_map):
        return mathutils.sum(count_map.values())


    def run(self):
        # single line
        stones = [int(x) for x in re.findall(r"\d+", self.input[0])]
        s = self.blink(stones)
        debug_print(f"stones {stones} {self.num_blinks} blinks -> {self.num_stones(s)} total")
        return self.num_stones(s)


    def set_num_blinks(self, num_blinks):
        self.num_blinks = num_blinks


    def _next_stones(self, s):
        def _num_digits(n):
            return int(math.log10(n)) + 1
        
        def _split(s):
            f = math.pow(10,  _num_digits(s) // 2)
            return [int(s // f), int(s % f)]
        
        if s == 0:
            return [1]
        if not _num_digits(s) % 2:
            return _split(s)
        return [s * 2024]


