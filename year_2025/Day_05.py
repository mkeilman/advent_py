import Day
from utils.debug import debug_print, debug_if
from utils import mathutils
import re

class AdventDay(Day.Base):

    TEST = [
        "3-5",
        "10-14",
        "16-20",
        "12-18",
        "",
        "1",
        "5",
        "8",
        "11",
        "17",
        "32",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 5)
        self.add_args(run_args)
        self.fresh_ranges = []
        self.available_ingredients = []


    def run(self):
        n = 0
        self._parse()
        n = self._num_fresh_ingredients()
        debug_print(f"NUM FRESH {n}")
        m = self._num_all_fresh()
        debug_print(f"NUM ALL FRESH {m}")
        return n
 

    # be wary of large numbers!
    def _num_all_fresh(self):
        n = 0
        mins = sorted([x[0] for x in self.fresh_ranges])
        maxs = sorted([x[-1] for x in self.fresh_ranges])
        all_limits = sorted(mins + maxs)
        #debug_print(f"MINS {mins} MAXS {maxs} ALL {all_limits}")
        do_count = True

        # first limit is guaranteed to be the lowest minimum
        r = [all_limits[0]]
        d = [r]
        # go through all limits
        for x in all_limits[1:]:
            # found a minimum - if we are counting, ignore it;
            # otherwise start a new range and start counting
            if x in mins:
                #debug_print(f"FOUND MIN {x}")
                if do_count:
                    continue
                r = [x]
                d.append(r)
                do_count = True
            # found a maximum - if we are counting, close the current range and stop counting;
            # otherwise not possible ???
            else:
                #debug_print(f"FOUND MAX {x}")
                if do_count:
                    r.append(x)
                    do_count = False
                    continue
                d.append([d[-1][1] + 1, x])
        #debug_print(f"DISJOINT RANGES {d}")
        n = mathutils.sum([x[1] - x[0] + 1 for x in d])
        return n



    def _num_fresh_ingredients(self):
        n = 0
        for i in self.available_ingredients:
            n += int(any([i in x for x in self.fresh_ranges]))
        return n

    def _parse(self):
        for line in self.input:
            if not line:
                continue
            if "-" in line:
                r = [int(x) for x in re.findall(r'\d+', line)]
                self.fresh_ranges.append(range(r[0], r[1] + 1))
            else:
                self.available_ingredients.append(int(line))
