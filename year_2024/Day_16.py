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
        self.start_dir = (0, 1)
        self.end = self._token_pos(Maze.END)
        self.connections = {k:[x for x in v if x not in self.walls] for k, v in self.coord_grid.coord_neighborhoods.items()}
    
    def display_path(self, path):
        #debug(path)
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
                    #debug(f"{path[i - 1]} -> {c}")
                    d =  self._dir(path[i - 1], c)
                    if d in Maze.DIR_SYMBOLS:
                        s +=  Maze.DIR_SYMBOLS[d]
                    else:
                        s += "*"
            debug(s)
        debug("")

    def score(self, path):
        s = len(path) - 1
        dirs = [self._dir(path[i - 1], path[i]) for i in range(1, len(path))]
        d0 = self.start_dir
        for i, d in enumerate(dirs):
            if d != d0:
                s += 1000
                d0 = d
        return s
    
    def _t(self):

        def _exclude(pos, connection, exclusions):
            #debug(f"EXCLUDE {connection} FROM {pos}")
            if not exclusions.get(pos):
                exclusions[pos] = []
            exclusions[pos].append(connection)
        
        def _conn(pos, path, exclusions={}, unused={}):
            return [x for x in self.connections[pos] if x != path[path.index(pos) - 1] and x not in path and x not in exclusions.get(pos, [])]

        def _pp(start_pos, end_pos, unused={}):
            import time

            pos = start_pos
            pp = [start_pos]
            done = False
            n_loops = 0
            while not done and pos != end_pos:
                # loop through the connections to this position, not counting the preivous position and excluded positions
                p_con = _conn(pos, pp, exclusions=exclusions)
                #debug(f"CONNECTIONS {pos}: {p_con}")
                for p in p_con:
                    #TODO: multiple paths
                    #debug(f"CHECK {pos} -> {p}")
                    #if p in pp:
                    #    debug(f"LOOP: {pos} -> {p}")
                    #    q = _trim_to_prev_branch(pp, exclusions)
                    #    done = not q
                    #    if not q:
                    #        break
                    #    pos = q
                    #    continue
                    pp.append(p)
                    pos = p
                    #debug(f"ADDED {p}")
                    break
                else:
                    #debug(f"NO ROUTE FROM {pos}")
                    pos = _trim_to_prev_branch(pp, exclusions)
                    done = not pos
                n_loops += 1
            #else:
            
            #debug(f"DONE! IN {n_loops} {pos} EX {exclusions.get(pos)} CONN {self.connections[pos]}")
            debug(f"DONE! IN {n_loops}")
            #debug(f"LEFTOVER BRANCHES { {k:v for k, v in self.connections.items() if not exclusions.get(k, [])} }")
            #if pos != self.end:
            #    pp = []
            self.display_path(pp)
            return pp
            #return pp

        def _prev_branch(path, exclusions={}):
            i = -1
            q = path[i]
            c = _conn(q, path, exclusions=exclusions)
            while not len(c):
                if i == -len(path):
                    return None
                i -= 1
                q = path[i]
                c = _conn(q, path, exclusions=exclusions)
            return q
        

        def _trim(arr, n):
            for _ in range(n):
                arr.pop()

        def _trim_to_pos(pos, path, exlcusions):
            n = len(path) - path.index(pos) - 1
            for i in range(n):
                # exclude intervening postions if they have no valid connections
                _exclude(path[-i - 2], path[-i - 1], exlcusions)
            _trim(path, n)


        def _trim_to_prev_branch(path, exclusions):
            q = _prev_branch(path, exclusions=exclusions)
            if q:
                _trim_to_pos(q, path, exclusions)
            return q


        exclusions = {}
        r = _pp(self.start, self.end)
        u = self._unused_branches(r, exclusions)
        #debug(f"UNUSED {u}")
        #r2 = _pp(self.start, self.end)
        return r

    def _unused_branches(self, path, exclusions):
        u = {}
        for p in path:
            for q in self.connections[p]:
                if q not in path and not exclusions.get(q):
                    if not u.get(p):
                        u[p] = []
                    u[p].append(q)
        return u


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
        
        def _open_dirs(pos, path=[]):
            dirs = []
            for d in Maze.DIRECTIONS:
                q = _get_pos(pos, d)
                if q not in self.walls and q not in path:
                    dirs.append(q)
            return dirs

        def _opposite_dir(direction):
            i = (Maze.DIRECTIONS.index(direction) + 2) % len(Maze.DIRECTIONS)
            return Maze.DIRECTIONS[i]
        

        def _path(initial_path=None, initial_choices=None, max_score=1e23):

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
            
            def _prev_branch(path, dir_dict):
                p, q = _most_recent_multi(path, dir_dict)
                if p is None or q is None:
                    return None, None, None
                _prune(path, dir_dict, path.index(p))
                return p, q, _dir(p, q)


            def _prune(path, dir_dict, index):
                for od in path[index + 1:]:
                    for k in dir_dict:
                        v = dir_dict[k]
                        if od in v:
                            del v[v.index(od)]
                    del dir_dict[od]
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

            open_dirs = initial_choices or {pos: _open_dirs(pos)}

            while pos != self.end:
                ctl_loops += 1
                if self.score(path) > max_score:
                    pos, q, dir = _prev_branch(path, open_dirs)
                    if pos is None:
                        return [], {}
                next_pos = _get_pos(pos, dir)
                #debug(f"POS {pos} DIR {dir} NEXT {next_pos}")
                if next_pos in path:
                    # we've done a loop
                    p, next_pos, dir = _prev_branch(path, open_dirs)
                    if p is None:
                        return [], {}
                if next_pos not in self.walls:
                    path.append(next_pos)
                    pos = next_pos
                    open_dirs[pos] = _open_dirs(pos, path=path)
                    continue
                #debug(f"HIT WALL {next_pos}")
                # check +/- 90 degrees
                found_turn = False
                while path and not found_turn:
                    pos = path[-1]
                    for d in (_next_dir(dir), _opposite_dir(_next_dir(dir))):
                        q = _get_pos(pos, d)
                        if q not in self.walls:
                            path.append(q)
                            pos = q
                            open_dirs[pos] = _open_dirs(pos, path=path)
                            dir = d
                            found_turn = True
                            break
                    if found_turn:
                        continue
                    pos, q, dir = _prev_branch(path, open_dirs)
                    if pos is None:
                        return [], {}
                    break
            u = {k:[x for x in v if x not in path] for k, v in  _unexplored(path, open_dirs).items()}
            return path, u


        def _paths(initial_path=None, initial_choices=None, depth=0, max_score=1e23):
            paths = []
            path, choices = _path(initial_path=initial_path, initial_choices=initial_choices, max_score=max_score)
            if not path:
                debug(f"DONE EMPTY")
                return paths
            s = self.score(path)
            max_score = min(max_score, s)
            debug(f"{depth} NEW PATH SCORE {s} MIN {max_score}")
            paths.append(path)
            for p in choices:
                q2 = choices[p].pop(0)
                p2 = path[:path.index(p) + 1] + [q2]
                if (p, q2) in empty_choices:
                    debug(f"{depth} THIS START EMPTY {p} -> {q2}")
                    continue
                #debug(f"{depth} TRY NEW PATH START {p} -> {q2}")
                keys = list(choices.keys())
                # omit choices past the given branch point
                new_choices = {k:v for k, v in choices.items() if v and keys.index(k) <= keys.index(p)}
                cp = _paths(initial_path=p2, initial_choices=new_choices, depth=depth + 1, max_score=max_score)
                if not cp:
                    debug(f"{depth} CHOICE EMPTY")
                    empty_choices.append((p, q2))
                for q in cp:
                    s = self.score(q)
                    max_score = min(max_score, s)
                    debug(f"{depth} NEW PATH SCORE {s} MIN {max_score}")
                    paths.append(q)
            debug(f"{depth} DONE")
            return paths
                
        empty_choices = []
        return _paths()


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

    TWO_PATHS = [
        "###############",
        "#..#...#...#..#",
        "#....#...#...E#",
        "#.###########.#",
        "#S............#",
        "###############",
    ]

    LOOP = [
        "###############",
        "#............E#",
        "###############",
        "#......#......#",
        "#S............#",
        "###############",
    ]

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
            AdventDay.LOOP
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
        debug(f"RUN START {m.start} END {m.end}")
        t = m._t()
        #m.display_path(t)
        #debug(f"T {t}")
        #t = m.path_tree()
        #min_score = min([m.score(x) for x in t])
        #debug(f"NUM PATHS {len(t)} MIN SCORE {min_score}")
        #p = [x for x in t if m.score(x) == min_score][0]
        #m.display_path(p)
        #debug(f"MIN PATH LEN {len(p)}")




def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()