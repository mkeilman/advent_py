import math
import re
import Day
from utils import mathutils
from utils import string
from utils.debug import debug

class Foyer:
    def __init__(self, size, robots):
        self.size = size
        self.robots = robots
        self.quadrants = (
            (range(0, self.size[0] // 2), range(0, self.size[1] // 2)),
            (range(self.size[0] // 2 + 1, self.size[0]), range(0, self.size[1] // 2)),
            (range(0, self.size[0] // 2), range(self.size[1] // 2 + 1, self.size[1])),
            (range(self.size[0] // 2 + 1, self.size[0]), range(self.size[1] // 2 + 1, self.size[1])),
        )

    def find_tree(self, start_run=0, max_runs=100):
        self.move_robots(num_steps=start_run)
        if self.has_tree_top():
            return start_run
        for i in range(max_runs):
            if i % 100 == 0:
                debug(i)
            self.move_robots()
            tt = self.has_tree_top()
            if tt:
                debug(f"TT AT {tt}")
                self.display(start_line=tt[1])
                return start_run + i
        return -1
    

    def has_tree_top(self):
        tree_top = [[0, 0], [-1, 1], [1, 1], [-2, 2], [2, 2], [-3, 3], [3, 3]]
        r_pos = [x.pos for x in self.robots]
        for p in r_pos:
            if all([[x[0] + p[0], x[1] + p[1]] in r_pos for x in tree_top]):
                return p
        return None


    def move_robot(self, r, num_steps=1):
        for i in (0, 1):
            r.pos[i] = ((r.pos[i] + num_steps * r.velocity[i]) + self.size[i]) % self.size[i]


    def move_robots(self, num_steps=1):
        for r in self.robots:
            self.move_robot(r, num_steps=num_steps)


    def display(self, start_line=0, num_lines=None):
        for j in range(start_line, num_lines or self.size[1]):
            s = ""
            for i in range(self.size[0]):
                p = [i, j]
                n = len([x.pos for x in self.robots if x.pos == p])
                s += (str(n) if n else ".")
            debug(s)
        

    def reset(self):
        for r in self.robots:
            r.reset()

    def robot_counts(self):
        c = []
        for q in self.quadrants:
            n = 0
            for r in self.robots:
                if r.pos[0] in q[0] and r.pos[1] in q[1]:
                    n += 1
            c.append(n)
        return c

    
    def safety_factor(self):
        return mathutils.product(self.robot_counts())


    def set_robots(self, positions):
        for i in range(min(len(positions), len(self.robots))):
            self.robots[i].pos = [positions[i][0], positions[i][1]]



class Robot:
    def __init__(self, txt):
        m = re.match(r"p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)", txt)
        self.init_pos = [int(m.group(1)), int(m.group(2))]
        self.velocity = (int(m.group(3)), int(m.group(4)))
        self.reset()


    def reset(self):
        self.pos = self.init_pos[:]


class AdventDay(Day.Base):

    TEST = [
        "p=0,4 v=3,-3",
        "p=6,3 v=-1,-3",
        "p=10,3 v=-1,2",
        "p=2,0 v=2,-1",
        "p=0,0 v=1,3",
        "p=3,0 v=-2,-2",
        "p=7,6 v=-1,-3",
        "p=3,0 v=-1,-2",
        "p=9,3 v=2,3",
        "p=7,3 v=-1,2",
        "p=2,4 v=2,-3",
        "p=9,5 v=-3,-3",
    ]

    SYMMETRIC = [
        "p=5,0 v=0,0",
        "p=0,0 v=3,-3",
        "p=10,0 v=-1,-3",
        "p=1,0 v=3,-3",
        "p=9,0 v=-1,-3",
        "p=1,1 v=-1,2",
        "p=9,1 v=2,-1",
        "p=2,2 v=1,3",
        "p=8,2 v=-2,-2",
        "p=3,3 v=-1,-3",
        "p=7,3 v=-1,-2",
        "p=4,4 v=2,3",
        "p=6,4 v=-1,2",
        "p=5,5 v=2,-3",
    ]

    def __init__(self, year, day, run_args):
        super(AdventDay, self).__init__(
            year,
            day,
            AdventDay.SYMMETRIC
        )
        self.args_parser.add_argument(
            "--width",
            type=int,
            help="foyer width",
            default=11,
            dest="width",
        )
        self.args_parser.add_argument(
            "--height",
            type=int,
            help="foyer height",
            default=7,
            dest="height",
        )
        self.args_parser.add_argument(
            "--tree-tries",
            type=int,
            help="limit to finding easter egg",
            default=100,
            dest="tree_tries",
        )
        self.args_parser.add_argument(
            "--tree-start",
            type=int,
            help="start tree search here",
            default=0,
            dest="tree_start",
        )
        self.width = self.args_parser.parse_args(run_args).width
        self.height = self.args_parser.parse_args(run_args).height
        self.tree_tries = self.args_parser.parse_args(run_args).tree_tries
        self.tree_start = self.args_parser.parse_args(run_args).tree_start

    def run(self, v):
        r = [Robot(x) for x in v]
        f = Foyer((self.width, self.height), r)
        #f.display()
        #f.move_robots(num_steps=7790)
        #f.display()
        #debug(f"Q C {f.robot_counts()} SAFETY {f.safety_factor()}")
        n = f.find_tree(start_run=self.tree_start, max_runs=self.tree_tries)
        debug(f"TREE RUNS {n + 1} FOUND? {n >= 0}")
        f.display()


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
