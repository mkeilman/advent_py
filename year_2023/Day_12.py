import re
import Day
from utils import mathutils
from utils.debug import debug_print


class HotSpring():

    BASIC = [
        "???.### 1,1,3",
        ".??..??...?##. 1,1,3",
        "?#?#?#?#?#?#?#? 1,3,1,6",
        "????.#...#... 4,1,1",
        "????.######..#####. 1,6,5",
        "?###???????? 3,2,1",
    ]

    BUSTED = "#"
    UNKNOWN = "?"
    WORKING = "."

    RE_BUSTED = re.compile(fr"{BUSTED}+")
    
    def __init__(self, grid, num_folds=1):
        self.grid = grid
        self.schematic = [self._unfold(x.split()[0], HotSpring.UNKNOWN, num_folds=num_folds) for x in self.grid]
        g = [self._unfold(x.split()[1], ",", num_folds=num_folds) for x in self.grid]
        self.spring_groups = [[int(y) for y in re.findall(r"\d+", x)] for x in g]
        self.num_busted = [mathutils.sum(x) for x in [self._collect_symbol(list(y)) for y in self.schematic]]
        self.num_unknown = [self._collect_symbol(list(y), symbol=HotSpring.UNKNOWN) for y in self.schematic]
        self.num_left = [x - self.num_busted[i] for i, x in enumerate([mathutils.sum(y) for y in self.spring_groups])]
        self.valid_counts = [self._num_valid(x, self.num_left[i], self.spring_groups[i]) for i, x in enumerate(self.schematic)]

    def total_valid(self):
        return mathutils.sum(self.valid_counts)

    
    def _collect_symbol(self, arr, symbol=None, cmp_arr=None):
        a = []
        n = 0
        i = 0
        s = symbol or HotSpring.BUSTED
        debug_print(f"ARR {arr} CMP {cmp_arr}")
        for c in arr:
            if c == s:
                n += 1
                continue
            if n:
                if cmp_arr and n != cmp_arr[i]:
                    return None
                a.append(n)
                i += 1
            n = 0
        if n:
            a.append(n)
        return a
    
    def _cb(self, txt):
        return [len(x) for x in re.findall(HotSpring.RE_BUSTED, txt)]

    def _sr(self, arr, symbol=None):
        a = []
        n = 0
        j = 0
        for i, c in enumerate(arr):
            if c == (symbol or HotSpring.BUSTED):
                if not n:
                    j = i
                n += 1
                continue
            if n:
                a.append(range(j, j + n))
            n = 0
        if n:
            a.append(range(j, j + n))
        return a

    def _num_valid(self, txt, num_repl, groups):
        import itertools
        import time
        import math
        
        def _replace_with_busted(txt, c):
            l = list(txt)
            for i in c:
                l[i] = HotSpring.BUSTED 
            #debug_print(f"REPL {l}")
            return l

        def _check_groups(arr, groups, start=0):
            j = 0
            #debug_print(f"CHECK {arr} VS G {groups} STARTING AT {start}")
            #for i, g in enumerate(groups[start:]):
            for i, g in enumerate(arr[start:]):
                if i > len(groups) - 1:
                    break
                if g == groups[i]:
                    return 1
                    j = i + 1
            return 0

        n = 0
        #nn = 1
        #N = num_repl
        #pre_groups = self._sr(list(txt))
        #debug_print(f"PRE {pre_groups}")
        t = txt.replace(HotSpring.UNKNOWN, HotSpring.WORKING)
        #tb = self._collect_symbol(list(t))
        #u = self._collect_symbol(list(txt), symbol=HotSpring.UNKNOWN)
        #ur = self._sr(list(txt), symbol=HotSpring.UNKNOWN)
        tt = [i for i, x in enumerate(txt) if x == HotSpring.UNKNOWN]
        debug_print(f"NUM COMBOS {math.comb(len(tt), num_repl)}")
        #debug_print(f"UNK {tt} {ur} G {groups} TO REPL {num_repl}")
        t0 = time.time()
        p = 0
        j = 0
        #for r in ur:
        #    n = 0
        #    nr = min(N, len(r))
            #debug_print(f"DO {nr} REPL")
            #for i in r:
            #    pass
            # one check with no replacements
            #j = _check_groups(tb, groups)
            #for j in range(1, nr):
        #    for c in itertools.combinations(r, nr):
        #        b = self._collect_symbol(_replace_with_busted(t, c))
        #        #debug_print(f"C {c} B {b}")
        #        if b is None:
        #            continue
        #        n += _check_groups(b, groups, start=0)
        #    if n:
        #        #debug_print(f"FOUND n {n}")
        #        N -= nr
        #        nn *= n
        #return nn
        #debug_print(f"NUM COMBOS {math.comb(len(tt), nr)}")
        for c in itertools.combinations(tt, num_repl):
            #b = self._collect_symbol(_replace_with_busted(t, c), cmp_arr=groups)
            b = self._cb("".join(_replace_with_busted(t, c)))
            #if b is None:
            #    continue
            n += int(b == groups)
        t1 = time.time()
        debug_print(f"{n} NV TIME {int(t1 - t0)}")
        return n
        
    def _unfold(self, txt, sep, num_folds=1):
        return sep.join([txt] * num_folds)

class AdventDay(Day.Base):

    def __init__(self, run_args):
        def _pos_int_type(x):
            x = int(x)
            if x < 1:
                raise argparse.ArgumentTypeError(f"Number of folds {x} must be >= 1")
            return x
        
        import argparse
        super(AdventDay, self).__init__(
            2023,
            12,
            HotSpring.BASIC
        )
        self.args_parser.add_argument(
            "--num-folds",
            default=1,
            dest="num_folds",
            type=_pos_int_type,
        )
        self.num_folds = self.args_parser.parse_args(run_args).num_folds

    def run(self, v):
        h = HotSpring(v, num_folds=self.num_folds)
        debug_print(f"SUM VALID {h.total_valid()}")
    



def main():
    d = AdventDay()
    debug_print("TEST:")
    d.run_from_test_strings()
    debug_print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
