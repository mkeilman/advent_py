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
        self.interior_walls = self._interior_walls()
        #debug_print(f"IW {self.interior_walls}")
        self.start = self._token_pos(Maze.START)
        self.end = self._token_pos(Maze.END)
        self.connections = {k:[x for x in v if x not in self.walls] for k, v in self.coord_grid.coord_neighborhoods.items()}
        self.base_path = self.path()
        self.base_length = len(self.base_path) - 1
    

    def display_path(self, path, show_directions=False, show_walls=False):
        for r in self.coord_grid.coord_array:
            s = ""
            for c in r:
                if show_walls and c in self.walls:
                    s += Maze.WALL
                    continue
                if c == self.start:
                    s += Maze.START
                    continue
                if c == self.end:
                    s += Maze.END
                    continue
                if c not in path:
                    s += "."
                    continue

                i = path.index(c)
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


    def _interior_walls(self):
        return [x for x in self.walls if self._is_interior_wall(x)]


    def _is_interior_wall(self, coord):
        return 0 < coord[0] < self.coord_grid.size[0] and 0 < coord[1] < self.coord_grid.size[1]


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
            dest="min_difference",
        )
        self.add_args(run_args)
       

    def num_min_diffs(self):
        n = 0
        #for i in range(2, self.cheat_duration + 1):
        #    n += mathutils.sum([v for k, v in self._path_diffs(i).items() if k >= self.min_difference])
        #return n
        return mathutils.sum([v for k, v in self._path_diffs(self.cheat_duration).items() if k >= self.min_difference])
        

    def run(self):
        self.maze = Maze(self.input)
        #self.maze.display_path(self.maze.base_path)
        n = self.num_min_diffs()
        #m = self.maze.num_diffs_at_least(self.min_difference)
        #r = 10
        #ctr = (8, 8)
        #c = self.maze.coord_grid.circle(ctr, r)
        #debug_print(f"CTR : {ctr} R: {r} C {c}")
        #p1 = (12, 8)
        #p2 = (12, 12)
        #d = 1
        #c = self.maze.coord_grid.ell(p1, p2, direction=d)
        #self.maze.display_path(c)
        #debug_print(f"P1 {p1} P2 {p2} DIR {d} ELL {c}")
        debug_print(f"N : {n}")
        return n
        #return 0
    

    #def _alt_paths(self, path):
    #        alts = {}#
    #
    #        for p in path:
    #            alts[p] = {}
    #            for c in [x for x in self.coord_grid.neighborhood(p) if x in self.walls]:
    #                n = [x for x in self.coord_grid.neighborhood(c) if x in path and path.index(x) > path.index(p)]
    #                if n:
    #                    alts[p][c] = n
    #        return alts

    def _alt_paths(self, duration):

        alts = {}

        m = self.maze
        for coord in m.base_path:
            alts[coord] = {}
            for c in [x for x in m.coord_grid.neighborhood(coord) if x in m.walls]:
                n = [x for x in m.coord_grid.neighborhood(c) if x in m.base_path and m.base_path.index(x) > m.base_path.index(coord)]
                if n:
                    alts[coord][c] = n
        return alts
            # start "cheat" in an adjacent wall
            #for c in [x for x in m.coord_grid.neighborhood(coord) if x in m.interior_walls]:

            #    cc = [x for x in m.coord_grid.circle(c, duration - 1) if x in m.base_path and m.base_path.index(x) > m.base_path.index(coord)]
            #    # ELLS - 
            #    n = [m.coord_grid.ell(c, x) for x in cc]
            #    #debug_print(f"ELLS {cc} -> {ells}")
            #    #n = [x for x in cc if x in m.base_path and m.base_path.index(x) > m.base_path.index(coord)]
            #   #n = [x for x in ells if x in m.base_path and m.base_path.index(x) > m.base_path.index(coord)]
            #   if n:
            #        #debug_print(f"CHEAT START {c}")
            #        #m.display_path(cc)
            #        #for p in n:
            #        #    m.display_path(p)
            #        alts[coord][c] = n
        #return alts

    
    def _path_diffs(self, duration):
        def _alt_paths_at_coord(coord, alt_paths):
            if coord not in alt_paths:
                return None
            
            m = self.maze
            paths = []
            p = m.base_path[:m.base_path.index(coord) + 1]
            for start in alt_paths[coord]:
                for end in alt_paths[coord][start]:
                #debug_print(f"C {start}")
                #for pp in alt_paths[coord][start]:
                    #debug_print(f"C {start} -> {pp[-1]}")
                    debug_print(f"C {start} -> {end}")
                    m.display_path(p + [start] + [end])
                    #paths.append(p + [start] + pp + m.base_path[m.base_path.index(pp[-1]):])
                    #debug_print(f"START {start} END {end} LINE {m.coord_grid.line(start, end, allow_diags=False)}")
                    #paths.append(p + m.coord_grid.line(start, end, allow_diags=False) + m.base_path[m.base_path.index(end):])
                    paths.append(p + [end] + m.base_path[m.base_path.index(end):])
            return paths
    
        d = {}
        a = self._alt_paths(duration)
        for c in a:
            for p in _alt_paths_at_coord(c, a):
                #debug_print(f"C {c}")
                #self.maze.display_path(p)
                l = self.maze.base_length - len(p)
                if l not in d:
                    d[l] = 0
                d[l] += 1
        dd = {k:d[k] for k in sorted(d.keys())}
        debug_print(f"D {dd}")
        return d
    
