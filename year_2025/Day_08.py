import Day
from utils.debug import debug_print, debug_if
from utils import mathutils
from utils import collectionutils
import re

class AdventDay(Day.Base):

    TEST = [
        "162,817,812",
        "57,618,57",
        "906,360,560",
        "592,479,940",
        "352,342,300",
        "466,668,158",
        "542,29,236",
        "431,825,988",
        "739,650,466",
        "52,470,668",
        "216,146,977",
        "819,987,18",
        "117,168,530",
        "805,96,715",
        "346,949,466",
        "970,615,88",
        "941,993,340",
        "862,61,35",
        "984,92,344",
        "425,690,689",
    ]


    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(2025, 8)
        self.args_parser.add_argument(
            "--num-dists",
            type=int,
            help="number of shortest distances between junctions to combine",
            default=10,
            dest="num_dists",
        )
        self.args_parser.add_argument(
            "--num-circuit-lens",
            type=int,
            help="number of curcuit lengths to multiply",
            default=3,
            dest="num_circuit_lens",
        )
        self.args_parser.add_argument(
            "--stop-on-single-circuit",
            action=argparse.BooleanOptionalAction,
            default=False,
            dest="stop_on_single_circuit",
        )
        self.add_args(run_args)

        self.junctions = []
        self.dists = {}
        self.inverted_dists = {}
        self.circuits = []


    def run(self):
        n = 0
        self._parse()
        n = mathutils.product(
            sorted(
                [len(x) for x in self.circuits]
            )[-self.num_circuit_lens:]
        )
        #debug_print(len(self.dists))
        debug_print(f"C {self.circuits}")
        debug_print(f"NUM C {len(self.circuits)} PROD {n}")
        return n
 
    
    def _group_circuits(self):
        def _find_circ_with_junction(j):
            for c in self.circuits:
                if j in c:
                    return c
            return None
        
        # to_circuit always has 1
        def _move_junctions(from_circuit, to_circuit):
            if to_circuit[0] in from_circuit:
                return
            to_circuit.extend(from_circuit)
            del self.circuits[self.circuits.index(from_circuit)]


        num_dists = self.num_dists or len(self.dists)
        for d in sorted(self.inverted_dists.keys())[:num_dists]:
            p = self.inverted_dists[d]

            # junctions always in 1 and only 1 circuit
            c0 = _find_circ_with_junction(p[0])
            c1 = _find_circ_with_junction(p[1])
            
            # circuits must have length >= 1;
            # cannot both be > 1 (???)
            if len(c0) > 1:
                _move_junctions(c1, c0)
            else:
                if len(c1) > 1:
                    _move_junctions(c0, c1)
                else:
                    # both == 1
                    _move_junctions(c1, c0)

            if self.stop_on_single_circuit and len(self.circuits) == 1:
                debug_print(f"LAST PAIR {p} XP {p[0][0] * p[1][0]}")
                break


    def _parse(self):
        import itertools

        for line in self.input:
            self.junctions.append(tuple([int(x) for x in re.findall(r"\d+", line)]))

        self.circuits = [[x] for x in self.junctions]
        
        for pair in itertools.combinations(self.junctions, 2):
            self.dists[pair] = mathutils.sum(
                [(pair[0][i] - pair[1][i]) * (pair[0][i] - pair[1][i]) for i in range(3)]
            )
        
        # luckily this is a 1-1 / onto mapping!
        self.inverted_dists = {v: k for k, v in self.dists.items()}
        self._group_circuits()