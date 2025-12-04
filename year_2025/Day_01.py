import re
import Day
from utils import mathutils
from utils.debug import debug_print, debug_if

class Dial:

    def __init__(self, num_digits=100, init_pos=50):
        self.num_digits = num_digits
        self.init_pos = init_pos
        self.current_pos = init_pos


    # move one space at a time - easier than trying to keep track of
    # loops
    def turn(self, num_spaces):
        n = 0
        s = mathutils.sign(num_spaces)
        for _ in range(abs(num_spaces)):
            self.current_pos = (self.current_pos + s + self.num_digits) % self.num_digits
            n += not self.current_pos
        return n


    def spin(self, turns, count_interim_zeros=False):
        num_zeros = 0
        for t in turns:
            int_zeros = self.turn(t)
            if count_interim_zeros:
                num_zeros += int_zeros
            else:
                num_zeros += not self.current_pos
        return num_zeros


class AdventDay(Day.Base):

    TEST = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
    ]

    BIG_ROT = [
        "L1000",
    ]

    ZERO_WITH_FULL_ROTS = [
        "R50",
        "R100",
        #"R200",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 1)
        self.args_parser.add_argument(
            "--count-interim-zeros",
            action=argparse.BooleanOptionalAction,
            default=False,
            dest="count_interim_zeros",
        )
        self.add_args(run_args)


    def run(self):
        #self.input = AdventDay.BIG_ROT
        d = Dial()
        turns = [self._parse_turn(x) for x in self.input]
        n = d.spin(turns, count_interim_zeros=self.count_interim_zeros)
        debug_print(f"FINAL POS {d.current_pos} NUM ZEROS {n}")
        return n
 

    
    def _parse_turn(self, turn):
        return (1 if turn[0] == "R" else -1) * int(re.search(r'[LR](\d+)', turn).group(1))

