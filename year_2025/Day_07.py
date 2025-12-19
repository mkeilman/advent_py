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
        #"...............",
        #".....^.^.^.....",
        #"...............",
        #"....^.^...^....",
        #"...............",
        #"...^.^...^.^...",
        #"...............",
        #"..^...^.....^..",
        #"...............",
        #".^.^.^.^.^...^.",
        #"...............",
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
        self._print_beams(all_pos)
        m = self._num_paths(all_pos)
        debug_print(f"NUM PATHS {m}")
        return n
 

    def _np(self, beam_positons, curr_pos=None, depth=0, n=1):
        
        #n = 0
        n = 1
        if not beam_positons:
            return 0, []
        
        b0 = beam_positons[0]
        pos = curr_pos or self.entry_pos
        #debug_print(f"{depth} NP {beam_positons} CURR {pos} NEXT ROW {b0}")
        path = [pos]
        #paths = [path]
        # positions below and to either side of the current one; 
        # no split positions means the beam continues straight down
        next = [x for x in b0 if abs(x[1] - pos[1]) == 1] or [x for x in b0 if x[1] == pos[1]]
        n = len(next)
        #for _ in range(len(next) - 1):
        #    paths.append(path[:])
        debug_print(f"{depth} NEXT {n}")
        for i, q in enumerate(next):
            #paths[i].append(q)
            m, r = self._np(beam_positons[1:], curr_pos=q, depth=depth + 1, n=n * len(next))
            debug_print(f"{depth} R {r} N NON LIST {len([x for x in r if type(x) != list])}")
            if r:
                #path.extend(r)
                path.append(r)
                n += len([x for x in r if type(x) != list])
        #debug_print(f"{depth} N {n}")
        # done
        #if not depth:
        #    n = 1
        #    debug_print("DONE")
        #    p = path[:]
        #    n_loop = 4
        #    while p and n_loop:
        #        n *= len(p)
        #        debug_print(f"P {p}")
        #        p = [x for x in p if type(x) is list][0]
        #        n_loop -= 1
        #        
        #debug_print(f"N?? {n}")
        return n, path


    def _num_paths(self, beam_positons, depth=0):
        return self._np(beam_positons[1:])
        n = 0
        #n = 1
        #debug_print(f"{depth} GET P FROM {beam_positons}")
        for i in range(len(beam_positons) - 1):
            m = 1
            b1 = beam_positons[i]
            b2 = beam_positons[i + 1]
            debug_print(f"{depth} GET P FROM {b1} - {b2}")
            for r in b1:
                next = [x for x in b2 if abs(x[1] - r[1]) == 1] or [x for x in b2 if x[1] == r[1]]
                debug_print(f"{depth} NEXT {next}")
                #n += len(next)
                m *= len(next)
            n += m
        return n


    def _print_beams(self, beam_positons):
        for r in range(len(self.input)):
            s = ""
            for c in range(len(self.input[0])):
                p = (r, c)
                b = AdventDay.BEAM if any([p in x for x in beam_positons]) else AdventDay.SPACE
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
                p.append((i, r.index(token))) 
        return p