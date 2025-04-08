import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug_print

class Disk:

    def __init__(self, txt, whole_files=True):
        import math

        self.map = [int(x) for x in re.findall(r"\d", txt)]
        self.num_files = math.ceil(len(self.map) / 2)
        self.blocks = self._blocks()
        self.defragged = self._defrag(whole_files=whole_files)
        self.checksum = self._checksum()
        

    def _blocks(self):
        a = []
        for i, c in enumerate(self.map):
            a.extend(c * [-1 if i % 2 else (i // 2)])
        return a
    

    def _checksum(self):
        return mathutils.sum([i * x for i, x in enumerate(self.defragged) if x >= 0])


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
            for i in reversed(range(self.num_files)):
                a = string.indices(i, arr)
                na = len(a)
                e = [x for x in _empty_ranges(arr) if len(x) >= na]
                if not e or e[0][0] > a[-1]:
                    continue
                for j in e[0][:na]:
                    arr[j] = i
                for j in a:
                    arr[j] = -1
            return arr

        a = self.blocks[:]
        return _move_files(a) if whole_files else _move_blocks(a)
            

class AdventDay(Day.Base):
    
    CONSEC = [
        "12345",
    ]
    TEST = [
        "2333133121414131402",
    ]
    
    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 9)
        self.args_parser.add_argument(
            "--whole-files",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="whole_files",
        )
        self.add_args(run_args)

    def run(self):
        # single line
        d = Disk(self.input[0], whole_files=self.whole_files)
        n = d.checksum
        debug_print(f"C {n}")
        return n



def main():
    d = AdventDay()
    debug_print("TEST:")
    d.run_from_test_input()
    debug_print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
