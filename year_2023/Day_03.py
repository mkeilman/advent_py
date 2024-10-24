import re
import Day


class Grid:
    import re

    @classmethod
    def parts(cls, line):
        return re.findall(r"\D*(\d+)\D*", line)

    def __init__(self, schematic):
        self.schematic = schematic
        self.size = [len(self.schematic), len(self.schematic[0].strip())]
        self.gears = self._gears()
        self.gear_sum = self._gears_sum()
        self.ratio_sum = self._gear_ratio_sum()

    def _gear_ratio_sum(self):
        gears = {k: v for k, v in self.gears.items() if len(v) == 2}
        n = 0
        for g in gears:
            p = gears[g]
            n += (p[0] * p[1])
        return n

    def _gears_sum(self):
        n = 0
        for (i, line) in enumerate(self.schematic):
            l = line.strip()
            l_idx = 0
            for p in Grid.parts(l):
                c = l.index(p, l_idx)
                n += (int(p) if self._is_part(p, [c, i]) > -2 else 0)
                l_idx = c + len(p)
        return n

    def _gears(self):
        gears = {}
        for (i, line) in enumerate(self.schematic):
            l = line.strip()
            l_idx = 0
            for p in Grid.parts(l):
                c = l.index(p, l_idx)
                t = self._is_part(p, [c, i])
                if t > -1:
                    g = str(t)
                    if g not in gears:
                        gears[g] = []
                    gears[g].append(int(p))
                # in case of duplicate numbers on one line
                l_idx = c + len(p)
        return gears

    def _is_part(self, p, pos):
        n = self._neighborhood(p, pos)
        for r in n[1]:
            for c in n[0]:
                s = self.schematic[r][c]
                if not re.match(r"[.0-9]", s):
                    return (r * self.size[1] + c) if s == "*" else -1
        return -2

    def _neighborhood(self, txt, pos):
        rx = [x for x in range(pos[0] - 1, pos[0] + len(txt) + 1) if 0 <= x < self.size[0]]
        ry = [y for y in range(pos[1] - 1, pos[1] + 2) if 0 <= y < self.size[1]]
        return [rx, ry]

    def _print_neighborhood(self, txt, pos):
        n = self._neighborhood(txt, pos)
        for r in n[1]:
            print(self.schematic[r][n[0][0]:(n[0][-1] + 1)])


class AdventDay(Day.Base):

    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2023,
            3,
            [
                "467..114..",
                "...*......",
                "..35..633.",
                "......#...",
                "617*......",
                ".....+.58.",
                "..592.....",
                "......755.",
                "...$.*....",
                ".664.598..",
            ]
        )

    def run(self, v):
        grid = Grid(v)
        n = grid.gear_sum
        g = grid.ratio_sum
        print(f"SUM {n} GEARS {g}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
