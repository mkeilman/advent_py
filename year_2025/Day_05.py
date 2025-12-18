import Day
from utils.debug import debug_print, debug_if
from utils import collectionutils
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

        def _combine_adjacent(ranges):
            # sort before and after?
            ranges.sort(key=operator.itemgetter(0))
            both = [x for x in [y[0] for y in ranges] if x in [y[-1] for y in ranges]]
            # sort by range start
            a = sorted([x for x in ranges if x[0] in both], key=operator.itemgetter(0))
            combined = []
            inds = []
            for i in range(len(a) - 1):
                r1, r2 = a[i], a[i + 1]
                if r1[-1] != r2[0]:
                    continue
                combined.append(range(r1.start, r2.stop))
                inds.append(ranges.index(r1))
                inds.append(ranges.index(r2))
            for i in sorted(inds, reverse=True):
                #debug_print(f"ADJ: RM {ranges[i]} AT {i}")
                del ranges[i]
            ranges.extend(combined)
            ranges.sort(key=operator.itemgetter(0))
            return len(inds)


        def _combine_overlapping(ranges):
            combined = []
            #inds = []
            inds = set()
            ranges.sort(key=operator.itemgetter(0))
            for i in range(len(ranges)):
                r = ranges[i]
                r_inds = [ranges.index(x) for x in ranges[i + 1:] if x.start < r.stop and x.stop > r.stop]
                if not r_inds:
                    continue
                if i not in inds:
                    #inds.append(i)
                    inds.add(i)
                #inds.extend(r_inds)
                # one at a time?
                #inds = inds | set(r_inds)
                inds.add(r_inds[0])
                c = range(r.start, ranges[r_inds[-1]].stop)
                debug_print(f"OVR: CMB {ranges[i]} + {[ranges[x] for x in r_inds]} {r_inds} -> {c}")
                combined.append(c)
            for j in sorted(inds, reverse=True):
                debug_print(f"OVR: RM {ranges[j]} AT {j}")
                del ranges[j]
            ranges.extend(combined)
            ranges.sort(key=operator.itemgetter(0))
            return len(inds)
            

        def _remove_interior(ranges):
            ranges.sort(key=operator.itemgetter(0))
            inds = []
            for i in range(len(ranges)):
                r1 = ranges[i]
                inds.extend([ranges.index(x) for x in ranges[i + 1:] if x.start >= r1.start and x.stop <= r1.stop])
            for i in sorted(inds, reverse=True):
                del ranges[i]
            ranges.sort(key=operator.itemgetter(0))


        n = 0
        debug_print(f"NUM R INIT {len(self.fresh_ranges)}")
        #debug_print(f"{sorted(self.fresh_ranges, key=operator.itemgetter(0))}")

        # deal with single-member ranges
        single = [x for x in self.fresh_ranges if len(x) == 1]
        n = len(single)
        debug_print(f"NUM SINGLE {n} {sorted([x[0] for x in single])}")

        # the rest are multi-member ranges
        non_trivial = [x for x in self.fresh_ranges if len(x) > 1]
        debug_print(f"NUM R INIT {len(non_trivial)}")

        # combine adjacent
        while _combine_adjacent(non_trivial):
            pass
        debug_print(f"NUM R AFTER COMB ADJ {len(non_trivial)}")

        # combine overlapping - may take multiple iterations to get them all
        while _combine_overlapping(non_trivial):
            pass
        debug_print(f"NUM R AFTER COMB OVERLAP LEN {len(non_trivial)}")

        # remove interior
        _remove_interior(non_trivial)
        debug_print(f"NUM R AFTER RM INT {non_trivial}")

        debug_print(f"TOTAL? {n + mathutils.sum([len(x) for x in non_trivial])}")

        mins = sorted([x[0] for x in non_trivial])
        maxs = sorted([x[-1] for x in non_trivial])
        all_limits = sorted(mins + maxs)

        # THIS DOES NOT WORK --> sets = [set(x) for x in self.fresh_ranges]
        # the natural thing to try is to make sets out of the ranges, but they are
        # so large that converting them takes forever 124774261992335

        # first limit is guaranteed to be the lowest minimum
        r = [all_limits[0]]
        rangessss = [r]
        # depth is the number of concurrent ranges we are counting
        depth = 1
        # go through all limits
        for x in all_limits[1:]:
            # found a minimum - if we are counting, ignore it;
            # otherwise start a new range and start counting
            if x in mins:
                if not depth:
                    r = [x]
                    rangessss.append(r)
                depth += 1
            # found a maximum - if we are counting, close the current range and stop counting;
            # otherwise not possible ???
            else:
                if depth == 1:
                    r.append(x)
                depth -= 1
        #debug_print(f"DISJOINT RANGES {rangessss} LEN {len(rangessss)}")
        n += mathutils.sum([x[-1] - x[0] + 1 for x in rangessss if x])
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
        #debug_print(f"SAME STARTS {starts}")
