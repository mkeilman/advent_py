import re
import Day
from utils import math
from utils import string
from utils.debug import debug

class Room:

    @classmethod
    def is_loop(cls, arr):
        return len(arr) > len(set(arr))

    def __init__(self, grid):
        self.grid = grid
        self.size = (len(grid), len(grid[0]))


    def find_path(self, start_pos, start_dir):

        def _is_in_room(pos):
            return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]

        p = [(start_pos, start_dir)]
        pos = start_pos
        dir = start_dir
        d = list(Guard.DIRECTIONS.values())

        while _is_in_room(pos) and not Room.is_loop(p):
            q = (pos[0] + dir[0], pos[1] + dir[1])
            if _is_in_room(q):
                if self.grid[q[0]][q[1]] == "#":
                    dir = d[(d.index(dir) + 1) % len(d)]
                    p.append((pos, dir))
                    continue
                p.append((q, dir))
            # do not append spaces outside the room, but do set the position
            pos = q

        return p


class Guard:

    DIRECTIONS = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }

    RE_DIRS = {
        "^": r"\^",
        ">": r">",
        "v": r"v",
        "<": r"<",
    }

    def __init__(self, position, direction):
        self.position = position
        self.init_pos = self.position
        self.direction = Guard.DIRECTIONS[direction]
        self.init_dir = self.direction

    def _reset(self):
        self.position = self.init_pos
        self.direction = self.init_dir


class AdventDay(Day.Base):
            

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            6,
            [
                "....#.....",
                ".........#",
                "..........",
                "..#.......",
                ".......#..",
                "..........",
                ".#..^.....",
                "........#.",
                "#.........",
                "......#...",
            ]
        )

    def _get_guard(self, v):
        d = fr"[{'|'.join(Guard.RE_DIRS.values())}]"
        for i, r in enumerate(v):
            m = re.search(d, r)
            if m:
                return Guard((i, m.span()[0]), m[0])
        return None
    
    def count_loops(self, grid, init_path, pos, dir):
    #def count_loops(self, grid, init_row, init_col, pos, dir):
        
        o = []
        # do not include starting space
        # only need to consider spaces on the original path?
        #for space in set([x[0] for x in init_path[1:]]):
        for k in range(1, len(init_path)):
            space = init_path[k]
            prev_space = init_path[k - 1]
            i = space[0][0]
            j = space[0][1]
            if (i, j) in o:
                continue
            #if grid[i][j] == "#":
            #    continue
            #debug(f"{i} {j} CHECK LOOP")
            g = grid[:]
            g[i] = g[i][:j] + "#" + g[i][j + 1:]
            #p = Room(g).find_path(pos, dir)
            # start at the previous space
            p = Room(g).find_path(prev_space[0], prev_space[1])
            if Room.is_loop(p):
                debug(f"{k} {i} {j}")
                o.append((i, j))

        #for i in range(len(grid)):
        #    for j in range(len(grid[0])):
        #        if i == init_row and j == init_col:
        #            continue
        #        g = grid[:]
        #        if g[i][j] == "#":
        #            continue
        #        #debug(f"{i} {j} CHECK LOOP")
        #        g[i] = g[i][:j] + "#" + g[i][j + 1:]
        #        p = Room(g).find_path(pos, dir)
        #        if Room.is_loop(p):
        #            debug(f"{i} {j} LOOP FOUND")
        #            n += 1

        return len(o)
            

    def run(self, v):
        g = self._get_guard(v)
        r = Room(v)
        #debug(f"G POS {g.position} DIR {g.direction}")
        p = r.find_path(g.init_pos, g.init_dir)
        debug(f"UNIQUE PATH LEN {len(set([x[0] for x in p]))} FULL LEN {len(p)}")
        n = self.count_loops(v, p, g.init_pos, g.init_dir)
        #n = self.count_loops(v, p[0][0], p[0][1], g.init_pos, g.init_dir)
        debug(f"NUM LOOPS {n}")


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
