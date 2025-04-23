import re
import Day
from utils import mathutils
from utils.debug import debug_print

class AdventDay(Day.Base):

    TEST = [
        "r, wr, b, g, bwu, rb, gb, br",
        "",
        "rrbgbr",
        "brwrr",
        "bggr",
        "gbbr",
        "ubwu",
        "bwurrg",
        "brgr",
        "bbrgwb",
    ]

    OVERLAP = [
        "abc, bcd, a",
        "",
        "abcd"
    ]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 19)
        self.args_parser.add_argument(
            "--ignore-permutations",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="ignore_permutations",
        )
        self.add_args(run_args)

    def run(self):
        #self.input = AdventDay.OVERLAP
        self._parse()
        n = self._num_good_towels()
        debug_print(f"GOOD TOWELS {n} / {len(self.towels)}")
        return n
    
    def _check_towel(self, towel, max_length=None):
        i = len(towel) - 1
        ta = []
        k = 0

        m = max_length or self.max_pattern_len + 1
        patterns = [x for x in self.patterns if len(x) < m]

        # do comparisons from the end
        while i >= 0:
            while k < len(patterns):
                p = patterns[k]
                j = i - len(p) + 1
                k += 1
                if towel[j:i + 1] == p:
                    ta.insert(0, p)
                    i = j - 1
                    k = 0
                    break
            else:
                if not len(ta):
                    return []
                # find last pattern with at least 2 characters - if we found a match on a
                # single character we know we cannot replace it with another
                while ta and len(p) <= 1:
                    p = ta.pop(0)
                    i += len(p)
                kp = [x for x in patterns if len(x) < len(p)]
                if not kp:
                    return []
                k = patterns.index(kp[0])

        return ta
    
    
    def _num_good_towels(self):

        #def _combinations(arr, ref_arr, depth=0):
        def _combinations(arr, depth=0):
            n = 0
            i = 0
            arrs = [arr]
            #debug_print(f"{depth} DECOMP {arr}")
            #if len(arr) <= 1:
            #    return 1
            while i < len(arr):
                x = arr[i]
                if len(x) == self.max_pattern_len:
                    #debug_print(f"{x} MAX LEN")
                    i += 1
                    continue
                y = x
                j = 1
                while i + j < len(arr):
                    k = i + j
                    y += arr[k]
                    if len(y) > self.max_pattern_len:
                        break
                    #debug_print(f"{depth} CHECK {y} AT {i}")
                    j += 1
                    if y not in self.patterns:
                        continue
                    new_arr = arr[:i] + [y] + arr[k + 1:]
                    #debug_print(f"{depth} POSSIBLE NEW {new_arr}")
                    #if new_arr == ref_arr:
                        #debug_print(f"{depth} NEW IS REF {new_arr}")
                    #    continue
                    next_arr = new_arr[k:]
                    # no more elements
                    if not next_arr:
                        #debug_print(f"{depth} NO NEXT IN {new_arr}")
                        arrs.append(new_arr)
                        break
                    #debug_print(f"{depth} LOOK AFTER {new_arr[:k]} {next_arr}")
                    #if len(next_arr) > 1:
                    #n += _combinations(next_arr, ref_arr[k:], depth=depth + 1)
                    aa = _combinations(next_arr, depth=depth + 1)
                    if not aa:
                        #debug_print(f"{depth} NO COMBS USE {new_arr}")
                        arrs.append(new_arr)
                        continue
                    #debug_print(f"{depth} COMBS {aa}")
                    for a in aa:
                        #debug_print(f"{depth} FOUND NEW {new_arr[:k] + a}")
                        arrs.append(new_arr[:k] + a)
                i += 1
            #if not depth:
            #debug_print(f"{depth} ALL {arr} -> {arrs} LEN {len(arrs)}")
            return arrs
            #return len(arrs)


        def _reduce(arr):
            s = []
            nn = [self.pattern_decomp[x] for x in arr]
            if all([not x for x in nn]):
                return arr
            for i, x in enumerate(arr):
                if not nn[i]:
                    s.append(x)
                    continue
                s.extend(_reduce(nn[i]))
            return s


        t = [y for y in [self._check_towel(x) for x in self.towels] if y]
        n = 0 #len(t)
        if self.ignore_permutations:
            return len(t)
        
        c = []
        for a in t:
            cb = []
            #c.append(a)
            m = 1
            #n += 1
            b = _reduce(a)
            #debug_print(f"T {"".join(a)} REDUCED {b}")
            #debug_print(f"FIND COMB FOR {a}")
            # increment count if the reduced array differs from the original
            #m += int(b != a)
            #m += _combinations(b, a)
            #if b != a:
            #    cb.append(b)
            cbb = _combinations(b)
            cb.extend(cbb)
            #debug_print(f"{a} COMB {cb} {len(cb)}")
            c.extend(cb)
            #n += m
            #debug_print(f"{a} COMB {m} RUNNING TOTAL {n}")
            break
        return len(c)
        #return n


    def _parse(self):
        # do pattern comparisons from largest to smallest
        self.patterns = sorted(re.split(r",\s*", self.input[0]), key=len, reverse=True)
        self.pattern_lens = set([len(x) for x in self.patterns])
        self.max_pattern_len = max(self.pattern_lens)
        self.patterns_by_len = self._patterns_by_len()
        self.pattern_decomp = self._pattern_decomp()
        #debug_print(f"P {self.patterns} DECOMP {self.pattern_decomp}")
        self.towels = self.input[2:]
    

    def _pattern_decomp(self):
        d = {}
        for p in self.patterns:
            d[p] = self._check_towel(p, max_length=len(p))
        return d


    def _patterns_by_len(self):
        p = []
        for l in self.pattern_lens:
            p.append([x for x in self.patterns if len(x) == l])
        return sorted(p, key=lambda x: len(x[0]), reverse=True)
