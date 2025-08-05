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
        test_char = "t"
        trips = self._connections(self._parse(self.input))
        t_trips = [x for x in trips if any([y[0] == test_char for y in x])]
        debug_print(f"N T {self.num_connections} {trips} {len(trips)}")
        return len(t_trips)
    

    def _connections(self, pairs):
        import itertools 
        import math

        t = []
        tt = set()
        n = self.num_connections
        nc = (n * (n - 1)) // 2
        debug_print(f"{n} ELEMENTS -> {nc} CONNECTIONS")
        #all_c = list(itertools.combinations(pairs, nc))
        for p in pairs:
            all_c = itertools.combinations(pairs, nc)
            #pc = []
            debug_print(f"CHECK P {p} IN {math.comb(len(pairs), nc)}")
            #for x in all_c:
                #debug_print(f"CHECK X {x}")
            #    f = any([p[0] in y for y in x]) and any([p[1] in y for y in x])
                #debug_if(f"P {p} IN {x}", f)
            #    if f:
            #        pc.append(x)
                #for y in x:
                #    debug_if(f"P {p} IN {x}", p[0] in y or p[1] in y)
                    #if p[0] in y or p[1] in y:
                        #pc.append(x)
                        #break
            # each element of p must appear in at least one pair in this selection
            pc = [x for x in all_c if any([any([p[0] in y]) and any([p[1] in y]) for y in x])]
            #debug_print(f"P {p} -> PC {len(pc)}")
            # all unique pairs sharing one element of this pair
            s = {x for x in pairs if x[0] in p or x[1] in p}
            # combinations of <num_connections> pairs
            #for e in itertools.combinations(s, nc):
            for e in pc:
                u = set()
                for ee in e:
                    u = u | set(ee)
                # u is the set of all elements
                if len(u) != n or u in t:
                    continue
                debug_print(f"FOUND {self.num_connections}-TUPLE {u} IN {e}")
                t.append(u)
                tt = tt | u
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

