from functools import reduce
import re
import Day
import Utils


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
        #print(f"SCH {self.schematic} G {self.spring_groups}")
        self.num_busted = [Utils.Math.sum(x) for x in [self._collect_busted(list(y)) for y in self.schematic]]
        self.num_left = [x - self.num_busted[i] for i, x in enumerate([Utils.Math.sum(y) for y in self.spring_groups])]
        self.valid_counts = [self._num_valid(x, self.num_left[i], self.spring_groups[i]) for i, x in enumerate(self.schematic)]

    def total_valid(self):
        return Utils.Math.sum(self.valid_counts)

    
    def _collect_busted(self, arr):
        a = []
        n = 0
        for c in arr:
            if c == HotSpring.BUSTED:
                n += 1
                continue
            if n:
                a.append(n)
            n = 0
        if n:
            a.append(n)
        return a


    def _num_valid(self, txt, num_repl, groups):
        import itertools
        import time
        
        n = 0
        nn = 1
        t = txt.replace(HotSpring.UNKNOWN, HotSpring.WORKING)
        t0 = time.time()
        for c in itertools.combinations([i for i, x in enumerate(txt) if x == HotSpring.UNKNOWN], num_repl):
            l = list(t)
            for i in c:
                l[i] = HotSpring.BUSTED 
            n += int(self._collect_busted(l) == groups)
        t1 = time.time()
        print(f"{n} NV TIME {int(t1 - t0)}")
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
        print(f"SUM VALID {h.total_valid()}")
    



def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
