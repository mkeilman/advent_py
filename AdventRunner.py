import argparse
import importlib
from utils.debug import debug

def main():
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
    
    d = importlib.import_module(f"year_{a.year}.Day_{a.day:02d}").AdventDay(a.year, a.day, u)
    if a.mode in ("test", "all"):
        debug("TEST:")
        d.run_from_test_strings()
    if a.mode in ("file", "all"):
        debug("FILE:")
        d.run_from_file()


if __name__ == "__main__":
    main()
