import re
import Day
from utils import mathutils
from utils.debug import debug_print, debug_if

class AdventDay(Day.Base):

    SINGLE = [
        "123"
    ]

    TEST = [
        "1",
        "10",
        "100",
        "2024",
    ]


    TEST_2 = [
        "1",
        "2",
        "3",
        "2024",
    ]

    def __init__(self, run_args):
        super(AdventDay, self).__init__(2024, 22)
        self.change_group_size = 4
        self.args_parser.add_argument(
            "--num-iterations",
            type=int,
            help="number of iterations",
            default=1,
            dest="num_iterations",
        )
        self.add_args(run_args)


    def run(self):
        n = 0
        max_p = 0
        cg_dict = {}
        #self.input = AdventDay.TEST_2
        for s in self._parse(self.input):
            x, p = self._next(s)
            n += x
            g = []
            for j, ggg in enumerate(self._change_groups(p)):
                if ggg in g:
                    continue
                if ggg not in cg_dict:
                    cg_dict[ggg] = 0
                cg_dict[ggg] += p[j + self.change_group_size]
                g.append(ggg)
        max_p = max(cg_dict.values())
        max_g = [x for x in cg_dict if cg_dict[x] == max_p]
        #debug_print(f"CHECK {len(cg_dict)} GROUPS MAX? {max_p} G {max_g}")
        debug_print(f"MAX P {max_p}")
        return n
    

    def _add_group(self, g, groups):
        if g not in groups:
            groups.append(g)

    def _changes(self, prices):
        return [prices[i + 1] - prices[i] for i in range(len(prices) - 2)]
    

    def _change_groups(self, prices):
        changes = self._changes(prices)
        return [tuple(x) for x in [changes[i:i + self.change_group_size] for i in range(len(changes) - self.change_group_size + 1)]]


    def _mix(self, val, secret):
        return val ^ secret


    def _mix_prune(self, val, secret):
        return self._prune(val ^ secret)


    def _next(self, secret):
        n = secret
        p = [self._price(n)]
        for _ in range(self.num_iterations):
            n = self._mix_prune(64 * n, n)
            n = self._mix_prune(n // 32, n)
            n = self._mix_prune(2048 * n, n)
            p.append(self._price(n))

        return n, p


    def _parse(self, grid):
        return [int(x) for x in grid]


    def _price(self, secret):
        return secret % 10
    

    def _prune(self, secret):
        return secret % 16777216

