from functools import reduce
import re
import Day


class RouteNode():
    re_3 = r"[A-Z][A-Z][A-Z]"
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
        #assert len(set(self.node_names)) == len(self.node_names)


    def get_route(self, start_name, end_name):
        r = []
        i = 0
        n = 0
        curr = self.route_dict[start_name]
        next = curr
        while next.name != end_name:
            next = self.route_dict[curr.routes[self.directions[i]]]
            i = (i + 1) % len(self.directions)
            n += 1
            curr = next
        return n


class AdventDay(Day.Base):

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2023,
            8,
            [
                "RL",
                "",
                "AAA = (BBB, CCC)",
                "BBB = (DDD, EEE)",
                "CCC = (ZZZ, GGG)",
                "DDD = (DDD, DDD)",
                "EEE = (EEE, EEE)",
                "GGG = (GGG, GGG)",
                "ZZZ = (ZZZ, ZZZ)",
            ]
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
        print(f"N STEPS {self.route_map.get_route(self.start_node, self.end_node)}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
