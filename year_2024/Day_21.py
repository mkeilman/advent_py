import re
import Day
from utils.debug import debug_print

class Keypad:

    basis = [(1, 0), (0, 1)]
    
    layout = [
        "789",
        "456",
        "123",
        " 0A"
    ]

    move_map = {
        "^": (-1, 0),
        "<": (0, -1),
        "v": (1, 0),
        ">": (0, 1),
    }

    dir_map = {v:k for k, v in move_map.items()}

    def __init__(self, init_digit="A", activation_digit="A", layout=None):
        self.layout = layout or Keypad.layout
        self.size = (len(self.layout), len(self.layout[0]))
        self.init_digit = init_digit
        self.activation_digit = activation_digit
        self.init_pos = self._digit_pos(self.init_digit)
        self.activation_pos = self._digit_pos(self.activation_digit)
        self.invalid_pos = self._digit_pos(" ")
        self.current_digit = self.init_digit
        self.current_pos = self.init_pos
        
    
    def code(self, grid):
        s = ""
        for txt in grid:
            for d in txt:
                self.next(d)
            s += self.current_digit
        return s


    def next(self, direction):
        d = Keypad.move_map[direction]
        self.current_pos = (
            max(0, min(self.current_pos[0] + d[0], len(self.layout) - 1)),
            max(0, min(self.current_pos[1] + d[1], len(self.layout[0]) - 1)),
        )
        self.current_digit = self._pos_digit(self.current_pos)


    def _code_path(self, code):
        p = []
        v = self.init_digit
        for c in code:
            p.extend(self._key_path(v, c))
            v = c
        return p
    

    def _code_actions(self, code):
        p = ""
        v = self.init_digit
        for c in code:
            for i, d in enumerate(self._key_path(v, c)):
                p += Keypad.dir_map.get(d) or p[-1] #self.init_digit
            if p[-1] != self.init_digit:
                p += self.init_digit
            v = c
        return p
    

    def _digit_pos(self, digit):
        for i in range(self.size[0]):
            if digit in self.layout[i]:
                return (i, self.layout[i].index(digit))
        return None


    # really need the path or just the number of steps?
    def _key_path(self, val1, val2):
        from utils import mathutils

        def _next(curr, dir):
            n = (curr[0] + dir[0], curr[1] + dir[1])
            return n if self._is_valid_pos(n) else None

        p1 = self._digit_pos(val1)
        p2 = self._digit_pos(val2)
        #debug_print(f"V1 {val1} P1 {p1} V2 {val2} P1 {p2}")
        assert self._is_valid_pos(p1) and self._is_valid_pos(p2)
        d = (p2[0] - p1[0], p2[1] - p1[1])
        d_move = (mathutils.sign(d[0]), mathutils.sign(d[1]))
        d_num = (abs(d[0]), abs(d[1]))
        #debug_print(f"{val1} -> {val2}: {d} MOVE {d_move} NUM {d_num}")
        # no motion
        if d_num == (0, 0):
            return [d_num]
        # no vertical
        if not d_num[0]:
            return d_num[1] * [(0, d_move[1])]
        # no horizontal
        if not d_num[1]:
            return d_num[0] * [(d_move[0], 0)]
        s = []
        p = p1
        #i = d_num.index(max(*d_num))
        i = 0 if p2[1] == self.invalid_pos[1] else 1
        while p != p2:
            b = Keypad.basis[i]
            m = d_move[i]
            v = (m * b[0], m * b[1])
            pp = _next(p, v)
            #debug_print(f"P {p} V {v} NEXT {pp}")
            if pp:
                s.append(v)
                p = pp
                if p[i] == p2[i]:
                    i = 1 - i
            else:
                # move along other axis
                i = 1 - i
            #i = 1 - i
        return s


    def _pos_digit(self, pos):
        return Keypad.layout[pos[0]][pos[1]]


    def _is_valid_pos(self, pos):
        return pos and pos != self.invalid_pos and 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]


class AdventDay(Day.Base):

    REPEATS = [
        "379A",
    ]

    SINGLE = [
        "2A"
    ]

    TEST = [
        "029A",
        "980A",
        "179A",
        "456A",
        "379A",
    ]


    def __init__(self, run_args):
        super(AdventDay, self).__init__(2024, 21)
        d = [
            " ^A",
            "<v>",
        ]
        self.numeric_keypad = Keypad()
        self.directional_keypad = Keypad(layout=d)
    

    def run(self):
        from utils import string

        self.input = AdventDay.REPEATS
        for c in self.input:
            p = self.numeric_keypad._code_path(c)
            k = self.numeric_keypad._code_actions(c)
            debug_print(f"CODE {c} PATH {p} KEYS {k}")
            k2 = self.directional_keypad._code_actions(k)
            debug_print(f"CODE {c} DIR KEYS 1 {k2}")
            k3 = self.directional_keypad._code_actions(k2)
            debug_print(f"CODE {c} DIR KEYS 2 {k3} LEN {len(k3)} NUM A {len(string.re_indices("A", k3))}")
            t = "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
            debug_print(f"CODE {c} REAL KEYS 2 {t} LEN {len(t)} NUM A {len(string.re_indices("A", t))}")
        return self._code_complexity("")


    def _code_complexity(self, code):
        return 0
