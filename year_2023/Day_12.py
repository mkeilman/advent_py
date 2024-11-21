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

    
    def __init__(self, grid):
        self.grid = grid
        self.schematic = [x.split()[0] for x in self.grid]
        self.busted = [self._collect_busted(x) for x in self.schematic]
        self.spring_groups = [[int(y) for y in re.findall(r"\d+", x.split()[1])] for x in self.grid]
        self.num_springs = [Utils.sum(x) for x in self.spring_groups]
        self.num_busted = [len(Utils.sum(x, "")) for x in self.busted]
        self.num_left = [x - self.num_busted[i] for i, x in enumerate(self.num_springs)]
        self.valid_counts = [self._num_valid(x, self.num_left[i], self.spring_groups[i]) for i, x in enumerate(self.schematic)]


    def total_valid(self):
        return Utils.sum(self.valid_counts)
    
    def _collect_busted(self, txt):
        return re.findall(fr"{HotSpring.BUSTED}+", txt)

    def _pos_unknown(self, txt):
        p = 0
        a = []
        done = False
        while not done:
            try:
                pp = txt.index(HotSpring.UNKNOWN, p)
                a.append(pp)
                p = pp + 1
            except ValueError:
                done = True
        return a

    def _num_valid(self, txt, num_repl, groups):
        import itertools
        u = self._pos_unknown(txt)
        n = 0
        for c in itertools.combinations(u, num_repl):
            t = txt.replace(HotSpring.UNKNOWN, HotSpring.WORKING)
            for i in c:
                t = t[:i] + HotSpring.BUSTED + t[i + 1:]
            g = [len(x) for x in self._collect_busted(t)]
            n += int(g == groups)
        return n
        

class AdventDay(Day.Base):

    def __init__(self, run_args):

        import argparse
        super(AdventDay, self).__init__(
            2023,
            12,
            HotSpring.BASIC
        )

    def run(self, v):
        h = HotSpring(v)
        print(f"SUM VALID {h.total_valid()}")
    



def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
