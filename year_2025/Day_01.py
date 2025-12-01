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
        self.current_pos = (self.current_pos + self.num_digits + num_spaces) % self.num_digits
        #debug_print(f"CURRENT POS {self.current_pos}")



    def spin(self, turns):
        num_zeros = 0
        for t in turns:
            self.turn(t)
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


    def __init__(self, run_args):
        super(AdventDay, self).__init__(2025, 1)
        #self.args_parser.add_argument(
        #    "--calc",
        #    type=str,
        #    help="calculation",
        #    choices=["col-diffs", "similarity"],
        #    default="col-diffs",
        #    dest="calc",
        #)
        #self.add_args(run_args)


    def run(self):
        d = Dial()
        turns = [self._parse_turn(x) for x in self.input]
        n = d.spin(turns)
        debug_print(f"FINAL POS {d.current_pos} NUM 0 {n}")
 

    
    def _parse_turn(self, turn):
        return (1 if turn[0] == "R" else -1) * int(re.search(r'[LR](\d+)', turn).group(1))

