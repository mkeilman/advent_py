import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Region:
    def __init__(self, grid):
        self.grid = grid



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
        self.sides = {}
        for p in self.plants:
            self.regions[p] = self._regions_for_plant(p)
            self.areas[p] = [len(x) for x in self.regions[p]]
            self.perimeters[p] = [self._perimeter(x) for x in self.regions[p]]
            self.sides[p] = [self._num_sides(x) for x in self.regions[p]]
        #debug(f"R {self.regions} A {self.areas} P {self.perimeters}")

    def _is_corner(self, pos, region):
        x = [x[0] for x in region]
        y = [x[1] for x in region]
        for i in (min(x), max(x)):
            for j in (min(y), max(y)):
                if pos == (i, j):
                    return True
        return False
    

    def _to_grid(self, region):
        g = []
        rows = set([x[0] for x in region])
        cols = set([x[1] for x in region])
        for r in rows:
            arr = []
            for c in cols:
                p = (r, c)
                if p in region:
                    arr.append(p)
            g.append(arr)
        return g

    def _is_in_grid(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]
    
    def _is_rect(self, region):
        g = self._to_grid(region)
        return all([len(r) == len(list(g)[0]) for r in g])

    def _neighborhood(self, pos, restrict_to=None):
        n = []
        sites = {
            "r": ((-1, 0), (1, 0)),
            "c": ((0, -1), (0, 1)),
        }
        s = mathutils.sum(sites.values(), init_val=()) if restrict_to is None else sites[restrict_to]
        #for p in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        for p in s:
            q = (pos[0] + p[0], pos[1] + p[1])
            if self._is_in_grid(q):
                n.append(q)
        return n

    def _num_sides(self, region):
        import operator

        def _new_sides(pos):
            return 2 if self._is_corner(pos, region) else 4
        
        n = 4
        #if len(region) == 1:
        if self._is_rect(region) == 1:
            #debug(f"R {region} IS RECT")
            return n
        
        #edges = [x for x in region if 0 < len(set(self._neighborhood(x)).intersection(region)) < 4]
        #edges.sort(key=operator.itemgetter(0, 1))
        x = [x[0] for x in region]
        y = [x[1] for x in region]

        add_sides = False
        isolated = {}
        #top
        for p in [p for p in region if p[0] == min(x)]:
            isolated[p] = isolated.get(p) or not [q for q in self._neighborhood(p, restrict_to="c") if q in region]
            if not [q for q in self._neighborhood(p, restrict_to="c") if q in region]:
                add_sides = True
                n += _new_sides(p)
        
        #bottom
        for p in [p for p in region if p[0] == max(x)]:
            isolated[p] = isolated.get(p) or not [q for q in self._neighborhood(p, restrict_to="c") if q in region]
            if not [q for q in self._neighborhood(p, restrict_to="c") if q in region]:
                add_sides = True
                n += _new_sides(p)

        #left
        for p in [p for p in region if p[1] == min(y)]:
            isolated[p] = isolated.get(p) or not [q for q in self._neighborhood(p, restrict_to="r") if q in region]
            if not [q for q in self._neighborhood(p, restrict_to="r") if q in region]:
                add_sides = True
                n += _new_sides(p)

        #right
        for p in [p for p in region if p[1] == max(y)]:
            isolated[p] = isolated.get(p) or not [q for q in self._neighborhood(p, restrict_to="r") if q in region]
            if not [q for q in self._neighborhood(p, restrict_to="r") if q in region]:
                add_sides = True
                n += _new_sides(p)
        
        print(f"ISO {isolated}")
        #if add_sides:
        #    n += _new_sides(p)

        return n

    def _perimeter(self, region):
        p = 0
        for pos in region:
            m = set(self._neighborhood(pos))
            p += (4 - len(m.intersection(region)))
        return p

    def price(self, length_type="perimeter"):
        s = 0
        for p in self.plants:
            debug(f"{p} AREA {self.areas[p]} SIDES {self.sides[p]}")
            lengths = self.perimeters[p] if length_type == "perimeter" else self.sides[p]
            s += mathutils.sum([self.areas[p][i] * lengths[i] for i, _ in enumerate(self.areas[p])])
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
            #    "ABB",
            #    "AAA",
            #    "AAA",
            #    "BBA",
            #]
        )
        self.args_parser.add_argument(
            "--length-type",
            type=str,
            help="calculation",
            choices=["perimeter", "num-sides"],
            default="perimeter",
            dest="length_type",
        )
        self.length_type = self.args_parser.parse_args(run_args).length_type

    def run(self, v):
        p = Plot(v)
        debug(f"PRICE {p.price(length_type=self.length_type)}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
