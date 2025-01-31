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
        self.output = []
        self.pointer = 0
        self.program = []
        self.registers = {
            "A": 0,
            "B": 0,
            "C": 0,
        }


    def display_output(self):
        debug(",".join([str(x) for x in self.output]))

    def display_state(self):
        debug(f"PTR {self.pointer} REGS {self.registers}")

    def load(self, v):
        regs = r"Register\s+([ABC]):\s+(\d+)"
        for txt in v:
            if "Program" in txt:
                self.program = [int(x) for x in re.findall(r"\d", txt)]
                continue
            m = re.match(regs, txt)
            if m:
                self.registers[m.group(1)] = int(m.group(2))

    def run(self):
        self.pointer = 0
        while self.pointer < len(self.program):
            opc = self.program[self.pointer]
            op = self.program[self.pointer + 1]
            debug(f"OPCODE {opc} CMD {Computer.INSTRUCTIONS[opc]} OPERAND {op}")
            self.pointer += self._exec(self.program[self.pointer], self.program[self.pointer + 1])
            self.display_state()
        #self.display_output()

    def _combo(self, op):
        if op < 4:
            return op
        if op < 7:
            return self.registers[list(self.registers.keys())[op - 4]]
        raise ValueError
    
    def _adv(self, op):
        self.registers["A"] = math.floor(self.registers["A"] / pow(2, self._combo(op)))
        return 2
    
    def _bdv(self, op):
        self.registers["B"] = math.floor(self.registers["A"] / pow(2, self._combo(op)))
        return 2
    
    def _bst(self, op):
        self.registers["B"] = self._combo(op) % 8
        return 2
    
    def _bxc(self, op):
        self.registers["B"] = self.registers["B"] ^ self.registers["C"]
        return 2
    
    def _bxl(self, op):
        self.registers["B"] = self.registers["B"] ^ op
        return 2

    def _cdv(self, op):
        self.registers["C"] = math.floor(self.registers["A"] / pow(2, self._combo(op)))
        return 2
    
    def _jnz(self, op):
        if not self.registers["A"]:
            return 2
        return op - self.pointer
    
    def _out(self, op):
        debug(f"OUT OP {op} COMNBO {self._combo(op)}")
        self.output.append(self._combo(op) % 8)
        self.display_output()
        return 2

    def _exec(self, opcode, operand):
        debug(f"EXEC {opcode} ON {operand}")
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



    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            17,
            AdventDay.BASIC4
        )
        self.args_parser.add_argument(
            "--warehouse-size",
            type=str,
            help="single or double size",
            choices=["single", "double"],
            default="single",
            dest="warehouse_size",
        )
        self.add_args(run_args)
       

    def run(self, v):
        c = Computer()
        c.load(v)
        debug(f"RUN A {c.registers["A"]} B {c.registers["B"]} C {c.registers["C"]} PROG {c.program}")
        c.run()



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()