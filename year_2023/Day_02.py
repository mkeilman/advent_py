import numpy
import re
import Day

class AdventDay(Day.Base):

    @classmethod
    def _games_power_sum(cls, lines):
        n = 0
        for line in lines:
            n += Game(line).power
        return n

    @classmethod
    def _games_sum(cls, lines):
        n = 0
        for line in lines:
            n += Game(line).num
        return n

    def __init__(self):
        super(AdventDay, self).__init__(
            2023,
            2,
            [
                "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
                "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
                "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
                "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
                "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
            ]
        )

    def run(self, v):
        print(f"SUM {AdventDay._games_sum(v)}")
        print(f"POWER SUM {AdventDay._games_power_sum(v)}")


class Game:
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

    def __init__(self, txt):
        self.gid = int(re.match(Game.re_id, txt).group(1))
        self.colors = {}

        pulls = re.split(r";\s*", re.split(r":\s*", txt)[1])
        for (i, p) in enumerate(pulls):
            for (n, c) in re.findall(Game.re_pull, p):
                if c not in self.colors:
                    self.colors[c] = len(pulls) * [0]
                self.colors[c][i] = int(n)

        self.num = self._game_num()
        self.power = self._game_power()

    def _game_num(self):
        counts = []
        for c in self.colors:
            n = self.colors[c]
            counts.append(n)
            if any([x > Game.bag[c] for x in n]):
                return 0
        return 0 if any([x > Game.n_cubes for x in numpy.sum(counts, axis=0)]) else self.gid

    def _game_power(self):
        p = 1
        for c in self.colors:
            p *= max(self.colors[c])
        return p


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
