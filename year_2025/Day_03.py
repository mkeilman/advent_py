import Day
from utils.debug import debug_print, debug_if
from utils import collectionutils
from utils import stringutils

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
        #self.input = AdventDay.SHORT_BANK
        n = self._max_joltage_sum()
        debug_print(f"RUN {self.year} {self.day}: {n}")
        return n
 

    def _max_joltage(self, bank):
        if self.num_batts > len(bank):
            raise ValueError(f"too many batteries: {self.num_batts} > {len(bank)}")
        
        if self.num_batts < 2:
            raise ValueError(f"too few batteries: {self.num_batts} < 2")
        
        i = 0
        last_i = 0
        joltage = ""
        k = len(bank)
        n = 0
        sorted_bank = sorted(bank, reverse=True)
        inds = []
        for batt in sorted_bank:
            inds.extend([x for x in stringutils.indices(batt, bank) if x not in inds])
       
        debug_print(f"BANK {bank} SORTED {sorted_bank} INDS {inds}")
        start = 0
        digits = []
        i = 0
        #while not done:
        while len(digits) < self.num_batts:
            #j = inds[start + i]
            j = inds[start]
            # extract j?
            ii = [x for x in inds if x != j]
            debug_print(f"NEW INDS {ii}")
            for index in ii:
                digits.append(bank[j])
                debug_print(f"DIGITS NOW {digits}")
                debug_print(f"CHECK INDS {index} VS J {j}")
                if len(digits) == self.num_batts:
                    break
                if index < j:
                    debug_print(f"START OVER")
                    digits = []
                    start += 1
                    break
                #digits.append(bank[j])
                #debug_print(f"DIGITS NOW {digits}")
                #if len(digits) == self.num_batts:
                #    break
                j = index
            #i += 1
            # next digit is before the current
            #debug_print(f"CHECK INDS {ii[i]} VS J {j}")
            #if inds[start + i] < j:
            #if ii[i] < j:
            #    debug_print(f"START OVER")
            #    digits = []
            #    start += 1
            #    i = 0
            #    continue
            #debug_print(f"ADD IDX {j}")
            #digits.append(bank[j])
            #debug_print(f"DIGITS NOW {digits}")
        joltage = "".join(digits)


        #digits = sorted_bank[-self.num_batts:]
        #digit_inds = inds[-self.num_batts:]
        ##sorted_inds = sorted(digit_inds)
        #debug_print(f"DIGITS {digits} DIGIT INDS {digit_inds} SORTED INDS {sorted_inds}")
        #j = ""
        #for ii in sorted_inds:
        #    j += bank[ii]
        debug_print(f"MAX J ? {joltage}")
        return int(joltage)
    
        #while n < self.num_batts:
        while len(joltage) < self.num_batts:
            b = bank[i:k]
            debug_print(f"CHECK {b} I {i} -> K {k}")
            # no more batts
            # start over?
            if not b:
                debug_print(f"EMPTY BANK")
                i = 0
                last_i = 0
                k -= 1
                joltage = ""
            #    n = 0
                continue
            i = bank.index(str(max([int(x) for x in b])))
            # if we still have batteries to connect but have reached the
            # end of the bank, start again excluding the last battery
            #if n < self.num_batts - 1 and i == len(bank) - 1:
            if len(joltage) < self.num_batts - 1 and i == len(bank) - 1:
                debug_print(f"BANK {bank} J {bank[i]} AT {i} NO MORE BATTS")
                k -= 1
                i = last_i
                #joltage = joltage[:-1]
                continue
            joltage += bank[i]
            debug_print(f"J {joltage} AT {i}")
            # search for next digit after the one we found
            i += 1
            last_i = i
            n += 1
            # reset to check to the end of the bank?
            k = len(bank)

        debug_print(f"BANK {bank} J {joltage}")
        return int(joltage)


    def _max_joltage_sum(self):
        j = 0
        for bank in self.input:
            j += self._max_joltage(bank)
        return j