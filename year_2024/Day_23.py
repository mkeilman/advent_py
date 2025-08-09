import re
import Day
from utils import mathutils
from utils.debug import debug_print, debug_if

class AdventDay(Day.Base):

    TEST = [
        "kh-tc",
        "qp-kh",
        "de-cg",
        "ka-co",
        "yn-aq",
        "qp-ub",
        "cg-tb",
        "vc-aq",
        "tb-ka",
        "wh-tc",
        "yn-cg",
        "kh-ub",
        "ta-co",
        "de-co",
        "tc-td",
        "tb-wq",
        "wh-td",
        "ta-ka",
        "td-qp",
        "aq-cg",
        "wq-ub",
        "ub-vc",
        "de-ta",
        "wq-aq",
        "wq-vc",
        "wh-yn",
        "ka-de",
        "kh-ta",
        "co-tc",
        "wh-qp",
        "tb-vc",
        "td-yn",
    ]

    SIX = [
        "aa-bb",
        "aa-cc",
        "aa-dd",
        "aa-ee",
        "aa-ff",
        "aa-gg",
        "aa-hh",
        "bb-cc",
        "bb-dd",
        "bb-ee",
        "bb-ff",
        "bb-gg",
        "bb-hh",
        "cc-dd",
        "cc-ee",
        "cc-ff",
        "cc-gg",
        "cc-hh",
        "dd-ee",
        "dd-ff",
        "dd-gg",
        "dd-hh",
        "ee-ff",
        "ee-gg",
        "ee-hh",
        "ff-gg",
        "ff-hh",
        "gg-hh",
    ]

    def __init__(self, run_args):
        super(AdventDay, self).__init__(2024, 23)
        self.args_parser.add_argument(
            "--num-connections",
            type=int,
            help="number of connections",
            default=3,
            dest="num_connections",
        )
        self.add_args(run_args)


    def run(self):
        #self.input = AdventDay.SIX
        #test_char = "t"
        #trips = self._connections(self._parse(self.input), num_members=self.num_connections)
        pairs = self._parse(self.input)
        trips = self._connected_set(pairs, num_members=self.num_connections)
        #t_trips = [x for x in trips if any([y[0] == test_char for y in x])]
        #c = self._connected_combos(pairs, num_members=self.num_connections)
        #debug_print(f"N T {self.num_connections} {len(c)}")
        debug_print(f"N T {self.num_connections} {len(trips)}")
        return len(trips)
        #return len(c)
    

    def _connected_set(self, pairs, num_members=2):
        import math
        import time

        # no sets with a single member since they are always defined in pairs
        if num_members <= 1:
            return []
        
        # sets of size >= 3 are "non-trvial" in that they reduce the number of pairs
        # to be considered
        s = []
        c_map = {(): pairs}
        for n in range(2, num_members + 1):
            debug_print(f"N {n} NUM P {len(c_map)}", include_time=True)
            last_loop = n == num_members
            next_map = {}
            i = -1
            t0 = time.time()
            for combo in c_map:
                t1 = time.time()
                i += 1
                do_print = i % 1000 == 0
                p = c_map[combo]
                nc = (n * (n - 1)) // 2 - len(combo)
                debug_if(f"N {n} {i} CONN LEN P {len(p)} NUM COMBOS {math.comb(len(p), nc)}...", condition=do_print, include_time=True)
                cxc = self._connected_combos(p, base_combo=combo, num_members=n, do_print=do_print)
                #debug_if(f"DONE NEXT CXC {len(cxc)}", condition=do_print, include_time=True)
                if not cxc:
                    continue
                if last_loop:
                    # don't calculate next pairs since we won't use them
                    for comp in [self._members(x) for x in cxc]:
                        if comp not in s:
                            s.append(comp)
                    debug_if(f"N {n} LAST LOOP {i} DONE {time.time() - t1}", condition=do_print, include_time=True)
                    continue
                #debug_if(f"N {n} {i} BUIDLING NEXT MAP...", condition=do_print, include_time=True, end="")
                #debug_if(f"DONE NEXT CXC {len(cxc)}", condition=do_print, include_time=True)
                t2 = time.time()
                ms = set()
                for cc in cxc:
                    m = self._members(cc)
                    ms = ms | m
                    # next pairs under consideration must include the members already found
                    next_map[cc] = [x for x in pairs if any([y in x for y in m])]
                debug_if(f"N {n} LOOP {i} DONE LOOP TIME {time.time() - t1} CC TIME {time.time() - t2} CXC {len(cxc)} MEMS {len(ms)}", condition=do_print, include_time=True)
            #debug_print(f"N {n} ASSIGN NEXT MAP", include_time=True)
            c_map = next_map
            debug_print(f"N {n} DONE {time.time() - t0}", include_time=True)
        return s


    def _connected_combos(self, pairs, base_combo=(), num_members=2, do_print=True):
        import itertools 
        import math
        import time
        
        t0 = time.time()
        p = [x for x in pairs if x not in base_combo]
        n = num_members
        nc = (n * (n - 1)) // 2 - len(base_combo)
        #debug_if(f"N {n} NC {nc} NUM P {len(p)} NUM COMBOS {math.comb(len(p), nc)} BASE {base_combo}", condition=do_print, include_time=True)
        comps = self._members(p)
        assert len(comps) >= n
        assert len(p) >= nc

        t = []
        combos = itertools.combinations(p, nc)
        #debug_if(f"BUILING NEXT COMBOS...", condition=do_print, include_time=True, end="")
        for combo in combos:
            c = base_combo + combo
            u = self._members(c)
            if len(u) != n:
                continue
            t.append(c)
        #debug_print(f"{time.time() - t0}")
        #debug_if(f"DONE {time.time() - t0}", condition=do_print, include_time=True)
        return t


    def _connections(self, pairs, num_members=2):
        import itertools 
        import math

        
        return[self._members(x) for x in self._connected_combos(pairs, num_members=num_members)]


    def _members(self, pair_list):
        return {x[0] for x in pair_list} | {x[1] for x in pair_list}


    def _parse(self, grid):
        return [tuple(sorted(re.findall(r"[a-z][a-z]", x))) for x in grid]


    def _triples(self, pairs):
        import itertools 

        t = []
        tt = set()
        for p in pairs:
            # all unique pairs sharing one element of this pair
            s = {x for x in pairs if x[0] in p or x[1] in p}
            # combinations of 3 pairs
            for e in itertools.combinations(s, 3):
                u = set()
                for ee in e:
                    u = u | set(ee)
                if len(u) != 3 or u in t:
                    continue
                t.append(u)
                tt = tt | u
        return t

