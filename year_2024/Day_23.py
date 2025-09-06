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
        
        sample_freq = 1000
        # sets of size >= 3 are "non-trvial" in that they reduce the number of pairs
        # to be considered
        s = []
        c_map = {(): pairs}
        for n in range(2, num_members + 1):
            debug_print(f"N {n} NUM COMBOS {len(c_map)}", include_time=True)
            last_loop = n == num_members
            next_map = {}
            i = -1
            t0 = time.time()
            for combo in c_map:
                t1 = time.time()
                i += 1
                do_print = i % sample_freq == 0
                p = c_map[combo]
                #debug_print(f"CM {combo} P {p}")
                nc = (n * (n - 1)) // 2 - len(combo)
                debug_if(f"N {n} NC {nc} LOOP {i} NUM PAIRS {len(p)} NUM COMBOS {math.comb(len(p), nc)}...", condition=do_print, include_time=True)
                combos = self._connected_combos(p, base_combo=combo, num_members=n, do_print=do_print)
                debug_if(f"DONE NEXT combos {len(combos)}", condition=do_print, include_time=True)
                if not combos:
                    continue
                if last_loop:
                    # don't calculate next pairs since we won't use them
                    for comp in [self._members(x) for x in combos]:
                        if comp not in s:
                            s.append(comp)
                    debug_if(f"N {n} LAST LOOP {i} DONE {time.time() - t1}", condition=do_print, include_time=True)
                    continue
                t2 = time.time()
                for cc in combos:
                    np = self._next_pairs(pairs, cc, do_print)
                    #debug_print(f"{cc} -> {np}")
                    if np:
                        next_map[cc] = np
                t = time.time()
                debug_if(f"N {n} LOOP {i} DONE LOOP TIME {t - t1} CC TIME {t - t2} TOTAL TIME {t - t0}", condition=do_print, include_time=True)
            c_map = next_map
            debug_print(f"N {n} DONE {time.time() - t0}", include_time=True)
        return s


    def _connected_combos(self, pairs, base_combo=(), num_members=2, do_print=True):
        import itertools 
        import math
        import time
        
        p = pairs
        n = num_members
        nc = (n * (n - 1)) // 2 - len(base_combo)
        #debug_if(f"N {n} NC {nc} NUM P {len(p)} NUM COMBOS {math.comb(len(p), nc)} BASE {base_combo}", condition=do_print, include_time=True)
        if len(self._members(p)) < n or len(p) < nc:
            return []

        combos = itertools.combinations(p, nc)
        #debug_if(f"BUILING NEXT COMBOS...", condition=do_print, include_time=True, end="")
        return [base_combo + x for x in combos if len(self._members(base_combo + x)) == n]


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


    def _next_pairs(self, pairs, combo, do_print=False):
        import time

        #t0 = time.time()
        current_m = self._members(combo)
        # next pairs under consideration must include the individual members already found,
        # but not the pairs already found
        next_pairs = [x for x in pairs if x not in combo and any([self._has_member(y, x) for y in current_m])]
        #t = time.time()
        #debug_if(f"DT FOR RAW NEXT PAIRS {t - t0}", condition=do_print)
        # new members
        for new_m in self._members(next_pairs) - current_m:
            # pairs that have one new member and one current member
            np = [tuple(sorted((x, new_m))) for x in current_m]
            # mixed pairs not among the next pairs
            nnp = [x for x in np if x not in next_pairs]
            for new_pair in nnp:
                #if new_pair in next_pairs:
                #    continue
                debug_print(f"NEWP {new_pair}")
                for p in [x for x in np if x in next_pairs]:
                    debug_print(f"DEL {p}")
                    del next_pairs[next_pairs.index(p)]
        #t = time.time()
        #debug_if(f"DT FOR FILTERED NEXT PAIRS {t - t0}", condition=do_print)
        return next_pairs


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

