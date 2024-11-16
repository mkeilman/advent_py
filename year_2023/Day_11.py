from functools import reduce
import re
import Day


class Universe():

    BASIC = [
        "...#......",
        ".......#..",
        "#.........",
        "..........",
        "......#...",
        ".#........",
        ".........#",
        "..........",
        ".......#..",
        "#...#.....",
    ]

    GALAXY = "#"

    @classmethod
    def _dist(cls, g1, g2):
        return abs(g2[0] - g1[0]) + abs(g2[1] - g1[1])
    
    def __init__(self, grid, cc=1):
        self.grid = grid
        self.galaxies = self._expand(cosmological_const=cc)
        self.galaxy_pairs = self._pair()
        self.dists = [Universe._dist(x[0], x[1]) for x in self.galaxy_pairs]
        
    def dist_sum(self):
        return reduce((lambda x, y: x + y), self.dists, 0)
        
    def print_grid(self):
        for r in self.grid:
            print(r)

    def _expand(self, cosmological_const=1):
        g = []
        cc = cosmological_const - 1
        for j, r in enumerate(self.grid):
            for i, x in enumerate(r):
                if x == Universe.GALAXY:
                    g.append((j, i))

        r = [i for i, x in enumerate(self.grid) if Universe.GALAXY not in x]
        c = [j for j in range(len(self.grid[0])) if not any([self.grid[i][j] == Universe.GALAXY for i in range(len(self.grid))])]
        for i, gg in enumerate(g):
            g[i] = (
                    gg[0] + cc * len([x for x in r if x < gg[0]]),
                    gg[1] + cc * len([x for x in c if x < gg[1]])
                )
        return g
    
    def _pair(self):
        p = []
        for i in range(len(self.galaxies)):
            for j in range(i + 1, len(self.galaxies)):
                p.append((self.galaxies[i], self.galaxies[j]))
        return p

class AdventDay(Day.Base):

    def __init__(self, run_args):
        def _cc_type(x):
            x = int(x)
            if x < 1:
                raise argparse.ArgumentTypeError(f"Cosmological constant {x} must be >= 1")
            return x

        import argparse
        super(AdventDay, self).__init__(
            2023,
            11,
            Universe.BASIC
        )
        self.args_parser.add_argument(
            "--cosmo-const",
            default=1,
            dest="comso_const",
            type=_cc_type,
        )
        self.comso_const = self.args_parser.parse_args(run_args).comso_const

    def run(self, v):
        u = Universe(v, cc=self.comso_const)
        print(f"DIST SUM {u.dist_sum()}")



def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
