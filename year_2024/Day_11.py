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
        n =25
        for i in range(n):
            #if not i % 10:
            debug(f"{i + 1} -> {len(self.blink(stones, num_blinks=i + 1))}")
        #new_stones = self.blink(stones, num_blinks=n)
        #debug(f"{stones} BLINKS {n} -> N {len(new_stones)}")

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
        import math

        def _split(stone):
            f = math.pow(10,  (int(math.log10(stone)) + 1) // 2)
            return [int(stone // f), int(stone % f)]
        
        if num_blinks < 1:
            return stones
        
        st = stones[:]
        m = len(stones)
        for n in range(num_blinks):
            #new_stones = []
            #debug(f"INIT {st}")
            j = 0
            for i in range(len(st)):
                k = i + j
                s = st[k]
                if s == 0:
                    st[k] = 1
                    #new_stones.append(self._zero_to_one(s))
                elif not (int(math.log10(s)) + 1) % 2:
                    s1, s2 = _split(s)
                    st[k] = s1
                    st.insert(k + 1, s2)
                    j += 1
                    #new_stones.extend(_split(s))
                else:
                    st[k] = s * 2024
                    #new_stones.append(self._mult(s))
                #debug(f"N {n} I {i} {st}")
            #st = new_stones
        #return new_stones
        #debug(f"FINAL {st}")
        return st



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
