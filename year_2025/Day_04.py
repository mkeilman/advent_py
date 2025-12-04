import Day
from utils.debug import debug_print, debug_if

class AdventDay(Day.Base):

    TEST = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]

    PAPER = "@"

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 4)
        self.add_args(run_args)


    def run(self):
        n = 0
        self.grid = Day.Grid.grid_of_size(len(self.input[0]), len(self.input))
        n = self._num_accessable_bales()
        debug_print(f"RUN {self.year} {self.day}: {n}")
        return n
 

    def _num_accessable_bales(self):

        def _has_paper(pos):
            return self.input[pos[0]][pos[1]] == AdventDay.PAPER
        
        n = 0
        for pos in self.grid.flat_array:
            if not _has_paper(pos):
                continue
            nb = self.grid.neighborhood(pos, include=("row", "col", "corners"))
            if len([x for x in nb if _has_paper(x)]) < 4:
                n += 1
        return n

