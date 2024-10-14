class Base:

    @staticmethod
    def printStrings(v):
        print(v)

    def __init__(self, year, day, test_strings=None):
        self.input_file = f"year_{year}/input_day_{day:02d}.txt"
        self.test_strings = test_strings or []

    def run(self, v):
        Base.printStrings(v)

    def run_from_test_strings(self, substitute_strings=None):
        self.run(substitute_strings or self.test_strings)

    def run_from_file(self):
        with open(self.input_file, "r") as f:
            v = f.readlines()
            self.run(v)
