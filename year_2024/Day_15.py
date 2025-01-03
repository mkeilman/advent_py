import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Warehouse:
    WALL = "#"

    ROBOT = "@"

    BOX = "O"

    def __init__(self, grid):
        self.grid = grid
        self.boxes = self._boxes()
        self.walls = self._walls()

        for i, s in enumerate(grid):
            if Warehouse.ROBOT in s:
                self.robot = Robot((i, s.index(Warehouse.ROBOT)))
                break

    def _boxes(self):
        b = []
        for i, s in enumerate(self.grid):
            b.append([(i, j) for j in string.indices(Warehouse.BOX, s)])
        return b

    def _walls(self):
        w = []
        for i, s in enumerate(self.grid):
            w.append([(i, j) for j in string.indices(Warehouse.WALL, s)])
        return w

        

class Robot:

    move_map = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }

    def __init__(self, init_pos):
        self.init_pos = init_pos
        self.reset()

    def set_path(self, txt):
        self.path = txt

    def reset(self):
        self.pos = self.init_pos[:]


class AdventDay(Day.Base):

    TEST = [
        "########",
        "#..O.O.#",
        "##@.O..#",
        "#...O..#",
        "#.#.O..#",
        "#...O..#",
        "#......#",
        "########",
        "",
        "<^^>>>vv<v>>v<<",
    ]

    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2024,
            15,
            AdventDay.TEST
        )
        self.args_parser.add_argument(
            "--width",
            type=int,
            help="foyer width",
            default=11,
            dest="width",
        )
        self.width = self.args_parser.parse_args(run_args).width


    def run(self, v):
        w = self._parse(v)
        #debug(f"WALLS {w.walls} BOXES {w.boxes}")
        debug(f"R {w.robot.init_pos} {w.robot.path}")

    
    def _parse(self, v):
        j = 0
        s = v[j]
        w = []
        while s:
            w.append(s)
            j += 1
            s = v[j]
        wh = Warehouse(w)
        wh.robot.set_path("".join(v[j + 1:]))
        return wh


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
