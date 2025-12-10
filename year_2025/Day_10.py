import Day
from utils.debug import debug_print, debug_if
from utils import mathutils
from utils import stringutils
import re


class Machine:

    ON = "#"
    OFF = "."

    STATES = {
        f"{ON}": 1,
        f"{OFF}": 0,
    }
    STATE_VALS = {v: k for k, v in STATES.items()}

    @classmethod
    def state_str(cls, state, state_len):
        s = "["
        n = state
        for i in range(state_len):
            p = 1 << (state_len - i - 1)
            q = n // p
            s += cls.STATE_VALS[q]
            n -= p * q
        s += "]"
        return s


    def __init__(self, goal_state_str, buttons, joltage):
        s = goal_state_str.strip("[]")
        self.num_lights = len(s)
        self.state = 0
        self.goal_state = 0
        for i, x in enumerate(s):
            self.goal_state += Machine.STATES[x] * (1 << i)
        
        self.buttons = [mathutils.sum([1 << x for x in y]) for y in buttons]
        self.joltage = joltage


    def press(self, idx):
        self.state ^= self.buttons[idx]


    def state_str_to_int(self, txt):
        s = txt.strip("[]")


    def current_state_str(self):
        return Machine.state_str(self.state, self.num_lights)

        

class AdventDay(Day.Base):

    TEST = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 10)
        self.add_args(run_args)
        self.machines = []


    # eigenvalues?
    def run(self):
        n = 0
        self._parse()
        i = 0
        b = 5
        m = self.machines[i]
        debug_print(m.buttons)
        debug_print(f"START {m.state} B {m.buttons[b]}")
        m.press(b)
        debug_print(f"NEXT {m.current_state_str()}")
        return n
 

    def _parse(self):
        def _parse_button(txt):
            b = []
            starts = stringutils.indices("(", txt)
            ends = stringutils.indices(")", txt)
            for i, s in enumerate(starts):
                b.append([int(x) for x in re.findall(r"\d", txt[s + 1: ends[i]])])
            return b

        def _parse_joltage(txt):
            return [int(x) for x in re.findall(r"\d+", txt[txt.index("{"):txt.index("}")])]

        for line in self.input:
            b = _parse_button(line)
            j = _parse_joltage(line)
            g = re.match(fr"\[[\{Machine.OFF}{Machine.ON}]+\]", line)[0]
            self.machines.append(Machine(g, b, j))
