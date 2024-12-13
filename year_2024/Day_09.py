import re
import Day
from utils import math
from utils import string
from utils.debug import debug

class Disk:

    def __init__(self, txt):
        self.map = txt
        s = re.findall(r"\d", txt)
        self.files = [int(x) for i, x in enumerate(s) if not i % 2]
        self.spaces = [int(x) for i, x in enumerate(s) if i % 2]
        self.blocks = self._blocks()
        self.defragged = self._defrag()
        self.checksum = self._checksum()
        

    def _blocks(self):
        s = ""
        for i, c in enumerate(self.map):
            if not i % 2:
                s += int(c) * str(i // 2)
            else:
                s += int(c) * "."
        return s
    
    def _checksum(self):
        n = 0
        for i, c in enumerate(self.defragged):
            n += i * int(c)
        return n

    def _defrag(self):
        n = len(self.blocks)
        n_moves = 0
        arr = re.findall(r".", self.blocks)
        for i in range(n):
            j = n - i - 1
            c = self.blocks[j]
            if c == ".":
                continue
            k = arr.index(".")
            if k > j:
                break
            arr[k] = c
            arr[j] = "."
            n_moves += 1
        return "".join(arr).replace(".", "")
            


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
        debug(f"C {d.defragged}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
