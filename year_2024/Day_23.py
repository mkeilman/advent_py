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
        "yy-zz",
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
        #comps = self._member_count(pairs)
        #debug_print(f"COMPS {comps}")
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
        #c_map = {(): [self._members(x) for x in pairs]}
        for n in range(2, num_members + 1):
            #debug_print(f"N {n} NUM P {len(c_map)}", include_time=True)
            last_loop = n == num_members
            next_map = {}
            i = -1
            t0 = time.time()
            for combo in c_map:
                t1 = time.time()
                i += 1
                do_print = i % 1000 == 0
                p = c_map[combo]
                #c = c_map[combo]
                #p = [x for x in pairs if any([y in x for y in c])]
                #debug_print(f"CM {c} P {p}")
                nc = (n * (n - 1)) // 2 - len(combo)
                debug_if(f"N {n} {i} CONN LEN P {len(p)} NUM COMBOS {math.comb(len(p), nc)}...", condition=do_print, include_time=True)
                combos = self._connected_combos(p, base_combo=combo, num_members=n, do_print=do_print)
                #debug_if(f"DONE NEXT combos {len(combos)}", condition=do_print, include_time=True)
                if not combos:
                    continue
                if last_loop:
                    # don't calculate next pairs since we won't use them
                    for comp in [self._members(x) for x in combos]:
                        if comp not in s:
                            s.append(comp)
                    debug_if(f"N {n} LAST LOOP {i} DONE {time.time() - t1}", condition=do_print, include_time=True)
                    continue
                #debug_if(f"N {n} {i} BUIDLING NEXT MAP...", condition=do_print, include_time=True, end="")
                #debug_if(f"DONE NEXT combos {len(combos)}", condition=do_print, include_time=True)
                t2 = time.time()
                #ms = set()
                for cc in combos:
                    m = self._members(cc)
                    #debug_print(f"M {m}")
                    #ms = ms | m
                    # next pairs under consideration must include the members already found
                    next_pairs = [x for x in pairs if x not in cc and any([self._has_member(y, x) for y in m])]
                    new_members = self._members(next_pairs) - m
                    for newm in new_members:
                        np = [tuple(sorted((x, newm))) for x in m]
                        ok = True
                        for ppp in np:
                            if ppp not in next_pairs:
                                #debug_print(f"INVALID NEWM {newm}: {ppp} NOT IN {next_pairs}")
                                ok = False
                                break
                            #else:
                            #    debug_print(f"OK NEWM {newm}")
                        #debug_print(f"{newm} NP {np} VS {next_pairs}")
                        #ok = ok and all([x in next_pairs for x in np])
                        #debug_print(f"{np} VS {next_pairs}")
                        #debug_if(f"N {n} VALID NEWM {newm}", condition=ok)
                        if not ok:
                            for ppp in [x for x in np if x in next_pairs]:
                                del next_pairs[next_pairs.index(ppp)]
                                #debug_print(f"DEL {ppp}")
                    next_map[cc] = next_pairs
                    #debug_print(f"NEXT PAIRS {cc} -> {next_pairs}")
                    #next_map[cc] = [x for x in pairs if any([y in x for y in m])]
                    #next_map[cc] = self._members(cc)
                debug_if(f"N {n} LOOP {i} DONE LOOP TIME {time.time() - t1} CC TIME {time.time() - t2}", condition=do_print, include_time=True)
            c_map = next_map
            debug_print(f"N {n} DONE {time.time() - t0}", include_time=True)
        return s


    def _connected_combos(self, pairs, base_combo=(), num_members=2, do_print=True):
        import itertools 
        import math
        import time
        
        t0 = time.time()
        #p = [x for x in pairs if x not in base_combo]
        p = pairs
        n = num_members
        nc = (n * (n - 1)) // 2 - len(base_combo)
        #debug_if(f"N {n} NC {nc} NUM P {len(p)} NUM COMBOS {math.comb(len(p), nc)} BASE {base_combo}", condition=do_print, include_time=True)
        comps = self._members(p)
        if len(comps) < n:
            #debug_print(f"NOT ENOUGH COMPS: {len(comps)} < {n}")
            return []
        #assert len(comps) >= n
        if len(p) < nc:
            #debug_print(f"NOT ENOUGH COMBOS: {len(p)} < {nc}")
            return []
        #assert len(p) >= nc

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


    def _has_member(self, member, pair):
        return member in pair


    def _members(self, pair_list):
        return {x[0] for x in pair_list} | {x[1] for x in pair_list}


    def _member_count(self, pair_list):
        counts = {}
        m = self._members(pair_list)
        for c in m:
            if c not in counts:
                counts[c] = 0
            for p in pair_list:
                if c in p:
                    counts[c] += 1
        return counts


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

