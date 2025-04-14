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
        i = 0
        s = ""
        #t = ""
        ta = []
        found = False
        k = 0
        tries = 0
        while i < len(towel):
            found = False
            #for p in self.patterns:
            while k < len(self.patterns):
                p = self.patterns[k]
                j = i + len(p)
                tt = towel[i:j]
                #debug_print(f"CHECK {tt} VS {p}")
                k += 1
                if tt == p:
                    #debug_print(f"FOUND {p} IN {towel}")
                    #t += p
                    ta.append(p)
                    i = j
                    found = True
                    k = 0
                    break
            else:
                # try next pattern
                tries += 1
                if not tries % 100000:
                    debug_print(f"{tries} BAD {towel} {ta} I {i} J {j} K {k} P {p}")
                #debug_print(f"BAD {towel} {ta} I {i} J {j} K {k} P {p}")
                if not len(ta):
                    #debug_print(f"NO MATCHES {towel}")
                    break
                while ta and len(p) <= 1:
                    p = ta.pop()
                    i -= len(p)
                    #debug_print(f"TRY SHORTER THAN {p} {ta} I {i}")
                kp = [x for x in self.patterns if len(x) < len(p)]
                if not kp:
                    #debug_print(f"ALL SINGLES {towel}")
                    break
                k = self.patterns.index(kp[0])
                #else:
                #    break
                #break
        if found:
            debug_print(f"GOOD {towel}")
        else:
            debug_print(f"BAD {towel}")
        #    debug_print(f"IN {towel} OUT {''.join(t)} EQ? {towel == t}")
        return found
    
    
    def _num_good_towels(self):
        return len([y for y in [self._check_towel(x) for x in self.towels[8:9]] if y])

    def _parse(self):
        self.patterns = sorted(re.split(r",\s*", self.input[0]), key=len, reverse=True)
        self.pattern_lens = set([len(x) for x in self.patterns])
        self.max_pattern_len = max(self.pattern_lens)
        self.patterns_by_len = self._patterns_by_len()
        #debug_print(self.patterns_by_len)
        self.towels = self.input[2:]
        #debug_print(f"P {self.patterns} MAX {self.max_pattern_len}")
    

    def _patterns_by_len(self):
        p = []
        for l in self.pattern_lens:
            p.append([x for x in self.patterns if len(x) == l])
        return sorted(p, key=lambda x: len(x[0]), reverse=True)
