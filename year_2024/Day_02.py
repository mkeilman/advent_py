import re
import Day
import Utils


class AdventDay(Day.Base):

    def safe_sum(self, v):
        d = [[int(y) for y in re.findall(r"\d+", x)] for x in v]
        s = [int(self._is_safe(x)) for x in d]
        return Utils.Math.sum(s)

    
    def _is_safe(self, arr):
        max_diff = 3
        min_diff = 1

        d = [arr[i + 1] - arr[i] for i, _ in enumerate(arr[1:])]
        if not all([Utils.Math.sign(x) == Utils.Math.sign(d[0]) for x in d]):
            return False
        return all([min_diff <= abs(x) <= max_diff for x in d])

    def __init__(self, run_args):
        super(AdventDay, self).__init__(
            2024,
            2,
            [
                "7 6 4 2 1",
                "1 2 7 8 9",
                "9 7 6 2 1",
                "1 3 2 4 5",
                "8 6 4 4 1",
                "1 3 6 7 9",
            ]
        )

    def run(self, v):
        print(f"SAFE {self.safe_sum(v)}")


def main():
    d = AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == '__main__':
    main()
