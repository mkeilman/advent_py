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
        #"819121",
        "8119",
        #"24234278",
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
 

    def _bank_to_batt_index(self, bank):
        import operator

        inds = []
        for batt in sorted(bank, reverse=True):
            inds.extend([x for x in stringutils.indices(batt, bank) if x not in inds])
        return  sorted([(i, bank[i]) for i in inds], reverse=True, key=operator.itemgetter(1))


    def _max_joltage_list(self, batt_index, num_batts=None, max_index=0, depth=0):
        import operator
        
        nb = num_batts or self.num_batts
        # the number as written is the largest it can be
        #if nb == len(bank):
        #    return "".join(bank)
        
        i = 0

        #batt_index = self._bank_to_batt_index(bank)
       
        #debug_print(f"{depth} BANK {batt_index} NB {nb}")
        start = 0
        digits = []
        i = 0
        #sbi = sorted(batt_index, reverse=True, key=operator.itemgetter(1))
        #debug_print(f"{depth} SBI {sbi}")
        i, d = batt_index[start]
        digits.append(d)
        while len(digits) < nb:
            #debug_print(f"NEXT {start}")
            # get the remaining digits whose index is greater than the current digit's index
            remainder = [x for x in batt_index if x[0] > i]
            #debug_print(f"{depth} D {digits} R {remainder}")
            total = len(digits) + len(remainder)
            # if the number of digits plus the number remaining is num_batts, add to the 
            # remainder sorted by index - we're done
            if total == nb:
                digits.extend([x[1] for x in sorted(remainder, key=operator.itemgetter(0))])
                return digits

            # if there are too few, start over with the next largest digt
            if total < nb:
                start += 1
                i, d = batt_index[start]
                digits = [d]
                #debug_print(f"{depth} START OVER AT {start}")
                continue

            #remove_idx = i
            #debug_print(f"{depth} REMOVE {d} AT {i}")
            #i, d = remainder[0]
            #debug_print(f"{depth} NEXT DGIT OK {i} {d}")
            digits.extend(self._max_joltage_list(remainder, num_batts=nb - 1, depth=depth + 1))

        return digits


    def _max_joltage(self, bank, depth=0):
        import operator

        if self.num_batts > len(bank):
            raise ValueError(f"too many batteries: {self.num_batts} > {len(bank)}")
        
        if self.num_batts < 2:
            raise ValueError(f"too few batteries: {self.num_batts} < 2")
        
        #debug_print(f"GET J FOR {bank}")
        batt_index = self._bank_to_batt_index(bank)

        js = self._max_joltage_list(batt_index)
        #debug_print(f"MAX J ? {int("".join(js))}")
        return int("".join(js))

        # the number as written is the largest it can be
        if self.num_batts == len(bank):
            return int("".join(bank))
        
        i = 0
        last_i = 0
        joltage = ""
        k = len(bank)
        n = 0

        # sort the batteries largest to smallest, keeping track of the original order 
        sorted_bank = sorted(bank, reverse=True)
        
        inds = []
        for batt in sorted_bank:
            inds.extend([x for x in stringutils.indices(batt, bank) if x not in inds])
        batt_index = [(i, bank[i]) for i in inds]
       
        #debug_print(f"BANK {bank} SORTED {sorted_bank} INDS {inds} BI {batt_index}")
        debug_print(f"BANK {bank}")
        start = 0
        digits = []
        i = 0
        #while not done:
        sbi = sorted(batt_index, reverse=True, key=operator.itemgetter(1))  #[:self.num_batts]
        #digits = [x[1] for x in sorted(sbi, key=operator.itemgetter(0))]
        debug_print(f"SBI {sbi}")
        i, d = sbi[start]
        digits.append(d)
        while len(digits) < self.num_batts:
            #debug_print(f"NEXT {start}")
            #digits.append(sbi[start][1])

            # get the remaining digits whose index is greater than the current digit's index
            remainder = [x for x in sbi if x[0] > i]
            debug_print(f"D {digits} R {remainder}")
            total = len(digits) + len(remainder)
            # if the number of digits plus the number remaining is num_batts, add to the 
            # remainder sorted by index - we're done
            if total == self.num_batts:
                digits.extend([x[1] for x in sorted(remainder, key=operator.itemgetter(0))])
                #debug_print(f"DONE {digits}")
                break

            # if there are too few, start over with the next largest digt
            if total < self.num_batts:
                start += 1
                i, d = sbi[start]
                digits = [d]
                debug_print(f"START OVER AT {start}")
                continue

            
            # ???
            i, d = remainder[0]
            debug_print(f"NEXT DGIT OK {i} {d}")
            digits.append(d)

        joltage = "".join(digits)
        debug_print(f"MAX J ? {joltage}")
        return int(joltage)


    def _max_joltage_sum(self):
        j = 0
        for bank in self.input:
            j += self._max_joltage(bank)
        return j