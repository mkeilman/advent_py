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


    def display_output(self):
        debug(",".join([str(x) for x in self.output]))

    def display_state(self):
        debug(f"PTR {self.pointer} REGS {self.registers} OUT {self.output}")

    def load(self, v, init_val_a=-1):
        self.pointer = 0
        self.output = []
        regs = r"Register\s+([ABC]):\s+(\d+)"
        for txt in v:
            if "Program" in txt:
                self.program = [int(x) for x in re.findall(r"\d", txt)]
                continue
            m = re.match(regs, txt)
            if m:
                self.registers[m.group(1)] = int(m.group(2))
        if init_val_a >= 0:
            self.registers["A"] = init_val_a
        #debug("LOAD")
        #self.display_state()

    # adaptive step size?
    def run_reg_a_range(self, v, a_start=0, a_end=None, a_step=1):
        last_out_len = 0
        last_index = a_start
        d = a_step
        last_d = d
        i = a_start
        done = False
        while not done:
            self.load(v, init_val_a=i)
            pm = self.run(output_check=self.program)
            dl = len(self.output) - last_out_len
            if dl > 0:
                #if dl > 1:
                #    debug(f"{i} TOO FAR {pm}")
                #    i = last_index
                #    d = d // 2 or 1
                #    continue
                last_out_len = len(self.output)
                if i > last_index:
                    last_d = d
                    # double?
                    d *= 8
                    #d = i - last_index
                last_index = i
                debug(f"MORE MATCHES {i} {pm} D {d}")
                self.display_state()
            #if len(pm) < len(self.program) and i + d > a_end:
            #    debug("NOT DONE YET KEEP D")
            #    #d = last_d // 2 or 1

            i += d
            if a_end is not None:
                done = i > a_end
            else:
                done = len(pm) == len(self.program)
                

    def run(self, output_check=None):
        self.pointer = 0
        self.loop_cnt = 0
        self.output = []
        partial_match = []
        while self.pointer < len(self.program):
            self.pointer += self._exec(self.program[self.pointer], self.program[self.pointer + 1])
            if self.pointer == 0:
                self.loop_cnt += 1
            #self.display_state()
            if output_check and self.output:
                if self.output != output_check[:len(self.output)]:
                    break
                #self.display_state()
                partial_match = self.output[:]
        #self.display_output()
        return partial_match

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
        self.output.append(self._combo(op) % 8)
        #self.display_output()
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



    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            17,
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
        #c.load(v, init_val_a=117441)
        #c.run()
        #debug(f"RUN A {c.registers["A"]} B {c.registers["B"]} C {c.registers["C"]} PROG {c.program} LEN {len(c.program)}")
        #debug(f"RAN {c.loop_cnt + 1} LOOPS")
        #for i in range(pow(8, 15), pow(8, 16), pow(8, 8)): 
        #c.run_reg_a_range(v, a_range=range(pow(8, 15) + 10000, pow(8, 15) + 20000)) # MAX 61629537462831 [2, 4, 1, 1, 7, 5, 4, 7, 1, 4, 0, 3, 5, 5, 3]
        m = 35184395692586
        d0 = 6000000
        d1 = d0 + 2000000
        c.run_reg_a_range(v, a_start=61629537462831, a_end=pow(8, 16), a_step=33554432)
        


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()