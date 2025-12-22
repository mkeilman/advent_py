import Day
from utils.debug import debug_print, debug_if
from utils import collectionutils
from utils import stringutils

class AdventDay(Day.Base):

    TEST = [
        ".......S.......",
        "...............",
        ".......^.......",
        "...............",
        "......^.^......",
        "...............",
        ".....^.^.^.....",
        "...............",
        "....^.^...^....",
        "...............",
        "...^.^...^.^...",
        "...............",
        "..^...^.....^..",
        "...............",
        ".^.^.^.^.^...^.",
        "...............",
    ]

    BEAM = "|"
    ENTRY = "S"
    SPLITTER = "^"
    SPACE = "."


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 7)
        self.add_args(run_args)


    def run(self):
        n = 0
        self.entry_pos = self._token_pos(AdventDay.ENTRY)
        self.splitter_pos = self._token_positions(AdventDay.SPLITTER)
        #debug_print(f"ENTRY {self.entry_pos} S {self.splitter_pos}")
        n, all_pos = self._propagate()
        debug_print(f"NUM SPLITS {n}")
        #self._print_beams(all_pos)
        #m, paths = self._num_paths(all_pos[1:])
        #m = self._num_paths(all_pos[1:]) + 1
        self.num_recur = 0
        m = self._num_paths() + 1
        debug_print(f"NUM PATHS {m}")
        #for p in paths:
        #    self._print_beams([p])
        #    debug_print(p)
        return n
 

    #def _num_paths(self, beam_positions, curr_pos=None, depth=0):
    def _num_paths(self, curr_pos=None, depth=0):
        
        self.num_recur += 1
        pos = curr_pos or self.entry_pos
        if pos[0] == len(self.input) - 1:
            return 0
        #if not beam_positions:
        #    return 0 #, []
        
        n = 0
        row = 0
        next = [pos]
        #b0 = beam_positions[0]
        #pos = curr_pos or self.entry_pos
        #debug_print(f"{depth} NP {beam_positions} CURR {pos} NEXT ROW {b0}")
        #debug_if(f"{depth} START ROW {pos[0]}", condition=n > 100)
        #p0 = [pos]
        #paths = [p0]
        # positions below and to either side of the current one (if a splitter is below); 
        # no split positions means the beam continues straight down
        while row < len(self.input):
            debug_print(f"{depth} ON ROW {row} NUM POS {len(next)}", include_time=True)
            #if row % 2:
            #    debug_print(f"{depth} ON ROW {row} NUM POS {len(next)} NEXT {next}")
            #    next = [(row + 1, x[1]) for x in next]
            #    row += 1
            #    continue
            p = []
            for pos in next:
                below = (row + 1, pos[1])
                left = (row + 1, pos[1] - 1)
                right = (row + 1, pos[1] + 1)
                if below in self.splitter_pos:
                    n += 1
                    p.extend([left, right])
                else:
                    p.append(below)
                #next = (left, right) if below in self.splitter_pos else (below,)  
            next = p  
            row += 1
        #below = (pos[0] + 1, pos[1])
        #left = (pos[0] + 1, pos[1] - 1)
        #right = (pos[0] + 1, pos[1] + 1)
        #next = (left, right) if below in self.splitter_pos else (below,)
        #if below in self.splitter_pos:
        ##    n = n + 1 + self._num_paths(curr_pos=left, depth=depth + 1) + self._num_paths(curr_pos=right, depth=depth + 1)
        #    debug_if(f"{depth} NR {self.num_recur} N {n} DONE ROW {pos[0]}", condition=not self.num_recur % 10000)
        #    return n #+ 1 + self._num_paths(curr_pos=left, depth=depth + 1) + self._num_paths(curr_pos=right, depth=depth + 1)
        #n += self._num_paths(curr_pos=below, depth=depth + 1)
        #debug_if(f"{depth} NR {self.num_recur} N {n} DONE ROW {pos[0]}", condition=not self.num_recur % 10000)
        return n #+ self._num_paths(curr_pos=below, depth=depth + 1)
        #next = [x for x in b0 if abs(x[1] - pos[1]) == 1 and (x[0], pos[1]) in self.splitter_pos] or [x for x in b0 if x[1] == pos[1]]
        # copy what we have so far - each possible adjacent position sprouts a new path
        # straight paths do NOT
        #n += (len(next) - 1)
        #num_new = len(next) - 1
        #if num_new:
        #    n += 1
        #paths += num_new * [p0[:]]
        #debug_print(f"{depth} LEN {len(paths)} N {n} NEXT {next}")
        
        #i = 0
        for q in next:
            pass
            #debug_print(f"{depth} GET PATHS FOR {q}")
            #m, r_paths = self._num_paths(beam_positions[1:], curr_pos=q, depth=depth + 1)
            #n += self._num_paths(beam_positions[1:], curr_pos=q, depth=depth + 1)
            #n += self._num_paths(curr_pos=q, depth=depth + 1)
            #debug_print(f"{depth} M {m} LEN {len(r_paths)}")
            #debug_print(f"{depth} M {m}")
            #if not m:
                #paths[i].append(q)
                #i += 1
                #continue
            #num_r = len(r_paths) - 1
            #num_r = m - 1
            #debug_print(f"{depth} M {m} VS NUM R {num_r}")
            #debug_print(f"{depth} ADDING {num_r} COPIES OF {paths[i]} INTO {paths} AT {i} FOR {r_paths}")
            # insert new paths
            #debug_print(f"{depth} N {n} NP BEFORE {len(paths)}")
            #for _ in range(num_r):
            #   paths.append(paths[i][:])
            #n += m
            #n += num_r
            #debug_print(f"{depth} N {n} NP AFTER {len(paths)}")
            #debug_print(f"{depth} AFTER INSERT N {n} LEN {len(paths) - 1}")
            #for j, r in enumerate(r_paths):
            #    paths[i + j].extend(r)
                #debug_print(f"{depth} PATH[{i + j}] NOW {paths[i + j]}")
            #i = len(paths) - 1
        #n += i
        #debug_print(f"{depth} DONE N {n} NP {len(paths)}")
        return n #, paths


    def _print_beams(self, beam_positions):
        for r in range(len(self.input)):
            s = ""
            for c in range(len(self.input[0])):
                p = (r, c)
                b = AdventDay.BEAM if any([p in x for x in beam_positions]) else AdventDay.SPACE
                s += AdventDay.SPLITTER if p in self.splitter_pos else b
            debug_print(s)


    def _propagate(self):
        def _next_pos(bp, row):
            ns = 0
            np = 0

            splitter_pos = [(i, j) for j in stringutils.indices(AdventDay.SPLITTER, list(row))]
            next_pos = set()
            for p in bp:
                new_pos = (i, p[1])
                if new_pos not in splitter_pos:
                    next_pos.add(new_pos)
                else:
                    next_pos.add((i, p[1] + 1))
                    next_pos.add((i, p[1] - 1))
                    ns += 1
                    np += 2
            return np, ns, next_pos

        num_splits = 0
        num_paths = 0
        beam_positions = set([self.entry_pos])
        all_pos = []
        for i, r in enumerate(self.input):
            n, m, beam_positions = _next_pos(beam_positions, r)
            all_pos.append(beam_positions)
            num_splits += m
            num_paths += n
        return num_splits, all_pos


    def _token_pos(self, token):
        for i, r in enumerate(self.input):
            if token in r:
                return (i, r.index(token))
        return None


    def _token_positions(self, token):
        p = []
        for i, r in enumerate(self.input):
            if token in r:
                for t in stringutils.indices(token, r):
                    p.append((i, t)) 
        return p