import Day
from utils.debug import debug_print, debug_if
from utils import collectionutils
from utils import mathutils
import re

class Shape:

    EMPTY = "."
    FULL = "#"

    def __init__(self, shape_grid):
        self.shape_grid = shape_grid
        self.flat_grid = collectionutils.flatten(self.shape_grid)
        self.size = (len(shape_grid), len(shape_grid[0]))


    def __repr__(self):
        return f"{self.shape_grid}"


    def flip(self, axis):
        if axis == 0:
            return Shape(self.shape_grid[::-1])
        return Shape([x[::-1] for x in self.shape_grid])
        

    # 90 degrees at a time, always around the center
    def rotate(self, direction):
        d = mathutils.sign(direction)
        if not d:
            return Shape(self.shape_grid)
        g = []
        for i in range(self.size[0]):
            r = ""
            for j in range(self.size[1]):
                r += self.shape_grid[j][i]
            g.append(r)
        return Shape(g).flip(1 if d == 1 else 0)


class Region:

    def __init__(self, size, required_shapes):
        self.size = size
        self.area = size[0] * size[1]
        self.required_shapes = required_shapes


    def fits(self, *args):
        return False
        #s0 = self.flat_grid
        #s1 = other_shape.flat_grid
        #return all([x == Shape.EMPTY or s1[i] == Shape.EMPTY for i, x in enumerate(s0)])



class AdventDay(Day.Base):

    TEST = [
        "0:",
        "###",
        "##.",
        "##.",
        "",
        "1:",
        "###",
        "##.",
        ".##",
        "",
        "2:",
        ".##",
        "###",
        "##.",
        "",
        "3:",
        "##.",
        "###",
        "##.",
        "",
        "4:",
        "###",
        "#..",
        "###",
        "",
        "5:",
        "###",
        ".#.",
        "###",
        "",
        "4x4: 0 0 0 0 2 0",
        "12x5: 1 0 1 0 2 2",
        "12x5: 1 0 1 0 3 2",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 12)
        self.add_args(run_args)
        self.shapes = []
        self.regions = []


    def run(self):
        n = 0
        self._parse()
        s = self.shapes[0]
        debug_print(f"SHAPE {s} ROT 1 {s.rotate(1)} ROT -1 {s.rotate(-1)}")
        return n
 

    def _parse(self):
        in_shape = False
        s = None
        for line in self.input:
            if not line:
                if in_shape:
                    self.shapes.append(Shape(s))
                in_shape = False
                continue
            if re.match(r"^\d:", line):
                in_shape = True
                s = []
                continue
            if in_shape:
                s.append(line)
            m = re.match( r"^(\d+)x(\d+)", line)
            if m:
                self.regions.append(
                    Region(
                        [int(m.group(1)), int(m.group(2))],
                        [int(x) for x in re.findall(r"\d", line.split(":")[1])]
                    )
                )
            

