import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print

class AdventDay(Day.Base):

    TEST = [
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
    ]

    TEST_2 = [
        "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))",
    ]
    
    def _get_muls(self):

        def _enabled_ranges(e, d, max_index):
            r = []
            ei = 0
            i = 1
            j = 0
            d_index = 0

            # only enabled index is 0, so turn off at 1st disabled index (or max if never disabled)
            if len(e) == 1:
                return [range(d[0])] if len(d) > 0 else [range(max_index)]
            
            for e_index in e[1:]:
                # out of disabled indices before enabled indices
                if j == len(d):
                    # current enabled index is below the previous disabled index
                    if e_index < d_index:
                        r.append(range(ei, d[-1]))
                    # current enabled index is beyond the previous disabled index, enable to end of line
                    else:
                        r.append(range(ei, max_index))
                    break
                d_index = d[j]
                if e_index < d_index:
                    continue
                r.append(range(ei, d_index))
                ei = e_index
                while j < len(d):
                    if ei > d[j]:
                        j += 1
                    else:
                        break

            # still have disabled indices
            if j < len(d):
                # current enabled index is beyond the previous disabled index
                if ei > d[j]:
                    r.append(range(ei, d[j + 1] if j < len(d) -1 else d[-1]))
                # current enabled index is below the previous disabled index
                else:
                    r.append(range(ei, d[j]))
            else:
                if ei > d[-1]:
                    r.append(range(ei, max_index))
            return r

        # input needs to be on a single line
        vv = "".join(self.input)
        m = re.findall(r"mul\(\d+,\d+\)", vv)
        if not self.respect_enables:
            return [m]
        
        n = []
        e = [0] + string.indices("do()", vv)
        d = string.indices("don\'t", vv)
        er = _enabled_ranges(e, d, len(vv))
        for mm in m:
            # could be duplicates
            for pos in [x for x in string.indices(mm, vv) if any([x in y for y in er])]:
                n.append(mm)
        return [n]


    def _do_muls(self, arr):
        s = 0
        for m in arr:
            s += mathutils.product([int(x) for x in re.findall(r"\d+", m)])
        return s


    def mul_sum(self):
        s = 0
        for m in self._get_muls():
            s += self._do_muls(m)
        return s

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 3)
        self.args_parser.add_argument(
            "--respect-enables",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="respect_enables",
        )
        self.add_args(run_args)


    def run(self):
        s = self.mul_sum()
        debug_print(f"M {s}")
        return s


