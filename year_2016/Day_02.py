import numpy
import re
import Day
from utils.debug import debug_print

class Keypad:

    layout = [
        "123",
        "456",
        "789"
    ]

    move_map = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }

    def __init__(self, init_digit):
        self.size = (len(Keypad.layout), len(Keypad.layout[0]))
        self.init_digit = init_digit
        self.init_pos = self._digit_pos(self.init_digit)
        self.current_digit = self.init_digit
        self.current_pos = self.init_pos
        
    
    def code(self, grid):
        s = ""
        for txt in grid:
            for d in txt:
                self.next(d)
            #debug_print(f"LANDED ON {self.current_digit}")
            s += self.current_digit
        return s


    def next(self, direction):
        d = Keypad.move_map[direction]
        self.current_pos = (
            max(0, min(self.current_pos[0] + d[0], len(Keypad.layout) - 1)),
            max(0, min(self.current_pos[1] + d[1], len(Keypad.layout[0]) - 1)),
        )
        #debug_print(f"D {direction} -> {self.current_pos}")
        self.current_digit = self._pos_digit(self.current_pos)


    def _digit_pos(self, digit):
        for i in range(len(Keypad.layout)):
            if digit in Keypad.layout[i]:
                return (i, Keypad.layout[i].index(digit))
        return None
    

    def _pos_digit(self, pos):
        return Keypad.layout[pos[0]][pos[1]]


class AdventDay(Day.Base):

    TEST = [
        "ULL",
        "RRDDD",
        "LURDL",
        "UUUUD",
    ]


    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2016,
            2,
            AdventDay.TEST
        )

    
    def run(self, v):
        k = Keypad("5")
        debug_print(f"CODE {k.code(v)}")


def main():
    d = AdventDay()
    debug_print("TEST:")
    d.run_from_test_input()
    debug_print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
