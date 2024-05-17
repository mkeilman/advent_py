import numpy
import re

bag = {
    "blue": 14,
    "green": 13,
    "red": 12,
}

colors = list(bag.keys())
n_cubes = numpy.sum(list(bag.values()))
re_colors = r"|".join(colors)
re_id = r"Game\s*(\d+):"
re_pull = fr"(\d+)\s*({re_colors}),*\s*"

test_games = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]


def _game_test():
    return _games_sum(test_games)


def _power_test():
    return _games_power_sum(test_games)


def _to_game(line):
    gid = int(re.match(re_id, line).group(1))
    g = {
        "id": gid,
        "colors": {},
    }
    pulls = re.split(r";\s*", re.split(r":\s*", line)[1])
    for (i, p) in enumerate(pulls):
        for (n, c) in re.findall(re_pull, p):
            if c not in g["colors"]:
                g["colors"][c] = len(pulls) * [0]
            g["colors"][c][i] = int(n)
    return g


def _game_num(game):
    counts = []
    for c in game["colors"]:
        n = game["colors"][c]
        counts.append(n)
        if any([x > bag[c] for x in n]):
            return 0
    return 0 if any([x > n_cubes for x in numpy.sum(counts, axis=0)]) else game["id"]


def _game_power(game):
    p = 1
    for c in game["colors"]:
        p *= max(game["colors"][c])
    return p


def _games_sum(lines):
    n = 0
    for line in lines:
        n += _game_num(_to_game(line))
    return n


def _games_power_sum(lines):
    n = 0
    for line in lines:
        n += _game_power(_to_game(line))
    return n


def main():
    with open("input_day_02.txt", "r") as f:
        g = f.readlines()
        s = _games_sum(g)
        p = _games_power_sum(g)
    print("SUM {}".format(s))
    print("POWER SUM {}".format(p))

    #print("SUM TEST {}".format(_game_test()))
    #print("POWER TEST {}".format(_power_test()))


if __name__ == '__main__':
    main()
