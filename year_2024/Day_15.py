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
        #if pos in [x[0] for x in self._box_ranges()]:
        if pos in [x[0] for x in self.boxes]:
            return t["box"][self.size]
        if self.robot.pos == pos:
            return t["robot"]["single"]
        return "."


    def gps(self):
        return mathutils.sum([100 * x[0][0] + x[0][1] for x in self.boxes])
    

    def move_robot(self):

        def _move_box(old_pos, direction):
            b0 = self._get_box(old_pos)
            q = (old_pos[0] + direction[0], old_pos[1] + direction[1])
            #debug(f"TRY BOX {b0} {old_pos} -> {q}")
            #debug(f"{b0} HITS WALL? {self._hits_wall(b0, direction)}")
            #if q in self.walls:
            if self._hits_wall(b0, direction):
                #debug(f"CANNOT PUSH BOX TO {q}")
                return old_pos
            #if q in self._box_coords():
            b = self._get_box(q)
            # pushing one side of a box into the other side
            if b == b0:
                q = (q[0] + direction[0], q[1] + direction[1])
                #debug(f"PUSHING BOX INTO ITSELF, PUSH NEXT SIDE {q}")
                b = self._get_box(q)
            if b and self._hits_box(b):
                #debug(f"BOX HIT BOX AT {q}: {b}")
                r = _move_box(q, direction)
                if r == q:
                    return old_pos
                

            #debug(f"PUSH BOX {old_pos} -> {q}")
            #op = old_pos
            #qq = q
            #if old_pos not in self.boxes:
            #if not self._hits_box(old_pos):
            #    #?
            #    op = (old_pos[0] - direction[0], old_pos[1] - direction[1])
            #    qq = (q[0] - direction[0], q[1] +  - direction[1])
            #   #_move_box((old_pos[0], old_pos[1] + 1), direction)
            #i = self.boxes.index(old_pos)
            #self.boxes = self.boxes[:i] + [q] + self.boxes[i + 1:]
            b = self._get_box(old_pos)
            self._set_box(b, q)
            #i = self.boxes.index(op)
            #self.boxes = self.boxes[:i] + [qq] + self.boxes[i + 1:]
            #self.display()
            return q


        dir = self.robot.get_move()
        next_p = (self.robot.pos[0] + dir[0], self.robot.pos[1] + dir[1])
        #debug(f"TRY MOVING TO {next_p}")
        #bc = self._box_coords()
        #br = self._box_ranges()
        #debug(f"BR {br}")
        if next_p in self.walls:
        #if self._hits_wall([next_p]):
            #debug(f"HIT WALL AT {next_p}")
            self.robot.move(None)
            return
        if self._hits_box([next_p]):
            #debug(f"HIT BOX AT {next_p}")
            q = _move_box(next_p, dir)
            if q == next_p:
                self.robot.move(None)
                return
        #debug(f"MOVING TO {next_p}")
        self.robot.move(next_p)
        #self.display()
        

    def run_robot(self):
        self.reset_boxes()
        self.reset_robot()
        debug(f"START ROBOT {self.robot.init_pos}")
        while self.robot.has_moves():
            self.move_robot()



    def _box_coords(self):
        if self.size == "single":
            return self.boxes
        return self.boxes + [(x[0], x[1] + 1) for x in self.boxes]


    def _box_ranges(self):
        dy = int(self.size == "double")
        return [(x, (x[0], x[1] + dy)) for x in self.boxes]


    def _get_box(self, pos):
        for r in self.boxes:
            if pos in r:
                return r
        return None
    
    def _get_boxes(self, positions):
        b = []
        for p in positions:
            b.append(self._get_box(p))
        return [x for x in b if x]
    
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

    def _hits_boxes(self, box, direction):
        q = [(x[0] + direction[0], x[1] + direction[1]) for x in box]
        debug(f"CHECK BOXES {box}: {q}")
        return self._hits_box(q)
    
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

    def __init__(self, init_pos=(0,0)):
        self.init_pos = init_pos
        self.path = ""
        self.reset()

    def has_moves(self):
        return self.path_index < len(self.path)
    
    def get_move(self):
        return Robot.move_map[self.path[self.path_index]]
    
    def move(self, next_pos):
        if next_pos:
            self.pos = next_pos
        self.path_index += 1

    def set_path(self, txt):
        self.path = txt
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
            help="single or double size",
            choices=["single", "double"],
            default="single",
            dest="warehouse_size",
        )
        self.add_args(run_args)
       

    def run(self, v):
        w = self._parse(v)
        w.display()
        w.run_robot()
        debug(f"GPS {w.gps()}")
        w.display()

    
    def _parse(self, v):
        j = 0
        s = v[j]
        w = []
        while s:
            w.append(s)
            j += 1
            s = v[j]
        wh = Warehouse(w, size=self.args["warehouse_size"])
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