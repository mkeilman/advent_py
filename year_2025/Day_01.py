import re
import Day
from utils import mathutils
from utils.debug import debug_print

class Dial:

    def __init__(self, num_digits=100, init_pos=50):
        self.num_digits = num_digits
        self.init_pos = init_pos
        self.current_pos = init_pos

    
    def turn(self, num_spaces):
        # pre-modulo
        pos = self.current_pos + num_spaces
        # don't count interim 0 if starting at
        interim = int(self.current_pos and (pos < 0 or pos > self.num_digits))
        n = abs(num_spaces) // self.num_digits
        if n:
            interim += (n - 1)
        #debug_print(f"PREMOD {self.current_pos} -> {pos} NUM FULL ROT {n} INT 0 {interim}")
        self.current_pos = (pos + self.num_digits) % self.num_digits
        return interim


    def spin(self, turns, count_interim_zeros=False):
        num_zeros = 0
        for t in turns:
            int_zeros = self.turn(t)
            # lands on 0
            num_zeros += not self.current_pos
            if count_interim_zeros:
                num_zeros += int_zeros
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
        d = Dial()
        turns = [self._parse_turn(x) for x in self.input]
        n = d.spin(turns, count_interim_zeros=self.count_interim_zeros)
        debug_print(f"FINAL POS {d.current_pos} NUM ZEROS {n}")
        return n
 

    
    def _parse_turn(self, turn):
        return (1 if turn[0] == "R" else -1) * int(re.search(r'[LR](\d+)', turn).group(1))

