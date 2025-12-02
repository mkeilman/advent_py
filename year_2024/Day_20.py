import math
import re
import Day
from utils import mathutils
from utils import stringutils
from utils.debug import debug_print, debug_if


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
        self.start = self._token_pos(Maze.START)
        self.end = self._token_pos(Maze.END)
        self.connections = {k:[x for x in v if x not in self.walls] for k, v in self.coord_grid.coord_neighborhoods.items()}
        self.base_path = self.path()
        self.base_length = len(self.base_path) - 1
    

    def display_path(self, path, show_directions=False, show_walls=False, decorations=None):
        def _path_char(c):
            se = _start_end_char(c)
            if se:
                return se
            
            i = path.index(c)
            if not show_directions:
                return "x"
            return Maze.DIR_SYMBOLS.get(self._dir(path[i - 1], c), "*")
                
            
        def _start_end_char(c):
            if c == self.start:
                return Maze.START
            if c == self.end:
                return Maze.END
            return ""

        for r in self.coord_grid.coord_array:
            s = ""
            for c in r:
                if decorations and c in decorations:
                    s += decorations.get(c, "-")
                    continue
                if c in path:
                    s += _path_char(c)
                    continue

                if show_walls and c in self.walls:
                    s += Maze.WALL
                    continue
                se = _start_end_char(c)
                s += (se if se else ".")
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
        debug_print(f"FOUND BASE PATH LEN {len(path)}")
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
            for j in stringutils.indices(Maze.WALL, r):
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
        self.args_parser.add_argument(
            "--use-exact-difference",
            action=argparse.BooleanOptionalAction,
            help="treat minimum difference as exact",
            default=False,
            dest="use_exact_difference",
        )
        self.add_args(run_args)
       

    def num_min_diffs(self):
        import operator
        n = 0
        op = operator.eq if self.use_exact_difference else operator.ge
        for i in range(2, self.cheat_duration + 1):
            #debug_print(f"CHEAT DUR {i}")
            d = self._path_diffs(i)
            n += mathutils.sum([v for k, v in d.items() if op(k, self.min_difference)])
        return n
        

    def run(self):
        self.maze = Maze(self.input)
        #self.maze.display_path(self.maze.base_path)
        n = self.num_min_diffs()
        debug_print(f"CHEAT DUR {self.cheat_duration} MIN DIFF {self.min_difference} N : {n}")
        return n


    def _alt_paths(self, duration):

        alts = {}

        m = self.maze
        for coord in m.base_path:
            alts[coord] = {}
            #for c in [x for x in m.coord_grid.neighborhood(coord) if x in m.walls]:
            #    n = [x for x in m.coord_grid.neighborhood(c) if x in m.base_path and m.base_path.index(x) > m.base_path.index(coord)]
            #    if n:
            #        alts[coord][c] = n
        #return alts
            # start "cheat" in an adjacent wall
            for c in [x for x in m.coord_grid.neighborhood(coord) if x in m.interior_walls]:
                cc = [x for x in m.coord_grid.circle(c, duration - 1) if x in m.base_path and m.base_path.index(x) > m.base_path.index(coord)]
                #m.display_path(cc, decorations={c: "+"})
                n = [m.coord_grid.ell(c, x, direction=1) for x in cc] + [m.coord_grid.ell(c, x, direction=-1) for x in cc]
                if n:
                    alts[coord][c] = n
        debug_print(f"GOT ALT PATHS FOR DUR {duration}")
        return alts


    def _path_diff(self, path):
        return self.maze.base_length - (len(path) - 1)
    

    def _path_diffs(self, duration):
        def _alt_paths_at_coord(coord, alt_paths):
            if coord not in alt_paths:
                return None
            
            m = self.maze
            paths = []
            p = m.base_path[:m.base_path.index(coord) + 1]
            ends = []
            for start in alt_paths[coord]:
                #for end in alt_paths[coord][start]:
                #debug_print(f"COORD {coord} WALL {start}")
                for pp in alt_paths[coord][start]:
                    end = pp[-1]
                    # cheats with the same start and end coords are considered identical
                    if end in ends:
                        continue
                    alt = p + pp + m.base_path[m.base_path.index(end) + 1:]
                    # prevent backtracking
                    if len(alt) != len(set(alt)):
                        continue
                    # ignore paths that are too long
                    if self._path_diff(alt) < self.min_difference:
                        continue
                    ends.append(end)
                    disp = self._path_diff(alt) == self.min_difference
                    debug_if(f"COORD {coord} WALL {start} NEXT PATH {end} IND {m.base_path.index(end)} P {p} PP {pp} LAST {m.base_path[m.base_path.index(end):]} FULL LEN {alt}", condition=disp)
                    if disp:
                        m.display_path(alt, show_walls=True, decorations={start: "@", end: "%"})
                    #m.display_path(p + [start] + [end])
                    #paths.append(p + [start] + pp + m.base_path[m.base_path.index(pp[-1]):])
                    #debug_print(f"START {start} END {end} LINE {m.coord_grid.line(start, end, allow_diags=False)}")
                    #paths.append(p + m.coord_grid.line(start, end, allow_diags=False) + m.base_path[m.base_path.index(end):])
                    paths.append(alt)
            return paths
    
        d = {}
        a = self._alt_paths(duration)
        for c in a:
            for p in _alt_paths_at_coord(c, a):
                #debug_print(f"C {c}")
                #self.maze.display_path(p)
                l = self._path_diff(p)
                if l not in d:
                    d[l] = 0
                d[l] += 1
        dd = {k:d[k] for k in sorted(d.keys())}
        #debug_print(f"D {dd}")
        #debug_if(f"D {dd}", condition=any([x == self.min_difference for x in dd.keys()]))
        return d
    
