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

    def __init__(self, init_key="A", activation_key="A", invalid_key=" ", layout=None):
        self.layout = layout or Keypad.layout
        self.size = (len(self.layout), len(self.layout[0]))
        self.grid = Day.Grid.grid_of_size(*self.size)
        self.init_key = init_key
        self.activation_key = activation_key
        self.invalid_key = invalid_key
        self.init_pos = self._position_of(self.init_key)
        self.activation_pos = self._position_of(self.activation_key)
        self.invalid_pos = self._position_of(self.invalid_key)
        self.all_paths = self._all_paths()
        self.current_digit = self.init_key
        self.current_pos = self.init_pos
        
    
    def code(self, grid):
        s = ""
        for txt in grid:
            for d in txt:
                self.next(d)
            s += self.current_digit
        return s


    def to_input(self, txt):
        r = txt[::-1]
        i = self.activation_key
        p = self.init_pos
        did_poke = False
        for c in r[1:]:
            if c == self.activation_key:
                if not did_poke:
                    i += self._digit_at(p)
                else:
                    did_poke = True
                continue
            if did_poke:
                i += self._digit_at(p)
                did_poke = False
            d = Keypad.move_map[c]
            p = (p[0] - d[0], p[1] - d[1])
        return i[::-1]
    

    def next(self, direction):
        d = Keypad.move_map[direction]
        self.current_pos = (
            max(0, min(self.current_pos[0] + d[0], len(self.layout) - 1)),
            max(0, min(self.current_pos[1] + d[1], len(self.layout[0]) - 1)),
        )
        self.current_digit = self._digit_at(self.current_pos)


    def _all_paths(self):
        paths = {}
        a = self.grid.flat_array
        n = len(a)
        for i in range(n):
            if a[i] == self.invalid_pos:
                continue
            for j in range(i + 1, n):
                if a[j] == self.invalid_pos:
                    continue
                p = self._paths(a[i], a[j])
                paths[(a[i], a[j])] = p
        # build the paths going the other direction
        r = {}
        for k in paths.keys():
            r[(k[1], k[0])] = []
            for rp in [x[::-1] for x in paths[k]]:
                r[(k[1], k[0])].append([(-1 * x[0], -1 * x[1]) for x in rp])
        paths.update(r)
        return paths

    def _paths(self, p1, p2):
        from utils import mathutils
        
        assert p1 != self.invalid_pos and p2 != self.invalid_pos
        
        if p1 == p2:
            return []
        
        paths = []

        dp = (p2[0] - p1[0], p2[1] - p1[1])
        d = (mathutils.sign(dp[0]), mathutils.sign(dp[1]))
        if not d[0]:
            return [abs(dp[1]) * [d]]
        if not d[1]:
            return [abs(dp[0]) * [d]]
        # row 1st
        n = (p1[0] + d[0], p1[1])
        if n != self.invalid_pos:
            for x in self._paths(n, p2):
                paths.append([(d[0], 0)]  + x)
        # col 2nd
        n = (p1[0], p1[1] + d[1])
        if n != self.invalid_pos:
            for x in self._paths(n, p2):
                paths.append([(0, d[1])]  + x)
        return paths


    def _code_path(self, code):
        p = []
        v = self.init_key
        for c in code:
            p.extend(self._key_path(v, c))
            v = c
        return p
    

    def _code_keys(self, code, depth=0, key_dict=None):
        import sys

        def _keys(path):
            k = ""
            for d in path:
                k += Keypad.dir_map.get(d) or k[-1]
            if k[-1] != self.init_key:
                k += self.init_key
            return k


        assert depth >= 0

        #debug_print(f"{depth} CK {code}")

        #p = ""
        key1 = self.init_key
        keys = key_dict or {}
        #keys[code] = []
        keys[depth] = keys.get(depth) or {}
        #keys[depth][code] = []
        pp = []
        for key2 in code:
            q = [] if key1 == key2 else [_keys(x) for x in self._key_paths(key1, key2)]
            #debug_print(f"{key1} -> {key2}: Q {q}")
            key1 = key2
            if not pp:
                pp = q
                continue
            d = []
            for x in pp:
                for y in q or [x[-1]]:
                    d.append(x + y)
            pp = d
            #debug_print(f"{key1} -> {key2}: Q {q} PP {pp}")

            #for path in self._key_paths(key1, key2):
            #    #p = ""
            #    #key1 = self.init_key
            #    for d in path: #self._key_path(key1, key2):
            #        p += Keypad.dir_map.get(d) or p[-1]
            #    #debug_print(f"{code} -> PATH {path} -> P {p}")
            #    if p[-1] != self.init_key:
            #        p += self.init_key
            #key1 = key2
        #min_len = min([len(x) for x in keys[depth].values()])
        #mn = min([len(x) for x in pp])
        keys[depth][code] = pp
        #debug_print(f"{depth} C {code} -> NPP {len(pp)} MN {len(pp[0])}")
        #min_len = min([len(x) for x in keys[depth].values()])
        #min_len = min([len(x) for x in pp])

        if depth:
            #min_len = sys.maxsize
            #debug_print(f"{depth} NEW MIN {min_len}")
            for p in pp:
                next = self._code_keys(p, depth=depth-1, key_dict=keys)
                #mn = min([len(x) for x in next[depth - 1][p]])
                #l = len(next[p][0])
                #if mn > min_len:
                #    debug_print(f"{depth} SKIP {p} ({mn} VS {min_len})")
                #    continue
                #debug_print(f"{depth} KEEP {p} ({mn} VS {min_len})")
                keys.update(next)
                #min_len = mn
        return keys
        #return self._code_keys(p, depth=depth-1) if depth else p
    

    def _position_of(self, key):
        for i in range(self.size[0]):
            if key in self.layout[i]:
                return (i, self.layout[i].index(key))
        return None


    def _is_valid_pos(self, pos):
        return pos and pos != self.invalid_pos and 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]


    def _pos_paths(self, p1, p2):
        assert self._is_valid_pos(p1) and self._is_valid_pos(p2)
        return [[(0, 0)]] if p1 == p2 else self.all_paths[(p1, p2)]


    # really need the path or just the number of steps?
    def _pos_path(self, p1, p2):
        from utils import mathutils

        def _next(curr, dir):
            n = (curr[0] + dir[0], curr[1] + dir[1])
            return n if self._is_valid_pos(n) else None

        assert self._is_valid_pos(p1) and self._is_valid_pos(p2)

        d = (p2[0] - p1[0], p2[1] - p1[1])
        d_move = (mathutils.sign(d[0]), mathutils.sign(d[1]))
        d_num = (abs(d[0]), abs(d[1]))
        # no motion
        if d_num == (0, 0):
            return [d_num]
        
        p = self.all_paths[(p1, p2)][0]
        #debug_print(f"P1 {p1} -> P2 {p2}: {p}")
        return self.all_paths[(p1, p2)][0]
    
        # no vertical
        if not d_num[0]:
            return d_num[1] * [(0, d_move[1])]
        # no horizontal
        if not d_num[1]:
            return d_num[0] * [(d_move[0], 0)]
        s = []
        p = p1
        #i = d_num.index(max(*d_num))
        i = 0 if p1[0] == self.invalid_pos[0] else 1 #if p1[1] == self.invalid_pos[1] else 1
        while p != p2:
            b = Keypad.basis[i]
            m = d_move[i]
            v = (m * b[0], m * b[1])
            pp = _next(p, v)
            #debug_print(f"P {p} V {v} NEXT {pp}")
            if pp:
                s.append(v)
                p = pp
                # reached the final row or column, switch to other axis
                if p[i] == p2[i]:
                    i = 1 - i
            else:
                # can't move to this key, switch to other axis
                i = 1 - i
        #debug_print(f"P1 {p1} P2 {p2} PATH {s}")
        return s


    def _digit_at(self, pos):
        return self.layout[pos[0]][pos[1]]


    def _reverse_direction(self, dir):
        return (-1 * dir[0], -1 * dir[1])


    def _reverse_key(self, key):
        return Keypad.dir_map[self._reverse_direction(Keypad.move_map[key])]


    def _key_path(self, val1, val2):
        return self._pos_path(self._position_of(val1), self._position_of(val2))


    def _key_paths(self, val1, val2):
        return self._pos_paths(self._position_of(val1), self._position_of(val2))


class AdventDay(Day.Base):

    REPEATS = [
        "222A",
    ]

    SINGLE = [
        "9A"
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

        #self.input = AdventDay.REPEATS
        complexity = 0
        for c in self.input:
            #p = self.numeric_keypad._code_path(c)
            #k = self.numeric_keypad._code_keys(c)
            #debug_print(f"CODE {c} PATH {p} KEYS {k}")
            #p2 = self.directional_keypad._code_path(k)
            #k2 = self.directional_keypad._code_keys(k)
            #debug_print(f"CODE {c} PATH {p2} DIR KEYS 1 {k2}")
            #k3 = self.directional_keypad._code_keys(k2)
            #debug_print(f"CODE {c} DIR KEYS 2 {k3} LEN {len(k3)} NUM A {len(string.re_indices("A", k3))}")
            #i2 = self.directional_keypad.to_input(k3)
            #i1 = self.directional_keypad.to_input(i2)
            #cc = self.numeric_keypad.to_input(i1)
            #debug_print(f"CODE {c} INPUTS {k3} -> {i2} -> {i1} -> {cc}")
            complexity += self._code_complexity(c)
        #t = "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"
        #t1 = "^A<<^^A>>AvvvA"
        #t2 = "<A>Av<<AA>^AA>AvAA^A<vAAA>^A"
        #t2 = self.directional_keypad._code_keys(t1)
        #tt = self.directional_keypad._code_keys(t2)
        #debug_print(tt)
        #ti = self.directional_keypad.to_input(t)
        #tii = self.directional_keypad.to_input(ti)
        #tiii = self.numeric_keypad.to_input(tii)
        #debug_print(f"T {t} -> {ti} -> {tii} -> {tiii}")
        debug_print(f"COMPL {complexity}")
        return complexity


    def _code_complexity(self, code):
        import sys

        nk = self.numeric_keypad._code_keys(code)
        dk = {}
        for c in nk[0][code]:
            dk = self.directional_keypad._code_keys(c, depth=1, key_dict=dk)
        #k = self.directional_keypad._code_keys(
        #    self.numeric_keypad._code_keys(code),
        #    depth=1
        #)
        n = int(re.match(r"\d+", code).group(0))
        dkk = list(dk.keys())
        nkk = list(nk.keys())
        # final iteration is 0
        mn = sys.maxsize
        for x in dk[0]:
            a = dk[0][x]
            #debug_print(f"{x}: {len(a)} {len(a[0])}")
            mn = min(mn, len(a[0]))
        ld = dk[0].keys()
        l = [len(x) for x in dk[0].values()]
        #mn = min(dk[0].values())

        debug_print(f"CODE {code} MN {mn} {n}")
        return n * mn
