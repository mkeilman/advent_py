"""Classes and functions for Avent of Code Day 11, 2024
https://adventofcode.com/2024/day/11

In brief: given a string of space-delimited non-negative integers ("stones"), process the integers according to these rules:
    Replace 0 with 1
    Replace integers with 2N digits with two new integers composed of the left and right N digits, minus leading 0s
    Otherwise replace the integer N with 2024 * N

Repeat this operation (a "blink") a specified number of times and count the final number of "stones"
"""

import math
import re
import Day
from utils import mathutils
from utils.debug import debug_print


class AdventDay(Day.Base):
    """AdventDay Day 11, 2024
    """

    SMALL = [
        "125 17",
    ]

    TEST = [
         "0 1 10 99 999",
    ]

    def __init__(self, run_args):
        """Initialize

        Args:
            run_args (dict): command line arguments

        Run args:
            num_blinks (int): the number of blinks to perform
        """
        super(AdventDay, self).__init__(2024, 11)
        self.args_parser.add_argument(
            "--num-blinks",
            type=int,
            help="number of blinks",
            default=25,
            dest="num_blinks",
        )
        self.add_args(run_args)


    def run(self):
        # single line
        stones = [int(x) for x in re.findall(r"\d+", self.input[0])]
        s = self._blink(stones)
        n = self._num_stones(s)
        debug_print(f"stones {stones} {self.num_blinks} blinks -> {n} total")
        return n


    def set_num_blinks(self, num_blinks):
        self.num_blinks = num_blinks


    def _blink(self, stones):
        """Generate new stones from the given array. Luckily the goal of this exercise is to *count* the
        resultant number of stones, *not* to deliver the entire assortment

        Args:
            stones (int[]): array of stone values

        Returns:
            (dict) a map of stone values to the number of stones with that value
        """

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


    def _next_stones(self, s):
        """Generates new stones accordong to the above rules

        Args:
            s (int): the value of the current stone

        Returns:
            (s[]) an array of generated stones
        """

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


    def _num_stones(self, count_map):
        return mathutils.sum(count_map.values())
