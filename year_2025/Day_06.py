import Day
import operator
import re
from utils.debug import debug_print, debug_if
from utils import mathutils

class AdventDay(Day.Base):

    TEST = [
        "123 328  51 64" ,
        "45 64  387 23" ,
        "6 98  215 314 ",
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
        self.nuns = []
        self.ops = []
        self.results = []
        n = 0
        self._parse()
        self._apply_ops()
        #debug_print(f"OPS {self.ops} NUMS {self.nums} RES {self.results}")
        n = mathutils.sum(self.results)
        debug_print(f"RES SUM {n}")
        return n
    
    def _parse(self):
        self.nums = []
        for line in self.input[:-1]:
            self.nums.append([int(x) for x in re.findall(r"\d+", line)])

        k = ["\\" + x for x in AdventDay.OPS.keys()]
        re_ops = fr"[{'|'.join(k)}]"
        op_keys = re.findall(re_ops, self.input[-1])
        self.ops = [AdventDay.OPS[x]["op"] for x in op_keys]
        self.results = [AdventDay.OPS[x]["unit"] for x in op_keys]
 

    def _apply_ops(self):
        for r in self.nums:
            for i, n in enumerate(r):
                self.results[i] = self.ops[i](self.results[i], n)

