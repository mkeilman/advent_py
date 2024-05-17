import re
from functools import reduce

re_part = r"\D*(\d+)\D*"
re_digit_or_dot = r"[.0-9]"
re_seeds = r"(?:seeds:\s+)*(\d+)\s?"


test_maps = [
    "seeds: 79 14 55 13",
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
]


def _parse_maps(maps):
    ranges = {}
    s = "|".join((
        "fertilizer",
        "humidity",
        "light",
        "location",
        "seed",
        "soil",
        "temperature",
        "water",
    ))
    re_map = rf"({s})-to-({s})\s*map:"
    seeds = [int(x) for x in re.findall(re_seeds, maps[0])]
    map_source = None
    for i in range(1, len(maps)):
        m = maps[i].strip()
        if not m:
            map_source = None
            continue
        if map_source:
            ranges[map_source]["maps"].append(m)
            continue
        ml = re.match(re_map, maps[i])
        if ml:
            map_source, map_dest = ml.groups()
            if map_source not in ranges:
                ranges[map_source] = {
                    "dest": map_dest,
                    "maps": [],
                }

    return seeds, ranges


def _map_to_lambda(m, x):
    return _range_to_lambda(_map_to_range(m), x)


def _map_to_range(m):
    return [int(x) for x in re.findall(re_part, m)]


def _range_dest(a):
    return range(a[0], a[0] + a[2])


def _range_source(a):
    return range(a[1], a[1] + a[2])


def _seeds_to_ranges(seeds):
    import numpy

    return [
        range(r[0], r[0] + r[1]) for r in sorted(
            numpy.array(seeds).reshape((len(seeds) // 2, 2)),
            key=lambda x: x[0]
        )
    ]


def _range_to_lambda(a, x):
    rd = _range_dest(a)
    rs = _range_source(a)
    return x if x not in rs else rd[rs.index(x)]


def _loc_dest_ranges(ranges):
    return [_range_dest(_map_to_range(x)) for x in ranges["humidity"]["maps"]]


def _min_loc(maps):
    import sys

    loc = sys.maxsize * 2 + 1
    last_loc = loc
    seeds, ranges = _parse_maps(maps)
    loc_maps = ranges["humidity"]["maps"]
    loc_dest_ranges = [_range_dest(_map_to_range(x)) for x in loc_maps]
    min_map_val = sys.maxsize * 2 + 1
    #for s in seeds:
    min_loc_range = range(min_map_val, min_map_val + 2)
    min_loc_range_index = None
    seed_ranges = []
    seed_maps = []
    for j, r in enumerate(_seeds_to_ranges(seeds)):
        #print(f"r {r} STEPS {len(r)}")
        #i, l0 = _map_seed(r[0], ranges)
        #j, l1 = _map_seed(r[-1], ranges)
        sm = {}
        ml = _map_ranges(r, ranges, seed_map=sm)
        seed_ranges.append(ml)
        seed_maps.append(sm)
        print(f"SEED R {j} {ml} {sm}")
        min_ml = min(list(ml), key=lambda x: _range_dest(_map_to_range(loc_maps[x]))[0])
        #min_map = _map_to_range(loc_maps[min_ml])
        min_dest = loc_dest_ranges[min_ml] #range(min_map[1], min_map[1] + min_map[2])
        min_map_val = min(min_map_val, min_dest[0])
        if min_map_val < min_loc_range[0]:
            min_loc_range = min_dest
            min_loc_range_index = min_ml
        #print(f"{j} MIN SEED LOC {min_loc_range_index} {min_map_val} {min_loc_range}")
        # far too many iterations...
        #for i, s in enumerate(r):
        #    pass
            #loc = min(loc, _map_seed(s, ranges))
        #    if i % (len(r) // 10) == 0:
        #        print(f"LOC {i}: {loc}")
            #if loc == last_loc:
            #    print(f"NEW LOC {loc} IN {i + 1} STEPS")
            #    break
            #last_loc = loc
    #print(f"{min_loc_range_index} {sm[min_loc_range_index]}")
    for j, r in enumerate(_seeds_to_ranges(seeds)):
        if min_loc_range_index in seed_ranges[j]:
            print(f"{j} {_min_seed_loc(r, min_loc_range_index, ranges)} {seed_maps[j][min_loc_range_index]}")
    return loc


def _in_to_out(maps, x):
    i = -1
    for i, m in enumerate(maps):
        y = _map_to_lambda(m, x)
        if x != y:
            return i, y
    return i, x


def _map_seed(seed, ranges):
    src = "seed"
    i = seed
    n = -1
    o = i
    while src in ranges:
        r = ranges[src]
        d = r["dest"]
        m = r["maps"]
        n, o = _in_to_out(m, i)
        src = d
        i = o
    #print(f"LOC MAP {n}")
    return n, o


def _map_ranges(start_range, ranges, seed_map=None):
    r = set()
    s = {} if seed_map is None else seed_map
    n = len(start_range) // 2
    i, _ = _map_seed(start_range[0], ranges)
    j, _ = _map_seed(start_range[-1], ranges)
    r.add(i)

    #print(f"{idx} S1 {start_range[0]} {i} S2 {start_range[-1]} {j}")
    if i != j:
        r.add(j)
        r = r | _map_ranges(start_range[0:n], ranges, seed_map=s)
        r = r | _map_ranges(start_range[n:], ranges, seed_map=s)
    #print(f"S1 {start_range[0]} {i} S2 {start_range[-1]} {j}")
    s[i] = [start_range[0], start_range[-1]]
    return r


def _min_seed_loc(start_range, loc_range_index, ranges):
    import sys

    loc = sys.maxsize * 2 + 1

    lr = _loc_dest_ranges(ranges)
    n = len(start_range) // 2
    i = -1
    start = 0
    last_start = 0
    end = len(start_range) - 1
    i, l0 = _map_seed(start_range[end], ranges)
    print(f"MIN SEED LOC FOR {start_range} IN {loc_range_index}")
    #while i != loc_range_index and end > 0:
    #    end = end // 2
    #    i, l0 = _map_seed(start_range[end], ranges)
    #    print(f"{end} {i} {l0}")
    #j, l1 = _map_seed(start_range[0], ranges)
    #while j != loc_range_index and start < end:
    #    start = (end - start) // 2
    #    j, l1 = _map_seed(start_range[start], ranges)
    return l0



def _map_test():
    return _min_loc(test_maps)


def _map_file(filename):
    with open(filename, "r") as f:
        return _min_loc(f.readlines())


def main():
    #loc = _map_test()
    loc = _map_file("input_day_05.txt")
    print(f"MIN LOC {loc}")


if __name__ == "__main__":
    main()
