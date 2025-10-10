import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print

class Region:
    def __init__(self, grid, plant):
        self.grid = grid
        self.plant = plant
        self.coords = self._coords(plant, {})


    def is_corner(self, pos):
        x = [x[0] for x in self.coords]
        y = [x[1] for x in self.coords]
        for i in (min(x), max(x)):
            for j in (min(y), max(y)):
                if pos == (i, j):
                    return True
        return False

    def to_grid(self):
        g = []
        rows = set([x[0] for x in self.coords])
        cols = set([x[1] for x in self.coords])
        for r in rows:
            arr = []
            for c in cols:
                p = (r, c)
                if p in self.coords:
                    arr.append(p)
            g.append(arr)
        return g
    
    def _coords(self, p, c, s=None):
        r = s or set([p])
        if not c[p]:
            # plants with no connections are their own regions
            return r
        for n in [x for x in c[p] if x not in r]:
            r.add(n)
            r = r.union(self._coords(n, c, s=r))
        return r
    


class Plot:
    def __init__(self, grid, exclude=None, offset=(0,0)):
        self.grid = Day.Grid(grid)
        self.plants = set()
        for r in self.grid.coord_array:
            self.plants = self.plants.union(set(r))
        self.regions = {}
        self.areas = {}
        self.perimeters = {}
        self.sides = {}
        for p in self.plants:
            if exclude and p == exclude:
                continue
            self.regions[p] = self._regions_for_plant(p, offset=offset)
            self.areas[p] = [len(x) for x in self.regions[p]]
            self.perimeters[p] = [self._perimeter(x) for x in self.regions[p]]
            self.sides[p] = [self._num_sides(p, x) for x in self.regions[p]]
        #for p in self.plants:
        #    n = [self._num_interior_sides(p, x) for x in self.regions[p]]
        #    self.sides[p] = [x + n[i] for i, x in enumerate(self.sides[p])]

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

    def _complement(self, plant, region):
        import time

        # rectangles have no complements
        if self._is_rect(region):
            return None
        
        x = [x[0] for x in region]
        y = [x[1] for x in region]

        grid = []
        for r in range(min(x), max(x) + 1):
            s = ""
            for c in range(min(y), max(y) + 1):
                s += ("+" if (r, c) in region else "-")
            grid.append(s)
        debug_print(f"{plant} G {grid}")
        if not grid:
            return None
        p = Plot(grid, exclude="+", offset=(min(x), min(y)))
        return p
        #return p.regions.get("-", [])
        
    
    def _is_rect(self, region):
        g = self._to_grid(region)
        return all([len(r) == len(list(g)[0]) for r in g])

    def _num_sides(self, plant, region):

        def _new_sides(pos):
            return 2 if self._is_corner(pos, region) else 4
        
        n = 4
        #if self._is_rect(region):
        #    return n
        
        cmp = self._complement(plant, region)
        if cmp is not None:
            #m = 4
            for r in cmp.regions.get("-", []):
                #m = m + cmp._num_sides("-", r)
                nn = cmp._num_sides(plant, r)
                debug_print(f"{plant} ADD {nn}")
                n = n + nn
                if any([self._is_corner(x, r) for x in r]):
                    #m -= 2
                    n -= 2
                #debug_print(f"R {r} M NOW {m}")
                #d = -2 if any([self._is_corner(x, r) for x in r]) else 0
            #debug_print(f"{plant} M {m}")
            debug_print(f"{plant} M {n}")

        #cmp = self._complement(plant, region)
        #debug_print(f"{plant} CMP PLOT REG {cmp.regions}")

        x = [x[0] for x in region]
        y = [x[1] for x in region]

        #for i, r in enumerate(Day.Grid.neighborhoods):
        #    c = (x, y)[i]
        #    for f in (min, max):
        #        for p in [p for p in region if p[i] == f(c)]:
        #            if not [q for q in self.grid.neighborhood(p, restrict_to=r) if q in region]:
        #                debug_print(f"{plant} NEW SIDES {p}: {_new_sides(p)}")
        #                n += _new_sides(p)

        return n
    
    def _num_interior_sides(self, plant, region):
        x = [x[0] for x in region]
        y = [x[1] for x in region]

        n = 0
        for p in self.regions:
            if p == plant:
                continue
            for r in self.regions[p]:
                # must be completely interior
                xr = [x[0] for x in r]
                yr = [x[1] for x in r]
                if min(x) < min(xr) and max(x) > max(xr) and min(y) < min(yr) and max(y) > max(yr):
                    n += self._num_sides(p, r)
        
        debug_print(f"PL {plant} INT {n}")
        return n
    

    def _perimeter(self, region):
        p = 0
        for pos in region:
            m = set(self.grid.neighborhood(pos))
            p += (4 - len(m.intersection(region)))
        return p

    def price(self, length_type="perimeter"):
        s = 0
        for p in self.plants:
            debug_print(f"{p} AREA {self.areas[p]} SIDES {self.sides[p]}")
            lengths = self.perimeters[p] if length_type == "perimeter" else self.sides[p]
            s += mathutils.sum([self.areas[p][i] * lengths[i] for i, _ in enumerate(self.areas[p])])
        return s

    def _regions_for_plant(self, plant, offset=(0, 0)):
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
        for i, r in enumerate(self.grid.coord_array):
            reg.extend([(i + offset[0], j + offset[1]) for j in string.indices(plant, r)])
        conn = {}
        for p in reg:
            n = []
            for q in reg:
                if p != q and p in self.grid.neighborhood(q):
                    n.append(q)
            conn[p] = n
        p_reg = []
        for p in conn:
            r = _region(p, conn)
            if r not in p_reg:
                p_reg.append(r)
        return p_reg


class AdventDay(Day.Base):

    TEST = [
        "AAAA",
        "BBCD",
        "BBCC",
        "EEEC",
    ]

    #COMPLEX = [
    #    "RRRRIICCFF",
    #    "RRRRIICCCF",
    #    "VVRRRCCFFF",
    #    "VVRCCCJFFF",
    #    "VVVVCJJCFE",
    #    "VVIVCCJJEE",
    #    "VVIIICJJEE",
    ###    "MIIIIIJJEE",
    #    "MIIISIJEEE",
    ##    "MMMISSJEEE",
    #]

    COMPLEX = [
        "......CC..",
        "......CCC.",
        ".....CC...",
        "...CCC....",
        "....C..C..",
        "....CC....",
        ".....C....",
        "..........",
        "..........",
        "..........",
    ]

    EX = [
        "EEEEE",
        "EXXXX",
        "EEEEE",
        "EXXXX",
        "EEEEE",
    ]

    RING = [
        "AAA",
        "ABA",
        "AAA",
    ]

    TWO_BLOCK = [
        "AAAAAA",
        "AAABBA",
        "AAABBA",
        "ABBAAA",
        "ABBAAA",
        "AAAAAA",
    ]

    XO = [
        "OOOOO",
        "OXOXO",
        "OOOOO",
        "OXOXO",
        "OOOOO",
    ]

    def __init__(self, run_args):
        super(AdventDay, self).__init__(2024, 12)
        self.args_parser.add_argument(
            "--length-type",
            type=str,
            help="calculation",
            choices=["perimeter", "num-sides"],
            default="perimeter",
            dest="length_type",
        )
        self.length_type = self.args_parser.parse_args(run_args).length_type

    def run(self):
        p = Plot(self.input)
        debug_print(f"PRICE {p.price(length_type=self.length_type)}")

