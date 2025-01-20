from utils.debug import debug

class Base:

    @staticmethod
    def print_strings(v):
        debug(v)

    def __init__(self, year, day, test_strings=None):
        import argparse
        self.input_file = f"year_{year}/input_day_{day:02d}.txt"
        self.test_strings = test_strings or []
        self.args_parser = argparse.ArgumentParser()
        self.args = {}

    def add_args(self, run_args):
        v = vars(self.args_parser.parse_args(run_args))
        for arg in v:
            self.args[arg] = v[arg]

    def run(self, v):
        Base.print_strings(v)

    def run_from_test_strings(self, substitute_strings=None):
        self.run(substitute_strings or self.test_strings)

    def run_from_file(self):
        with open(self.input_file, "r") as f:
            v = [x.strip() for x in f.readlines()]
            self.run(v)


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
    
    def neighborhood(self, pos, restrict_to=None):
        from utils import mathutils

        n = []
        s = mathutils.sum(Grid.neighborhoods.values(), init_val=()) if restrict_to is None else Grid.neighborhoods[restrict_to]
        for p in s:
            q = (pos[0] + p[0], pos[1] + p[1])
            if self.contains(q):
                n.append(q)
        return n
    

    
