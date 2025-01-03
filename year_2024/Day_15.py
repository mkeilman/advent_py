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

    def display(self):
        for i in range(len(self.grid)):
            s = ""
            for j in range(len(self.grid[0])):
                s += self._str_at((i, j))
            debug(s)

    def _str_at(self, pos):
        if pos in self.walls:
            return Warehouse.WALL
        if pos in self.boxes:
            return Warehouse.BOX
        if self.robot.pos == pos:
            return Warehouse.ROBOT
        return "."

    def move_robot(self):

        def _move_box(old_pos, direction):
            q = (old_pos[0] + direction[0], old_pos[1] + direction[1])
            if q in self.walls:
                debug(f"CANNOT PUSH BOX TO {q}")
                return old_pos
            if q in self.boxes:
                q = _move_box(q, direction)
            if q == old_pos:
                return old_pos
            debug(f"PUSH BOX {old_pos} -> {q}")
            i = self.boxes.index(old_pos)
            self.boxes = self.boxes[:i] + [q] + self.boxes[i + 1:]
            return q

        dir = self.robot.get_move()
        p = (self.robot.pos[0] + dir[0], self.robot.pos[1] + dir[1])
        if p in self.walls:
            debug(f"HIT WALL AT {p}")
            p = self.robot.pos
        elif p in self.boxes:
            debug(f"HIT BOX AT {p}")
            q = _move_box(p, dir)
            if q == p:
                p = self.robot.pos
            #q = (p[0] + dir[0], p[1] + dir[1])
            #if q in self.boxes or q in self.walls:
            #    debug(f"CANNOT PUSH BOX TO {q}")
            #    p = self.robot.pos
            #else:
            #    _move_box(p, dir)
            #    #i = self.boxes.index(p)
            #    #self.boxes = self.boxes[:i] + [q] + self.boxes[i + 1:]
        debug(f"MOVING TO {p}")
        self.robot.move(p)
        

    def run_robot(self):
        debug(f"START ROBOT {self.robot.init_pos}")
        while self.robot.has_moves():
            self.move_robot()
            self.display()
    

    def _boxes(self):
        b = []
        for i, s in enumerate(self.grid):
            for j in string.indices(Warehouse.BOX, s):
                b.append((i, j))
        return b

    def _walls(self):
        w = []
        for i, s in enumerate(self.grid):
            for j in string.indices(Warehouse.WALL, s):
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
        w.display()
        #debug(f"WALLS {w.walls} BOXES {w.boxes}")
        #debug(f"R {w.robot.init_pos} {w.robot.path}")
        w.run_robot()
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