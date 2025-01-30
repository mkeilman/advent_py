import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug


class Computer:

    DIRECTIONS = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    DIR_SYMBOLS = {
        (0, 1): ">",
        (1, 0): "v",
        (0, -1): "<",
        (-1, 0): "^",
    }

    START = "S"
    END = "E"

    WALL = "#"

    MAX_SCORE = 1e23

    def __init__(self):
        self.pointer = 0
        self.program = []
        self.registers = {
            "A": 0,
            "B": 0,
            "C": 0,
        }


    def load(self, v):
        regs = r"Register\s+([ABC]):\s+(\d+)"
        for txt in v:
            if "Program" in txt:
                self.program = [int(x) for x in re.findall(r"\d", txt)]
                continue
            m = re.match(regs, txt)
            if m:
                self.registers[m.group(1)] = int(m.group(2))

    

class AdventDay(Day.Base):

    TEST = [
        "Register A: 729",
        "Register B: 0",
        "Register C: 0",
        "",
        "Program: 0,1,5,4,3,0",
    ]



    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            17,
            AdventDay.TEST
        )
        self.args_parser.add_argument(
            "--warehouse-size",
            type=str,
            help="single or double size",
            choices=["single", "double"],
            default="single",
            dest="warehouse_size",
        )
        self.add_args(run_args)
       

    def run(self, v):
        c = Computer()
        c.load(v)
        debug(f"RUN A {c.registers["A"]} B {c.registers["B"]} C {c.registers["C"]} PROG {c.program}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()