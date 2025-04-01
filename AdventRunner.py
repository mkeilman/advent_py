import argparse
from utils.debug import debug_print

def main():
    import Day

    p = argparse.ArgumentParser(description="run AdventOfCode for the given year and day")
    p.add_argument("year", type=int, help="year to run")
    p.add_argument("day", type=int, help="day to run")
    p.add_argument(
        "--mode",
        type=str,
        help="run mode",
        choices=["test", "file", "all"],
        default="all",
        dest="mode",
    )
    a, u = p.parse_known_args()
    d = Day.Base.get_day(a.year, a.day, u)

    if a.mode in ("test", "all"):
        debug_print("TEST:")
        d.run_from_test_strings()
    if a.mode in ("file", "all"):
        debug_print("FILE:")
        d.run_from_file()


if __name__ == "__main__":
    main()
