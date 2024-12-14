import re
import Day
from utils import math
from utils import string
from utils.debug import debug

class Disk:

    def __init__(self, txt, whole_files=True):
        self.map = [int(x) for x in re.findall(r"\d", txt)]
        f = [x for i, x in enumerate(self.map) if not i % 2]
        self.num_files = len(f)
        self.blocks = self._blocks()
        self.defragged = self._defrag(whole_files=whole_files)
        self.checksum = self._checksum()
        

    def _blocks(self):
        a = []
        for i, c in enumerate(self.map):
            a.extend(c * [-1 if i % 2 else (i // 2)])
        return a
    

    def _checksum(self):
        return math.sum([i * x for i, x in enumerate(self.defragged) if x >= 0])


    def _defrag(self, whole_files=True):
        def _empty_ranges(arr):
            a = []
            j = 0
            for i, c in enumerate(arr):
                if c >= 0:
                    if i > j:
                        a.append(range(j, i))
                        j = i
                    j += 1
            return a

        def _move_blocks(arr):
            #debug(f"MT {arr} {_empty_ranges(arr)}")
            n = len(self.blocks)
            for i in range(n):
                j = n - i - 1
                c = self.blocks[j]
                if c == -1:
                    continue
                k = arr.index(-1)
                if k > j:
                    break
                arr[k] = c
                arr[j] = -1
            return [x for x in arr if x >= 0]

        def _move_files(arr):

            e = _empty_ranges(arr)

            return arr

        a = self.blocks[:]
        if whole_files:
            return _move_files(a)
        return _move_blocks(a)
            

class AdventDay(Day.Base):
            
    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            9,
            [
                "2333133121414131402",
            ]
            #[
            #    "12345",
            #]
        )
        self.args_parser.add_argument(
            "--whole-files",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="whole_files",
        )
        self.whole_files = self.args_parser.parse_args(run_args).whole_files

    def run(self, v):
        # single line
        d = Disk(v[0], whole_files=self.whole_files)
        debug(f"C {d.checksum}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
