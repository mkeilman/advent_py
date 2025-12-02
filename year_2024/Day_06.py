import re
import Day
from utils import mathutils
from utils import stringutils
from utils.debug import debug_print, debug_if


class DirectedPath:

    def __init__(self):
        self.elements = []


    def __eq__(self, other_path):
        return not (set([x[0] for x in self.elements]) ^ set([x[0] for x in other_path.elements]))
    

    def __len__(self):
        return len(self.elements)


    def append(self, pos, dir):
        self.elements.append((pos, dir))


    def get_loop(self):
        for c in self.elements:
            inds = stringutils.indices(c, self.elements)
            if len(inds) > 1:
                return self.elements[inds[0]:inds[1]]
        return None


    def is_loop(self):
        #return self.elements[0] == self.elements[-1]
        return len(self.elements) > len(set(self.elements))
    

    def positions(self):
        return [x[0] for x in self.elements]
    


class Room:

    WALL = "#"

    def __init__(self, grid):
        self.grid = grid
        self.size = (len(grid), len(grid[0]))


    def find_path(self, start_pos, start_dir):

        def _is_in_room(pos):
            return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]

        p = DirectedPath()
        p.append(start_pos, start_dir)
        pos = start_pos
        dir = start_dir
        d = list(Guard.DIRECTIONS.values())

        while _is_in_room(pos) and not p.is_loop():
            q = (pos[0] + dir[0], pos[1] + dir[1])
            if _is_in_room(q):
                if self.grid[q[0]][q[1]] == Room.WALL:
                    # ran into a wall, so try moving in the next direction
                    dir = d[(d.index(dir) + 1) % len(d)]
                    p.append(pos, dir)
                    continue
                p.append(q, dir)
            # do not append spaces outside the room, but do set the position
            pos = q

        return p
                    

    def print_path(self, path):
        dirs = {v: k for k, v in Guard.DIRECTIONS.items()}
        for i, r in enumerate(self.grid):
            l = ""
            e = [x[0] for x in path if x[0][0] == i]
            d = [x[1] for x in path if x[0][0] == i]
            for j, c in enumerate(r):
                l += dirs[d[e.index((i, j))]] if (i, j) in e else c
            debug_print(l)
        debug_print("")


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
            
    TEST = [
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
    
    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 6)


    def _get_guard(self, v):
        d = fr"[{'|'.join(Guard.RE_DIRS.values())}]"
        for i, r in enumerate(v):
            m = re.search(d, r)
            if m:
                return Guard((i, m.span()[0]), m[0])
        return None
    
    def count_loops(self, grid, init_path):
        
        o = []
        n_loops = 0
        e = init_path.elements
        # omit initial step
        # only need to consider steps on the original path
        for k in range(1, len(e)):
            #debug_print(f"CHECK K {k}")
            i, j = e[k][0]
            # already placed a barrier here, so thr guard could not have reached this step
            if (i, j) in o:
                continue
            o.append((i, j))

            # copy the gird
            g = grid[:]

            # place a wall here
            g[i] = g[i][:j] + Room.WALL + g[i][j + 1:]
        
            # make a room with the new wall and find a path starting at the previous step
            n_loops += Room(g).find_path(*e[k - 1]).is_loop()

        return n_loops
            

    def run(self):
        g = self._get_guard(self.input)
        r = Room(self.input)
        p = r.find_path(g.init_pos, g.init_dir)
        debug_print(f"UNIQUE PATH LEN {len(set([x[0] for x in p.elements]))} FULL LEN {len(p)}")
        n = self.count_loops(self.input, p)
        debug_print(f"NUM LOOPS {n}")

