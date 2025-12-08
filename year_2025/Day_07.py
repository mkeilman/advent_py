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
        #"...............",
    ]

    ENTRY = "S"

    SPLITTER = "^"


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
        m = self._num_paths(all_pos)
        debug_print(f"NUM SPLITS {m}")
        return n
 

    def _num_paths(self, beam_positons, depth=0):
        n = 0
        #debug_print(f"{depth} GET P FROM {beam_positons}")
        for i in range(len(beam_positons) - 1):
            b1 = beam_positons[i]
            b2 = beam_positons[i + 1]
            debug_print(f"{depth} GET P FROM {b1} - {b2}")
            for r in b1:
                #debug_print(r)
                next = [x for x in b2 if abs(x[1] - r[1]) == 1]
                debug_print(f"{depth} NEXT {next}")
                n += len(next)
        return n


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
            debug_print(ns)
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