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
        self.end = self._token_pos(Maze.END)
    

    def display_path(self, path):
        for r in self.coord_grid.coord_array:
            s = ""
            for c in r:
                s += ("X" if c in path else ".")
            debug(s)

    # note these are not necessarily "good" mazes in that they can contain islands,
    # and thus "left hand on the wall" will not work
    def path_tree(self):

        def _dir(pos1, pos2):
            return (mathutils.sign(pos2[0] - pos1[0]), mathutils.sign(pos2[1] - pos1[1]))
        
        def _dirs_taken(path):
            return [_dir(path[i - 1], path[i]) for i, _ in path[1:]]

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
        

        def _path():

            def _multi_dir_positions(dir_dict):
                return {k:v for k, v in dir_dict.items() if len(v) > 1}
            

            ctl_loops = 0
            path = [self.start]
            pos = self.start
            dir = (0, 1)
            open_dirs = {
                pos: _open_dirs(pos)
            }

            while ctl_loops < 60 and pos != self.end:
                ctl_loops += 1
                next_pos = _get_pos(pos, dir)
                if next_pos in path:
                    # we've done a loop
                    mp = _multi_dir_positions(open_dirs)
                    non_mp = {k:v for k, v in mp.items() if any([x not in path for x in v])}
                    debug(f"PATH {path} NON {non_mp}")
                    lmp = list(mp.keys())[-1]
                    nmp = list(non_mp.keys())[-1]
                    nmv = [x for x in non_mp[nmp] if x not in path][0]
                    i = path.index(nmp)
                    lmv = mp[lmp]
                    debug(f"LOOPED TO {next_pos} STEP {ctl_loops}; LAST OPEN DIRS {nmp} {nmv} STEP {i} / {len(path)} DIR TAKEN {_dir(path[i - 1], nmp)}")
                    dir = _dir(nmp, nmv)
                    next_pos = nmv
                    del path[i + 1:]
                if next_pos not in self.walls:
                    path.append(next_pos)
                    pos = next_pos
                    open_dirs[pos] = _open_dirs(pos)
                    continue
                debug(f"HIT WALL {next_pos}")
                # check +/- 90 degrees
                found_turn = False
                while path and not found_turn:
                    pos = path[-1]
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
                    debug("DEAD END")
                    # prune
                    del path[-1]
            return path          


        t = []
        path = _path()
        self.display_path(path)
        #debug(f"PATH LEN {len(path)}")
        t.append(path)
        return t


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
        debug(f"RUN STRAR {m.start} END {m.end}")
        t = m.path_tree()
        debug(f"T {t}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()