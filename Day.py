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
