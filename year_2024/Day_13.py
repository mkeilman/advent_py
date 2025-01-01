import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Crane:
    def __init__(self, lines):
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
        return (int(m.group(1)), int(m.group(2)))


    def _paths(self):
        paths = []
        for n in range(self.buttons["A"]["max_presses"]):
            for m in range(self.buttons["B"]["max_presses"]):
        #for n in range(0, self.prize_coords[0] // self.buttons["A"]["X"]):
        #    for m in range(0, self.prize_coords[0] // self.buttons["B"]["X"]):
                x = n * self.buttons["A"]["X"] + m * self.buttons["B"]["X"]
                y = n * self.buttons["A"]["Y"] + m * self.buttons["B"]["Y"]
                if x == self.prize_coords[0] and y == self.prize_coords[1]:
                    paths.append((n, m))
        
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

    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2024,
            13,
            AdventDay.TEST
        )
        self.args_parser.add_argument(
            "--length-type",
            type=str,
            help="calculation",
            choices=["perimeter", "num-sides"],
            default="perimeter",
            dest="length_type",
        )
        self.length_type = self.args_parser.parse_args(run_args).length_type

    def run(self, v):
        self.cranes = self._parse(v)
        debug(f"NUM CR {len(self.cranes)} LAST {self.cranes[-1].paths}")
        min_price = mathutils.sum([x.min_price for x in self.cranes])
        debug(f"MIN PRICE {min_price}")

    def _parse(self, grid):
        i = 0
        cranes = []
        while i < len(grid):
            cranes.append(Crane(grid[i:i + 3]))
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