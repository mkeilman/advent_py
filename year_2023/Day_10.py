from functools import reduce
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
    re_pipe = fr"[{connections.keys()}]"
    START = "S"
    GROUND = "."

    def __init__(self, label, pos):
        self.label = label
        self.pos = pos
        self.connections = []
        for c in Pipe.connections.get(self.label):
            self.connections.append((pos[0] + c[0], pos[1] + c[1]))
    

    def does_connect_pipe(self, other_pipe):
        return self.does_connect_pos(other_pipe.pos)
    

    def does_connect_pos(self, other_pos):
        return other_pos in self.connections


class Plumbing():
    def __init__(self, grid):
        self.grid = grid
        self.grid_range = [range(len(grid)), range(len(grid[0]))]
        self.num_pipes = len(grid) * len(grid[0])
        self.start_pos = self._start_pos()
        self.start_pipe = self._start_pipe()
        self.pipe_loop = self._pipe_loop()

    def _make_pipe(self, label, pos):
        if label in (Pipe.START, Pipe.GROUND):
            return None
        p = Pipe(label, pos)
        p.connections = [x for x in p.connections if x[0] in self.grid_range[0] and x[1] in self.grid_range[1]]
        return p

    def _pipe_loop(self):

            def _can_add(pipe, arr):
                return pipe is not None and pipe.pos not in [x.pos for x in arr]
            
            curr_pipe = self.start_pipe
            l = [curr_pipe]

            did_add = True
            #i = 0
            while did_add:
                n = curr_pipe.connections[0]
                p = self._make_pipe(self.grid[n[0]][n[1]], n)
                if not _can_add(p, l):
                    n = curr_pipe.connections[1]
                    p = self._make_pipe(self.grid[n[0]][n[1]], n)
                    if not _can_add(p, l):
                        did_add = False
                    else:
                        l.append(p)
                        #print(f"ADDED {p.label} AT {p.pos}")
                        curr_pipe = p
                        continue
                else:
                    l.append(p)
                    #print(f"ADDED {p.label} AT {p.pos}")
                    curr_pipe = p
                #i += 1
                #did_add = i < 10
            return l

    def _start_pipe(self):
        for t in Pipe.connections:
            s = self._make_pipe(t, self.start_pos)
            #print(f"CHECK PIPE {s.label}")
            nx = 0
            for n in s.connections:
                #print(f"CONNECTION {n} {self.grid[n[0]][n[1]]}")
                p = self._make_pipe(self.grid[n[0]][n[1]], n)
                #print(f"NB {n} PIPE {p.label}")
                if p and p.does_connect_pipe(s):
                    #print(f"NB {n} PIPE {p.label} CONNECTS TO {s.label}")
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
            #[
            #    "-L|F7",
            #    "7S-7|",
            #    "L|7||",
            #    "-L-J|",
            #    "L|-JF",
            #]
            [
                "7-F7-",
                ".FJ|7",
                "SJLL7",
                "|F--J",
                "LJ.LJ",
            ]
        )


    def run(self, v):
        pl = Plumbing(v)
        #print(f"START {self.start_pos} PIPE {self.start_pipe.label} LOOP {[x.label for x in self.pipe_loop]} LEN {len(self.pipe_loop)}")
        print(f"START {pl.start_pos} PIPE {pl.start_pipe.label} LOOP LEN {len(pl.pipe_loop)} MAX DIST {len(pl.pipe_loop) // 2}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
