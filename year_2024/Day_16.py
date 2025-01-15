import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Maze:

    DIRECTIONS = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]

    START = "S"
    END = "E"

    WALL = "#"

    def __init__(self, grid):
        self.grid = grid
        self.coord_grid = Day.Grid.grid_of_size(len(self.grid), len(self.grid[0]))
        self.walls = self._walls()
        self.start = self._token_pos(Maze.START)
        self.start_dir = (0, 1)
        self.end = self._token_pos(Maze.END)
        self.pos_with_choices = {}
        self.min_path_score = 1e23
    

    def display_path(self, path):
        for r in self.coord_grid.coord_array:
            s = ""
            for c in r:
                s += ("X" if c in path else ".")
            debug(s)

    def score(self, path):
        s = len(path) - 1
        dirs = [self._dir(path[i - 1], path[i]) for i in range(1, len(path))]
        d0 = self.start_dir
        for i, d in enumerate(dirs):
            if d != d0:
                #debug(f"CHANGE DIR {d0} -> {d} AT {i}")
                s += 1000
                d0 = d
        #debug(f"DIRS {dirs}")
        return s
    

    # note these are not necessarily "good" mazes in that they can contain islands,
    # and thus "left hand on the wall" will not work
    def path_tree(self):

        def _dir(pos1, pos2):
            return self._dir(pos1, pos2)

        def _get_pos(curr_pos, direction):
            return (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
        
        def _next_dir(direction):
            i = (Maze.DIRECTIONS.index(direction) + 1) % len(Maze.DIRECTIONS)
            return Maze.DIRECTIONS[i]
        
        def _open_dirs(pos):
            dirs = []
            for d in Maze.DIRECTIONS:
                q = _get_pos(pos, d)
                if q not in self.walls:
                    dirs.append(q)
            return dirs

        def _opposite_dir(direction):
            i = (Maze.DIRECTIONS.index(direction) + 2) % len(Maze.DIRECTIONS)
            return Maze.DIRECTIONS[i]
        

        def _path(initial_path=None, initial_choices=None):

            def _unexplored(path, open_directions):
                return {k:v for k, v in _multi_dir_positions(open_directions).items() if any([x not in path for x in v])}

            def _most_recent_multi(path, open_directions):
                unexplored = _unexplored(path, open_directions)
                if not unexplored:
                    return None, None
                base_pos = list(unexplored.keys())[-1]
                up = [x for x in unexplored[base_pos] if x not in path]
                unex_pos = up[0]
                return base_pos, unex_pos

            def _multi_dir_positions(dir_dict):
                return {k:v for k, v in dir_dict.items() if len(v) > 1}
            
            def _prune(path, open_directions, index):
                for od in path[index + 1:]:
                    for k in open_directions:
                        v = open_directions[k]
                        if od in v:
                            del v[v.index(od)]
                    del open_directions[od]
                del path[index + 1:]

            ctl_loops = 0
            path = initial_path or [self.start]
            pos = path[-1]

            if initial_path:
                if len(initial_path) < 2:
                    dir = self._dir(self.start_dir, initial_path[0])
                else:
                    dir = self._dir(initial_path[-2], initial_path[-1])
            else:
                dir = self.start_dir

            #debug(f"INIT PATH {initial_path} INIT DIR {dir}")

            open_dirs = initial_choices or {pos: _open_dirs(pos)}

            while pos != self.end:
                ctl_loops += 1
                next_pos = _get_pos(pos, dir)
                #debug(f"POS {pos} DIR {dir} NEXT {next_pos}")
                if next_pos in path:
                    # we've done a loop
                    #self.display_path(path)
                    #debug(f"LOOPED TO {next_pos}")
                    p, q = _most_recent_multi(path, open_dirs)
                    if p is None or q is None:
                        return [], {}
                    #debug(f"MRM {p} -> {q}")
                    dir = _dir(p, q)
                    next_pos = q
                    _prune(path, open_dirs, path.index(p))
                if next_pos not in self.walls:
                    path.append(next_pos)
                    pos = next_pos
                    open_dirs[pos] = _open_dirs(pos)
                    continue
                #debug(f"HIT WALL {next_pos}")
                # check +/- 90 degrees
                found_turn = False
                while path and not found_turn:
                    pos = path[-1]
                    #debug(f"TURNS FOR {pos} {open_dirs[pos]}")
                    for d in (_next_dir(dir), _opposite_dir(_next_dir(dir))):
                        q = _get_pos(pos, d)
                        if q not in self.walls:
                            path.append(q)
                            pos = q
                            open_dirs[pos] = _open_dirs(pos)
                            dir = d
                            found_turn = True
                            break
                    if found_turn:
                        continue
                    #debug(f"DEAD END {pos} BACK TO? {_most_recent_multi(path, open_dirs)}")
                    pos, q = _most_recent_multi(path, open_dirs)
                    if pos is None or q is None:
                        return [], {}
                    dir = _dir(pos, q)
                    _prune(path, open_dirs, path.index(pos))
                    break
            u = {k:[x for x in v if x not in path] for k, v in  _unexplored(path, open_dirs).items()}
            #debug(f"MDIRS {u}")
            return path, u


        def _paths(initial_path=None, initial_choices=None):
            paths = []
            # first path
            path, choices = _path(initial_path=initial_path, initial_choices=initial_choices)
            if not path:
                return paths
            paths.append(path)
            for p in choices:
                debug(f"TRY NEW PATH START {p} -> {choices[p][0]}")
                i = path.index(p)
                p2 = path[:i + 1] + [choices[p][0]]
                del choices[p][0]
                new_choices = {}
                # omit choices past the given branch point
                for k in choices.keys():
                    new_choices[k] = choices[k]
                    if k == p:
                        break
                for p in _paths(initial_path=p2, initial_choices=new_choices):
                    if p and p not in paths:
                        paths.append(p)
            return paths
                

        t = []
        #path, choices = _path()
        t = _paths()
        #self.display_path(path)
        #debug(f"PATH LEN {len(path)} SCORE {self.score(path)}")
        #t.append(path)
        #for p in choices:
        #    debug(f"TRY NEW PATH START {p} -> {choices[p][0]}")
        #    i = path.index(p)
        #    p2 = path[:i + 1] + [choices[p][0]]
        #    del choices[p][0]
        #    new_choices = {}
        #    # omit choices past the given branch point
        #    for k in choices.keys():
        #        new_choices[k] = choices[k]
        #        if k == p:
        #            break
        #        
        #    np, c = _path(initial_path=p2, initial_choices=new_choices)
        #    #debug(f"NEW PATH {np} CH {c} LEN {len(np)} SCORE {self.score(np)}")
        #    if np:
        #        #self.display_path(np)
        #        debug(f"NEW PATH LEN {len(np)} SCORE {self.score(np)}")
        #        t.append(np)
        return t


    def _dir(self, pos1, pos2):
        return (mathutils.sign(pos2[0] - pos1[0]), mathutils.sign(pos2[1] - pos1[1]))
    
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


class Reindeer:

    def __init__(self, init_pos=(0, 0), init_direction=(0, 1)):
        pass


class AdventDay(Day.Base):


    TEST = [
        "###############",
        "#.......#....E#",
        "#.#.###.#.###.#",
        "#.....#.#...#.#",
        "#.###.#####.#.#",
        "#.#.#.......#.#",
        "#.#.#####.###.#",
        "#...........#.#",
        "###.#.#####.#.#",
        "#...#.....#.#.#",
        "#.#.#.###.#.#.#",
        "#.....#...#.#.#",
        "#.###.#.#.#.#.#",
        "#S..#.....#...#",
        "###############",
    ]

    TEST_LARGE = [
        "#################",
        "#...#...#...#..E#",
        "#.#.#.#.#.#.#.#.#",
        "#.#.#.#...#...#.#",
        "#.#.#.#.###.#.#.#",
        "#...#.#.#.....#.#",
        "#.#.#.#.#.#####.#",
        "#.#...#.#.#.....#",
        "#.#.#####.#.###.#",
        "#.#.#.......#...#",
        "#.#.###.#####.###",
        "#.#.#...#.....#.#",
        "#.#.#.#####.###.#",
        "#.#.#.........#.#",
        "#.#.#.#########.#",
        "#S#.............#",
        "#################",
    ]

    IMPOSSIBLE = [
        "###############",
        "#.......#....E#",
        "#####.#.#.#.###",
        "#S..#.....#...#",
        "###############",
    ]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            16,
            AdventDay.TEST
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
        m = Maze(v)
        r = Reindeer(m.start)
        debug(f"RUN START {m.start} END {m.end}")
        t = m.path_tree()
        debug(f"NUM PATHS {len(t)} MIN SCORE {min([m.score(x) for x in t])}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()