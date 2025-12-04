import re
import Day
from utils import mathutils
from utils.debug import debug_print, debug_if

class Dial:

    def __init__(self, num_digits=100, init_pos=50):
        self.num_digits = num_digits
        self.init_pos = init_pos
        self.current_pos = init_pos

    
    def turn(self, num_spaces):
        # pre-modulo
        p0 = self.current_pos
        pos = p0 + num_spaces
        # we always start with a position 0 - <num_digits - 1>; thus we
        # know that if the new position is less than 0 or more than num_digits,
        # we must have passed 0 at least once
        # don't count interim 0 if starting at 0 - we'll get that later
        #interim = 0 #int(p0 and (pos < 0 or pos > self.num_digits))
        interim = 0
        n_loops = abs(num_spaces) // self.num_digits
        if n_loops:
            if p0:
                interim += n_loops
            else:
                interim += (n_loops - 1)
        # remaining spaces
        d = num_spaces - mathutils.sign(num_spaces) * n_loops * self.num_digits
        debug_if(f"{p0} D {d} INITIAL ZERO {interim}", "", "", n_loops)
        # if the remaining spaces passes 0 again, count it
        pd = p0 + d
        # count crossing 0 with the remaining spaces - BUT if we started at 0,
        # ending negative does NOT cross 0 again. Positive spins cannot end up
        # over num_digits
        r = int((p0 > 0 and pd < 0) or pd > self.num_digits)
        interim += r
        #debug_print(f"ADDED FOR REMAINDER: {r}")
        # ensure we have a positive modulus
        p1 = (pos + (n_loops + 1) * self.num_digits) % self.num_digits
        #if n_loops:
        #    # add the number of loops
        #    interim += (n_loops - 1)
        #    if not p0:
        #        # if started at 0 and went around at least once, add one UNLESS we land on 0 again, because we
        #        # count that later
        #        interim += (1 if p1 else 0)
        debug_if(f"{p0} + {num_spaces} -> {pos} NEW {p1} NUM FULL ROT {n_loops} ZERO {interim}", "", "", n_loops)
        
        self.current_pos = p1
        return interim


    # move one space at a time - easier than trying to keep track of
    # loops
    def cheesy_turn(self, num_spaces):
        n = 0
        s = mathutils.sign(num_spaces)
        for _ in range(abs(num_spaces)):
            self.current_pos = (self.current_pos + s + self.num_digits) % self.num_digits
            n += not self.current_pos
        return n


    def spin(self, turns, count_interim_zeros=False):
        num_zeros = 0
        for t in turns:
            int_zeros = self.cheesy_turn(t)
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

