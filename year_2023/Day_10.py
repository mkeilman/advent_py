import re
import Day


class Pipe():
    connections = {
        "|": ((-1, 0), (1, 0)),
        "-": ((0, -1), (0, 1)),
        "L": ((-1, 0), (0, 1)),
        "J": ((-1, 0), (0, -1)),
        "7": ((1, 0), (0, -1)),
        "F": ((1, 0), (0, 1)),
    }
    connection_counts = {
        "|": 1,
        "-": 0,
        "L": 0.5,
        "J": -0.5,
        "7": 0.5,
        "F": -0.5,
    }
    re_pipe = fr"[{connections.keys()}]"
    START = "S"
    GROUND = "."

    def __init__(self, label, pos):
        self.label = label
        self.is_corner = self.label in ("L", "J", "7", "F")
        self.pos = pos
        self.connections = []
        self.count = Pipe.connection_counts[self.label]
        for c in Pipe.connections.get(self.label):
            self.connections.append((pos[0] + c[0], pos[1] + c[1]))
    

    def does_connect_pipe(self, other_pipe):
        return self.does_connect_pos(other_pipe.pos)
    

    def does_connect_pos(self, other_pos):
        return other_pos in self.connections


class Plumbing():

    SQUARE = [
                    "-L|F7",
                    "7S-7|",
                    "L|7||",
                    "-L-J|",
                    "L|-JF",
                ]
    TWISTY = [
                    "7-F7-",
                    ".FJ|7",
                    "SJLL7",
                    "|F--J",
                    "LJ.LJ",
                ]
    BOTTLE = [
                    "...........",
                    ".S-------7.",
                    ".|F-----7|.",
                    ".||.....||.",
                    ".||.....||.",
                    ".|L-7.F-J|.",
                    ".|..|.|..|.",
                    ".L--J.L--J.",
                    "...........",
                ]
    BOTTLE2 = [
                    "..........",
                    ".S------7.",
                    ".|F----7|.",
                    ".||....||.",
                    ".||....||.",
                    ".|L-7F-J|.",
                    ".|..||..|.",
                    ".L--JL--J.",
                    "..........",
                ]
    MAZE = [
                    ".F----7F7F7F7F-7....",
                    ".|F--7||||||||FJ....",
                    ".||.FJ||||||||L7....",
                    "FJL7L7LJLJ||LJ.L-7..",
                    "L--J.L7...LJS7F-7L7.",
                    "....F-J..F7FJ|L7L7L7",
                    "....L7.F7||L7|.L7L7|",
                    ".....|FJLJ|FJ|F7|.LJ",
                    "....FJL-7.||.||||...",
                    "....L---J.LJ.LJLJ...",
                ]
    MAZE2 = [
        "FF7FSF7F7F7F7F7F---7",
        "L|LJ||||||||||||F--J",
        "FL-7LJLJ||||||LJL-77",
        "F--JF--7||LJLJ7F7FJ-",
        "L---JF-JLJ.||-FJLJJ7",
        "|F|F-JF---7F7-L7L|7|",
        "|FFJF7L7F-JF7|JL---7",
        "7-L-JL7||F7|L7F-7F7|",
        "L.L7LFJ|||||FJL7||LJ",
        "L7JLJL-JLJLJL--JLJ.L",
    ]


    def __init__(self, grid):
        self.grid = grid
        self.grid_range = [range(len(grid)), range(len(grid[0]))]
        self.start_pos = self._start_pos()
        self.start_pipe = self._start_pipe()
        self.pipe_loop = self._pipe_loop()
        #self.pipe_positions = [x.pos for x in self.pipe_loop]
        self.pipe_positions = [x["pos"] for x in self.pipe_loop.values()]
        x = [x[0] for x in self.pipe_positions]
        y = [x[1] for x in self.pipe_positions]
        self.pipe_loop_range = [range(min(*x) + 1, max(*x)), range(min(*y) + 1, max(*y))]

    def interior_tiles(self):
        #print("GET INT")
        not_pipe = []
        #print("GET NOT PIPES...", end="")
        for i in self.pipe_loop_range[0]:
            for j in self.pipe_loop_range[1]:
                if (i, j) not in self.pipe_positions:
                    not_pipe.append((i, j))
        #print("DONE")

        n = 0
        for c in not_pipe:
            m = 0
            # draw a line to "infinity" and count the number of crossings
            for y in range(c[1], len(self.grid_range[1])):
                p = self._get_pipe((c[0], y))
                m += 0 if p is None else p.count
            n += int(m) % 2
        return n


    def print_loop(self):
        for i in self.grid_range[0]:
            for j in self.grid_range[1]:
                print(self.grid[i][j] if (i, j) in self.pipe_positions else ".", end="")
            print("")

    def _get_pipe(self, pos):
        p = self.pipe_loop.get(f"{pos}")
        return None if p is None else p.get("pipe")

    def _make_pipe(self, label, pos):
        if label in (Pipe.START, Pipe.GROUND):
            return None
        p = Pipe(label, pos)
        p.connections = [x for x in p.connections if x[0] in self.grid_range[0] and x[1] in self.grid_range[1]]
        return p

    def _pipe_loop(self):
        #print("PIPE LOOP")
        def _add_pipe(d, p):
            d[f"{p.pos}"] = {"pos": p.pos, "pipe": p}

        def _can_add(pipe, d):
            return pipe is not None and f"{pipe.pos}" not in d.keys()
        
        
        m = {}
        curr_pipe = self.start_pipe
        _add_pipe(m, curr_pipe)

        did_add = True
        #print("BUILD LOOP...", end="")
        while did_add:
            n = curr_pipe.connections[0]
            p = self._make_pipe(self.grid[n[0]][n[1]], n)
            if not _can_add(p, m):
                n = curr_pipe.connections[1]
                p = self._make_pipe(self.grid[n[0]][n[1]], n)
                if not _can_add(p, m):
                    did_add = False
                else:
                    curr_pipe = p
                    _add_pipe(m, curr_pipe)
                    continue
            else:
                curr_pipe = p
                _add_pipe(m, curr_pipe)
                
        #print("DONE")
        return m

    def _start_pipe(self):
        for t in Pipe.connections:
            s = self._make_pipe(t, self.start_pos)
            nx = 0
            for n in s.connections:
                p = self._make_pipe(self.grid[n[0]][n[1]], n)
                if p and p.does_connect_pipe(s):
                    nx += 1
            # must connect to 2 and only 2 other pipes
            if nx == 2:
                return s
        return None


    def _start_pos(self):
        for i in self.grid_range[0]:
            for j in self.grid_range[1]:
                if self.grid[i][j] == Pipe.START:
                    return (i, j)
        return None


class AdventDay(Day.Base):

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2023,
            10,
            Plumbing.MAZE2
        )


    def run(self, v):
        pl = Plumbing(v)
        print(f"START PIPE {pl.start_pipe.label} NUM INT {pl.interior_tiles()}")
        #pl.print_loop()
        #print(f"START {pl.start_pos} PIPE {pl.start_pipe.label} LOOP LEN {len(pl.pipe_loop)} MAX DIST {len(pl.pipe_loop) // 2}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
