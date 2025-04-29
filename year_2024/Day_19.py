import re
import Day
from utils import mathutils
from utils.debug import debug_if
from utils.debug import debug_print

class AdventDay(Day.Base):

    A = [
        "a, aa, aaa, aaa",
        "",
        "aaaa"
    ]

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
        self.input = AdventDay.A
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

        _comb_map = {}

        self.nc = 0
        self.max_depth = 0

        def _combos(arr, depth=0):
            self.nc += 1
            self.max_depth = max(self.max_depth, depth)
            arr_str = "".join(arr)
            #debug_print(f"{depth} START {arr_str}")
            if arr_str in _comb_map:
                #debug_print(f"{depth} FOUND {arr_str} -> {_comb_map[arr_str]}")
                return _comb_map[arr_str]
            
            i = 0
            #debug_if(f"{depth} ADD {arr}", condition=0)
            n = 1
            while i < len(arr):
                #debug_if(f"{depth} {self.nc} CHECK AT I {i}", not self.nc % 1e6)
                y = arr[i]
                # this pattern is already max size - further concatenation is invalid
                if len(y) == self.max_pattern_len:
                    i += 1
                    continue
                j = 1
                #debug_if(f"{depth} CHECK {y} AT {i}/{len(arr)}", condition=1)
                while i + j < len(arr) and len(y) <= self.max_pattern_len:
                    k = i + j
                    y += arr[k]
                    #debug_if(f"{depth} CHECK {y} AT {i}/{len(arr)}", condition=1)
                    j += 1
                    if y not in self.patterns:
                        continue
                    # new array is the old array up to the current index,
                    # then the new pattern, then the rest of the old array
                    new_arr = arr[:i] + [y] + arr[k + 1:]
                    #new_arr =  arr[:k + 1] + [y] + arr[i:]
                    next_arr = new_arr[k:]
                    # no more elements
                    if not next_arr:
                        #debug_if(f"{depth} ADD {new_arr}", condition=0)
                        n += 1
                        #break
                    n += _combos(next_arr, depth=depth + 1)
                i += 1
            #debug_if(f"{depth} {self.nc} DONE {n}", condition=depth == self.max_depth)
            _comb_map[arr_str] = n
            return n

        def _combinations(arr, depth=0):
            m = _combos(arr)
            #debug_print(f"COMBOS? {m}")
            return m
            arr_str = "".join(arr)
            debug_print(f"{depth} START {arr_str}")
            if arr_str in _comb_map:
                #debug_print(f"{depth} FOUND {arr_str} -> {len(_comb_map[arr_str])}")
                return _comb_map[arr_str]
            n = 1
            i = 0
            arrs = [arr]
            #debug_print(f"{depth} DECOMP {len(arr)}")
            #debug_print(f"{depth} DECOMP {arr}")
            while i < len(arr):
                x = arr[i]
                #debug_print(f"{depth} START {x} AT {i}")
                if len(x) == self.max_pattern_len:
                    #debug_print(f"{depth} {x} MAX LEN")
                    i += 1
                    continue
                y = x
                j = 1
                while i + j < len(arr) and len(y) <= self.max_pattern_len:
                    k = i + j
                    y += arr[k]
                    #if len(y) > self.max_pattern_len:
                    #    break
                    #debug_print(f"{depth} CHECK {y} AT {i}")
                    j += 1
                    if y not in self.patterns:
                        continue
                    new_arr = arr[:i] + [y] + arr[k + 1:]
                    #debug_print(f"{depth} POSSIBLE NEW {new_arr}")
                    next_arr = new_arr[k:]
                    # no more elements
                    if not next_arr:
                        #debug_print(f"{depth} NO NEXT IN {new_arr}")
                        arrs.append(new_arr)
                        n += 1
                        break
                    #debug_print(f"{depth} LOOK AFTER {new_arr[:k]} {next_arr}")
                    #n += _combinations(next_arr, ref_arr[k:], depth=depth + 1)
                    #nk = "".join(next_arr)
                    #if nk in _comb_map:
                    #    #debug_print(f"{depth} NEXT ARR IN MAP {nk}")
                    #    aa = _comb_map[nk]
                    #else:
                    aa = _combinations(next_arr, depth=depth + 1)
                    if not aa:
                        #debug_print(f"{depth} NO COMBS USE {new_arr}")
                        arrs.append(new_arr)
                        n += 1
                        continue
                    n += len(aa)
                    debug_print(f"{depth} ADD {len(aa)}")
                    # much too slow for large numbers
                    arrs.extend([new_arr[:k] + a for a in aa])
                    #nnn = 0
                    #for a in aa:
                    #    #n += 1
                    #    arrs.append(new_arr[:k] + a)
                    #    nnn += 1
                    debug_print(f"{depth} DONE ADDING {len(aa)}")
                i += 1
            #debug_print(f"{depth} ALL {arr} -> LEN {len(arrs)} N {n}")
            _comb_map[arr_str] = arrs
            debug_print(f"{depth} DONE {arr_str}")
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
            #debug_print(f"FULL {a} T {"".join(a)} REDUCED {b}")
            #debug_print(f"FIND COMB FOR {a}")
            # increment count if the reduced array differs from the original
            #m += int(b != a)
            #m += _combinations(b, a)
            #if b != a:
            #    cb.append(b)
            #cbb = _combinations(b)
            #cb.extend(cbb)
            #debug_print(f"{a} COMB {cb} {len(cb)}")
            #c.extend(cb)
            #n += len(_combinations(b))
            n += _combos(b)
            #n += m
            #debug_print(f"{''.join(a)} COMB RUNNING TOTAL {n}")
            #break
        #return len(c)
        return n


    def _parse(self):
        # do pattern comparisons from largest to smallest
        self.patterns = sorted(re.split(r",\s*", self.input[0]), key=len, reverse=True)
        self.pattern_lens = set([len(x) for x in self.patterns])
        self.max_pattern_len = max(self.pattern_lens)
        self.patterns_by_len = self._patterns_by_len()
        self.pattern_decomp = self._pattern_decomp()
        #debug_print(f"P {self.patterns} DECOMP {self.pattern_decomp}")
        self.towels = self.input[2:]
        self.nc = 0
    

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
