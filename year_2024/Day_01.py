import re
import Day
import Utils


class AdventDay(Day.Base):

    def col_diff_sum(self, v):
        d = self._col_diffs(*self._get_cols(v))
        return Utils.Math.sum(d)
    
    
    def _col_diffs(self, c1, c2):
        return [abs(c1[i] - c2[i]) for i, _ in enumerate(c1)]
    

    def _get_cols(self, v):
        d = [re.findall(r"\d+", x) for x in v]
        c1 = sorted([int(x[0]) for x in d])
        c2 = sorted([int(x[1]) for x in d])
        return c1, c2

    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2024,
            1,
            [
                "3   4",
                "4   3",
                "2   5",
                "1   3",
                "3   9",
                "3   3",
            ]
        )

    def run(self, v):
        print(f"C {self.col_diff_sum(v)}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
