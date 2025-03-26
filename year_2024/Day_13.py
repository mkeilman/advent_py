import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Crane:
    def __init__(self, lines, prize_offset=0):
        self.buttons = {
            "A": {
                "cost": 3,
                "max_presses": 100,
            },
            "B": {
                "cost": 1,
                "max_presses": 100,
            },
        }
        self.start = (0, 0)
        self.prize_offset = prize_offset
        for i in (0, 1):
            self._build_button(lines[i])
        self.prize_coords = self._prize_coords(lines[2])
        self.paths = self._paths()
        self.prices = [self.path_price(x) for x in self.paths]
        self.min_price = min(self.prices) if self.paths else 0

    def path_price(self, path):
        return path[0] * self.buttons["A"]["cost"] + path[1] * self.buttons["B"]["cost"]


    def _build_button(self, txt):
        m = re.match(r"Button\s+([AB]):\s+X[+-](\d+),\s+Y[+-](\d+)", txt)
        label = m.group(1)
        for i, c in enumerate(("X", "Y")):
            self.buttons[label][c] = int(m.group(2 + i))
    

    def _prize_coords(self, txt):
        m = re.match(r"Prize:\s+X=(\d+),\s+Y=(\d+)", txt)
        return (int(m.group(1)) + self.prize_offset, int(m.group(2)) + self.prize_offset)


    def _paths(self):
        paths = []
        dxa = self.buttons["A"]["X"]
        dxb = self.buttons["B"]["X"]
        dya = self.buttons["A"]["Y"]
        dyb = self.buttons["B"]["Y"]

        m = (self.prize_coords[1] * dxa - self.prize_coords[0] * dya) / (dxa * dyb - dxb * dya)
        n = (self.prize_coords[0] - m * dxb) / dxa
        if n % 1 == 0 and m % 1 == 0:
            paths.append((int(n), int(m)))
        #for n in range(self.buttons["A"]["max_presses"]):
        #    for m in range(self.buttons["B"]["max_presses"]):
        #for n in range(0, self.prize_coords[0] // self.buttons["A"]["X"]):
        #    for m in range(0, self.prize_coords[0] // self.buttons["B"]["X"]):
        #        x = n * self.buttons["A"]["X"] + m * self.buttons["B"]["X"]
        #        y = n * self.buttons["A"]["Y"] + m * self.buttons["B"]["Y"]
        #        if x == self.prize_coords[0] and y == self.prize_coords[1]:
        #            paths.append((n, m))
        
        return paths

class AdventDay(Day.Base):

    TEST = [
        "Button A: X+94, Y+34",
        "Button B: X+22, Y+67",
        "Prize: X=8400, Y=5400",
        "",
        "Button A: X+26, Y+66",
        "Button B: X+67, Y+21",
        "Prize: X=12748, Y=12176",
        "",
        "Button A: X+17, Y+86",
        "Button B: X+84, Y+37",
        "Prize: X=7870, Y=6450",
        "",
        "Button A: X+69, Y+23",
        "Button B: X+27, Y+71",
        "Prize: X=18641, Y=10279",
    ]

    def __init__(self, year, day, run_args):
        super(AdventDay, self).__init__(
            year,
            day,
        )
        self.args_parser.add_argument(
            "--prize-offset",
            type=int,
            help="prize offset",
            default=0,
            dest="prize_offset",
        )
        self.prize_offset = self.args_parser.parse_args(run_args).prize_offset

    def run(self, v):
        self.cranes = self._parse(v)
        min_price = mathutils.sum([x.min_price for x in self.cranes])
        debug(f"MIN PRICE {min_price}")

    def _parse(self, grid):
        i = 0
        cranes = []
        while i < len(grid):
            cranes.append(Crane(grid[i:i + 3], prize_offset=self.prize_offset))
            i += 4
        return cranes


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
