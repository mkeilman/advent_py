import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class PathTree:
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.parent = None
        self.children = []
    
    def add(self, node):
        node.parent = self
        self.children.append(node)

    def is_leaf(self):
        return not self.children

    def leaves(self):
        l = []
        for c in self.children:
            if c.is_leaf():
                l.append(c)
                continue
            l.extend(c.leaves())
        return l

    
    def path_to(self, node):
        # go backwards?
        p = [node]
        pp = node.parent
        while pp is not None:
            p.append(pp)
            pp = pp.parent
        return reversed(p)

        
    def to_string(self):
        # avoid nested f-strings
        s = "" + f"{self.unique_id}" + ": ["
        for c in self.children:
            s = s + c.to_string()
        s += "]"
        return s
    

class Terrain:
    def __init__(self, grid):
        self.grid = grid
        self.size = [len(self.grid), len(self.grid[0])]
        self.trailheads = self._trailheads()
    

    def _is_in_grid(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]

    def _trailheads(self):
        th = []
        for i, r in enumerate(self.grid):
            th.extend([(i, j) for j in string.indices("0", r)])
        return th


    def _paths(self, pos):
        def _neighborhood(pos):
            n = []
            for p in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                q = (pos[0] + p[0], pos[1] + p[1])
                if self._is_in_grid(q) and self._val(q) == self._val(pos) + 1:
                    n.append(q)
            return n
        
        def _path(pos):
            t = PathTree(pos)
            #path = [pos]
            #pp = []
            #debug(f"P {pos} N {n}")
            for p in _neighborhood(pos):
                # new array for every pos in neighborhood
                #pp = [pos]
                v = self._val(p)
                if v == self._val(pos) + 1:
                    pt = _path(p)
                    t.add(pt)
                    #debug(f"PATH FROM {t.unique_id} TO {pt.unique_id} {[x.unique_id for x in t.path_to(pt)]}")
                #debug(f"POS {pos} N {p}")
                #path.extend(_path(p))
                #pp = pp + _path(pos)
            #path.append(pp)
            return t
            #return path

        #debug(f"P {trailhead} N {_neighborhood(trailhead)}")
        #debug(f"{[x for x in _neighborhood(trailhead) if self._val(x) == self._val(trailhead) + 1]}")
        
        paths = []
        p = _path(pos)
        #for l in p.leaves():
        #    debug(f"P {p.unique_id} TO {l.unique_id}: {[x.unique_id for x in p.path_to(l)]}")
        paths.append(p)
        #if p and self._val(p[-1]) == 9:
        #    paths.append(p)

        #for p in [x for x in _neighborhood(trailhead) if self._val(x) == self._val(trailhead) + 1]:
            #paths.extend(self._paths(p))

        return paths


    def _val(self, pos):
        return int(self.grid[pos[0]][pos[1]])

class Path:
    def __init__(self, grid):
        self.grid = grid
    
        

class AdventDay(Day.Base):
            
    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            10,
            #[
            #    "89010123",
            #    "78121874",
            #    "87430965",
            #    "96549874",
            #    "45678903",
            #    "32019012",
            #    "01329801",
            #    "10456732",
            #]
            [
                "012345",
                "199996",
                "299997",
                "399958",
                "499999",
                "599999",
                "659999",
                "788999",
            ]
            #[
            #    "01234",
            #    "98765",
            #]
        )
        self.args_parser.add_argument(
            "--whole-files",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="whole_files",
        )
        self.whole_files = self.args_parser.parse_args(run_args).whole_files

    def run(self, v):
        t = Terrain(v)
        p = t._paths(t.trailheads[0])
        #debug(f"P {p[0]} L {len(p[0])} V {[t._val(x) for x in p[0]]}")
        debug(f"P {[x.unique_id for x in p[0].leaves()]}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
