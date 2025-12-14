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
        self.num_full = mathutils.sum([int(x == Shape.FULL) for x in self.flat_grid])
        self.size = (len(shape_grid), len(shape_grid[0]))


    def __repr__(self):
        return "\n".join(self.shape_grid)
        #return f"{self.shape_grid}"


    # flip around the specified axis
    def flip(self, axis):
        if axis == 0:
            return Shape(self.shape_grid[::-1], self.shape_prototype)
        return Shape([x[::-1] for x in self.shape_grid], self.shape_prototype)
        

    # 90 degrees at a time around the center, preserving the id
    def rotate(self, direction):
        d = mathutils.sign(direction)
        if not d:
            return Shape(self.shape_grid, self.shape_prototype)
        g = []
        for i in range(self.size[0]):
            r = ""
            for j in range(self.size[1]):
                r += self.shape_grid[j][i]
            g.append(r)
        return Shape(g, self.shape_prototype).flip(1 if d == 1 else 0)


class Region:

    @classmethod
    def bounds(cls, shape, coords):
        return {
            "row": {
                "min": coords[0],
                "max": coords[0] + shape.size[0] - 1
            },
            "col": {
                "min": coords[1],
                "max": coords[1] + shape.size[1] - 1
            },
        }
        #return (
        #    (coords, (coords[0] + shape.size[0], coords[1])),
        #    ((coords[0], coords[1] + shape.size[1]), (coords[0] + shape.size[0], coords[1] + shape.size[1])),
        #)
    

    @classmethod
    def overlap(cls, shape_entry0, shape_entry1):
        #debug_print(f"S0 {shape_entry0} S1 {shape_entry1}")
        b0 = shape_entry0["bounds"]
        b1 = shape_entry1["bounds"]
        # check x
        o = []
        debug_print(f"S0 {b0} S1 {b1}")
        rows = max(b0["row"]["min"],  b1["row"]["min"]), min(b0["row"]["max"], b1["row"]["max"])
        cols = range(max(b0["col"]["min"], b1["col"]["min"]), min(b0["col"]["max"], b1["col"]["max"]))
        debug_print(f"ROWS {rows} COLS {cols}")
        for r in rows:
            debug_print(f"R {r}")
            for c in cols:
                debug_print(f"C {c}")
                o.append((r, c))
        debug_print(o)
        #if b1[0][0] > b0[0][1] or b1[0][1] < b0[0][0]:
        #    return False
        
        # check y
        #if b1[1][0] > b0[1][1] or b1[1][1] < b0[1][0]:
        #    return False

        return o
        return True


    def __init__(self, size, shape_prototypes, required_shapes):
        self.size = size
        self.area = size[0] * size[1]
        self.shape_prototypes = shape_prototypes
        self.required_shapes = required_shapes
        self.num_required = mathutils.sum(self.required_shapes)
        self.required_full = mathutils.sum([self.required_shapes[i] * x.num_full for i, x in enumerate(self.shape_prototypes)])
        self.valid = self.required_full <= self.area
        #if not self.valid:
        #    debug_print(f"invalid region: {self.required_full} > {self.area}")
        self.shapes_dict = {}


    def __repr__(self):
        txt = self.size[0] * [self.size[1] * Shape.EMPTY]
        for s_id in self.shapes_dict:
            s = self.shapes_dict[s_id]["shape"]
            b = self.shapes_dict[s_id]["bounds"]
            r, c = b["row"]["min"], b["col"]["min"]
            #debug_print(f"CHECK R {r} C {c}")
            for i in range(s.size[0]):
                txt[r + i] = txt[r + i][:c] + s.shape_grid[i] + txt[r + i][c + s.size[1]:]
        return "\n".join(txt)


    # add a shape with the upper left corner at the given coords
    def add_shape(self, shape, coords=(0, 0)):
        #debug_print(f"TRY {shape} AT {coords}")
        shape_entry = {
            "shape": shape,
            "bounds": Region.bounds(shape, coords)
        }
        if self.fits(shape_entry, coords):
            self.shapes_dict[shape.shape_id] = shape_entry
            return True
        debug_print(f"CANNOT FIT\n{shape} AT {coords}")
        return False


    def add_all_required(self):
        #debug_print(f"REQ: {self.required_shapes}")
        for i, p in enumerate(self.required_shapes):
            s = self.shape_prototypes[i]
            debug_print(f"TRY {p}\n{s}")
            # 
            for _ in range(p):
                pass
        pass


    def fits(self, shape_entry, coords):
        shape = shape_entry["shape"]
        debug_print(f"R SZ {self.size} SH SZ {shape.size} C {coords}: {coords[0] + shape.size[0]} {coords[1] + shape.size[1]}")
        # check that the shape is inside the region
        if not (0 <= (coords[0] + shape.size[0]) <= self.size[0] and 0 <= (coords[1] + shape.size[1]) <= self.size[1]):
            return False
        
        debug_print(f"{shape.shape_id} IS IN REGION")
        for s_id in self.shapes_dict:
            s = self.shapes_dict[s_id]
            # if the bounds do not overlap, the new shape fits
            overlap = Region.overlap(s, shape_entry)
            if not overlap:
                continue

            debug_print(f"{shape.shape_id} OVERLAPS {s_id}")
            # at most one shape can be FULL at this coordinate if they are to fit together
            for c in overlap:
                

            if not all([x == Shape.EMPTY or shape.flat_grid[i] == Shape.EMPTY for i, x in enumerate(s["shape"].flat_grid)]):
                return False

        return True
    

    def is_coord_in_shape(self, coord, shape_id):
        b = self.shapes_dict[shape_id]["bounds"]
        return b[0][0] < coord[0] < b[0][1] and b[1][0] < coord[1] < b[1][1]
    

    def _shape_coord_ranges(self, shape):
        return range(self.size[0] - shape.size[0]), range(self.size[1] - shape.size[1])




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
        v = [x for x in self.regions if x.valid]
        #debug_print(f"NUM VALID {len(v)} / {len(self.regions)}")
        #for i, r in enumerate(v):
        #    debug_print(f"FIT ALL IN {i}")
        #    r.add_all_required()
        r = self.regions[0]
        s = self.shapes[4]
        r.add_shape(s)
        debug_print(r)
        sf = s.flip(1)
        r.add_shape(sf, coords=(1, 1))
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
                        self.shapes,
                        [int(x) for x in re.findall(r"\d+", line.split(":")[1])]
                    )
                )
            

