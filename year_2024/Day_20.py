import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print


class Maze:
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


    def __init__(self, grid):
        self.grid = grid
        self.coord_grid = Day.Grid.grid_of_size(len(self.grid), len(self.grid[0]))
        self.walls = self._walls()
        self.start = self._token_pos(Maze.START)
        self.end = self._token_pos(Maze.END)
        self.connections = {k:[x for x in v if x not in self.walls] for k, v in self.coord_grid.coord_neighborhoods.items()}
        self.base_path = self.path()
        self.base_length = len(self.base_path) - 1
        self.alt_paths = self._alt_paths(self.base_path)
    
    def display_path(self, path, show_directions=False, show_walls=False):
        for r in self.coord_grid.coord_array:
            s = ""
            for c in r:
                if show_walls and c in self.walls:
                    s += Maze.WALL
                    continue
                if c not in path:
                    s += "."
                    continue

                i = path.index(c)
                if c == self.start:
                    s += Maze.START
                    continue
                if c == self.end:
                    s += Maze.END
                    continue
                if show_directions:
                    d =  self._dir(path[i - 1], c)
                    if d in Maze.DIR_SYMBOLS:
                        s +=  Maze.DIR_SYMBOLS[d]
                    else:
                        s += "*"
                else:
                    s += "x"
                    
            debug_print(s)
        debug_print("")

    def _dir(self, pos1, pos2):
        return (mathutils.sign(pos2[0] - pos1[0]), mathutils.sign(pos2[1] - pos1[1]))
    
    def _alt_paths(self, path):
        alts = {}

        for p in path:
            alts[p] = {}
            for c in [x for x in self.coord_grid.neighborhood(p) if x in self.walls]:
                n = [x for x in self.coord_grid.neighborhood(c) if x in path and path.index(x) > path.index(p)]
                if n:
                    alts[p][c] = n
        return alts

    def path_diffs(self):
        d = {}
        for c in self.alt_paths:
            for p in self.alt_paths_at_coord(c):
                l = self.base_length - len(p)
                if l not in d:
                    d[l] = 0
                d[l] += 1
        #dd = {k:d[k] for k in sorted(d.keys())}
        #debug_print(f"DIFFS {dd}")
        #return dd
        return d

    def num_diffs_at_least(self, l):
        d = self.path_diffs()
        return mathutils.sum([v for k, v in d.items() if k >= l])

    def alt_paths_at_coord(self, coord):
        if coord not in self.alt_paths:
            return None
        paths = []
        p = self.base_path[:self.base_path.index(coord)]
        for c in self.alt_paths[coord]:
            for cc in self.alt_paths[coord][c]:
                paths.append(p + [c] + self.base_path[self.base_path.index(cc):])
        return paths
            


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
        self.args_parser.add_argument(
            "--cheat-duration",
            type=int,
            help="duration of cheat time",
            default=2,
            dest="cheat_duration",
        )
        self.args_parser.add_argument(
            "--min-difference",
            type=int,
            help="minimum difference bewtween path length and base length to count",
            default=100,
            dest="min_path_length",
        )
        self.add_args(run_args)
       

    def run(self):
        m = Maze(self.input)
        #m.display_path(m.base_path)
        return(m.num_diffs_at_least(self.min_path_length))
        #t = self.min_path_length
        #debug_print(f"DIFF {t}: {m.num_diffs_at_least(t)}")

