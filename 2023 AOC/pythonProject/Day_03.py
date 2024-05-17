import re


re_part = r"\D*(\d+)\D*"
re_digit_or_dot = r"[.0-9]"

test_schematic = [
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


def _neighborhood(txt, pos, grid_size):
    rx = [x for x in range(pos[0] - 1, pos[0] + len(txt) + 1) if 0 <= x < grid_size[0]]
    ry = [y for y in range(pos[1] - 1, pos[1] + 2) if 0 <= y < grid_size[1]]
    return [rx, ry]


def _parts(line):
    return re.findall(re_part, line)


def _print_neighborhood(txt, pos, grid):
    n = _neighborhood(txt, pos, _schematic_size(grid))
    for r in n[1]:
        print(grid[r][n[0][0]:(n[0][-1] + 1)])


def _schematic_test():
    return _parts_sum(test_schematic)


def _gear_ratio_sum(gears):
    n = 0
    for g in gears:
        p = gears[g]
        n += (p[0] * p[1])
    return n


def is_part(neighborhood, grid):
    sz = _schematic_size(grid)
    for r in neighborhood[1]:
        for c in neighborhood[0]:
            s = grid[r][c]
            if not re.match(re_digit_or_dot, s):
                return (r * sz[1] + c) if s == "*" else -1
    return -2


def _schematic_size(lines):
    # rows, cols
    return [len(lines), len(lines[0].strip())]


def _schematic_file(filename):
    with open(filename, "r") as f:
        return  _parts_sum(f.readlines())



def _parts_sum(grid):
    n = 0
    gears = {}
    grid_size = _schematic_size(grid)
    for (i, line) in enumerate(grid):
        l = line.strip()
        l_idx = 0
        for p in _parts(l):
            c = l.index(p, l_idx)
            t = is_part(
                _neighborhood(p, [c, i], grid_size),
                grid
            )
            n += (int(p) if t > -2 else 0)
            if t > -1:
                g = str(t)
                if g not in gears:
                    gears[g] = []
                gears[g].append(int(p))
            # in case of duplicate numbers on one line
            l_idx = c + len(p)
    return n, _gear_ratio_sum({k:v for k, v in gears.items() if len(v) == 2})


def main():
    #n, g = _schematic_test()
    #print(f"TEST {n} GEARS {g}")
    n, g = _schematic_file("input_day_03.txt")
    print(f"SUM {n} GEARS {g}")


if __name__ == '__main__':
    main()
