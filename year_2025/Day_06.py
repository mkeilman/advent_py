import Day
import operator
import re
from utils.debug import debug_print, debug_if
from utils import mathutils
from utils import stringutils

class AdventDay(Day.Base):

    TEST = [
        "123 328  51 64 ",
        " 45 64  387 23 " ,
        "  6 98  215 314",
        "*   +   *   + ",
    ]

    TWO_DIGITS = [
        "12 90",
        "34 12",
        "45 34",
        "78 46",
        "*   + ",
    ]

    OPS = {
        "+": {
            "op": operator.add,
            "unit": 0,
        },
        "*": {
            "op": operator.mul,
            "unit": 1,
        }
    }


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 6)
        self.add_args(run_args)


    def run(self):
        self.nums = []
        self.cephs = []
        self.num_cols = []
        self.ops = []

        n = 0
        self._parse()
        n = mathutils.sum(self._apply_ops(self.nums))
        m =  mathutils.sum(self._apply_ops_ceph(self.cephs))
        debug_print(f"RES SUM {n}")
        debug_print(f"CEPH SUM {m}")
        return n
    

    def _apply_ops_ceph(self, vals):
        res = self._get_unit_res()
        for i, r in enumerate(vals):
            for n in r:
                res[i] = self.ops[i](res[i], n)
        return res
    

    def _apply_ops(self, vals):
        res = self._get_unit_res()
        for r in vals:
            for i, n in enumerate(r):
                res[i] = self.ops[i](res[i], n)
        return res
    

    def _get_ops(self):
        return self._get_op_params("op")


    def _get_unit_res(self):
        return self._get_op_params("unit")


    def _get_op_params(self, key):
        k = ["\\" + x for x in AdventDay.OPS.keys()]
        re_ops = fr"[{'|'.join(k)}]"
        op_keys = re.findall(re_ops, self.input[-1])
        return [AdventDay.OPS[x][key] for x in op_keys]


    def _parse(self):
        self.nums = []
        space_cols = set()
        for line in self.input[:-1]:
            self.nums.append([int(x) for x in re.findall(r"\d+", line)])
            spaces = stringutils.re_indices(r"\s+", line)
            sp = set(spaces)
            if space_cols:
                space_cols = space_cols.intersection(sp)
            else:
                space_cols = sp

        # reproduce the alignment - prolly a way to do this with regex
        # find the indices that are spaces for all rows
        space_cols = sorted(list(space_cols))
        justified = []
        for line in self.input[:-1]:
            nc = []
            j = 0
            for i in space_cols:
                nc.append(line[j:i])
                j = i + 1
            nc.append(line[j:])
            justified.append(nc)

        self.num_cols = [[] for _ in range(len(self.nums[0]))]

        for i, r in enumerate(justified):
            for j, n in enumerate(r):
                self.num_cols[j].append(r[j])

        self.cephs = [self._to_ceph(x) for x in self.num_cols]
        self.ops = self._get_ops()
    
    def _to_ceph(self, num_strings):
        num_len = len(num_strings[0])
        ceph = num_len * [""]
        for i in range(num_len):
            for s in num_strings:
                ceph[i] += s[i]
        return [int(x) for x in ceph]
