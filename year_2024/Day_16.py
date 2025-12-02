import math
import re
import Day
from utils import mathutils
from utils import stringutils
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

    MAX_SCORE = 1e23

    def __init__(self, grid):
        self.grid = grid
        self.coord_grid = Day.Grid.grid_of_size(len(self.grid), len(self.grid[0]))
        self.walls = self._walls()
        self.start = self._token_pos(Maze.START)
        self.start_dir = (0, 1)
        self.end = self._token_pos(Maze.END)
        self.connections = {k:[x for x in v if x not in self.walls] for k, v in self.coord_grid.coord_neighborhoods.items()}
        self.min_score = Maze.MAX_SCORE
    
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
            if not exclusions.get(pos):
                exclusions[pos] = []
            exclusions[pos].append(connection)
        
        def _conn(pos, path, exclusions={}, unused={}):
            return [x for x in self.connections[pos] if x != path[path.index(pos) - 1] and x not in path and x not in exclusions.get(pos, [])]

        def _path(initial_path, end_pos, exclusions={}):
            pos0 = initial_path[-1]
            #debug_print(f"P0 {pos0} X {exclusions}")
            #debug_print(f"P0 {pos0} SC {self.score(initial_path)} MAX {max_score}")
            #if self.score(initial_path) > max_score:
            #    debug_print(f"INIT PATH SCORE {self.score(initial_path)} TOO BIG {max_score}")
            #    return [], None, Maze.MAX_SCORE
            pos = pos0
            pp = initial_path
            done = False
            n_loops = 0
            unused = {}
            score = self.min_score
            while not done and pos != end_pos:
                # loop through the connections to this position, not counting
                # the preivous position and excluded positions
                p_con = _conn(pos, pp, exclusions=exclusions)
                #debug_print(f"CONNECTIONS {pos}: {p_con}")
                for p in p_con:
                    pp.append(p)
                    score = self.score(pp)
                    #if score > self.min_score:
                    #    continue
                    u = [x for x in p_con if x != p]
                    if u:
                        unused[pos] = u
                    pos = p
                    #debug_print(f"ADDED {p}")
                    break
                else:
                    #debug_print(f"NO BRANCH {pos}")
                    pos = _trim_to_prev_branch(pp, exclusions, limit=pos0)
                    done = not pos
                n_loops += 1
            #else:
            
            #debug_print(f"DONE! IN {n_loops} POS {pos} END {end_pos}")
            if pos != end_pos:
                return [], None, Maze.MAX_SCORE
            self.display_path(pp)
            return pp, unused, score

        def _prev_branch(path, exclusions={}, limit=None):
            i = -1
            q = path[i]
            c = _conn(q, path, exclusions=exclusions)
            while not len(c):
                if i == -len(path):
                    return None
                i -= 1
                q = path[i]
                if limit and q == limit and q != path[0]:
                    return None
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


        def _trim_to_prev_branch(path, exclusions, limit=None):
            q = _prev_branch(path, exclusions=exclusions, limit=limit)
            if q:
                _trim_to_pos(q, path, exclusions)
            return q


        def _amend_paths(base_path, unused_connections, depth=0, all_paths=[]):
            #a_paths = []
            self.min_score = min(self.min_score, min([x[2] for x in all_paths]))
            #s = max_score
            n = 0
            for pos in [x for x in unused_connections if x in base_path]:
                i = base_path.index(pos)
                initial_path = base_path[:i + 1]
                #if self.score(initial_path) > s:
                #    debug_print(f"{depth} INIT PATH SCORE {self.score(initial_path)} TOO BIG {s}")
                #    continue
                new_path, u, score = _path(initial_path, self.end, exclusions={pos: [base_path[i + 1]]})
                #self.display_path(new_path)
                n += 1
                debug_print(f"{depth} {n} NP {len(new_path)} SC {score}")
                if not new_path or not u:
                    continue
                if score < self.min_score:
                    debug_print(f"{depth} SCORE {score} PREV MAX {self.min_score} CHECK UNUSED {len(u)}")
                self.min_score = min(score, self.min_score)
                if new_path not in [x[0] for x in all_paths]:
                    all_paths.append((new_path, u, score))
                    #all_paths.extend(_amended_paths(new_path, u, depth=depth + 1, max_score=s, all_paths=all_paths))
                    _amend_paths(new_path, u, depth=depth + 1, all_paths=all_paths)
            #ap = []
            #for p, u in a_paths:
            #    ap.extend(_amended_paths(p, u, depth=depth + 1, max_score=s))
            #a_paths += ap
            debug_print(f"{depth} FOUND {len(all_paths)}")
            return
            #return all_paths

        def _diff(p1, p2):
            return [(i, x) for i, x in enumerate(p1) if x != p2[i]]

        self.bp = None
        paths = []
        pus = _path([self.start], self.end)
        debug_print(f"FIRST {pus[2]}")
        paths.append(pus)
        self.min_score = pus[2]
        _amend_paths(pus[0], pus[1], all_paths=paths)
        #paths.extend([x[0] for x in ap])


        #done = False
        #n = 0
        #while not done:
        #    n += 1
        #    for p, u in ap:
        #        np = _amended_paths(p, u, max_score=self.score(path))
        #    done = n > 0
        #paths.extend(_amended_paths(path, unused, max_score=self.score(path)))
        return [x[0] for x in paths]
        #return paths


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
        

        def _path(initial_path=None, initial_choices=None, max_score=Maze.MAX_SCORE):

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
                #debug_print(f"POS {pos} DIR {dir} NEXT {next_pos}")
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
                #debug_print(f"HIT WALL {next_pos}")
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


        def _paths(initial_path=None, initial_choices=None, depth=0, max_score=Maze.MAX_SCORE):
            paths = []
            path, choices = _path(initial_path=initial_path, initial_choices=initial_choices, max_score=max_score)
            if not path:
                debug_print(f"DONE EMPTY")
                return paths
            s = self.score(path)
            max_score = min(max_score, s)
            debug_print(f"{depth} NEW PATH SCORE {s} MIN {max_score}")
            paths.append(path)
            for p in choices:
                q2 = choices[p].pop(0)
                p2 = path[:path.index(p) + 1] + [q2]
                if (p, q2) in empty_choices:
                    debug_print(f"{depth} THIS START EMPTY {p} -> {q2}")
                    continue
                #debug_print(f"{depth} TRY NEW PATH START {p} -> {q2}")
                keys = list(choices.keys())
                # omit choices past the given branch point
                new_choices = {k:v for k, v in choices.items() if v and keys.index(k) <= keys.index(p)}
                cp = _paths(initial_path=p2, initial_choices=new_choices, depth=depth + 1, max_score=max_score)
                if not cp:
                    debug_print(f"{depth} CHOICE EMPTY")
                    empty_choices.append((p, q2))
                for q in cp:
                    s = self.score(q)
                    max_score = min(max_score, s)
                    debug_print(f"{depth} NEW PATH SCORE {s} MIN {max_score}")
                    paths.append(q)
            debug_print(f"{depth} DONE")
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
            for j in stringutils.indices(Maze.WALL, r):
                w.append((i, j))
        return w


class Reindeer:

    def __init__(self, init_pos=(0, 0), init_direction=(0, 1)):
        pass


class AdventDay(Day.Base):
    IMPOSSIBLE = [
        "###############",
        "#.......#....E#",
        "#####.#.#.#.###",
        "#S..#.....#...#",
        "###############",
    ]

    OPEN = [
        "######",
        "#...E#",
        "#....#",
        "#S...#",
        "######",
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

    TWO_PATHS = [
        "###############",
        "#..#...#...#..#",
        "#....#...#...E#",
        "#.###########.#",
        "#S............#",
        "###############",
    ]

    TWO_EQUAL_PATHS = [
        "####################",
        "#E......#.#.......##",
        "#######.#.##########",
        "#...#...#.......#.##",
        "#.#.#.#.#.#####.#.##",
        "#.#.#.#.......#...##",
        "#.#.#.#.#.#.#####.##",
        "#.#.#.....#.......##",
        "#.#.###.#.#.########",
        "#.#.....#.#.....#.##",
        "#S#####.#.#.###.#.##",
        "####################",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 16)
        self.args_parser.add_argument(
            "--warehouse-size",
            type=str,
            help="single or double size",
            choices=["single", "double"],
            default="single",
            dest="warehouse_size",
        )
        self.add_args(run_args)
       

    def run(self):
        #self.input = AdventDay.TEST_LARGE
        m = Maze(self.input)
        debug_print(f"RUN START {m.start} END {m.end}")
        t = m._t()
        #m.display_path(t)
        #debug_print(f"T {t}")
        #t = m.path_tree()
        min_score = min([m.score(x) for x in t])
        debug_print(f"NUM PATHS {len(t)} MIN SCORE {min_score}")
        #p = [x for x in t if m.score(x) == min_score][0]
        #m.display_path(p)
        #debug_print(f"MIN PATH LEN {len(p)}")
