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
        

    # 90 degrees at a time around the center
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

    @classmethod
    def bounds(cls, shape, coords):
        return (
            (coords, (coords[0] + shape.size[0], coords[1])),
            ((coords[0], coords[1] + shape.size[1]), (coords[0] + shape.size[0], coords[1] + shape.size[1])),
        )
    

    @classmethod
    def overlaps(cls, bounds0, bounds1):
        # check x
        if bounds1[0][0] > bounds0[0][1] or bounds1[0][1] < bounds0[0][0]:
            return False
        
        # check y
        if bounds1[1][0] > bounds0[1][1] or bounds1[1][1] < bounds0[1][0]:
            return False

        return True


    def __init__(self, size, required_shapes):
        self.size = size
        self.area = size[0] * size[1]
        self.required_shapes = required_shapes
        self.shapes = []


    # add a shape with the upper left corner at the given coords
    def add_shape(self, shape, coords):
        assert self.fits(shape, coords)
        self.shapes.append(
            {
                "shape": shape,
                "bounds": Region.bounds(shape, coords)
            }
        )


    def fits(self, shape, coords):
        debug_print(f"SZ {self.size} SH {shape.size} C {coords}: {coords[0] + shape.size[0]} {coords[1] + shape.size[1]}")
        # check that the shape is inside the region
        if not (0 <= (coords[0] + shape.size[0]) < self.size[0] and 0 <= (coords[1] + shape.size[1]) < self.size[1]):
            return False
        
        for s in self.shapes:
            b0 = s["bounds"]
            b1 = Region.bounds(shape, coords)
            # if the bounds do not overlap at all, the new shape fits
            if not Region.overlaps(b0, b1):
                continue
            g0 = s.flat_grid
            g1 = shape.flat_grid
            if not all([x == Shape.EMPTY or g1[i] == Shape.EMPTY for i, x in enumerate(g0)]):
                return False

        return True
    

    


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
        r = self.regions[0]
        r.add_shape(s, (0, 0))
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
                        (int(m.group(1)), int(m.group(2))),
                        [int(x) for x in re.findall(r"\d", line.split(":")[1])]
                    )
                )
            

