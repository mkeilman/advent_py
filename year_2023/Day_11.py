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
    SPACE = "."

    @classmethod
    def _dist(cls, g1, g2):
        return abs(g2[0] - g1[0]) + abs(g2[1] - g1[1])
    
    def __init__(self, grid):
        self.grid = self._expand(grid)
        #self.print_grid()
        self.grid_range = (range(len(self.grid)), range(len(self.grid[0])))
        self.galaxies = []
        for j, r in enumerate(self.grid):
            for i, x in enumerate(r):
                if x == Universe.GALAXY:
                    self.galaxies.append((j, i))
        self.galaxy_pairs = self._pair()
        self.dists = [Universe._dist(x[0], x[1]) for x in self.galaxy_pairs]
        
    def dist_sum(self):
        return reduce((lambda x, y: x + y), self.dists, 0)
        
    def print_grid(self):
        for r in self.grid:
            print(r)

    def _expand(self, init_grid):
        g = init_grid.copy()
        print(len(g), len(g[0]))
        r = [i for i, x in enumerate(g) if Universe.GALAXY not in x]
        c = [j for j in range(len(g[0])) if not any([g[i][j] == Universe.GALAXY for i in range(len(g))])]
        #print(f"ER {r}")
        #print(f"EC {c}")
        for i in reversed(r):
            g.insert(i, Universe.SPACE * len(g[0]))
        for i in range(len(g)):
            rr = g[i]
            for j in reversed(c):
                rr = rr[0:j] + Universe.SPACE + rr[j:]
            g[i] = rr
        return g
    
    def _pair(self):
        p = []
        for i in range(len(self.galaxies)):
            for j in range(i + 1, len(self.galaxies)):
                p.append((self.galaxies[i], self.galaxies[j]))
        return p

class AdventDay(Day.Base):

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2023,
            11,
            Universe.BASIC
        )


    def run(self, v):
        u = Universe(v)
        print(f"DIST SUM {u.dist_sum()}")



def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
