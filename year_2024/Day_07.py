import re
import Day
from utils import math
from utils import string
from utils.debug import debug

class Equation:
    import operator

    OPS = (
        operator.add,
        operator.mul,
        lambda x, y: int(str(x) + str(y))
    )

    def __init__(self, txt):
        e = [int(x) for x in re.findall(r"\d+", txt)]
        self.result = e[0]
        self.nums = e[1:]
        self.num_ops = len(Equation.OPS) ** (len(self.nums) - 1)
        self.ops = []



        
    def has_solutions(self):
    
        for i in range(self.num_ops):
            k = i
            op_arr = []
            ooo = []
            for j in reversed(range(len(self.nums) - 1)):
                n = len(Equation.OPS)**j
                r = k // n
                ooo.append(r)
                op_arr.append(Equation.OPS[r])
                k -= (r * n)

            res = self.nums[0]
            for j, n in enumerate(self.nums[1:]):
                res = op_arr[j](res, n)
            
            #debug(f"{self.nums} {op_arr} OP IN {i}: {res} CMP {self.result}")
            #debug(f"OP IN {i}: {res} CMP {self.result}")
            if res == self.result:
                return True

        return False
            
    

class AdventDay(Day.Base):
            

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            7,
            [
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
        )

    def solve_lines(self, v):
        s = 0
        for txt in v:
            e = Equation(txt)
            s += e.result * int(e.has_solutions())
        return s

    def run(self, v):
        s = self.solve_lines(v)
        debug(f"SOLUTION SUMS {s}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
