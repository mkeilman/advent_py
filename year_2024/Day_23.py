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
        #"aa-ee",
        #"aa-ff",
        "bb-cc",
        #"bb-dd",
        #"bb-ee",
        #"bb-ff",
        #"cc-dd",
        #"cc-ee",
        #"cc-ff",
        #"dd-ee",
        #"dd-ff",
        #"ee-ff",
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
        trips = self._connected_set(self._parse(self.input), num_members=self.num_connections)
        #t_trips = [x for x in trips if any([y[0] == test_char for y in x])]
        debug_print(f"N T {self.num_connections} {trips} {len(trips)}")
        return len(trips)
    

    def _connected_set(self, pairs, num_members=2):
        import math
        import time

        # no sets with a single member since they are always defined in pairs
        if num_members <= 1:
            return []
        #if num_members <= 2:
        #    return [set(x) for x in pairs]
        
        # sets of size >= 3 are "non-trvial" in that they reduce the number of pairs
        c = []
        #c_map = {}
        s = []
        #p = pairs
        #pa = [pairs]
        c_map = {(): pairs}
        for n in range(2, num_members + 1):
            debug_print(f"N {n} NUM P {len(c_map)}")
            #pp = []
            #ppp = set()
            #all_c = []
            last_loop = n == num_members
            next_map = {}
            #for i, p in enumerate(pa):
            i = -1
            for combo in c_map:
                i += 1
                #debug_print(f"COMBO {combo}")
                p = c_map[combo]
                nc = (n * (n - 1)) // 2 - len(combo)
                debug_if(f"N {n} {i} CONN LEN P {len(p)} NUM COMBOS {math.comb(len(p), nc)}...", condition=i % 1000 == 0, include_time=True)
                cxc = self._connected_combos(p, base_combo=combo, num_members=n)
                #c = self._connections(p, num_members=n)
                c = [self._members(x) for x in cxc]
                #debug_print(f"DONE", include_time=True)
                if not c: # or c in all_c:
                    continue
                #debug_print(f"{n} {i} {len(c)}", include_time=True)
                #all_c.append(c)
                if last_loop:
                    for comp in c:
                        if comp not in s:
                            s.append(comp)
                    continue
                #for cc in c:
                #c_map = {}
                for cc in cxc:
                    # next pairs under consideration must include the members already found
                    # sorted so we can avoid pair arrays alreay added
                    #sp = sorted([x for x in pairs if any([y in x for y in cc])])
                    tcc = tuple(cc)
                    sp = [x for x in pairs if any([y in x for y in self._members(cc)])]
                    next_map[tcc] = sp
                    #debug_print(f"{n} {i} {cc} -> {sp}")
                    #ppp = ppp | set(p)
                    #if sp not in pp:
                    #    pp.append(sp)
            #pa = pp
            #debug_print(f"NEW PA {pa} SET {ppp}")
            c_map = next_map
            debug_print(f"N {n} DONE")
        return s


    def _connected_combos(self, pairs, base_combo=(), num_members=2):
        import itertools 
        import math
        
        p = [x for x in pairs if x not in base_combo]
        n = num_members
        nc = (n * (n - 1)) // 2 - len(base_combo)
        #debug_print(f"N {n} NC {nc} NUM P {len(p)} NUM COMBOS {math.comb(len(p), nc)} BASE {base_combo}")
        comps = self._members(p)
        assert len(comps) >= n
        assert len(p) >= nc

        t = []
        combos = itertools.combinations(p, nc)
        #if base_combo:
        #    new_c = []
        #    #for x in combos:
        #    #    debug_print(f"CHECK FOR {base_combo} IN {x}")
        #    combos = [x for x in combos if all([y for y in base_combo if y in x])]
        #    debug_print(f"NEW C LEN {len(combos)}")
        for combo in combos:
        #for combo in [x for x in combos if len(self._members(x)) == n]:
            c = base_combo + combo
            #u = self._members(combo)
            u = self._members(c)
            if len(u) != n:
                continue
            #t.append(combo)
            t.append(c)
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

