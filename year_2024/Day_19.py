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
        self.input = AdventDay.OVERLAP
        self._parse()
        n = self._num_good_towels()
        debug_print(f"GOOD TOWELS {n} / {len(self.towels)}")
        return n
    
    def _check_towel(self, towel):
        i = 0
        s = ""
        t = ""
        ta = []
        found = False
        while i < len(towel):
            found = False
            for p in self.patterns:
                j = i + len(p)
                tt = towel[i:j]
                #debug_print(f"CHECK {tt} VS {p}")
                if tt == p:
                    #debug_print(f"FOUND {p} IN {towel}")
                    t += p
                    ta.append(p)
                    i = j
                    found = True
                    break
            if not found:
                debug_print(f"BAD {towel} {ta}")
                break
            #s += towel[i]
            #if len(s) > self.max_pattern_len:
            #    debug_print(f"{s} TOO LONG FOR {towel}")
            #    return False
            #if s in self.patterns:
            #    t += s
            #    #debug_print(f"FOUND {s} IN {towel}")
            #    s = ""
            #i += 1
        #debug_print([self.patterns.index(x) for x in t])
        #debug_print(max([len(x) for x in t]))
        
        #if found:
        #    #debug_print(f"GOOD {towel}")
        #    debug_print(f"IN {towel} OUT {''.join(t)} EQ? {towel == t}")
        return found
    
    
    def _num_good_towels(self):
        return len([y for y in [self._check_towel(x) for x in self.towels] if y])


    def _parse(self):
        self.patterns = sorted(re.split(r",\s*", self.input[0]), key=len, reverse=True)
        self.max_pattern_len = max([len(x) for x in self.patterns])
        self.towels = self.input[2:]
        #debug_print(f"P {self.patterns} MAX {self.max_pattern_len}")
    


