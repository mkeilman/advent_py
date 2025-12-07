import Day
import operator
import re
from utils.debug import debug_print, debug_if
from utils import mathutils

class AdventDay(Day.Base):

    TEST = [
        "123 328  51 64 ",
        " 45 64  387 23 " ,
        "  6 98  215 314",
        "*   +   *   + ",
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
        self.txt = []
        self.num_cols = []
        self.ops = []
        self.results = []
        self.magnitudes = []
        self.magnitude = pow(10, len(self.input) - 2)
        n = 0
        self._parse()
        self._apply_ops()
        #debug_print(f"OPS {self.ops} NUMS {self.nums} RES {self.results}")
        n = mathutils.sum(self.results)
        #debug_print(f"RES SUM {n} NUM COLS {self.num_cols}")
        return n
    

    def _apply_ops(self):
        for r in self.nums:
            for i, n in enumerate(r):
                self.results[i] = self.ops[i](self.results[i], n)
    

    def _parse(self):
        self.nums = []
        for line in self.input[:-1]:
            self.nums.append([int(x) for x in re.findall(r"\d+", line)])
            self.txt.append(re.findall(r"\s*\d+\s*", line))
        
        #debug_print(f"TXT {self.txt}")
        self.magnitudes = len(self.nums[0]) * [0]
        self.num_cols = [[] for _ in range(len(self.nums[0]))]
        #self.num_cols = ["" for _ in range(len(self.nums[0]))]

        for i, r in enumerate(self.nums):
            for j, n in enumerate(r):
                self.magnitudes[j] = max(self.magnitudes[j], len(str(n)) - 1)
                #self.num_cols[j].append(self.input[i][j])
                #self.num_cols[j] = self.input[i][j]
                self.num_cols[j].append(self.txt[i][j])

        #self.num_cols.reverse()
        #for i, c in enumerate(self.num_cols):
        #    if all([x[0] == " " for x in c]):
        #        self.num_cols[i] = [x[1:] for x in c]
        for i, c in enumerate(self.num_cols):
            #if all([x[-1] == " " for x in c]):
            #    self.num_cols[i] = [x[:-1] for x in c]
            debug_print(f"CEPH {self._to_ceph(c)}")
        debug_print(f"NUM COLS {self.num_cols}")

        k = ["\\" + x for x in AdventDay.OPS.keys()]
        re_ops = fr"[{'|'.join(k)}]"
        op_keys = re.findall(re_ops, self.input[-1])
        self.ops = [AdventDay.OPS[x]["op"] for x in op_keys]
        self.results = [AdventDay.OPS[x]["unit"] for x in op_keys]


    
    def _to_ceph(self, num_strings):
        ceph = len(num_strings) * [""]
        max_len = max([len(str(int(x))) for x in num_strings])
        for j in range(max_len):
            for s in num_strings:
                ceph[j] += s[j]
        return ceph
