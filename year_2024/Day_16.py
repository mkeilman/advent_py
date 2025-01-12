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
    

    # note these are not necessarily "good" mazes in that they can contain islands,
    # and thus "left hand on the wall" will not work
    def path_tree(self):

        def _next_dir(direction):
            i = (Maze.DIRECTIONS.index(direction) + 1) % len(Maze.DIRECTIONS)
            return Maze.DIRECTIONS[i]
        
        def _opposite_dir(direction):
            i = (Maze.DIRECTIONS.index(direction) + 2) % len(Maze.DIRECTIONS)
            return Maze.DIRECTIONS[i]
        
        def _get_pos(curr_pos, direction):
            return (curr_pos[0] + direction[0], curr_pos[1] + direction[1])
        
        def _dir(pos1, pos2):
            return (mathutils.sign(pos2[0] - pos1[0]), mathutils.sign(pos2[1] - pos1[1]))


        def _next_pos(path, direction):
            debug(f"NEXT POS FROM {path} DIR {direction}")
            if not path:
                return None, direction
            pos = path[-1]
            p = _get_pos(pos, direction)
            if not self.coord_grid.contains(p):
                return None, direction
            debug(f"CHECK P {p}")
            if p in self.walls:
                debug(f"HIT WALL {p}")
                # check +/- 90 degrees
                d = _next_dir(direction)
                q = _get_pos(p, d)
                if q not in self.walls:
                    return _next_pos(q, d)
                d = _opposite_dir(d)
                q = _get_pos(p, d)
                if q not in self.walls:
                    return _next_pos(q, d)
                debug("DEAD END")
                # prune
                del path[-1]
                return _next_pos(path, d)

                        
                direction = d
            return p, direction

        def _path():
            
            ctl_loops = 0
            path = [self.start]
            pos = self.start
            dir = (0, 1)
            
            while ctl_loops < 20 and pos != self.end:
                ctl_loops += 1
                next_pos = _get_pos(pos, dir)
                if pos in path:
                    # we've done a loop
                    i = path.index(pos)
                    old_dir = _dir(pos, path[i + 1])
                    debug(f"LOOPED TO {pos}; change direction {old_dir}")
                    pass
                if next_pos not in self.walls:
                    path.append(next_pos)
                    pos = next_pos
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
        has_more_paths = True
        last_good_pos = self.start
        last_dir = (0, 1)
        path = _path()
        #while has_more_paths:
        #for i in range(10):
        #    path_done = False
        #    path = [last_good_pos]
        #    d = last_dir
        #    #while not path_done:
        #    for j in range(10):
        #        p, d = _next_pos(path, d)
        #        if not p:
        #            break
        ###        path.append(p)
        ##        path_done = p == self.end
        #    t.append(path)
        #    has_more_paths = False

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