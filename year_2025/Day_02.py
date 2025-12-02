import re
import Day
from utils import mathutils
from utils import collectionutils
from utils.debug import debug_print, debug_if

class AdventDay(Day.Base):

    TEST = [
        """
        11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
        1698522-1698528,446443-446449,38593856-38593862,565653-565659,
        824824821-824824827,2121212118-2121212124
        """
    ]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 2)
        self.args_parser.add_argument(
            "--allow-any-repeat",
            action=argparse.BooleanOptionalAction,
            default=False,
            dest="allow_any_repeat",
        )
        self.add_args(run_args)


    def run(self):
        self.id_ranges = self._parse()
        n = self._find_dupe_seqs()
        debug_print(f"DUPE SUM {n}")
        return n
 

    # find ids with pattern <N><N>, that is any sequence repeated exactly twice
    # note this means we consider only those ids with an even number of digits
    def _find_dupe_seqs(self):
        dupe_sum = 0
        for r in self.id_ranges:
            for id_num in r:
                s = str(id_num)
                n = len(s)
                max_divs = n if self. allow_any_repeat else 2
                for num_divs in range(2, max_divs + 1):
                    # skip ids whose lengths are not divisible by div_len
                    if n % num_divs:
                        continue
                    div_len = n // num_divs
                    divs = [s[i * div_len:(i + 1) * div_len] for i in range(num_divs)]
                    if all([x == divs[0] for x in divs]):
                        dupe_sum += id_num
                        break
        return dupe_sum
    

    def _parse(self):
        # single element
        r = re.findall(r'(\d+)-(\d+)', self.input[0])
        return [range(int(x[0]), int(x[1]) + 1) for x in r]
