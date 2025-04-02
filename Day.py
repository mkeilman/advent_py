class Base:
    """Base class for all advent "days"
    """

    TEST = []

    @classmethod
    def get_day(cls, year, day, run_args):
        """Builds a specific advent day

        Args:
            year (int): advent year
            day (int): advent day
            run_args (dict): command line arguments
        """
        import importlib
        return importlib.import_module(f"year_{year}.Day_{day:02d}").AdventDay(run_args)


    def __init__(self, year, day):
        """Initialize

        Args:
            year (int): advent year
            day (int): advent day
        """
        import argparse

        self.set_input([])
        self.input_file = f"year_{year}/input_day_{day:02d}.txt"
        self.test_input = type(self).TEST or []
        self.args_parser = argparse.ArgumentParser()
        self.args = {}


    def add_args(self, run_args):
        """Adds command-line arguments to the instance

        Args:
            run_args (dict): command line arguments
        """
        v = vars(self.args_parser.parse_args(run_args))
        for arg in v:
            self.args[arg] = v[arg]


    def run(self):
        """Generic run method. Subclasses will override this to perform specific calculations.
        The input should be set beforehand
        """
        return 0


    def run_from_test_input(self, input=None):
        """Run using local test input

        Args:
            run_args (dict): command line arguments
        """
        self.set_input(input or self.test_input)
        return self.run()


    def run_from_file(self):
        with open(self.input_file, "r") as f:
            self.set_input([x.strip() for x in f.readlines()])
            return self.run()
        

    def set_input(self, v):
        self.input = v


class Grid:

    neighborhoods = {
        "col": ((0, -1), (0, 1)),
        "row": ((-1, 0), (1, 0)),
    }

    @staticmethod
    def grid_of_size(num_rows, num_cols):
        g = []
        for i in range(num_rows):
            r = []
            for j in range(num_cols):
                r.append((i, j))
            g.append(r)
        return Grid(g)

    def __init__(self, coord_array):
        self.coord_array = coord_array
        self.flat_array = [x for y in coord_array for x in y]
        self.size = (len(self.coord_array), len(self.coord_array[0]))
        self.coord_neighborhoods = {x:self.neighborhood(x) for x in self.flat_array}

    def contains(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]
    
    def line(self, start_pos, end_pos, allow_diags=True):
        import math
        from utils import mathutils
        assert start_pos in self.flat_array and end_pos in self.flat_array
        dr = end_pos[0] - start_pos[0]
        dc = end_pos[1] - start_pos[1]
        if dc == 0:
            return [(start_pos[0] + mathutils.sign(dr) * i, start_pos[1]) for i in range(abs(dr) + 1)]
        if dr == 0:
            return [(start_pos[0], start_pos[1] + mathutils.sign(dc) * i) for i in range(abs(dc) + 1)]
        
        slope = dr / dc
        s = mathutils.sign(slope)
        l = []
        rr = range(start_pos[1], end_pos[1] + s, s)
        for c in range(start_pos[1], end_pos[1] + s, s):
            r = start_pos[0] + math.floor(slope * (c - start_pos[1]))
            if not allow_diags and (r, c - s) in self.flat_array:
                l.append((r, c - s))
            l.append((r, c))
        return l



    def neighborhood(self, pos, restrict_to=None):
        from utils import mathutils

        n = []
        s = mathutils.sum(Grid.neighborhoods.values(), init_val=()) if restrict_to is None else Grid.neighborhoods[restrict_to]
        for p in s:
            q = (pos[0] + p[0], pos[1] + p[1])
            if self.contains(q):
                n.append(q)
        return n
    

    
