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

    FLOOR = "."

    PAPER = "@"

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 4)
        self.args_parser.add_argument(
            "--count-removed-bales",
            action=argparse.BooleanOptionalAction,
            default=False,
            dest="count_removed_bales",
        )
        self.add_args(run_args)


    def run(self):
        n = 0
        self.grid = Day.Grid.grid_of_size(len(self.input[0]), len(self.input))
        b = self._accessable_bales()
        if not self.count_removed_bales:
            return len(b)
        while b:
            n += len(b)
            for pos in b:
                self._remove_bale(pos)
            b = self._accessable_bales()
        debug_print(f"REMOVED BALES {n}")
        return n
 

    def _accessable_bales(self):
        b = {}
        for pos in self.grid.flat_array:
            if not self._has_paper(pos):
                continue
            nb = self.grid.neighborhood(pos, include=("row", "col", "corners"))
            pnb = [x for x in nb if self._has_paper(x)]
            if len(pnb) < 4:
                b[pos] = pnb
        return b
    

    def _has_paper(self, pos):
            return self.input[pos[0]][pos[1]] == AdventDay.PAPER
    

    def _num_accessable_bales(self):
        return len(self._accessable_bales())


    def _remove_bale(self, pos):
        r = self.input[pos[0]]
        self.input[pos[0]] = r[:pos[1]] + AdventDay.FLOOR + r[pos[1] + 1:]


