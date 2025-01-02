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
        t = self.tree()
        self.move_robots(num_steps=start_run)
        max_matches = 0
        debug(f"N TREE BOTS {len(t)}")
        for i in range(max_runs):
            self.move_robots()
            p = [tuple(x.pos) for x in self.robots]
            tree_match = [x in p for x in t]
            n_matches = len([x for x in tree_match if x])
            #max_matches = max(max_matches, n_matches)
            if n_matches > max_matches:
            #if any(tree_match) and i % 100 == 0:
                debug(f"RUN {i + 1} PARTIAL TREE {n_matches} MAX {max_matches}")
                max_matches = n_matches
            if all(tree_match):
                debug(f"FOUND TREE RUN {i + 1}")
                break
        return i
    
    def move_robot(self, r, num_steps=1):
        for i in (0, 1):
            r.pos[i] = ((r.pos[i] + num_steps * r.velocity[i]) + self.size[i]) % self.size[i]

    def move_robots(self, num_steps=1):
        for r in self.robots:
            self.move_robot(r, num_steps=num_steps)
            #for i in (0, 1):
            #    r.pos[i] = ((r.pos[i] + num_steps * r.velocity[i]) + self.size[i]) % self.size[i]

    def display(self):
        for j in range(self.size[1]):
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
    
    def robot_cycle_length(self, robot):
        n = 0
        nx = 0
        Nx = 1
        ny = 0
        robot.reset()
        tx = robot.init_pos[0] / robot.velocity[0]
        ty = robot.init_pos[1] / robot.velocity[1]
        #debug(f"X0 {robot.init_pos[0]} VX {robot.velocity[0]} TX {tx} INT? {tx % 1 == 0}")
        #debug(f"Y0 {robot.init_pos[1]} VY {robot.velocity[1]} TX {ty} INT? {ty % 1 == 0}")
        #self.move_robot(robot)
        #while robot.pos != robot.init_pos:

        n = 1
        found = False
        while not found:
            dx = robot.init_pos[0] + n * robot.velocity[0]
            # back to starting x, check y
            debug(f"DX {dx} MOD {dx % self.size[0]} START {robot.init_pos[0]}")
            if dx % self.size[0] == robot.init_pos[0]:
                dy = robot.init_pos[1] + n * robot.velocity[1]
                debug(f"DY {dy} MOD {dy % self.size[1]} START {robot.init_pos[1]}")
                found = dy % self.size[1] == robot.init_pos[1]
            n += 1

        #n = tx * (Nx * self.size[0] - 1)
        #while n % 1 != 0:
        ##    Nx += 1
        ##    #self.move_robot(robot)
        #    n = tx * (Nx * self.size[0] - 1)
        #debug(f"N {n} NX {Nx}")
        return n
    
    def safety_factor(self):
        return mathutils.product(self.robot_counts())


    def set_robots(self, positions):
        for i in range(min(len(positions), len(self.robots))):
            self.robots[i].pos = [positions[i][0], positions[i][1]]
    

    def tree(self, trunk_width=1):
        assert trunk_width % 2

        i = self.size[0] // 2
        j = 0
        k = i
        l = 1
        positions = [(i, j)]
        done = False
        while not done:
            i -= 1
            j += 1
            k = i + 2 * l
            positions.append((i, j))
            positions.append((k, j))
            done = i <= 0 or j >= self.size[1] or len(positions) >= len(self.robots)
            l += 1
        n = len(self.robots) - len(positions)
        n_base = 2 * l - 3
        n_trunk = trunk_width * (self.size[1] - j - 1)
       
        if n < n_base + n_trunk:
            debug("NOT ENOUGH ROBOTS")
            return positions
        for i in range(i + 1, k):
            positions.append((i, j))
        for j in range(j + 1, self.size[1]):
            for m in range(trunk_width):
                positions.append((self.size[0] // 2 - trunk_width // 2 + m, j))
        return positions



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

    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2024,
            14,
            AdventDay.TEST
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
        for i, rr in enumerate(r):
            n = f.robot_cycle_length(rr)
            debug(f"{i} CYCLE {n}")
        #f.display()
        #f.move_robots(num_steps=100)
        #debug(f"Q C {f.robot_counts()} SAFETY {f.safety_factor()}")
        #f.set_robots(f.tree(trunk_width=1))
        #f.display()
        #n = f.find_tree(start_run=self.tree_start, max_runs=self.tree_tries)
        #debug(f"TREE RUNS {n + 1} FOUND? {n >= self.tree_tries}")


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
