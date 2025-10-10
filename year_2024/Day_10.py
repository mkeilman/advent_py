import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print, debug_if

class PathTree:
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.parent = None
        self.children = []


    def __eq__(self, other_tree):
        return self.unique_id == other_tree.unique_id


    def __repr__(self):
        return f"{self.unique_id}"

    
    def add(self, node):
        node.parent = self
        self.children.append(node)


    def descendants(self):
        d = self.children[:]
        for c in self.children:
            d.extend([x for x in c.descendants() if x not in d])
        return d
        

    def find_node(self, node_id):
        if node_id == self.unique_id:
            return self
        
        d = self.descendants()
        ids = [x.unique_id for x in d]
        if node_id in ids:
            return d[ids.index(node_id)]
        return None
    

    def is_leaf(self):
        return not self.children


    def leaves(self):
        return [self.find_node(x) for x in self.leaf_ids()]
    

    def leaf_ids(self):
        l = set()
        for c in self.children:
            if c.is_leaf():
                l.add(c.unique_id)
                continue
            l = l | c.leaf_ids()
        return l


    def leaf_routes(self):
        return [self.route(x) for x in self.leaves()]
        

    def route(self, node):
        # go backwards?
        p = [node]
        pp = node.parent
        while pp is not None:
            p.append(pp)
            pp = pp.parent
        p.reverse()
        return p
    

    def routes(self, node, parent=None, depth=0):
        p = parent or self
        if not p.find_node(node):
            return [], 0
        
        if not p.children:
            return [], 1
        
        r = []
        leaf_count = 0
        for c in p.children:
            r.append(c)
            rr, lc = self.routes(node, parent=c, depth=depth + 1)
            leaf_count += lc
            if rr:
                r.append(rr)
        return r, leaf_count
    

class Terrain:
    def __init__(self, grid):
        self.grid = grid
        self.size = [len(self.grid), len(self.grid[0])]
        self.trailheads = self._trailheads()
        self.summits = self._summits()
    

    def th_routes(self):
        r = []
        for th in self.trailheads:
            r.append(self._path_tree(th).leaf_routes())
        return r
    

    def summit_routes(self):
        return [x for x in self.th_routes() if x[-1] in self.summits];


    def _elevations(self, e):
        arr = []
        for i, r in enumerate(self.grid):
            arr.extend([(i, j) for j in string.indices(e, r)])
        return arr


    def _is_in_grid(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]


    def _trailheads(self):
        return self._elevations("0")
    

    def _summits(self):
        return self._elevations("9")


    def _path_tree(self, pos):
        def _neighborhood(pos):
            n = []
            for p in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                q = (pos[0] + p[0], pos[1] + p[1])
                # count only positions whose values are one greater than pos
                if self._is_in_grid(q) and self._val(q) == self._val(pos) + 1:
                    n.append(q)
            return n
        
        def _path(pos):
            t = PathTree(pos)
            for p in _neighborhood(pos):
                t.add(_path(p))
            return t


        return _path(pos)


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

    THREE = [
        "9999909",
        "9943219",
        "9959929",
        "9965439",
        "9979949",
        "2287659",
        "2292222",
    ]

    TWO_TWO_SEVEN = [
        "012345",
        "123456",
        "234567",
        "345678",
        "486789",
        "567898",
    ]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 10)
        self.args_parser.add_argument(
            "--count-routes",
            action=argparse.BooleanOptionalAction,
            default=False,
            dest="count_routes",
        )
        self.count_routes = self.args_parser.parse_args(run_args).count_routes

    def run(self):
        #self.input = AdventDay.TWO_TWO_SEVEN
        t = Terrain(self.input)
        th_scores = 0
        th_ratings = 0
        for th in t.trailheads:
            pt = [x for x in t._path_tree(th).leaves() if x.unique_id in t.summits]
            th_scores += len(pt)
    
            if not self.count_routes:
                continue

            for s in t.summits:
                r, lc = t._path_tree(th).routes(s)
                if not r:
                    continue
                th_ratings += lc

        debug_print(f"N {th_scores} NT {th_ratings}")
        return th_ratings if self.count_routes else th_scores
