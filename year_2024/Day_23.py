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
        "bb-cc",
        "bb-dd",
        "bb-ee",
        "bb-ff",
        "cc-dd",
        "cc-ee",
        "cc-ff",
        "dd-ee",
        "dd-ff",
        "ee-ff",
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
        # no sets with a single member since they are always defined in pairs
        if num_members <= 1:
            return []
        if num_members <= 2:
            return [set(x) for x in pairs]
        
        # sets of size >= 3 are "non-trvial" in that they reduce the number of pairs
        c = []
        s = []
        p = pairs
        pa = [pairs]
        for n in range(3, num_members + 1):
            pp = []
            all_c = []
            for i, p in enumerate(pa):
                c = self._connections(p, num_members=n)
                if c in all_c:
                    continue
                debug_print(f"{n} {i} {c}")
                all_c.append(c)
                if n == num_members:
                    s.extend(c)
                for cc in c:
                    # next pairs under consideration must include the members already found
                    p = [x for x in pairs if any([y in x for y in cc])]
                    #debug_print(f"{n} {i} {cc} -> {p}")
                    pp.append(p)
            pa = pp
            #debug_print(f"NEW PA {pa}")
        return s


    def _connected_combos(self, pairs, num_members=2):
        import itertools 
        import math

        def _units(pair_list):
            return {x[0] for x in pair_list} | {x[1] for x in pair_list}
        
        n = num_members
        nc = (n * (n - 1)) // 2
        comps = _units(pairs)
        assert len(comps) >= n
        assert len(pairs) >= nc

        t = []
        for combo in itertools.combinations(pairs, nc):
            u = _units(combo)
            if len(u) != n:
                continue
            t.append(combo)
            #debug_print(f"FOUND CONNECTED {combo}")
        return t


    def _connections(self, pairs, num_members=2):
        import itertools 
        import math

        def _units(pair_list):
            return {x[0] for x in pair_list} | {x[1] for x in pair_list}
        
        return[_units(x) for x in self._connected_combos(pairs, num_members=num_members)]
    
        t = []
        #n = self.num_connections
        n = num_comps
        nc = (n * (n - 1)) // 2
        comps = _units(pairs)
        assert len(comps) >= n
        assert len(pairs) >= nc
        debug_print(f"{len(comps)} COMPS {len(pairs)} PAIRS {n} ELEMENTS -> {nc} CONNECTIONS COMBOS {math.comb(len(pairs), nc)}")

        #for c in comps:
        #    p = [x for x in pairs if c in x]
            #for cc in itertools.combinations(p, nc):

            #debug_print(f"{p} PAIRS HAVE {c}")
            #if len([x for x in pairs if c in x]) < nc - 1:
            #    debug_print(f"NOT ENOUGH PAIRS HAVE {c}")

        
    
        for combo in itertools.combinations(pairs, nc):
            u = _units(combo)
            if len(u) != n:
                continue
            t.append(u)
            debug_if(f"FOUND {self.num_connections}-TUPLE {u} IN {combo} TOTAL {len(t)}", True)
        return t


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

