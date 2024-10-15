from functools import reduce
import re
import Day

re_times = r"(?:Time:\s+)*(\d+)\s?"
re_dists = r"(?:Distance:\s+)*(\d+)\s?"


class AdventDay(Day.Base):

    @classmethod
    def _dist(cls, press_time, total_time):
        return press_time * (total_time - press_time)

    @classmethod
    def _get_wins_product(cls, lines):
        dists = []
        wins = []
        for t in [int(x) for x in re.findall(re_times, lines[0])]:
            dists.append([cls._dist(i, t) for i in range(t + 1)])
        #print(f"D {dists}")
        record_dists = [int(x) for x in re.findall(re_dists, lines[1])]
        for (i, d) in enumerate(dists):
            w = 0
            o = len(d) % 2
            j = len(d) // 2 + o
            hd = d[:j]
            for (k, dd) in enumerate(hd):
                p = 1 if o and k == len(hd) - 1 else 0
                w += (2 - p if dd > record_dists[i] else 0)
            wins.append(w)
        #print(f"W {wins}")
        return reduce((lambda x, y: x * y), wins, 1)
        

    def __init__(self):
        super(AdventDay, self).__init__(
            2023,
            6,
            [
                "Time:        7     15     30",
                "Distance:   9   40   200",
            ]
        )
    

    def run(self, v):
        print(f"DISTS {AdventDay._get_wins_product(v)}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
