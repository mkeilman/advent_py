import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug


class Plot:
    def __init__(self, grid):
        self.grid = grid
        self.size = [len(self.grid), len(self.grid[0])]
        self.plants = set()
        for r in self.grid:
            self.plants = self.plants.union(set(r))
        self.regions = {}
        self.areas = {}
        self.perimeters = {}
        for p in self.plants:
            self.regions[p] = self._regions_for_plant(p)
            self.areas[p] = [len(x) for x in self.regions[p]]
            self.perimeters[p] = [self._perimeter(x) for x in self.regions[p]]
        #debug(f"R {self.regions} A {self.areas} P {self.perimeters}")


    def _is_in_grid(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]
    
    def _neighborhood(self, pos):
        n = []
        for p in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            q = (pos[0] + p[0], pos[1] + p[1])
            if self._is_in_grid(q):
                n.append(q)
        return n

    def _perimeter(self, region):
        #x = [x[0] for x in region]
        #y = [x[1] for x in region]
        #p = 2 * abs(max(x) - min(x) + 1) + 2 * abs(max(y) - min(y) + 1)
        p = 0
        for pos in region:
            m = set(self._neighborhood(pos))
            p += (4 - len(m.intersection(region)))
        return p

    def price(self):
        s = 0
        for p in self.plants:
            s += mathutils.sum([self.areas[p][i] * self.perimeters[p][i] for i, _ in enumerate(self.areas[p])])
        return s

    def _regions_for_plant(self, plant):
        def _region(p, c, s=None):
            r = s or set([p])
            if not c[p]:
                # plants with no connections are their own regions
                return r
            for n in [x for x in c[p] if x not in r]:
                r.add(n)
                r = r.union(_region(n, c, s=r))
            return r

        reg = []
        for i, r in enumerate(self.grid):
            reg.extend([(i, j) for j in string.indices(plant, r)])
        conn = {}
        for p in reg:
            n = []
            for q in reg:
                if p != q and p in self._neighborhood(q):
                    n.append(q)
            conn[p] = n
        p_reg = []
        for p in conn:
            r = _region(p, conn)
            if r not in p_reg:
                p_reg.append(r)
        return p_reg


class AdventDay(Day.Base):

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            12,
            #[
            #    "RRRRIICCFF",
            #    "RRRRIICCCF",
            #    "VVRRRCCFFF",
            #    "VVRCCCJFFF",
            #    "VVVVCJJCFE",
            #    "VVIVCCJJEE",
            #    "VVIIICJJEE",
            #    "MIIIIIJJEE",
            #    "MIIISIJEEE",
            #    "MMMISSJEEE",
            #]
            #[
            #    "AAAA",
            #    "BBCD",
            #    "BBCC",
            #    "EEEC",
            #]
            [
                "OOOOO",
                "OXOXO",
                "OOOOO",
                "OXOXO",
                "OOOOO",
            ]
            #[
            #    "AABBB",
            #    "BBAAB",
            #]
        )

    def run(self, v):
        p = Plot(v)
        debug(f"PRICE {p.price()}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
