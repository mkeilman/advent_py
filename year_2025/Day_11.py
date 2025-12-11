import Day
from utils.debug import debug_print, debug_if
from utils import mathutils
import re

class AdventDay(Day.Base):

    TEST = [
        "aaa: you hhh",
        "you: bbb ccc",
        "bbb: ddd eee",
        "ccc: ddd eee fff",
        "ddd: ggg",
        "eee: out",
        "fff: out",
        "ggg: out",
        "hhh: ccc fff iii",
        "iii: out",
    ]

    SERVER = [
        "svr: aaa bbb",
        "aaa: fft",
        "fft: ccc",
        "bbb: tty",
        "tty: ccc",
        "ccc: ddd eee",
        "ddd: hub",
        "hub: fff",
        "eee: dac",
        "dac: fff",
        "fff: ggg hhh",
        "ggg: out",
        "hhh: out",
    ]

    DAC = "dac"
    FFT = "fft"
    OUT = "out"
    SVR = "svr"
    YOU = "you"
    


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 11)
        self.args_parser.add_argument(
            "--count-dac-fft",
            action=argparse.BooleanOptionalAction,
            default=False,
            dest="count_dac_fft",
        )
        self.add_args(run_args)
        self.rack = {}


    def run(self):
        n = 0
        if self.mode == "test" and self.count_dac_fft:
            self.input = AdventDay.SERVER
        self._parse()
        #n = self._num_paths()
        self._ancestors(AdventDay.DAC)
        debug_print(f"N {n}")
        return n
 

    def _ancestors(self, device, chain=None, depth=0):
        c = chain or []
        c.append(device)
        parents = [x for x in self.rack if device in self.rack[x]]
        for p in parents:
            self._ancestors(p, chain=c, depth=depth+1)
        debug_if(f"{depth} {c}", "", "", depth == 0)


    def _num_paths(self, key=None, depth=0, dev_chain=None):
        n = 0
        k = key or (AdventDay.SVR if self.count_dac_fft else AdventDay.YOU)
        c = dev_chain or f"{k}"
        for d in self.rack[k]:
            dl = f"{c}:{d}"
            debug_if(f"{depth} {dl}", "", "", depth == 0)
            if d == AdventDay.OUT:
                debug_print(f"{depth} {dl}")
                if self.count_dac_fft:
                    #if AdventDay.DAC in dl and AdventDay.FFT in dl:
                    #    debug_print(f"{depth} {dl}")
                    return int(AdventDay.DAC in dl and AdventDay.FFT in dl)
                return 1
            else:
                n += self._num_paths(key=d, depth=depth+1, dev_chain=dl)
        
        return n


    def _parse(self):
        for line in self.input:
            d = re.findall(r"[a-z]{3}", line)
            self.rack[d[0]] = d[1:]

        v = self.rack.values()
