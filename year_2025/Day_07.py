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
        m, paths = self._num_paths(all_pos)
        debug_print(f"NUM PATHS {m}")
        #for p in paths:
            #self._print_beams([p])
            #debug_print(p)
        return n
 

    def _np(self, beam_positions, curr_pos=None, depth=0, n=1, paths=None):
        
        if not beam_positions:
            #debug_print(f"{depth} END OF GRID")
            return 0, []
        

        b0 = beam_positions[0]
        pos = curr_pos or self.entry_pos
        #debug_print(f"{depth} NP {beam_positions} CURR {pos} NEXT ROW {b0}")
        p0 = [pos]
        paths = [p0]
        # positions below and to either side of the current one; 
        # no split positions means the beam continues straight down
        next = [x for x in b0 if abs(x[1] - pos[1]) == 1 and (x[0], pos[1]) in self.splitter_pos] or [x for x in b0 if x[1] == pos[1]]
        n *= len(next)
        # copy what we have so far - each possible next position sprouts a new path
        num_new = len(next) - 1
        #debug_print(f"{depth} APPENDING {num_new} COPIES OF {p0}")
        paths += num_new * [p0[:]]
        
        #debug_print(f"{depth} {pos} CURR PATHS {paths}; NEXT {next}")
        i = 0
        #for i, q in enumerate(next):
        for q in next:
            #debug_print(f"{depth} PATH[{i}] {paths[i]} + {q}")
            _, r_paths = self._np(beam_positions[1:], curr_pos=q, depth=depth + 1, n=n, paths=paths)
            if not r_paths:
                #debug_print(f"{depth} NO NEW PATHS FROM {q}")
                paths[i].append(q)
                i += 1
                continue
            #debug_print(f"{depth} PATH[{i}] R {r_paths}")
            # copy what we have so far
            num_r = len(r_paths) - 1
            #paths += (len(r_paths) - 1) * [paths[i][:]]
            #debug_print(f"{depth} I {i}")
            #debug_print(f"{depth} ADDING {num_r} COPIES OF {paths[i]} INTO {paths} AT {i} FOR {r_paths}")
            # insert new paths
            #paths = paths[:i] + num_r * [paths[i][:]] + paths[i:]
            for _ in range(num_r):
                #paths.append(paths[i][:])
                paths.append(paths[i][:])
            #debug_print(f"{depth} AFTER INSERT {paths} PATHS")
            for j, r in enumerate(r_paths):
            #for r in r_paths:
                #debug_print(f"{depth} I {i} PATH[{i + j}] {paths[i + j]} ADD ARR {r}")
                for p in r:
                    #debug_print(f"{depth} PATH[{i}] ADD POS {p}")
                    paths[i + j].append(p)
                    #paths[i].append(p)
                #debug_print(f"{depth} PATH[{i + j}] NOW {paths[i + j]}")
            #i += 1
            i = len(paths) - 1
        #debug_print(f"{depth} FINAL {paths}")
        return len(paths), paths


    def _num_paths(self, beam_positions, depth=0):
        return self._np(beam_positions[1:])
        n = 0
        #n = 1
        #debug_print(f"{depth} GET P FROM {beam_positions}")
        for i in range(len(beam_positions) - 1):
            m = 1
            b1 = beam_positions[i]
            b2 = beam_positions[i + 1]
            debug_print(f"{depth} GET P FROM {b1} - {b2}")
            for r in b1:
                next = [x for x in b2 if abs(x[1] - r[1]) == 1] or [x for x in b2 if x[1] == r[1]]
                debug_print(f"{depth} NEXT {next}")
                #n += len(next)
                m *= len(next)
            n += m
        return n


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
            #debug_print(ns)
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
        #debug_print(f"NP {num_paths}")
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