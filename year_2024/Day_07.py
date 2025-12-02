import re
import Day
from utils import mathutils
from utils import stringutils
from utils.debug import debug_print

class Equation:
    import operator

    OPS = (
        operator.add,
        operator.mul,
        lambda x, y: int(str(x) + str(y))
    )

    def __init__(self, txt, use_concat=False):
        e = [int(x) for x in re.findall(r"\d+", txt)]
        self.result = e[0]
        self.nums = e[1:]
        self.valid_ops = Equation.OPS[:(len(Equation.OPS) if use_concat else -1)]
        self.num_ops = len(self.valid_ops) ** (len(self.nums) - 1)
        self.ops = []

        
    def has_solutions(self):
    
        for i in range(self.num_ops):
            k = i
            op_arr = []
            ooo = []
            for j in reversed(range(len(self.nums) - 1)):
                n = len(self.valid_ops)**j
                r = k // n
                ooo.append(r)
                op_arr.append(self.valid_ops[r])
                k -= (r * n)

            res = self.nums[0]
            for j, n in enumerate(self.nums[1:]):
                res = op_arr[j](res, n)
            
            if res == self.result:
                return True

        return False
            
    

class AdventDay(Day.Base):
            
    TEST = [
        "190: 10 19",
        "3267: 81 40 27",
        "83: 17 5",
        "156: 15 6",
        "7290: 6 8 6 15",
        "161011: 16 10 13",
        "192: 17 8 14",
        "21037: 9 7 18 13",
        "292: 11 6 16 20",
    ]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 7)
        self.args_parser.add_argument(
            "--use-concat",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="use_concat",
        )
        self.add_args(run_args)

    def solve_lines(self):
        s = 0
        for txt in self.input:
            e = Equation(txt, use_concat=self.use_concat)
            s += e.result * int(e.has_solutions())
        return s

    def run(self):
        s = self.solve_lines()
        debug_print(f"SOLUTION SUMS {s}")
        return s


