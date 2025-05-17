class Base:
    """Base class for all advent "days"
    """

    #: array of strings to use as test input
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

        self.input = []
        self.input_file = f"year_{year}/input_day_{day:02d}.txt"
        self.test_input = type(self).TEST or []
        self.args_parser = argparse.ArgumentParser()


    def add_args(self, run_args):
        """Adds command-line arguments to the instance

        Args:
            run_args (dict): command line arguments
        """
        v = vars(self.args_parser.parse_args(run_args))
        for arg in v:
            setattr(self, arg, v[arg])


    def run(self, input):
        """Generic run method. Subclasses will override this to perform specific calculations.

        Args:
            input (str[]): array of strings to use as input
        """
        self.input = input
        return 0


    def run_from_test_input(self, input=None):
        """Run using local test input

        Args:
            input (str[]): array of strings to use as test input
        """
        self.input = input or self.test_input
        return self.run()


    def run_from_file(self):
        """Run using input from file
        """
        with open(self.input_file, "r") as f:
            self.input = [x.strip() for x in f.readlines()]
            return self.run()


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


    def circle(self, center, radius):
        assert center in self.flat_array and radius >= 0
        if radius == 0:
            return [center]

        c = []
        for i in [x for x in range(-radius, radius + 1) if center[0] + x >= 0 and center[0] + x < self.size[0]]:
            for j in [x for x in range(-radius, radius + 1) if center[1] + x >= 0 and center[1] + x < self.size[1]]:
                if abs(i + j) == radius:
                    c.append((center[0] + i, center[1] + j))
        return c


    def contains(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]
    

    def line(self, start_pos, end_pos, allow_diags=True):
        import math
        from utils import mathutils

        def _add(coord, arr):
            if coord not in arr:
                arr.append(coord)

        assert start_pos in self.flat_array and end_pos in self.flat_array
        delta_row = end_pos[0] - start_pos[0]
        delta_col = end_pos[1] - start_pos[1]
        if delta_col == 0:
            return [(start_pos[0] + mathutils.sign(delta_row) * i, start_pos[1]) for i in range(abs(delta_row) + 1)]
        if delta_row == 0:
            return [(start_pos[0], start_pos[1] + mathutils.sign(delta_col) * i) for i in range(abs(delta_col) + 1)]
        
        col_delta_dir = mathutils.sign(delta_col)
        l = []
        rr = range(start_pos[1], end_pos[1] + col_delta_dir, col_delta_dir)
        for c in rr:
            r = start_pos[0] + math.floor((delta_row / delta_col) * (c - start_pos[1]))
            cc = c - col_delta_dir
            if not allow_diags and cc in rr and (r, cc) in self.flat_array:
                _add((r, cc), l)
            _add((r, c), l)
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
    

    
