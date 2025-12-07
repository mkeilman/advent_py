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

    ENTRY = "S"

    SPLITTER = "^"


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 7)
        self.add_args(run_args)
        self.grid = None


    def run(self):
        n = 0
        self._parse()
        self.entry_pos = self._token_pos(AdventDay.ENTRY)
        self.splitter_pos = self._token_positions(AdventDay.SPLITTER)
        #debug_print(f"ENTRY {self.entry_pos} S {self.splitter_pos}")
        self._propagate()
        return n
 

    def _parse(self):
        self.grid = Day.Grid.grid_of_size(len(self.input), len(self.input[0]))


    def _propagate(self):
        def _next_pos(bp, row):
            n = 0
            splitter_pos = [(i, j) for j in stringutils.indices(AdventDay.SPLITTER, list(row))]
            next_pos = set()
            for p in bp:
                new_pos = (i, p[1])
                if new_pos not in splitter_pos:
                    next_pos.add(new_pos)
                else:
                    next_pos.add((i, p[1] + 1))
                    next_pos.add((i, p[1] - 1))
                    n += 1
            #debug_print(f"N S {n}")
            return n, next_pos
            

        num_splits = 0
        beam_positions = set([self.entry_pos])
        for i, r in enumerate(self.input):
            m, beam_positions = _next_pos(beam_positions, r)
            num_splits += m
            #debug_print(f"BP {beam_positions}")
        debug_print(f"NUM SPLITS {num_splits}")
                
            



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