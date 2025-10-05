import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print, debug_if

class Room:

    WALL = "#"

    #@classmethod
    #def is_loop(cls, arr):
    #    return len(arr) > len(set(arr))

    def __init__(self, grid):
        self.grid = grid
        self.size = (len(grid), len(grid[0]))


    # a path is an array (position, direction)
    def find_path(self, start_pos, start_dir):

        def _is_in_room(pos):
            return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]

        def _sub_string(pos, dir):
            if dir[0] == 0:
                s = self.grid[pos[0]][::dir[1]]
            elif dir[1] == 0:
                s = [x[pos[1]] for x in self.grid][::dir[0]]
            else:
                return ""

            if dir[1] > 0:
                try:
                    j = s.index(Room.WALL, pos[0])
                except  ValueError:
                    j = len(self.grid[0])
                return s[pos[1]:j + 1]
            #if dir[1] < 0:
            #    try:
            #        j = s.index(Room.WALL, pos[0])
            #    except  ValueError:
            #        j = 0
            #    return s[pos[1]:j + 1]
                
            return "X"

        p = [(start_pos, start_dir)]
        pos = start_pos
        dir = start_dir
        d = list(Guard.DIRECTIONS.values())

        while _is_in_room(pos) and not self.is_loop(p):
            #debug_print(f"CHECK STR {_sub_string(pos, dir)}")
            q = (pos[0] + dir[0], pos[1] + dir[1])
            if _is_in_room(q):
                if self.grid[q[0]][q[1]] == Room.WALL:
                    # ran into a wall, so try moving in the next direction
                    dir = d[(d.index(dir) + 1) % len(d)]
                    p.append((pos, dir))
                    continue
                p.append((q, dir))
            # do not append spaces outside the room, but do set the position
            pos = q

        return p

    def get_loop(self, arr):
        for c in arr:
            inds = string.indices(c, arr)
            if len(inds) > 1:
                return arr[inds[0]:inds[1]]
        return None
    

    def is_loop(self, arr):
        #if arr[0] == arr[-1]:
        #    debug_print(f"ARR0 {arr[0]} VS ARRN {arr[-1]} LENS? {len(arr) > len(set(arr))}")
        return len(arr) > len(set(arr))
    

    def print_path(self, path):
        dirs = {v: k for k, v in Guard.DIRECTIONS.items()}
        for i, r in enumerate(self.grid):
            l = ""
            e = [x[0] for x in path if x[0][0] == i]
            d = [x[1] for x in path if x[0][0] == i]
            for j, c in enumerate(r):
                l += dirs[d[e.index((i, j))]] if (i, j) in e else "."
            debug_print(l)
                


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
    
    def count_loops(self, grid, init_path, pos, dir):
    #def count_loops(self, grid, init_row, init_col, pos, dir):
        
        def _multiplex(pos, dir):
            return pos[0] * len(grid[0]) + pos[1] + (len(grid[0] * len(grid))) * list(Guard.DIRECTIONS.values()).index(dir)
        

        o = []
        pp = []
        n = 0
        loops = set()
        #o = set()
        # do not include starting space
        # only need to consider spaces on the original path?
        #for space in set([x[0] for x in init_path[1:]]):
        for k in range(1, len(init_path)):
            #debug_if(f"K {k}/{len(init_path)}", condition=k % 100 == 1, include_time=True)
            space = init_path[k]
            prev_space = init_path[k - 1]
            i, j = space[0]
            # already placed a barrier here
            if (i, j) in o:
                continue
            g = grid[:]
            g[i] = g[i][:j] + Room.WALL + g[i][j + 1:]
            #p = Room(g).find_path(pos, dir)
            # start at the previous space
            r = Room(g)
            p = r.find_path(*prev_space)
            if not r.is_loop(p):
                continue
            #debug_print(f"{k} {i} {j}")
            #n += 1
            o.append((i, j))
            l = r.get_loop(p)
            #r.print_path(l)
            #debug_if(f"K {k}/{len(init_path)} LOOP {l}", condition=True, include_time=True)
            #loops = loops.union(set(l))
            loops = loops | set(l)
            #debug_print(f"L {len(l)} N L {len(loops)}")
            #pp = pp.union(set(sorted([_multiplex(x[0], x[1]) for x in p])))
            #m = sorted([_multiplex(x[0], x[1]) for x in p])
            #if m not in pp:
            #    pp.append(m)
            #o = o.union(set(sorted(sorted(p, key=lambda x: x[0][0]), key=lambda x: x[0][1])))


        #debug_print(f"LOOPS UNIQUE? {loops}")
        #return n
        return len(o)
            

    def run(self):
        g = self._get_guard(self.input)
        r = Room(self.input)
        #debug_print(f"G POS {g.position} DIR {g.direction}")
        p = r.find_path(g.init_pos, g.init_dir)
        debug_print(f"UNIQUE PATH LEN {len(set([x[0] for x in p]))} FULL LEN {len(p)}")
        n = self.count_loops(self.input, p, g.init_pos, g.init_dir)
        #n = self.count_loops(v, p[0][0], p[0][1], g.init_pos, g.init_dir)
        debug_print(f"NUM LOOPS {n}")

