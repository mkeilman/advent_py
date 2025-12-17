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

    NESTED = [
        "1-10",
        "4-5",
        "6-7"
    ]

    OVERLAPPING = [
        "1-10",
        "5-20",
        "4-21",
    ]

    SINGLE = [
        "1-1",
        "1-10",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 5)
        self.add_args(run_args)
        self.fresh_ranges = []
        self.available_ingredients = []


    def run(self):
        #self.input = AdventDay.SINGLE
        n = 0
        self._parse()
        n = self._num_fresh_ingredients()
        debug_print(f"NUM FRESH {n}")
        m = self._num_all_fresh()
        debug_print(f"NUM ALL FRESH {m}")
        return n
 

    # be wary of large numbers!
    def _num_all_fresh(self):
        import operator

        n = 0
        # deal with single-member ranges first
        n = len([x for x in self.fresh_ranges if x[0] == x[-1]])

        non_trivial = sorted([x for x in self.fresh_ranges if x[0] != x[-1]], key=operator.itemgetter(0))
        mins = sorted([x[0] for x in non_trivial])
        maxs = sorted([x[-1] for x in non_trivial])
        both = [x for x in mins if x in maxs]
        adjacent = [x for x in non_trivial if x[0] in both]
        debug_print(f"N MIN {len(mins)} N MAX {len(maxs)} BOTH {adjacent}")
        all_limits = sorted(mins + maxs)
        #debug_print(f"MINS {mins} MAXS {maxs} ALL {all_limits}")

        # THIS DOES NOT WORK --> sets = [set(x) for x in self.fresh_ranges]
        # the natural thing to try is to make sets out of the ranges, but they are
        # so large that converting them takes forever

        # renormalize? all we want is a count, so offset by the smallest min?
        #offset = mins[0]
        #rr = [range(x[0] - offset, x[-1] - offset) for x in self.fresh_ranges]
        #debug_print(f"RENORM {rr}")


        # first limit is guaranteed to be the lowest minimum
        r = [all_limits[0]]
        ranges = [r]
        # depth is the number of concurrent ranges we are counting
        depth = 1
        # go through all limits
        for x in all_limits[1:]:
            #debug_print(f"DEPTH {depth}")
            # found a minimum - if we are counting, ignore it;
            # otherwise start a new range and start counting
            if x in mins:
                #debug_print(f"FOUND MIN {x}")
                if not depth:
                #depth += 1
                #if do_count:
                #    continue
                    r = [x]
                    ranges.append(r)
                depth += 1
            # found a maximum - if we are counting, close the current range and stop counting;
            # otherwise not possible ???
            else:
                #debug_print(f"FOUND MAX {x}")
                if depth == 1:
                #depth -= 1
                #if do_count:
                    r.append(x)
                    #continue
                #d.append([d[-1][1] + 1, x])
                depth -= 1
        debug_print(f"DISJOINT RANGES {ranges} DEPTH {depth}")
        #debug_print(f"DEPTH {depth}")
        n += mathutils.sum([x[-1] - x[0] + 1 for x in ranges if x])
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
                r = [int(x) for x in re.findall(r"\d+", line)]
                #if r[0] == r[-1]:
                #    debug_print(f"ZERO RANGE {r}")
                # Note the range stop is one more than the second parameter;
                # this is because the ranges here include the final value
                self.fresh_ranges.append(range(r[0], r[1] + 1))
                
            else:
                self.available_ingredients.append(int(line))

        # if any ranges have the same start, combine them
        starts = {}
        for i, r in enumerate(self.fresh_ranges):
            start = r[0]
            #debug_print(f"CHECK {start}")
            rr = [x for x in self.fresh_ranges if x[0] == start and x != r]
            if not rr:
                continue
            starts[start] = [i]
            starts[start].extend([self.fresh_ranges.index(x) for x in rr])
            #new_end = max([x[-1] for x in rr])
            #new_range = range(r[0], new_end + 1)
            #debug_print(f"SAME START {rr} NEW {new_range}")
        debug_print(f"SAME STARTS {starts}")
