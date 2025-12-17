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


    def _max_joltage_list(self, batt_index, num_batts=None, depth=0):
        import operator
        
        nb = num_batts or self.num_batts
        
        start = 0
        i, d = batt_index[start]
        digits = [d]
        while len(digits) < nb:
            # get the remaining digits whose index is greater than the current digit's index
            remainder = [x for x in batt_index if x[0] > i]

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
                continue

            digits.extend(self._max_joltage_list(remainder, num_batts=nb - 1, depth=depth + 1))

        return digits


    def _max_joltage(self, bank, depth=0):
        import operator

        if self.num_batts > len(bank):
            raise ValueError(f"too many batteries: {self.num_batts} > {len(bank)}")
        
        if self.num_batts < 2:
            raise ValueError(f"too few batteries: {self.num_batts} < 2")
        
        batt_index = self._bank_to_batt_index(bank)
        return int("".join(self._max_joltage_list(batt_index)))


    def _max_joltage_sum(self):
        j = 0
        for bank in self.input:
            j += self._max_joltage(bank)
        return j