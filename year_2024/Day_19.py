import re
import Day
from utils import mathutils
from utils.debug import debug_print

class AdventDay(Day.Base):

    TEST = [
        "r, wr, b, g, bwu, rb, gb, br",
        "",
        "brwrr",
        "bggr",
        "gbbr",
        "rrbgbr",
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
        super(AdventDay, self).__init__(2024, 19)
        self.args_parser.add_argument(
            "--calc",
            type=str,
            help="calculation",
            choices=["col-diffs", "similarity"],
            default="col-diffs",
            dest="calc",
        )
        self.add_args(run_args)

    def run(self):
        #self.input = AdventDay.OVERLAP
        self._parse()
        n = self._num_good_towels()
        debug_print(f"GOOD TOWELS {n} / {len(self.towels)}")
        return n
    
    def _check_towel(self, towel):
        i = len(towel) - 1
        ta = []
        found = False
        k = 0

        # do comparisons from the end
        while i >= 0:
            found = False
            while k < len(self.patterns):
                p = self.patterns[k]
                j = i - len(p) + 1
                tt = towel[j:i + 1]
                #debug_print(f"CHECK {tt} VS {p}")
                k += 1
                if tt == p:
                    ta.insert(0, p)
                    i = j - 1
                    found = True
                    k = 0
                    break
            else:
                # try next pattern
                #debug_print(f"{tries} BAD {towel} {ta} I {i}/{len(towel)} J {j}")
                if not len(ta):
                    break
                # find last pattern with at least 2 characters - if we found a match on a
                # single character we know we cannot replace it with another
                while ta and len(p) <= 1:
                    p = ta.pop(0)
                    i += len(p)
                    #debug_print(f"{towel} TRY SHORTER THAN {p} {ta} I {i}")
                kp = [x for x in self.patterns if len(x) < len(p)]
                if not kp:
                    break
                k = self.patterns.index(kp[0])
        #if found:
        #    debug_print(f"GOOD {towel}")
        #else:
        #    debug_print(f"BAD {towel}")
        return found
    
    
    def _num_good_towels(self):
        return len([y for y in [self._check_towel(x) for x in self.towels] if y])


    def _parse(self):
        self.patterns = sorted(re.split(r",\s*", self.input[0]), key=len, reverse=True)
        self.pattern_lens = set([len(x) for x in self.patterns])
        self.max_pattern_len = max(self.pattern_lens)
        self.patterns_by_len = self._patterns_by_len()
        self.towels = self.input[2:]
        #debug_print(f"P {self.patterns} MAX {self.max_pattern_len}")
    

    def _patterns_by_len(self):
        p = []
        for l in self.pattern_lens:
            p.append([x for x in self.patterns if len(x) == l])
        return sorted(p, key=lambda x: len(x[0]), reverse=True)
