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

    LEVER_STATE_IND = "indicators"
    LEVER_STATE_JOLT = "joltage"

    @classmethod
    def state_int_to_str(cls, state, state_len):
        s = ""
        n = state
        for i in range(state_len):
            p = 1 << (state_len - i - 1)
            q = n // p
            s += cls.STATE_VALS[q]
            n -= p * q
        return f"[{s}]"


    @classmethod
    def state_str_to_int(cls, txt):
        s = txt.strip("[]")
        l = len(s)
        state = 0
        for i, p in enumerate(s):
            state += Machine.STATES[p] * (1 << (l - i - 1))
        return state, l
        

    def __init__(self, goal_state_str, buttons, goal_joltage):
        self.state = 0
        self.goal_state_str = goal_state_str
        self.goal_state, self.num_bits = Machine.state_str_to_int(goal_state_str)
        self.buttons = [mathutils.sum([1 << (self.num_bits - x - 1)for x in y]) for y in buttons]
        self.button_indices = buttons
        self.goal_joltage = goal_joltage
        self.joltage = len(self.goal_joltage) * [0]

        self.goal_fns = {
            f"{Machine.LEVER_STATE_IND}": self.seek_goal_state,
            f"{Machine.LEVER_STATE_JOLT}": self.seek_goal_joltage
        }
        self.lever_state = Machine.LEVER_STATE_IND


    def current_state_str(self):
        return Machine.state_int_to_str(self.state, self.num_bits)


    def seek_goal(self):
        return self.goal_fns[self.lever_state]()


    def seek_goal_joltage(self):
        import itertools

        debug_print("J")
        return 0
        indices = list(range(len(self.buttons)))
        for n in range(1, len(self.buttons) + 1):
            self.state = 0
            for c in itertools.combinations(indices, n):
                self.press_buttons(*c)
                if self.state == self.goal_state:
                    return n
                self.state = 0
        return 0
    

    def seek_goal_state(self):
        import itertools

        indices = list(range(len(self.buttons)))
        for n in range(1, len(self.buttons) + 1):
            self.state = 0
            for c in itertools.combinations(indices, n):
                self.press_buttons(*c)
                if self.state == self.goal_state:
                    return n
                self.state = 0
        return 0


    # a toggle is the same as bitwise exclusive or (^)
    def next_state(self, val):
            self.state ^= val

    
    def press(self, idx):
        self.next_state(self.buttons[idx])
        for i in self.button_indices[idx]:
            self.joltage[i] += 1
            #debug_print(f"PRESSSED {i} {self.button_indices[idx]} J NOW {self.joltage}")
    

    def press_buttons(self, *args):
        for i in args:
            self.press(i)
    


class AdventDay(Day.Base):

    TEST = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}",
    ]

    TWO_BIT = [
        "[.#] (0) (1) (1,0) {3,5,4,7}",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 10)
        self.args_parser.add_argument(
            "--lever-state",
            type=str,
            help="property for which to minimize button presses",
            choices=[Machine.LEVER_STATE_IND, Machine.LEVER_STATE_JOLT],
            default=Machine.LEVER_STATE_IND,
            dest="lever_state",
        )
        self.add_args(run_args)
        self.machines = []


    def run(self):
        n = 0
        self._parse()
        m = self.machines[2]
        m.press_buttons(0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 3)
        debug_print(f"{0} JOLTAGE {m.joltage} VS GOAL {m.goal_joltage}")
        return 0
        for i, m in enumerate(self.machines):
            m.press_buttons(*list(range(len(m.buttons))))
            debug_print(f"{i} JOLTAGE GOAL IN {m.joltage}")
            continue
            p = m.seek_goal()
            n += p
            debug_print(f"{i} FOUND GOAL IN {p} PRESSES")
        debug_print(f"{n} TOTAL PRESSES")
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
            m = Machine(g, b, j)
            m.lever_state = self.lever_state
            self.machines.append(m)
