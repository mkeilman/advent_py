import re
import Day
from utils import math
from utils import string
from utils.debug import debug

class Antenna:

    @staticmethod
    def dist(node1, node2):
        # note this is a signed value
        return ((node2[0] - node1[0]), (node2[1] - node1[1]))

    def __init__(self, grid):
        self.grid = grid
        self.size = (len(grid), len(grid[0]))
        self.nodes = self._nodes()
        self.all_nodes = self._all_nodes()
        self.node_pairs = self._node_pairs()
        self.node_pair_dists = self._node_pair_dists()
        self.antinodes = self._antinodes()
        self.all_antinodes = self._all_antinodes()
        #debug(f"NODES {self.nodes}")
        #debug(f"ALL NODES {self.all_nodes}")
        #debug(f"PAIRS {self.node_pairs}")
        #debug(f"DISTS {self.node_pair_dists}")
        #debug(f"ANTINODES {self.all_antinodes}")


    def _all_antinodes(self):
        nodes = set()
        x = []
        for n in self.antinodes:
            nn = self.antinodes[n]
            nodes = nodes.union(set(nn))
            x.extend(nn)
        debug(f"A ARR {x} {len(x)}")
        return nodes
    
    def _all_nodes(self):
        nodes = []
        for n in self.nodes:
            nodes.extend(self.nodes[n])
        return nodes


    def _antinodes(self):
        nodes = {}
        for n in self.node_pairs:
            p = self.node_pairs[n]
            d = self.node_pair_dists[n]
            nodes[n] = []
            for j, nn in enumerate(p):
                dd = d[j]
                for node in nn:
                    for dir in (-1, 1):
                        q = (node[0] + dir * dd[0], node[1] + dir * dd[1])
                        if q not in nn and self._is_in_grid(q):
                            nodes[n].append(q)
        return nodes


    def _nodes(self):
        nodes = {}
        for i, r in enumerate(self.grid):
            for n in re.findall(r"[0-9a-zA-Z]", r):
                if n not in nodes:
                    nodes[n] = []
                nodes[n].extend([(i, j) for j in string.indices(n, r)])
        return nodes
    
    def _is_in_grid(self, pos):
        return pos[0] >= 0 and pos[0] < self.size[0] and pos[1] >= 0 and pos[1] < self.size[1]

    def _node_pairs(self):
        import itertools

        pairs = {}
        for n in self.nodes:
            pairs[n] = list(itertools.combinations(self.nodes[n], 2))
        return pairs
    

    def _node_pair_dists(self):
        import itertools

        dists = {}
        for n in self.node_pairs:
            dists[n] = [Antenna.dist(x[1], x[0]) for x in self.node_pairs[n]]
        return dists
    

class AdventDay(Day.Base):
            

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            8,
            [
                "............",
                "........0...",
                ".....0......",
                ".......0....",
                "....0.......",
                "......A.....",
                "............",
                "............",
                "........A...",
                ".........A..",
                "............",
                "............",
            ]
        )

    def run(self, v):
        a = Antenna(v)
        debug(f"NUM ANTI {len(a.all_antinodes)}")



def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
