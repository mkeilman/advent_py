import Day
from utils.debug import debug_print, debug_if

class AdventDay(Day.Base):

    TEST = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]

    SHORT_BANK = [
        #"8119",
        "24234278",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 3)
        self.args_parser.add_argument(
            "--num-batts",
            type=int,
            help="number of batteries",
            default=2,
            dest="num_batts",
        )
        self.add_args(run_args)


    def run(self):
        self.input = AdventDay.SHORT_BANK
        n = self._max_joltage_sum()
        debug_print(f"RUN {self.year} {self.day}: {n}")
        return n
 

    def _max_joltage(self, bank):
        if self.num_batts > len(bank):
            raise ValueError(f"too many batteries: {self.num_batts} > {len(bank)}")
        
        i = 0
        last_i = 0
        j = ""
        k = len(bank)
        n = 0
        #while n < self.num_batts:
        while len(j) < self.num_batts:
            b = bank[i:k]
            debug_print(f"CHECK {b} I {i} -> K {k}")
            # no more batts
            # start over?
            if not b:
                debug_print(f"EMPTY BANK")
                i = 0
                last_i = 0
                k -= 1
                j = ""
            #    n = 0
                continue
            i = bank.index(str(max([int(x) for x in b])))
            # if we still have batteries to connect but have reached the
            # end of the bank, start again excluding the last battery
            #if n < self.num_batts - 1 and i == len(bank) - 1:
            if len(j) < self.num_batts - 1 and i == len(bank) - 1:
                debug_print(f"BANK {bank} J {bank[i]} AT {i} NO MORE BATTS")
                k -= 1
                i = last_i
                #j = j[:-1]
                continue
            j += bank[i]
            debug_print(f"J {j} AT {i}")
            # search for next digit after the one we found
            i += 1
            last_i = i
            n += 1
            # reset to check to the end of the bank?
            k = len(bank)

        debug_print(f"BANK {bank} J {j}")
        return int(j)


    def _max_joltage_sum(self):
        j = 0
        for bank in self.input:
            j += self._max_joltage(bank)
        return j