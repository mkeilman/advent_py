import re
import Day
from utils import math
from utils import string
from utils.debug import debug

class Guard:

    DIRECTIONS = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }

    RE_DIRS = {
        "^": r"\^",
        ">": r">",
        "v": r"v",
        "<": r"<",
    }

    def __init__(self, position, direction):
        self.position = position
        self.init_pos = self.position
        self.direction = Guard.DIRECTIONS[direction]
        self.init_dir = self.direction


    def find_path(self, room):
        def _is_in_room(pos, room):
            nr = len(room)
            nc = len(room[0])
            return 0 <= pos[0] < nr and 0 <= pos[1] < nc


        p = [self.position]
        r = room[p[0][0]][p[0][1]]
        d = list(Guard.DIRECTIONS.values())

        while _is_in_room(self.position, room):
            q = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
            if _is_in_room(q, room):
                if room[q[0]][q[1]] == "#":
                    self.direction = d[(d.index(self.direction) + 1) % len(d)]
                    continue
                # do not include spaces outside the room, but do set the position
                p.append(q)
            self.position = q

        return p

    def next_position(self):
        return self.position


class AdventDay(Day.Base):
            

    def __init__(self, run_args):
        import argparse
        super(AdventDay, self).__init__(
            2024,
            6,
            [
                "....#.....",
                ".........#",
                "..........",
                "..#.......",
                ".......#..",
                "..........",
                ".#..^.....",
                "........#.",
                "#.........",
                "......#...",
            ]
        )

    def _get_guard(self, v):
        d = fr"[{'|'.join(Guard.RE_DIRS.values())}]"
        for i, r in enumerate(v):
            m = re.search(d, r)
            if m:
                return Guard((i, m.span()[0]), m[0])
        return None
    
    def run(self, v):
        g = self._get_guard(v)
        debug(f"G POS {g.position} DIR {g.direction}")
        p = g.find_path(v)
        debug(f"UNIQUE PATH LEN {len(set(p))}")
        pass


def main():
    d = AdventDay()
    debug("TEST:")
    d.run_from_test_strings()
    debug("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
