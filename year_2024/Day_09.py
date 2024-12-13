import re
import Day
from utils import math
from utils import string
from utils.debug import debug

class Disk:

    def __init__(self, txt):
        self.map = txt
        s = [int(x) for x in re.findall(r"\d", self.map)]
        self.map_arr = s
        f = [x for i, x in enumerate(s) if not i % 2]
        num_files = len(f)
        debug(f"N FILES {num_files}")
        sp = [x for i, x in enumerate(s) if i % 2]
        num_spaces = len(sp)
        self.space_inds = [math.sum(f[:i]) + math.sum(sp[:i - 1]) for i in range(1, num_files)]
        self.size = math.sum(f)
        debug(f"SZ {self.size}")
        self.blocks = self._blocks()
        self.defragged = self._defrag()
        debug(f"DF SZ {len(self.defragged)}")
        self.checksum = self._checksum()
        self.df = [None] * (num_files + num_spaces)
        

    def _blocks(self):
        s = ""
        a = []
        for i, c in enumerate(self.map_arr):
            if not i % 2:
                a.extend(c * [i // 2])
            else:
                a.extend(c * [-1])
        return a


        for i, c in enumerate(self.map):
            if not i % 2:
                s += int(c) * str(i // 2)
            else:
                s += int(c) * "."
        return s
    
    def _checksum(self):
        #return math.sum([i * int(x) for i, x in enumerate(self.defragged)])
        return math.sum([i * x for i, x in enumerate(self.defragged)])

    def _defrag(self):
        n = len(self.blocks)
        n_moves = 0
        #arr = re.findall(r".", self.blocks)
        arr = self.blocks[:]
        for i in range(n):
            j = n - i - 1
            c = self.blocks[j]
            if c == -1:
            #if c == ".":
                continue
            #k = arr.index(".")
            k = arr.index(-1)
            if k > j:
                break
            arr[k] = c
            #arr[j] = "."
            arr[j] = -1
            #debug("".join(arr))
            n_moves += 1
        #return "".join(arr).replace(".", "")
        return [x for x in arr if x >= 0]
            


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
            "--t-nodes",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="t_nodes",
        )
        self.t_nodes = self.args_parser.parse_args(run_args).t_nodes

    def run(self, v):
        # single line
        d = Disk(v[0])
        debug(f"C {d.checksum}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
