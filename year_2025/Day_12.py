import Day
from utils.debug import debug_print, debug_if
from utils import collectionutils
from utils import mathutils
import re

class Shape:

    EMPTY = "."
    FULL = "#"

    def __init__(self, shape_grid, shape_prototype, shape_id=None):
        self.shape_prototype = shape_prototype
        self.shape_id = shape_id or collectionutils.random_base62(8)
        self.shape_grid = shape_grid
        self.flat_grid = collectionutils.flatten(self.shape_grid)
        self.size = (len(shape_grid), len(shape_grid[0]))


    def __repr__(self):
        return f"{self.shape_grid}"


    # flip around the specified axis, preserving the id
    def flip(self, axis):
        if axis == 0:
            return Shape(self.shape_grid[::-1], self.shape_prototype, shape_id=self.shape_id)
        return Shape([x[::-1] for x in self.shape_grid], self.shape_prototype, shape_id=self.shape_id)
        

    # 90 degrees at a time around the center, preserving the id
    def rotate(self, direction):
        d = mathutils.sign(direction)
        if not d:
            return Shape(self.shape_grid, self.shape_prototype, shape_id=self.shape_id)
        g = []
        for i in range(self.size[0]):
            r = ""
            for j in range(self.size[1]):
                r += self.shape_grid[j][i]
            g.append(r)
        return Shape(g, self.shape_prototype, shape_id=self.shape_id).flip(1 if d == 1 else 0)


class Region:

    @classmethod
    def bounds(cls, shape, coords):
        return (
            (coords, (coords[0] + shape.size[0], coords[1])),
            ((coords[0], coords[1] + shape.size[1]), (coords[0] + shape.size[0], coords[1] + shape.size[1])),
        )
    

    @classmethod
    def overlaps(cls, shape_entry0, shape_entry1):
        #debug_print(f"S0 {shape_entry0} S1 {shape_entry1}")
        b0 = shape_entry0["bounds"]
        b1 = shape_entry1["bounds"]
        # check x
        if b1[0][0] > b0[0][1] or b1[0][1] < b0[0][0]:
            return False
        
        # check y
        if b1[1][0] > b0[1][1] or b1[1][1] < b0[1][0]:
            return False

        return True


    def __init__(self, size, required_shapes):
        self.size = size
        self.area = size[0] * size[1]
        self.required_shapes = required_shapes
        self.shapes_dict = {}


    def __repr__(self):
        txt = self.size[0] * [self.size[1] * Shape.EMPTY]
        for s_id in self.shapes_dict:
            s = self.shapes_dict[s_id]["shape"]
            b = self.shapes_dict[s_id]["bounds"]
            r, c = b[0][0][0], b[1][0][0]
            debug_print(f"CHECK R {r} C {c}")
            for i in range(s.size[0]):
                txt[r + i] = txt[r + i][:c] + s.shape_grid[i] + txt[r + i][c + s.size[1]:]
        return "\n".join(txt)


    # add a shape with the upper left corner at the given coords
    def add_shape(self, shape, coords):
        debug_print(f"ADD {shape} AT {coords}")
        shape_entry = {
            "shape": shape,
            "bounds": Region.bounds(shape, coords)
        }
        assert self.fits(shape_entry, coords)
        self.shapes_dict[shape.shape_id] = shape_entry


    def fits(self, shape_entry, coords):
        shape = shape_entry["shape"]
        debug_print(f"SZ {self.size} SH {shape.size} C {coords}: {coords[0] + shape.size[0]} {coords[1] + shape.size[1]}")
        # check that the shape is inside the region
        if not (0 <= (coords[0] + shape.size[0]) < self.size[0] and 0 <= (coords[1] + shape.size[1]) < self.size[1]):
            return False
        
        for s_id in self.shapes_dict:
            s = self.shapes_dict[s_id]
            debug_print(f"S {s}")
            # if the bounds do not overlap at all, the new shape fits
            if not Region.overlaps(s, shape_entry):
                continue
            if not all([x == Shape.EMPTY or shape.flat_grid[i] == Shape.EMPTY for i, x in enumerate(s["shape"].flat_grid)]):
                return False

        return True
    

    def is_coord_in_shape(self, coord, shape_id):
        b = self.shapes_dict[shape_id]["bounds"]
        return b[0][0] < coord[0] < b[0][1] and b[1][0] < coord[1] < b[1][1]
    





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
        #debug_print(f"SHAPE {s} ROT 1 {s.rotate(1)} ROT -1 {s.rotate(-1)}")
        r = self.regions[0]
        r.add_shape(s, (0, 0))
        debug_print(f"{r}")
        r.add_shape(s, (0, 0))
        return n
 

    def _parse(self):
        in_shape = False
        s = None
        s_p = None
        for line in self.input:
            if not line:
                if in_shape:
                    self.shapes.append(Shape(s, s_p))
                in_shape = False
                continue
            m = re.match(r"^(\d):", line)
            if m:
                in_shape = True
                s_p = int(m.group(1))
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
            

