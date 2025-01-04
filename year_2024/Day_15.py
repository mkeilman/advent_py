import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Warehouse:

    TOKENS = {
        "wall": {
            "base": "#",
            "re": "#",
            "double": "##",
        },
        "box": {
            "base": "O",
            "re": "O",
            "double": "[]",
        },
        "space": {
            "base": ".",
            "re": r"\.",
            "double": "..",
        },
        "robot": {
            "base": "@",
            "re": "@",
            "double": "@.",
        },
    }
    

    def __init__(self, grid):
        self.grids = {
            "base": grid,
        }
        self.grids["double"] = self.double()
        self.walls = {
            "base": self._walls(),
            "double": self._walls(warehouse_size="double"),
        }
        self.robot = Robot((0, 0))
        self.reset_boxes()


    def double(self):
        g = []
        for s in self.grids["base"]:
            for t in Warehouse.TOKENS:
                s = re.sub(Warehouse.TOKENS[t]["re"], Warehouse.TOKENS[t]["double"], s)
            debug(s)
            g.append(s)
        return g


    def display(self, warehouse_size="base"):
        g = self.grids[warehouse_size]
        for i in range(len(g)):
            s = ""
            for j in range(len(g[0])):
                s += self._str_at((i, j), warehouse_size=warehouse_size)
            debug(s)


    def reset_boxes(self):
        self.boxes = {
            "base": self._boxes(),
        }
        self.boxes["double"] = self._boxes(warehouse_size="double")
        

    def reset_robot(self, warehouse_size=False):
        for i, s in enumerate(self.grids[warehouse_size]):
            r = Warehouse.TOKENS["robot"]["base"]
            if r in s:
                self.robot.pos = [i, s.index(r)]
                break
    

    def _str_at(self, pos, warehouse_size="base"):
        t = Warehouse.TOKENS
        # walls only double at initial generation
        if pos in self.walls[warehouse_size]:
            return t["wall"]["base"]
        if pos in self.boxes[warehouse_size]:
            return t["box"][warehouse_size]
        if self.robot.pos == pos:
            return t["robot"]["base"]
        return "."


    def gps(self):
        return mathutils.sum([100 * x[0] + x[1] for x in self.boxes])
    

    def move_robot(self):

        def _move_box(old_pos, direction):
            q = (old_pos[0] + direction[0], old_pos[1] + direction[1])
            #debug(f"TRY BOX {old_pos} -> {q}")
            if q in self.walls:
                #debug(f"CANNOT PUSH BOX TO {q}")
                return old_pos
            if q in self.boxes:
                #debug(f"BOX HIT BOX AT {q}")
                r = _move_box(q, direction)
                if r == q:
                    return old_pos
            #debug(f"PUSH BOX {old_pos} -> {q}")
            i = self.boxes.index(old_pos)
            self.boxes = self.boxes[:i] + [q] + self.boxes[i + 1:]
            return q

        dir = self.robot.get_move()
        next_p = (self.robot.pos[0] + dir[0], self.robot.pos[1] + dir[1])
        if next_p in self.walls:
            #debug(f"HIT WALL AT {next_p}")
            next_p = self.robot.pos
        elif next_p in self.boxes:
            #debug(f"HIT BOX AT {next_p}")
            q = _move_box(next_p, dir)
            if q == next_p:
                next_p = self.robot.pos
        #debug(f"MOVING TO {next_p}")
        self.robot.move(next_p)
        

    def run_robot(self, warehouse_size="base"):
        self.reset_boxes()
        self.reset_robot(warehouse_size=warehouse_size)
        debug(f"START ROBOT {self.robot.init_pos}")
        while self.robot.has_moves():
            self.move_robot()
    

    def _boxes(self, warehouse_size="base"):
        b = []
        for i, s in enumerate(self.grids[warehouse_size]):
            for j in string.indices(Warehouse.TOKENS["box"]["base"], s):
                b.append((i, j))
        return b


    def _walls(self, warehouse_size="base"):
        w = []
        for i, s in enumerate(self.grids[warehouse_size]):
            for j in string.indices(Warehouse.TOKENS["wall"]["base"], s):
                w.append((i, j))
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
        self.path = ""
        self.reset()

    def has_moves(self):
        return self.path_index < len(self.path)
    
    def get_move(self):
        return Robot.move_map[self.path[self.path_index]]
    
    def move(self, next_pos):
        self.pos = next_pos
        self.path_index += 1

    def set_path(self, txt):
        self.path = txt
        self.reset()

    def reset(self):
        self.pos = self.init_pos[:]
        self.path_index = 0


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

    TEST_LARGE = [
        "##########",
        "#..O..O.O#",
        "#......O.#",
        "#.OO..O.O#",
        "#..O@..O.#",
        "#O#..O...#",
        "#O..O..O.#",
        "#.OO.O.OO#",
        "#....O...#",
        "##########",
        "",
        "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^",
        "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v",
        "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<",
        "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^",
        "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><",
        "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^",
        ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^",
        "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>",
        "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>",
        "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^",
    ]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            15,
            AdventDay.TEST_LARGE
        )
        self.args_parser.add_argument(
            "--warehouse-size",
            type=str,
            help="base or double size",
            choices=["base", "double"],
            default="base",
            dest="warehouse_size",
        )
        self.add_args(run_args)
       

    def run(self, v):
        w = self._parse(v)
        w.display(warehouse_size=self.args["warehouse_size"])
        #debug(f"WALLS {w.walls} BOXES {w.boxes}")
        #debug(f"R {w.robot.init_pos} {w.robot.path}")
        #w.run_robot()
        #debug(f"GPS {w.gps()}")
        #w.display()

    
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