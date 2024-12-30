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

    def run(self, v):
        Base.print_strings(v)

    def run_from_test_strings(self, substitute_strings=None):
        self.run(substitute_strings or self.test_strings)

    def run_from_file(self):
        with open(self.input_file, "r") as f:
            v = [x.strip() for x in f.readlines()]
            self.run(v)


class Grid:
    def __init__(self, coord_array):
        self.coord_array = coord_array
        self.size = [len(self.coord_array), len(self.coord_array[0])]

    def contains(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]
    
    def neighborhood(self, pos, restrict_to=None):
        from utils import mathutils

        n = []
        sites = {
            "row": ((-1, 0), (1, 0)),
            "col": ((0, -1), (0, 1)),
        }
        s = mathutils.sum(sites.values(), init_val=()) if restrict_to is None else sites[restrict_to]
        for p in s:
            q = (pos[0] + p[0], pos[1] + p[1])
            if self.contains(q):
                n.append(q)
        return n
    
