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
        cg = set()
        groups = []
        prices = []
        #self.input = AdventDay.TEST_2
        for s in self._parse(self.input):
            x, p = self._next(s)
            n += x
            prices.append(p)
            g = self._change_groups(self._changes(p))
            groups.append(g)
            cg = cg | set(g)
        #debug_print(f"N {n} NUM CH {len(cg)}")
        #debug_print(f"ALL P {prices}")
        gsz = len(groups[0][0])
        debug_print(f"CHECK {len(cg)} GROUPS")
        k = 0
        for g in cg:
            debug_if(f"CG {k}", k % 100 == 0)
            p_sum = 0
            for i, gg in enumerate(groups):
                if g not in gg:
                    #debug_print(f"{i} SKIP")
                    continue
                j = gg.index(g)
                #debug_print(f"{i} FOUND {g} AT {j}/{len(gg)} CHECK P {gsz + j}/{len(prices[i])}")
                p_sum += prices[i][gsz + j]
                #debug_if(f"{i} P {prices[i][gsz + j - 1]}", g == (-2, 1, -1, 3))
            debug_if(f"NEW SUM {p_sum} FOR {g}", p_sum > max_p)
            max_p = max(max_p, p_sum)
            k += 1
        debug_print(f"MAX P {max_p}")
        return n
    

    def _add_group(self, g, groups):
        if g not in groups:
            groups.append(g)

    def _changes(self, prices):
        return [prices[i + 1] - prices[i] for i in range(len(prices) - 2)]
    

    def _change_groups(self, changes, group_size=4):
        return [tuple(x) for x in [changes[i:i + group_size] for i in range(len(changes) - group_size + 1)]]


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
        #c = self._changes(p)
        #debug_print(f"P {p} CH {c} G {self._change_groups(c)}")

        return n, p


    def _parse(self, grid):
        return [int(x) for x in grid]


    def _price(self, secret):
        return secret % 10
    

    def _prune(self, secret):
        return secret % 16777216

