import re
import Day


class RouteNode():
    re_3 = r"[A-Z0-9]{3}"
    re_node = fr"({re_3})\s*=\s*\(({re_3}),\s*({re_3})\)"

    def __init__(self, node_str):
        m = re.findall(RouteNode.re_node, node_str)[0]
        self.name = m[0]
        self.routes = {
            "L": m[1],
            "R": m[2],
        }


class RouteMap():
    def __init__(self, directions, route_nodes):
        self.directions = directions.strip()
        self.route_nodes = route_nodes
        self.route_dict = {n.name: n for n in self.route_nodes}

    def _next_node(self, node, direction_index):
        return self.route_dict[node.routes[self.directions[direction_index]]]
    
    def _next_dir(self, direction_index):
        return (direction_index + 1) % len(self.directions)
    
    def get_route(self, start_name, end_name):
        i = 0
        n = 0
        curr = self.route_dict[start_name]
        next = curr
        while next.name != end_name:
            next = self._next_node(curr, i)
            i = self._next_dir(i)
            n += 1
            curr = next
        return n
    
    def get_ghost_route(self):
        import math

        start_nodes = [x for x in self.route_nodes if x.name[-1] == "A"]
        end_nodes = [x for x in self.route_nodes if x.name[-1] == "Z"]
        print([x.name for x in start_nodes])
        print([x.name for x in end_nodes])

        n = 1
        c = []
        for node in start_nodes:
            i = 0
            m = 0
            nn = node
            while nn not in end_nodes:
                nn = self._next_node(nn, i)
                i = self._next_dir(i)
                m += 1
            n *= m
            c.append(m)

        return math.lcm(*c)


class AdventDay(Day.Base):

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2023,
            8,
            [
                "LR",
                "",
                "11A = (11B, XXX)",
                "11B = (XXX, 11Z)",
                "11Z = (11B, XXX)",
                "22A = (22B, XXX)",
                "22B = (22C, 22C)",
                "22C = (22Z, 22Z)",
                "22Z = (22B, 22B)",
                "XXX = (XXX, XXX)",
            ]
            #[
            #    "RL",
            #    "",
            #    "AAA = (BBB, CCC)",
            #    "BBB = (DDD, EEE)",
            #    "CCC = (ZZZ, GGG)",
            #    "DDD = (DDD, DDD)",
            #    "EEE = (EEE, EEE)",
            #    "GGG = (GGG, GGG)",
            #    "ZZZ = (ZZZ, ZZZ)",
            #]
        )
        self.args_parser.add_argument(
            "--start-node",
            default="AAA",
            dest="start_node",
        )
        self.args_parser.add_argument(
            "--end-node",
            default="ZZZ",
            dest="end_node",
        )
        self.start_node = self.args_parser.parse_args(run_args).start_node
        self.end_node = self.args_parser.parse_args(run_args).end_node


    def run(self, v):
        self.route_map = RouteMap(v[0], [RouteNode(x) for x in v[2:]])
        print(f"GHOST STEPS {self.route_map.get_ghost_route()}")
        #print(f"STEPS {self.route_map.get_route(self.start_node, self.end_node)}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
