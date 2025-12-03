import Day
from utils.debug import debug_print, debug_if

class AdventDay(Day.Base):

    TEST = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 3)
        self.add_args(run_args)


    def run(self):
        n = self._max_joltage_sum(num_batts=2)
        debug_print(f"RUN {self.year} {self.day}: {n}")
        return n
 

    def _max_joltage(self, bank, num_batts=2):
        i = 0
        last_i = 0
        j = ""
        k = len(bank)
        n = 0
        while n < num_batts:
            #debug_print(f"CHECK {bank[i:k]}")
            i = bank.index(str(max([int(x) for x in bank[i:k]])))
            # if we still have batteries to connect but have reached the
            # end of the bank, start again
            if n < num_batts - 1 and i == len(bank) - 1:
                #debug_print(f"BANK {bank} J {bank[i]} AT {i} NO MORE BATTS")
                k -= 1
                i = last_i
                continue
            j += bank[i]
            #debug_print(f"BANK {bank} J {j} AT {i}")
            i += 1
            last_i = i
            n += 1
            k = len(bank)

        debug_print(f"BANK {bank} J {j}")
        return int(j)


    def _max_joltage_sum(self, num_batts=2):
        j = 0
        for bank in self.input:
            j += self._max_joltage(bank, num_batts=num_batts)
        return j