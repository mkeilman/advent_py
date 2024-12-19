import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug
    
class AdventDay(Day.Base):

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            11,
            #[
            #    "0 1 10 99 999",
            #],
            [
                "125 17",
            ]
            #[
            #    "0",
            #]
        )

    def run(self, v):
        # single line
        stones = [int(x) for x in re.findall(r"\d+", v[0])]
        n = 75
        #for i in range(n):
        #    #if not i % 10:
        #    debug(f"{i + 1} -> {len(self.blink(stones, num_blinks=i + 1))}")
        s = self.blink(stones, num_blinks=n)
        debug(f"{n} -> {self.num_stones(s)}")


    #def blink(self, stones, num_blinks=1):
    #    if num_blinks < 1:
    #        return stones
    #    m = len(stones)
    #    new_stones = []
    #    for s in stones:
    #        if s == 0:
    #            new_stones.append(self._zero_to_one(s))
    #        elif not len(f"{s}") % 2:
    #            m += 1
    #            new_stones.extend(self._split(s))
    #        else:
    #            new_stones.append(self._mult(s))
    #    #debug(f"M {m}")
    #    return new_stones if num_blinks == 1 else self.blink(new_stones, num_blinks=num_blinks - 1)

    def blink(self, stones, num_blinks=1):
        import time

        def _num_digits(s):
            if s == 0:
                return 1
            return int(math.log10(s)) + 1
        
        def _split(s):
            f = math.pow(10,  _num_digits(s) // 2)
            return [int(s // f), int(s % f)]
        
        if num_blinks < 1:
            return stones
        
        st = stones[:]
        #debug(f"N DIGS {[_num_digits(x) for x in st]}")
        tt = time.time()
        p_dict = {}
        #pd = {}
        self._fill_p_dict(st, p_dict)
        #for s in p_dict:
        #    p_dict[s]["next"] = self._next_stones(s)
        #debug(p_dict)
        max_s = 0
        m = len(st)
        last_len = len(st)
        for n in range(num_blinks):
            t0 = time.time()
            new_stones = []
            pd = {}
            #self._fill_p_dict(st, p_dict)
            for s in p_dict:
            #for s in st:
            #    if s not in p_dict:
            #        p_dict[s] = {"count": 0, "next": -1}
            #    p_dict[s]["count"] += 1
                next_s = p_dict[s]["next"]
                if next_s == -1:
                    #ns = self._next_stones(s)
                    #p_dict[s]["next"] = ns
                    p_dict[s]["next"] = self._next_stones(s)
                else:
                    #debug(f"{n} FILL WITH {p_dict[s]["next"]}")
                    self._fill_p_dict(p_dict[s]["next"], pd, num_stones=p_dict[s]["count"])
                    #ns = next_s
                #ns = self._next_stones(s)
                #new_stones.extend(ns)
            #debug(f"PD {pd}")
            p_dict = pd
            #self._merge_dicts(p_dict, pd)
            #st = new_stones
            #st_set = set(st)
            #debug(f"N DIGS {[_num_digits(x) for x in st]}")
            #max_s = max(max_s, max(st))
            t1 = time.time()
            #debug(f"{n} LEN {len(st)} DIFF {len(st) - last_len} LEN SET {len(st_set)} SET FACTOR {len(st) / len(st_set)} TIME {int(t1 - t0)}")
            last_len = len(st)
        #debug(f"FINAL {st}")
        t1 = time.time()
        debug(f"{num_blinks} TOTAL TIME {int(t1 - tt)}")
        return p_dict
        #return st


    def num_stones(self, p_dict):
        n = 0
        for s in p_dict:
            n += p_dict[s]["count"]
        return n
        

    def _fill_p_dict(self, st, p_dict, num_stones=1):
        for s in st:
            if s not in p_dict:
                p_dict[s] = {"count": 0, "next": self._next_stones(s)}
            p_dict[s]["count"] += num_stones

    # d2 into d1
    def _merge_dicts(self, d1, d2):
        for k in d2:
            if k not in d1:
                d1[k] = d2[k]
            else:
                d1[k]["count"] += d2[k]["count"]
        #for k in [x for x in d1.keys() if x not in d2]:
        #    del d1[k]
 


    def _inds(self, s):
        pass

    def _nsa(self, arr):
        r = []
        for s in arr:
            r.extend(self._next_stones(s))
        return r

    def _next_stones(self, s):
        def _split(s):
            f = math.pow(10,  (int(math.log10(s)) + 1) // 2)
            return [int(s // f), int(s % f)]
        
        if s == 0:
            return [1]
        if not (int(math.log10(s)) + 1) % 2:
            return _split(s)
        return [s * 2024]


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
