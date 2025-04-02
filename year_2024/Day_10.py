import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print

class PathTree:
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.parent = None
        self.children = []
    
    def add(self, node):
        node.parent = self
        self.children.append(node)


    def descendants(self):
        d = self.children[:]
        for c in self.children:
            d.extend(c.descendants())
        return d
        

    def find_node(self, node_id):
        if node_id == self.unique_id:
            return self
        
        d = self.descendants()
        ids = [x.unique_id for x in d]
        if node_id in ids:
            return [ids.index(node_id)]
        return None

        #for c in self.children:
        #    #debug_print(f"CHECK {c.unique_id} VS {node_id}")
        #    if c.unique_id == node_id:
        #        #debug_print("FOUND")
        #        return c
        #    return c.find_node(node_id)
        #return None

    def is_leaf(self):
        return not self.children

    def leaves(self):
        #l = []
        #for c in self.children:
        #    #debug_print(f"{self.unique_id} SO FAR {[x.unique_id for x in l]}")
        #    if c.is_leaf() and c.unique_id not in [x.unique_id for x in l]:
        #        #debug_print(f"{self.unique_id} LEAF {c.unique_id}")
        #        l.append(c)
        #        continue
        #    for ll in c.leaves():
        #        if ll.is_leaf() and ll.unique_id not in l:
        #            l.append(ll)
        #    #l.extend()
        return [self.find_node(x) for x in self.leaf_ids()]
    
    def leaf_ids(self):
        l = set()
        for c in self.children:
            if c.is_leaf():
                l.add(c.unique_id)
                continue
            l = l.union(c.leaf_ids())
            #for ll in c.leaves():
            ##    if ll.is_leaf():
            #        l.add(ll.unique_id)
        return l

    def leaf_routes(self):
        return [self.route(x) for x in self.leaves()]
    
    def prune(self, node_id):
        n = self.find_node(node_id)
        if not n:
            return
        n.children = []
        del n.parent[n]
        

    def route(self, node):
        # go backwards?
        p = [node]
        pp = node.parent
        while pp is not None:
            p.append(pp)
            pp = pp.parent
        p.reverse()
        return p

        
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
    

    def th_routes(self):
        r = []
        for th in self.trailheads:
            p = self._paths(th)
            r.append([x.leaf_routes() for x in p if len(x.leaf_routes()) == 10])
        return r

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
            for p in _neighborhood(pos):
                v = self._val(p)
                if v == self._val(pos) + 1:
                    t.add(_path(p))
            return t

        #debug_print(f"P {trailhead} N {_neighborhood(trailhead)}")
        #debug_print(f"{[x for x in _neighborhood(trailhead) if self._val(x) == self._val(trailhead) + 1]}")
        
        #paths = []
        #p = _path(pos)
        #for l in p.leaves():
        #    debug_print(f"P {p.unique_id} TO {l.unique_id}: {[x.unique_id for x in p.path_to(l)]}")
        #paths.append(p)
        #if p and self._val(p[-1]) == 9:
        #    paths.append(p)

        #for p in [x for x in _neighborhood(trailhead) if self._val(x) == self._val(trailhead) + 1]:
            #paths.extend(self._paths(p))

        return _path(pos)
        #return paths


    def _val(self, pos):
        return int(self.grid[pos[0]][pos[1]])

            

class AdventDay(Day.Base):
    
    SPLIT = [
        "012345",
        "199996",
        "299997",
        "399958",
        "499999",
        "599999",
        "659999",
        "789999",
    ]

    TEST = [
        "89010123",
        "78121874",
        "87430965",
        "96549874",
        "45678903",
        "32019012",
        "01329801",
        "10456732",
    ]

    TWO = [
        "01234",
        "98765",
        "01234",
        "98765",
    ]

    def __init__(self, year, day, run_args):
        import argparse
        super(AdventDay, self).__init__(
            year,
            day,
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
        #p = t._paths(t.trailheads[0])
        #debug_print(f"TH {t.trailheads}")
        n = 0
        for th in t.trailheads:
            pt = [x for x in t._paths(th).leaves()]
            debug_print(f"TH {th} LEN {[x.unique_id for x in t._paths(th).descendants()]}")
            n += len(pt)
            for r in pt:
                pass
                #debug_print(f"TH {th} LEN {len(pt)}")
                #debug_print(f"TH {th}  {[(x.unique_id, t._val(x.unique_id)) for x in r]}")

        debug_print(f"N {n}")
        #thr = t.th_routes()
        #debug_print(f"P {p[0]} L {len(p[0])} V {[t._val(x) for x in p[0]]}")
        #for p in thr:
        #    for pp in p:
        #        for r in pp:
        #            debug_print(f"RR {[rr.unique_id for rr in r]}")



def main():
    d = AdventDay()
    debug_print("TEST:")
    d.run_from_test_input()
    debug_print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
