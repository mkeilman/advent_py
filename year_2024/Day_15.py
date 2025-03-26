import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Warehouse:

    TOKENS = {
        "wall": {
            "single": "#",
            "re": "#",
            "double": "##",
        },
        "box": {
            "single": "O",
            "re": "O",
            "double": "[]",
        },
        "space": {
            "single": ".",
            "re": r"\.",
            "double": "..",
        },
        "robot": {
            "single": "@",
            "re": "@",
            "double": "@.",
        },
    }
    

    def __init__(self, grid, size="single"):
        self.size = size
        self.base_grid = grid
        self.grid = self.base_grid if self.size == "single" else self.double()
        self.walls = self._walls()
        self.box_hits = 0
        self.robot = Robot()
        self.reset_robot()
        self.reset_boxes()


    def double(self):
        g = []
        for s in self.base_grid:
            for t in Warehouse.TOKENS:
                s = re.sub(Warehouse.TOKENS[t]["re"], Warehouse.TOKENS[t]["double"], s)
            g.append(s)
        return g


    def display(self):
        g = self.grid
        for i in range(len(g)):
            s = ""
            j = 0
            while j in range(len(g[0])):
                t = self._str_at((i, j))
                s += t
                j += len(t)
            debug(s)


    def reset_boxes(self):
        dy = int(self.size == "double")
        self.boxes = []
        for i, s in enumerate(self.grid):
            for j in string.indices(Warehouse.TOKENS["box"][self.size], s):
                p = [(i, j)]
                if self.size == "double":
                    p.append((i, j + 1))
                self.boxes.append(p)


    def reset_robot(self):
        r = Warehouse.TOKENS["robot"]["single"]
        for i, s in enumerate(self.grid):
            if r in s:
                self.robot.init_pos = (i, s.index(r))
                self.robot.pos = self.robot.init_pos
                return
    

    def _str_at(self, pos):
        #debug(f"POS {pos} R {self.robot.pos}")
        t = Warehouse.TOKENS
        # walls only double at initial generation
        if pos in self.walls:
            return t["wall"]["single"]
        if pos in [x[0] for x in self.boxes]:
            return t["box"][self.size]
        if self.robot.pos == pos:
            return t["robot"]["single"]
        return "."


    def gps(self):
        return mathutils.sum([100 * x[0][0] + x[0][1] for x in self.boxes])
    

    def move_robot(self):

        def _can_all_move(boxes, direction):
            return all([_move_box(x, direction, check_only=True) for x in boxes])

        def _move_box(b0, direction, check_only=False):
            # the "core" of the box is the first position
            q0 = (b0[0][0] + direction[0], b0[0][1] + direction[1])
            #debug(f"TRY BOX {b0} -> {q0}")
            if self._hits_wall(b0, direction):
                #debug(f"BOX HIT WALL")
                return False
            bb = [y for y in self._get_boxes([(x[0] + direction[0], x[1] + direction[1]) for x in b0]) if y != b0]
            #debug(f"BB {bb}")
            if not _can_all_move(bb, direction):
                self.box_hits += 1
                if self.robot.path_index > 468:
                    debug(f"{self.robot.path_index} {self.robot.get_move_symbol()} SOME BOXES BLOCKED {bb}")
                    self.display()
                return False
            for b in bb:
                _move_box(b, direction)

            #debug(f"PUSH BOX {b0} -> {q0}")
            if not check_only:
                #debug(f"PUSH BOX {b0} -> {q0}")
                #predict = self.gps() + 100 * direction[0] + direction[1]
                #debug(f"PREDICTED GPS {predict}")
                #self.display()
                self._set_box(b0, q0)
                #if predict != self.gps():
                #    debug(f"BAD GPS!")
            #self.display()
            return True


        dir = self.robot.get_move()
        next_p = (self.robot.pos[0] + dir[0], self.robot.pos[1] + dir[1])
        #debug(f"TRY MOVING {self.robot.pos} -> {next_p}")
        if next_p in self.walls:
        #if self._hits_wall([next_p]):
            #debug(f"ROBOT HIT WALL")
            self.robot.move(None)
            return
        hb = self._hits_box([next_p])
        if hb:
            #self.box_hits += 1
            #debug(f"{self.robot.path_index} {self.robot.get_move_symbol()} HIT BOX AT {next_p} {self.box_hits}")
            q = _move_box(self._get_box(next_p), dir)
            if not q:
                self.robot.move(None)
                return
        #debug(f"MOVING TO {next_p}")
        self.robot.move(next_p)
        #if hb:
        #    self.display()
        #if not self.robot.path_index % 1000:
        #    self.display()
        #self.display()
        

    def run_robot(self):
        self.reset_boxes()
        self.reset_robot()
        debug(f"START ROBOT {self.robot.init_pos}")
        while self.robot.has_moves():
            self.move_robot()

    def _get_box(self, pos):
        for r in self.boxes:
            if pos in r:
                return r
        return None
    
    def _get_boxes(self, positions):
        boxes = []
        for p in positions:
            b = self._get_box(p)
            if b not in boxes:
                boxes.append(b)
        return [x for x in boxes if x]
    
    def _set_box(self, box, pos):
        box[0] = pos
        if len(box) == 2:
            box[1] = (pos[0], pos[1] + 1)

    def _hits_box(self, positions):
        br = self.boxes
        for p in positions:
            if any([p in x for x in br]):
                return True
        return False
    
    def _hits_wall(self, box, direction):
        q = [(x[0] + direction[0], x[1] + direction[1]) for x in box]
        return any([x in self.walls for x in q])

    def _walls(self):
        w = []
        for i, s in enumerate(self.grid):
            for j in string.indices(Warehouse.TOKENS["wall"]["single"], s):
                w.append((i, j))
        return w


class Robot:

    move_map = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }

    def __init__(self, init_pos=(0,0), max_moves=0):
        self.init_pos = init_pos
        self.max_moves = max_moves
        self.path = ""
        self.reset()

    def has_moves(self):
        return self.path_index < len(self.path)
    
    def get_move(self):
        return Robot.move_map[self.get_move_symbol()]
    
    def get_move_symbol(self):
        return self.path[self.path_index]
    
    def move(self, next_pos):
        if next_pos:
            self.pos = next_pos
        self.path_index += 1
        

    def set_path(self, txt):
        #self.path = txt
        self.max_moves = self.max_moves or len(txt)
        debug(f"N {self.max_moves}")
        self.path = txt[0:self.max_moves]
        self.reset()

    def reset(self):
        self.pos = self.init_pos[:]
        self.path_index = 0


class AdventDay(Day.Base):

    PYRAMID = [
        "#######",
        "#...#.#",
        "#.....#",
        "#..OO@#",
        "#..O..#",
        "#.....#",
        "#######",
        "",
        "<vv<<^^<<^^",
    ]

    RIGHT = [
        "#########",
        "#...@...#",
        "#..O....#",
        "#.#O....#",
        "#..O....#",
        "#.......#",
        "#.......#",
        "#########",
        "",
        "v<>vv<>^^<^<vvv>vv<^",
    ]

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

    def __init__(self, year, day, run_args):
        import argparse
        super(AdventDay, self).__init__(
            year,
            day,
            AdventDay.RIGHT
        )
        self.args_parser.add_argument(
            "--warehouse-size",
            type=str,
            help="single or double size",
            choices=["single", "double"],
            default="single",
            dest="warehouse_size",
        )
        self.args_parser.add_argument(
            "--max-moves",
            type=int,
            help="max moves the robot can make (0 = all)",
            default=0,
            dest="max_moves",
        )
        self.add_args(run_args)
       

    def run(self, v):
        w = self._parse(v)
        #w.display()
        w.run_robot()
        debug(f"GPS {w.gps()} BOX STUCK {w.box_hits}")
        #w.display()

    
    def _parse(self, v):
        j = 0
        s = v[j]
        w = []
        while s:
            w.append(s)
            j += 1
            s = v[j]
        wh = Warehouse(w, size=self.args["warehouse_size"])
        wh.robot.max_moves = self.args["max_moves"]
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