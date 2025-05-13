import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print


class Maze:

    START = "S"
    END = "E"
    WALL = "#"


    def __init__(self, grid):
        self.grid = grid
        self.coord_grid = Day.Grid.grid_of_size(len(self.grid), len(self.grid[0]))
        self.walls = self._walls()
        self.start = self._token_pos(Maze.START)
        self.end = self._token_pos(Maze.END)
        self.connections = {k:[x for x in v if x not in self.walls] for k, v in self.coord_grid.coord_neighborhoods.items()}
    
    def display_path(self, path):
        for r in self.coord_grid.coord_array:
            s = ""
            for c in r:
                #if c in self.walls:
                #    s += Maze.WALL
                if c not in path:
                    s += "."
                else:
                    i = path.index(c)
                    if c == self.start:
                        s += Maze.START
                        continue
                    if c == self.end:
                        s += Maze.END
                        continue
                    d =  self._dir(path[i - 1], c)
                    if d in Maze.DIR_SYMBOLS:
                        s +=  Maze.DIR_SYMBOLS[d]
                    else:
                        s += "*"
            debug_print(s)
        debug_print("")

    def _dir(self, pos1, pos2):
        return (mathutils.sign(pos2[0] - pos1[0]), mathutils.sign(pos2[1] - pos1[1]))
    
    # this particular maze type has one and only one path
    def path(self):
        def _conn(pos, path):
            return [x for x in self.connections[pos] if x != path[path.index(pos) - 1] and x not in path]
    
        pos = self.start
        path = [pos]
        while pos != self.end:
            pos = _conn(pos, path)[0]
            path.append(pos)
        return path

    def _token_pos(self, token):
        for i, r in enumerate(self.grid):
            if token in r:
                return (i, r.index(token))
        return None

    def _walls(self):
        w = []
        for i, r in enumerate(self.grid):
            for j in string.indices(Maze.WALL, r):
                w.append((i, j))
        return w


class AdventDay(Day.Base):

    TEST = [
        "###############",
        "#...#...#.....#",
        "#.#.#.#.#.###.#",
        "#S#...#.#.#...#",
        "#######.#.#.###",
        "#######.#.#...#",
        "#######.#.###.#",
        "###..E#...#...#",
        "###.#######.###",
        "#...###...#...#",
        "#.#####.#.###.#",
        "#.#...#.#.#...#",
        "#.#.#.#.#.#.###",
        "#...#...#...###",
        "###############",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 20)
        self.add_args(run_args)
       

    def run(self):
        m = Maze(self.input)
        #c = {k:v for k, v in m.connections.items() if v}
        p = m.path()
        debug_print(f"RUN START {m.start} END {m.end} P {p} LEN {len(p) - 1}")

