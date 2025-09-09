import re
import Day
from utils import mathutils
from utils.debug import debug_print, debug_if

class Wire:

    def __init__(self, name, init_val=None):
        self.name = name
        self.init_val = init_val
        self.reset()

    def __repr__(self):
        return f"{self.name}: {self.val}"
    

    def reset(self):
        self.val = self.init_val


class Gate:

    op_map = {
        "AND": lambda x, y: int(x and y),
        "OR": lambda x, y: int(x or y),
        "XOR": lambda x, y: int(x != y),
    }

    def __init__(self, in1, in2, out, op_str):
        self.in1 = in1
        self.in2 = in2
        self.inputs = (self.in1, self.in2)
        self.out = out
        self.name = out.name
        self.op_str = op_str
        self.wires = (in1, in2, out)
        self.op = Gate.op_map[op_str]


    def __repr__(self):
        return f"{self.in1.name} {self.op_str} {self.in2.name}: {self.out.name}"


    def eval(self):
        self.out.val = self.op(self.in1.val, self.in2.val)
    

    def vals(self):
        return [x.val for x in self.wires]
    
    
    

class AdventDay(Day.Base):

    TEST = [
        "x00: 1",
        "x01: 1",
        "x02: 1",
        "y00: 0",
        "y01: 1",
        "y02: 0",
        "",
        "x00 AND y00 -> z00",
        "x01 XOR y01 -> z01",
        "x02 OR y02 -> z02",
    ]

    TEST_LARGE = [
        "x00: 1",
        "x01: 0",
        "x02: 1",
        "x03: 1",
        "x04: 0",
        "y00: 1",
        "y01: 1",
        "y02: 1",
        "y03: 1",
        "y04: 1",
        "",
        "ntg XOR fgs -> mjb",
        "y02 OR x01 -> tnw",
        "kwq OR kpj -> z05",
        "x00 OR x03 -> fst",
        "tgd XOR rvg -> z01",
        "vdt OR tnw -> bfw",
        "bfw AND frj -> z10",
        "ffh OR nrd -> bqk",
        "y00 AND y03 -> djm",
        "y03 OR y00 -> psh",
        "bqk OR frj -> z08",
        "tnw OR fst -> frj",
        "gnj AND tgd -> z11",
        "bfw XOR mjb -> z00",
        "x03 OR x00 -> vdt",
        "gnj AND wpb -> z02",
        "x04 AND y00 -> kjc",
        "djm OR pbm -> qhw",
        "nrd AND vdt -> hwm",
        "kjc AND fst -> rvg",
        "y04 OR y02 -> fgs",
        "y01 AND x02 -> pbm",
        "ntg OR kjc -> kwq",
        "psh XOR fgs -> tgd",
        "qhw XOR tgd -> z09",
        "pbm OR djm -> kpj",
        "x03 XOR y03 -> ffh",
        "x00 XOR y04 -> ntg",
        "bfw OR bqk -> z06",
        "nrd XOR fgs -> wpb",
        "frj XOR qhw -> z04",
        "bqk OR frj -> z07",
        "y03 OR x01 -> nrd",
        "hwm AND bqk -> z03",
        "tgd XOR rvg -> z12",
        "tnw OR pbm -> gnj",
    ]

    TEST_SWAPPED = [
        "x00: 0",
        "x01: 1",
        "x02: 0",
        "x03: 1",
        "x04: 0",
        "x05: 1",
        "y00: 0",
        "y01: 0",
        "y02: 1",
        "y03: 1",
        "y04: 0",
        "y05: 1",
        "",
        "x00 AND y00 -> z00",
        "x01 AND y01 -> z01",
        "x02 AND y02 -> z02",
        "x03 AND y03 -> z03",
        "x04 AND y04 -> z04",
        "x05 AND y05 -> z05",
    ]

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2024, 24)
        self.args_parser.add_argument(
            "--validate-sum",
            action=argparse.BooleanOptionalAction,
            default=True,
            dest="validate_sum",
        )
        self.add_args(run_args)
        self.gates = []
        self.wires = {}
        self.num_bits = 0
    

    def solve(self):
        self.reset()
        while self._wires_with_no_value():
            for g in self._solved_gates():
                g.eval()
    

    def reset(self):
        for w in self.wires.values():
            w.reset()


    def run(self):
        #self.input = AdventDay.TEST_SWAPPED
        self._parse()
        self.solve()
        #b = self.num_bits
        xyz, sum, mod_sum = self._get_sum()
        #debug_print(f"X {xyz['x']} + Y {xyz['y']} -> Z {xyz['z']} VS SUM {sum}")
        if not self.validate_sum:
            return xyz["z"]
        debug_print(f"VALIDATE {len([x.name for x in self._get_outputs()])}")
        self._validate()
        return 0


    def _solved_gates(self):
        return [x for x in self.gates if x.in1.val is not None and x.in2.val is not None]


    def _gates_with_wire(self, wire_name):
        gates = []
        for g in self.gates:
            if wire_name in [x.name for x in g.wires]:
                gates.append(g)
        return gates
    

    def _gates_connected_to(self, wire_name):
        res = []
        for g in self._gates_with_wire(wire_name):
            res.extend([self._gates_connected_to(x.name) for x in g.wires])
        return res


    def _gates_for_bit(self, bit_num):
        return self._gates_with_wire(f"z{bit_num:02}")

    def _gates_for_bits(self, n_bits):
        res = []
        for i in range(n_bits):
            res.extend(self._gates_for_bit(i))
        return res


    def _get_sum(self, max_bits=None):
        res = {}
        mb = max_bits or self.num_bits
        for w in ("x", "y", "z"):
            res[w] = self._tag_number(w, max_bits=mb)
        #debug_print(f"{mb} BITS: SUM {res["x"] + res["y"]}; MOD SUM {(res["x"] + res["y"]) % (1 << mb)}")
        return res, res["x"] + res["y"], (res["x"] + res["y"]) % (1 << mb)
        #return res, res["x"] + res["y"]


    def _get_outputs(self):
        return [x.out for x in self.gates]


    def _parse(self):
        def _parse_wire(txt):
            m = re.search(fr"({n}):\s+([01])$", txt)
            return Wire(m.group(1), init_val=int(m.group(2)))
        
        def _parse_gate(txt, preset_wires):
            m = re.search(fr"({n})\s+(AND|OR|XOR)\s+({n})\s+->\s+({n})", txt)
            return Gate(
                preset_wires.get(m.group(1)) or Wire(m.group(1)),
                preset_wires.get(m.group(3)) or Wire(m.group(3)),
                preset_wires.get(m.group(4)) or Wire(m.group(4)),
                m.group(2)
            )


        n = r"[a-z0-9]{3}"
        wires_done = False
        for line in self.input:
            if not line:
                wires_done = True
                continue
            if not wires_done:
                w = _parse_wire(line)
                self.wires[w.name] = w
            else:
                g = _parse_gate(line, self.wires)
                self.gates.append(g)
                for w in [x for x in g.wires if x.name not in self.wires]:
                    self.wires[w.name] = w
        self.num_bits = len(self._tag_wires("z"))
    

    def _swap_vals(self, w1, w2):
        t = w1.val
        w1.val = w2.val
        w2.val = t

    def _swap_outputs(self, gate1, gate2):
        t = gate1.out
        gate1.out = gate2.out
        gate2.out = t


    def _tag_number(self, tag, max_bits=None):
        res = 0
        w = self._tag_wires(tag)
        mb = max_bits or len(w)
        for i, w in enumerate(w[:mb]):
            res += w.val << i
        return res


    def _tag_wires(self, tag):
        return sorted([v for k, v in self.wires.items() if k.startswith(tag)], key=lambda x: x.name)
    

    def _validate(self):
        import math
        import itertools
        import copy

        for b in range(1, self.num_bits):
            #b = 1
            total_swaps = 4
            n_swaps = 0
            xyz, sum, mod_sum = self._get_sum(b)
            zn = self._tag_number("z", max_bits=b)
            if mod_sum == zn:
                continue
            if n_swaps == total_swaps:
                break
            debug_print(f"INVALID SUM Z B {b} X {xyz['x']} + Y {xyz['y']} {zn} != {mod_sum} ({sum})")
            gates = self._gates_for_bits(b)
            gg = self._gates_for_bit(b)
            #s = set(gates)
            s = set(gg)
            debug_print(f"B {b} GATES {gg}")
            #for g in gates:
            for g in gg:
                #debug_print(f"B {b} G {g}")
                for w in g.wires:
                    ggg = self._gates_with_wire(w.name)
                    s = s | set(ggg)
                    #gg = self._gates_connected_to(w.name)
                    debug_print(f"B {b} WIRE {w} GG {ggg}")
            debug_print(f"B {b} SET {s}")
            outs = [x.out for x in s]
            debug_print(f"B {b}/{self.num_bits} SET OUT {outs}")
            for p in itertools.combinations(s, 2):
                if p[0].out in p[1].inputs or p[1].out in p[0].inputs:
                    debug_print(f"CANNOT SWAP {p}")
                    continue
                debug_print(f"SWAP {p}")
                self._swap_outputs(p[0], p[1])
                self.solve()
                zyx, smm, mmssmm = self._get_sum(b)
                zznn = self._tag_number("z", max_bits=b)
                debug_print(f"NEW SUM Z B {b} X {zyx['x']} + Y {zyx['y']} {zznn} VS {mmssmm} ({smm})")
                if mod_sum == zn:
                    n_swaps += 1
                    break
                #put them back
                self._swap_outputs(p[0], p[1])
            break
            
        

    def _wire_names(self):
        return [x.name for x in self.wires]


    def _wires_with_values(self):
        return [x for x in self.wires if x.values is not None]
    

    def _wires_with_no_value(self):
        return [w for w in self.wires.values() if w.val is None]