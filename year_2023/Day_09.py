import re
import Day
from utils import math


class Sequence():

    @classmethod
    def seq_sums(cls, seqs, index=-1):
        return math.sum([x.seq[0][index] for x in seqs])
    
    def __init__(self, seq_str):
        self.seq = []
        self.seq.append([int(x) for x in re.findall(r"\-?\d+", seq_str)])
        curr = self.seq[0]
        while not all([not x for x in curr]) and len(curr):
            curr = [curr[i + 1] - x for i, x in enumerate(curr[:-1])]
            self.seq.append(curr)
        self._complete_seqs()
        #print(self.seq)

    def _complete_seqs(self):
        d = self.seq[-1][-1]
        dd = self.seq[-1][0]
        for s in reversed(self.seq[:-1]):
            s.append(s[-1] + d)
            s.insert(0, s[0] - dd)
            d = s[-1]
            dd = s[0]
        
            

class AdventDay(Day.Base):

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2023,
            9,
            [
                "0 3 6 9 12 15",
                "1 3 6 10 15 21",
                "10 13 16 21 30 45",
            ]
        )


    def run(self, v):
        self.seqs = [Sequence(x) for x in v]
        print(f"SUM {Sequence.seq_sums(self.seqs, index=0)}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
