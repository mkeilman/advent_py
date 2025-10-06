import re
import Day
from utils import mathutils
from utils import string
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
            inds = string.indices(c, self.elements)
            if len(inds) > 1:
                return self.elements[inds[0]:inds[1]]
        return None


    def is_line(self):
        p = self.positions()
        allx = all([x[0] == p[0][0] for x in p])
        ally = all([x[1] == p[0][1] for x in p])
        return allx or ally


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
                
            return "X"

        p = DirectedPath()
        p.append(start_pos, start_dir)
        pos = start_pos
        dir = start_dir
        d = list(Guard.DIRECTIONS.values())

        while _is_in_room(pos) and not p.is_loop():
            #debug_print(f"CHECK STR {_sub_string(pos, dir)}")
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
        #loops = set()
        n_lines = 0
        n_loops = 0
        e = init_path.elements
        # omit initial step
        # only need to consider steps on the original path
        for k in range(1, len(e)):
            #debug_print(f"CHECK K {k}")
            i, j = e[k][0]
            # already placed a barrier here
            if (i, j) in o:
                continue

            o.append((i, j))
            # copy the gird
            g = grid[:]

            # place a wall in this spot
            g[i] = g[i][:j] + Room.WALL + g[i][j + 1:]
        
            # make a room with the new wall and find a path starting at the previous step
            r = Room(g)
            p = r.find_path(*e[k - 1])

            # lines happen if the only way to bounce off the new wall is to return to
            # the start
            
            if p.is_line():
                debug_print(f"K {k} PATH IS LINE")
                n_lines += 1
                #continue
            if not p.is_loop():
                continue
            #o.append((i, j))
            #if p.is_line():
            #    debug_print(f"K {k} LINE IS LOOP {p.elements}")
                #r.print_path(p.elements)
            n_loops += 1
            #l = p.get_loop()
            # last element is the same as the first
            #del p.elements[-1]
            #r.print_path(l)
            #debug_if(f"K {k}/{len(init_path)} LOOP {l[0]}-{l[-1]} LEN {len(l)}", condition=True, include_time=True)
            #loops = loops | set(p.elements)

        #debug_print(f"FOUND {n_lines} LINES")
        #return len(o)
        return n_loops
            

    def run(self):
        g = self._get_guard(self.input)
        r = Room(self.input)
        p = r.find_path(g.init_pos, g.init_dir)
        debug_print(f"UNIQUE PATH LEN {len(set([x[0] for x in p.elements]))} FULL LEN {len(p)}")
        n = self.count_loops(self.input, p)
        debug_print(f"NUM LOOPS {n}")

