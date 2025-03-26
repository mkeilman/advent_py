import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug


class Computer:

    INSTRUCTIONS = [
        "_adv",
        "_bxl",
        "_bst",
        "_jnz",
        "_bxc",
        "_out",
        "_bdv",
        "_cdv",
    ]

    def __init__(self):
        self.loop_cnt = 0
        self.output = []
        self.pointer = 0
        self.program = []
        self.registers = {
            "A": 0,
            "B": 0,
            "C": 0,
        }
        self.loaded = False


    def display_output(self):
        debug(",".join([str(x) for x in self.output]))

    def display_state(self):
        debug(f"PTR {self.pointer} REGS {self.registers} OUT {self.output} OUT IS PROG? {self.output == self.program}")


    def set_register(self, r, val):
        self.registers[r] = val

    def set_registers(self, registers):
        for k in self.registers:
            self.set_register(k, registers[k])

    def generate_self_range(self):
        ops = self.opcodes()
        p_len = len(self.program)
        num_outs = len([x for x in ops if x == "_out"])
        if not num_outs:
            debug(f"CANNOT GENERATE SELF: NO OUTPUT IN {self.program}")
            return None
        # the total number of outputs must match the length of the program.
        # too hard to consider every possible program, so assume at most a
        # single jump to the start in combination with the appropriate
        # number of outputs
        op = self.opcode(self.program[-2])
        if op != "_jnz":
            debug(f"CANNOT GENERATE SELF: RESTRICTED TO FINAL JMP: {op}")
            return None
        else:
            if self.program[-1]:
                debug(f"CANNOT GENERATE SELF: MUST JMP TO 0 {self.program[-1]}")
                return None
        if p_len % num_outs:
            debug(f"CANNOT GENERATE SELF: NUM OUTPUTS MUST DIVIDE INTO LENGTH: {num_outs} VS {p_len}")
            return None
        n = p_len // num_outs
        return pow(8, n - 1), pow(8, n) - 1

    def load(self, v, init_registers=None):
        self.pointer = 0
        self.output = []
        re_regs = r"Register\s+([ABC]):\s+(\d+)"
        for txt in v:
            if "Program" in txt:
                self.program = [int(x) for x in re.findall(r"\d", txt)]
                continue
            m = re.match(re_regs, txt)
            if not m:
                continue
            r = m.group(1)
            self.set_register(r, init_registers[r] if (init_registers or {}).get(r, None) is not None else int(m.group(2)))
        self.init_registers = self.registers.copy()
        self.loaded = True
        #self.display_state()
        #debug(f"LOAD {self.op_pairs()}")

    def reload(self):
        self.set_registers(self.init_registers)

    def opcode(self, op):
        return Computer.INSTRUCTIONS[op]
    
    def opcodes(self):
        return [self.opcode(x) for i, x in enumerate(self.program) if not i % 2]
    
    def op_pairs(self):
        return [(self.program[2 * i], self.program[2 * i + 1]) for i in range(len(self.program) // 2)]

    def run_reg_a_range(self, v, a_start=0, a_end=1, a_step=1):
        last_out_len = 0
        last_index = a_start
        d = a_step
        i = a_start
        done = False
        self.load(v)
        while not done:
            self.reload()
            self.set_register("A", i)
            #pm = self.run(output_check=self.program)
            pm = self.run()
            sz = len(pm)
            dl = sz - last_out_len
            if dl > 0:
                last_out_len = sz
                #if i > last_index:
                #    d *= 8
                last_index = i
                debug(f"MORE MATCHES {i} {pm} D {d} BM8 {self.registers["B"] % 8}")
                self.display_state()
                if pm == self.program:
                    return i

            self.display_state()
            i += d
            done = i > a_end
        return None
                

    def run(self, output_check=None):
        assert self.loaded
        self.pointer = 0
        self.output = []
        partial_match = []
        while self.pointer < len(self.program):
            self.pointer += self._exec(self.program[self.pointer], self.program[self.pointer + 1])
            if self.pointer == 0:
                self.loop_cnt += 1
            if output_check and self.output:
                if self.output != output_check[:len(self.output)]:
                    break
                partial_match = self.output[:]
        return partial_match

    def reverse(self, registers):
        self.set_registers(registers)
        for opcode, operand in reversed(self.op_pairs()):
            getattr(self, Computer.INSTRUCTIONS[opcode])(operand, reversed=True)
        self.display_state()

    def _combo(self, op):
        if op < 4:
            return op
        if op < 7:
            return self.registers[list(self.registers.keys())[op - 4]]
        raise ValueError
    
    def _adv(self, op, reversed=False):
        self.registers["A"] = self.registers["A"] * pow(2, self._combo(op)) if reversed else math.floor(self.registers["A"] / pow(2, self._combo(op)))
        return 2
    
    def _bdv(self, op, reversed=False):
        self.registers["B"] = self.registers["A"] * pow(2, self._combo(op)) if reversed else math.floor(self.registers["A"] / pow(2, self._combo(op)))
        return 2
    
    def _bst(self, op, reversed=False):
        self.registers["B"] = self._combo(op) if reversed else self._combo(op) % 8
        return 2
    
    def _bxc(self, op, reversed=False):
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]
        return 2
    
    def _bxl(self, op, reversed=False):
        self.registers["B"] = self.registers["B"] ^ op
        return 2

    def _cdv(self, op, reversed=False):
        self.registers["C"] = self.registers["A"] * pow(2, self._combo(op)) if reversed else math.floor(self.registers["A"] / pow(2, self._combo(op)))
        return 2
    
    def _jnz(self, op, reversed=False):
        if reversed or not self.registers["A"]:
            return 2
        return op - self.pointer
    
    def _out(self, op, reversed=False):
        if reversed:
            return 2
        self.output.append(self._combo(op) % 8)
        return 2

    def _exec(self, opcode, operand):
        return getattr(self, Computer.INSTRUCTIONS[opcode])(operand)
    

class AdventDay(Day.Base):

    BASIC0 = [
        "Register A: 0",
        "Register B: 0",
        "Register C: 9",
        "",
        "Program: 2,6",
    ]

    BASIC1 = [
        "Register A: 10",
        "Register B: 0",
        "Register C: 9",
        "",
        "Program: 5,0,5,1,5,4",
    ]
    
    BASIC2 = [
        "Register A: 2024",
        "Register B: 0",
        "Register C: 9",
        "",
        "Program: 0,1,5,4,3,0",
    ]
    
    BASIC3 = [
        "Register A: 2024",
        "Register B: 29",
        "Register C: 9",
        "",
        "Program: 1,7",
    ]

    BASIC4 = [
        "Register A: 2024",
        "Register B: 2024",
        "Register C: 43690",
        "",
        "Program: 4,0",
    ]

    SELF = [
        "Register A: 117440",
        "Register B: 0",
        "Register C: 0",
        "",
        "Program: 0,3,5,4,3,0",
    ]

    SIMPLE = [
        "Register A: 16",
        "Register B: 0",
        "Register C: 0",
        "",
        "Program: 0,1,0,1,0,1",
    ]

    TEST = [
        "Register A: 729",
        "Register B: 0",
        "Register C: 0",
        "",
        "Program: 0,1,5,4,3,0",
    ]



    def __init__(self, year, day, run_args):
        import argparse
        super(AdventDay, self).__init__(
            year,
            day,
            AdventDay.SELF
        )
        self.args_parser.add_argument(
            "--init-val-a",
            type=int,
            help="initial value of register A (-1 to keep value from input)",
            default=-1,
            dest="init_val_a",
        )
        self.add_args(run_args)
       

    def run(self, v):
        c = Computer()
        c.load(v)
        #c.set_register("A", pow(8, 15))
        #c.display_state()
        #c.run()
        #c.display_state()
        a_start, a_end = c.generate_self_range()
        prog_reg = c.run_reg_a_range(v, a_start=202367025818154, a_end=202367025818154 + 100)
        debug(f"FOUND? {prog_reg is not None} REG {prog_reg}")
        


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()