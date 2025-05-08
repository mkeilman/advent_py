import re
import Day
from utils import mathutils
from utils.debug import debug_if
from utils.debug import debug_print
from utils.string import get_chars

class AdventDay(Day.Base):

    A = [
        "a, aa, aaa, aaaa",
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
        "abc, bcd, a, d",
        "",
        "abcd",
    ]

    FILE_TEST = [
        "X, wugw, wrrbgr, rbgr, bgbrb, wuwb, bug, wubur, uwbuwbug, wruu, rbbr, wbgrrg, uuwr, bub, brbggggr, brgguw, gwwuu, uwrbggw, wuwrrr, wbuurww, wwwuwru, gubgr, gubu, ug, ubu, gggrgr, wg, wrgbggu, uwgwubw, bgrgb, uu, gbug, gwuwgr, bgwg, rurgb, rr, ubw, wrr, rggw, ubuu, ubr, ugrr, wrbwrruw, uw, ruggrb, urwwurg, gwr, rurwb, bu, uuu, bbuwb, urbu, ugb, uruub, gwgrrw, wbbw, rwgr, wur, bwbu, bbg, wrbugw, brgr, uurrwg, guruu, uurrrbw, bwwbrguw, gbbgu, bgg, bbwwgbw, rww, uurrr, bgubwb, wwgr, gw, wrgub, wgrg, rugwbb, bgwbuguw, brg, ggbw, bgbubb, wwgu, gwgb, grur, gubw, wbruug, rg, brubbgw, uuugr, rru, brbr, rwbuuu, ubuw, rgru, rwrwgb, wub, rwbu, bwwrr, bwrg, uggbur, gwb, gbugwb, br, rbwu, urubg, uuw, rbb, rgrwu, bguuw, w, www, wurgb, rwwu, rwg, uww, gbwurubb, uuugb, rbrurw, gggbwu, rbrwrgwr, bw, uwrw, bugw, brgguugb, brubw, bbrb, bru, urgr, urwu, bwbb, bur, rwrr, wrrbu, guu, ggugwuw, rwrurb, wbur, gbu, bbb, ur, brw, wrwbb, ugbuwgug, rrugbbru, wwggbw, gwgwgur, rgw, rwwr, wrg, wugrwru, ggwr, ggr, wug, ugu, gbbw, wgww, gwwwuw, gbr, rbwwru, bbru, ruw, gbrgw, gug, bwbuwrb, uwg, rbww, bbbrb, ub, rgrbr, ubg, wugwub, bgr, ru, bwr, bwbug, rgr, wwugr, grg, rwu, wbgg, rgwu, ubugubr, buggur, wwb, rub, wugbb, uubb, uwb, wbb, uwgbw, rubrg, rwubgu, wgwbb, bubrbrww, bg, wwrggu, gr, gggr, ggb, wuuuu, bggwb, ubgrwbr, rgubwu, rwr, gbww, wgbub, ubrb, ruu, rgg, wgrwurrw, ubwggr, uubr, wrwrbrr, ruguw, bwu, guwrug, bgggw, urubr, rruruuw, gur, wrgru, wb, rgwwg, rrguu, wwwugg, rgbg, uwwgg, urr, gwu, ruwb, buwbgur, bbwugb, bubu, rwurwg, wgrb, rrw, uwgwr, ugwu, rgrurg, ww, uwgrrrgb, wrub, bgb, grr, bgwbru, wr, brrbg, rurur, wgbbbur, brwgg, bwgwbw, uuurg, rw, uuwguu, guw, bwg, bwrrwrr, ugr, rbwrg, rwb, urw, uubg, bbwrugr, bgw, brb, rb, rbr, ubbwurb, gbw, buu, wgg, wbw, ugguubw, rurbr, rrwbuur, ubwuwr, urg, wwu, wrguwb, bbgbur, grb, gww, gb, buw, bwbg, grgb, bbu, rbw, rrbu, gruwbw, uur, wwbgr, bwbwu, bgug, uwu, wubbw, rgwr, rrgrr, gwg, bbbubu, wwgrbrw, wuuubb, gbg, uwbwbg, wgwbr, ububb, ubbb, rug, gwbbrb, ubrub, urb, ggrwrgg, rrg, wbr, uub, wbrwbb, ugg, wrgb, bbwu, grurwb, uwbr, ugug, grw, gru, rwgu, wrru, rwgggu, rrr, ugwb, rrrw, brr, buwb, rbwbrg, ugw, rwuuguw, bwgggwb, bugr, wggbrr, uwgrrbub, bgbuuwug, burrrbu, wubwuu, ubwur, ubgwb, uru, brrb, wgb, bwuwgbu, wwuwwbu, bgbbg, wwru, wgr, ggg, guwuu, brbg, gbrb, ugrg, wwgur, wbbu, rwug, gbb, wugr, wuur, ubwurrwg, gwruubgu, wrrw, wubwwg, gugur, urgwu, wrbu, wbg, grwb, ugrrrrb, grbg, ggbbu, gbru, wgw, ggug, ubuub, ggu, wuwrbugb, ugrrrr, gbbubrr, rbgbb, bwwbu, uwwu, wwgbbb, gbbu, b, brwgr, wrb, rwrrw, rubwugg, bbr, wwr, wu, bbgwgbb, rbg, rwwgbbu, bgu, wubuug, ubwww, uggr, rbbbw, rbwgwrbw, bbw, bbgr, rur, ubb, uurbg, wguwb, ubbrgug, wrwr, rwwugb, uwrubb, rrgbbru, bwb, gub, ggbu, wwg, bww, ruwrwg, gbwu, wuu, gbbur, wrubru, rgb, grugwbbw, r, rwww, rbbru, wbrrb, rwgub, ubbrr, wuw, uug, rgu, rggg, bb, g, wru, urgw, ggw, ugwwbrg, grrbw, rbu, bbgugrw, grguw",
        "",
        "bubXbubXbub",
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
        #s, i, o = get_chars(["abc", "def", "gh"], offset=1, num_chars=6)
        #debug_print(f"S {s} I {i} O {o}")
        #return 0
        if self.mode == "test":
            pass
            self.input = AdventDay.A
        self._parse()
        #for t in self.towels:
        #    debug_print(f"T {t} NP {self._ng(t)}")
        #return 0
        n = self._num_good_towels()
        debug_print(f"GOOD TOWELS {n} / {len(self.towels)}")
        return n
    
    def _trailing_patterns(self, towel, max_patterns=0):
        k = 0
        n = 1
        tp = []

        while k < len(self.patterns):
            p = self.patterns[k]
            k += 1
            if towel[-len(p):] == p:
                tp.append(p)
                if max_patterns and n >= max_patterns:
                    return tp
                n += 1
        return tp

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
    
    def _ng(self, towel):
        _p_map = {}

        i = 0

        def _build_p_map(t, depth=0):
            if t not in _p_map:
                _p_map[t] = self._trailing_patterns(t)
            tp = _p_map[t]
            
            debug_print(f"{depth} MAP {_p_map}")
            if not tp:
                return
            n = len(tp)
            for p in tp:
                tt = t[:-len(p)]
                if not tt or tt in _p_map:
                    continue
                _build_p_map(tt, depth=depth + 1)
            return

        def _num_good_patterns(t, depth=0):
            if t not in _p_map:
                return 0
                #_p_map[t] = self._trailing_patterns(t)
            tp = _p_map[t]
            
            #debug_print(f"{depth} T {t} TP {tp}")
            #if not tp:
            #    return 0
            n = 0
            for p in tp:
                tt = t[:-len(p)]
                if not tt:
                    continue
                n += _num_good_patterns(tt, depth=depth + 1)
                #ttpp = self._trailing_patterns(tt)
                #debug_print(f"{depth} TT {tt} TTPP {ttpp} P {p}")
                #if not ttpp:
                #    continue
                #n += 1
                
            return n
        
        _build_p_map(towel)
        return 0 #_num_good_patterns(towel)
            
    def _num_good_towels(self):

        _comb_map = {}

        self.nc = 0
        self.max_depth = 0

        def _combos(arr, prev_arr=[], depth=0):
            #arr = _reduce(a)
            self.nc += 1
            self.max_depth = max(self.max_depth, depth)
            #if not arr:
            #    return 0
            arr_str = "".join(arr)
            debug_print(f"{depth} START {arr}")
            #if arr_str in _comb_map:
            #    debug_print(f"{depth} FOUND {arr_str} -> {_comb_map[arr_str]}")
            #    return _comb_map[arr_str]
            
            i = 0
            #debug_if(f"{depth} ADD {arr}", condition=not depth)
            n = 1
            while i < len(arr):
                y = arr[i]
                r = "".join(arr[i + 1:])
                # this pattern is already max size - further concatenation is invalid
                if len(y) == self.max_pattern_len:
                    debug_if(f"{depth} MAX {y}", condition=1)
                    i += 1
                    continue
                #j = 1
                j = i
                o = 1
                # GET CHARS INDEX SEPERATE FROM I
                debug_if(f"{depth} CHECK '{y}' AT INDEX {i}/{len(arr)} REMAINDER {r}", condition=1)
                #while i + j < len(arr) and len(y) <= self.max_pattern_len:
                #while j < len(r) and len(y) <= self.max_pattern_len:
                while len(y) <= self.max_pattern_len and o is not None and j is not None:
                    #k = i + j
                    #y += arr[k]
                    #rr = r[j + 1:].split()
                    #rrc = self._check_towel(r[j + 1:])
                    s, j, o = get_chars(arr, index=j, offset=o)
                    debug_if(f"{depth} S {s} INDEX {j} OFFSET {o}", condition=1)
                    rrc = [arr[j][o:]] + arr[j + 1:] if j is not None and o is not None else []
                    #v_rrc = self._check_towel("".join(rrc))
                    #y += r[j]
                    if s is not None:
                        y += s
                    debug_if(f"{depth} INDEX {j} Y {y} RRC {rrc}", condition=1)
                    #j += 1
                    if y not in self.patterns: # or not rrc:
                        #debug_if(f"{depth} BAD {y} RRC {rrc} V {v_rrc}", condition=1)
                        continue
                    # new array is the old array up to the current index,
                    # then the new pattern, then the rest of the old array
                    #new_arr = arr[:i] + [y] + arr[k + 1:]
                    new_arr = prev_arr + [y] + rrc
                    #debug_print(f"{depth} POSSIBLE NEW {arr[:i]}+{[y]}+{arr[k + 1:]} = {new_arr}")
                    debug_print(f"{depth} POSSIBLE NEW {prev_arr}+{[y]}+{rrc} = {new_arr}")
                    #next_arr = arr[k + 1:]
                    next_arr = rrc
                    debug_if(f"{depth} ADD {new_arr} NEXT? {next_arr}", condition=1)
                    
                    # no more elements
                    if not next_arr:
                        #debug_if(f"{depth} ADDING {new_arr}", condition=1)
                        n += 1
                        #break
                    if next_arr:
                        n += _combos(next_arr, prev_arr=prev_arr + [y], depth=depth + 1)
                i += 1
            #debug_if(f"{depth} {self.nc} DONE {n}", condition=depth == self.max_depth)
            _comb_map[arr_str] = n
            #debug_print(f"COMB MAP {_comb_map}")
            return n

        def _combinations(arr, depth=0):
            arr_str = "".join(arr)
            #debug_print(f"{depth} START {arr_str}")
            if arr_str in _comb_map:
                #debug_print(f"{depth} FOUND {arr_str} -> {len(_comb_map[arr_str])}")
                return _comb_map[arr_str]
            n = 1
            i = 0
            arrs = [arr]
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
                    #debug_print(f"{depth} CONCATED {arr[k]} CHECK {y} AT {i}-{i + j}")
                    j += 1
                    if y not in self.patterns:
                        #debug_print(f"{depth} NON PATTERN {y}")
                        continue
                    new_arr = arr[:i] + [y] + arr[k + 1:]
                    #debug_print(f"{depth} POSSIBLE NEW {arr[:i]}+{[y]}+{arr[k + 1:]} = {new_arr}")
                    next_arr = new_arr[k:]
                    #next_arr = arr[k + 1:]
                    #debug_print(f"{depth} NEXT {next_arr}")
                    # no more elements
                    if not next_arr:
                        #debug_print(f"{depth} NO NEXT IN {new_arr}")
                        arrs.append(new_arr)
                        n += 1
                        #break
                    #debug_print(f"{depth} LOOK AFTER {new_arr[:k]} {next_arr}")
                    #n += _combinations(next_arr, ref_arr[k:], depth=depth + 1)
                    #nk = "".join(next_arr)
                    #if nk in _comb_map:
                    #    #debug_print(f"{depth} NEXT ARR IN MAP {nk}")
                    #    aa = _comb_map[nk]
                    #else:
                    if next_arr:
                        aa = _combinations(next_arr, depth=depth + 1)
                        if not aa:
                            #debug_print(f"{depth} NO COMBS USE {new_arr}")
                            arrs.append(new_arr)
                            n += 1
                            continue    
                        n += len(aa)
                        #debug_print(f"{depth} ADD {len(aa)}")
                        # much too slow for large numbers
                        arrs.extend([new_arr[:k] + a for a in aa])
                        #debug_print(f"{depth} DONE ADDING {len(aa)}")
                i += 1
            #debug_print(f"{depth} ALL {arr} -> LEN {len(arrs)} N {n}")
            _comb_map[arr_str] = arrs
            debug_print(f"{depth} DONE {arr_str}")
            return arrs


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
        
        for a in t:
            #c = _combinations(_reduce(a))
            #n += len(c)
            c = []
            n += _combos(_reduce(a))
            #n += _combos(a)
            debug_print(f"{''.join(a)} COMB {c} RUNNING TOTAL {n}")
            break
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
