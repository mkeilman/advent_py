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
    

    def _code_keys(self, code, iteration=0, key_dict=None):
        import sys

        #debug_print(f"GET KEYS FROM {code}")

        def _keys(path):
            k = ""
            for d in path:
                k += Keypad.dir_map.get(d) or k[-1]
            if k[-1] != self.init_key:
                k += self.init_key
            return k


        def _next_keys(last_keys):
            next_keys = []
            #mnd = sys.maxsize
            key1 = self.init_key
            for key2 in last_keys:
                q = [] if key1 == key2 else [_keys(x) for x in self._key_paths(key1, key2)]
                key1 = key2
                if not next_keys:
                    next_keys = q
                    continue
                d = []
                for x in next_keys:
                    for y in q or [x[-1]]:
                        #mnd = min(mnd, len(x + y))
                        d.append(x + y)
                next_keys = d
            #debug_print(f"LAST {last_keys} -> NEXT {next_keys}")
            return next_keys

        assert iteration >= 0

        #debug_print(f"{iteration} CK {code}")

        is_single_code = isinstance(code, str)
        keys = key_dict or {}
        
        codes = [code] if is_single_code else code

        while iteration >= 0:
            mn = sys.maxsize
            #key1 = self.init_key
            #keys = key_dict or {}
            #keys[iteration] = {} #keys.get(iteration) or {}
            #keys[iteration][code] = []
            #pp = []
            #mnd = sys.maxsize
            #for key2 in code:
            #    q = [] if key1 == key2 else [_keys(x) for x in self._key_paths(key1, key2)]
            #    #debug_print(f"{key1} -> {key2}: Q {q}")
            #    key1 = key2
            #    if not pp:
            #        pp = q
            #        continue
            #    d = []
            #    for x in pp:
            #        for y in q or [x[-1]]:
            #            mnd = min(mnd, len(x + y))
            #            d.append(x + y)
            #    pp = d

            #min_len = min([len(x[0]) for x in keys[iteration].values()]) if keys[iteration] else sys.maxsize
            #mn = min([len(x) for x in pp])
            #debug_print(f"{iteration} C {code} -> MN {mn} MIN LEN {min_len}")
            #codes = [_next_keys(x) for x in codes]
            cc = []
            for c in codes:
                n = _next_keys(c)
                l = len(n[0])
                #if iteration:
                #    #debug_print(f"{iteration} KEEP ALL {l}")
                #    #cc = n
                #    cc.extend(n)
                #    continue
                # new min, replace
                if l < mn:
                    #debug_print(f"{iteration} NEW MIN {l}")
                    mn = l
                    cc = n
                # existing min, add
                elif l == mn:
                    #debug_print(f"{iteration} EXISTING MIN {l}")
                    cc.extend(n)
                else:
                    #debug_print(f"{iteration} TOO BIG {l}")
                    pass
            codes = cc
            debug_print(f"C {code} MAPS TO {len(codes)} KEYS")
            #keys[iteration][code] = _next_keys(code) #pp
            iteration -= 1
        #keys[code] = codes
        #debug_print(f"LENS {[len(x) for x in codes]}")
        return codes if is_single_code else codes[0]


        #keys[iteration][code] = pp
        #if iteration:
        #    for p in pp:
        #        keys.update(self._code_keys(p, iteration=iteration-1, key_dict=keys))
        return keys
    

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
        return [d_num] if d_num == (0, 0) else self.all_paths[(p1, p2)][0]



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
        self.args_parser.add_argument(
            "--num-iterations",
            type=int,
            help="number of directional keypad iterations",
            default=1,
            dest="num_iterations",
        )
        self.add_args(run_args)
        self.numeric_keypad = Keypad()
        self.directional_keypad = Keypad(layout=[" ^A", "<v>",])
    

    def run(self):
        from utils import string

        self.input = AdventDay.SINGLE
        complexity = 0
        for c in self.input:
            complexity += self._code_complexity(c)
        debug_print(f"COMPL {complexity}")
        return complexity


    def _code_complexity(self, code):
        import sys

        nk = self.numeric_keypad._code_keys(code)
        #debug_print(f"NK {nk}")
        dk = {}
        #for c in nk[0][code]:
        #for c in nk[code]:
        #for c in nk:
        dk = self.directional_keypad._code_keys(nk, iteration=self.num_iterations, key_dict=dk)
        #debug_print(f"DK {dk}")
        n = int(re.match(r"\d+", code).group(0))
        mn = len(dk)
        # final iteration is 0
        #mn = sys.maxsize
        #for x in dk[0]:
        #    a = dk[0][x]
        #    #debug_print(f"{x}: {len(a)} {len(a[0])}")
        #    mn = min(mn, len(a[0]))
        #mn = min(dk[0].values())

        debug_print(f"CODE {code} MN {mn} {n}")
        return n * mn
