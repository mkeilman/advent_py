import re
import Day
from utils import mathutils
from utils.debug import debug_print, debug_if

class Wire:

    def __init__(self, name, init_val=None):
        self.name = name
        self.init_val = init_val
        self.val = init_val
    
class Gate:

    op_map = {
        "AND": lambda x, y: x and y,
        "OR": lambda x, y: x or y,
        "XOR": lambda x, y: int(x != y),
    }

    def __init__(self, in1, in2, out, op_str):
        self.in1 = in1
        self.in2 = in2
        self.inputs = (self.in1, self.in2)
        self.out = out
        self.op_str = op_str
        self.wires = (in1, in2, out)
        self.op = Gate.op_map[op_str]


    def vals(self):
        return [x.val for x in self.wires]
    
    def eval(self):
        self.out.val = self.op(self.in1.val, self.in2.val)
    

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

    def __init__(self, run_args):
        super(AdventDay, self).__init__(2024, 24)
        #self.args_parser.add_argument(
        #    "--num-connections",
        #    type=int,
        #    help="number of connections",
        #    default=3,
        #    dest="num_connections",
        #)
        #self.add_args(run_args)
        self.gates = []
        self.wires = {}
    

    def anneal(self):
        while self._wires_with_no_value():
            for g in self._annealed_gates():
                g.eval()
        res = 0
        for i, w in enumerate(self._z_wires()):
            #debug_print(f"{w.name}")
            res += w.val << i
        return res


    def output_bits(self):
        return len(self._z_wires())
    


    def run(self):
        #self.input = AdventDay.TEST_LARGE
        self._parse()
        n = self.anneal()
        debug_print(f"N {n}")
        return n


    def _annealed_gates(self):
        return [x for x in self.gates if x.in1.val is not None and x.in2.val is not None]


    def _parse(self):
        def _parse_wire(txt):
            m = re.search(fr"({n}):\s+([01])", txt)
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
                
        
    def _wire_names(self):
        return [x.name for x in self.wires]


    def _wires_with_values(self):
        return [x for x in self.wires if x.values is not None]
    

    def _wires_with_no_value(self):
        return [v for k, v in self.wires.items() if v.val is None]
    

    def _z_wires(self):
        return sorted([v for k, v in self.wires.items() if k.startswith("z")], key=lambda x: x.name)
    
