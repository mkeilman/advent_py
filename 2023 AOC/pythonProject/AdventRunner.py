import argparse
import importlib
import Day


def main():
    p = argparse.ArgumentParser(description='run AdventOfCode for the given day')
    p.add_argument("day", type=int, help="day to run")
    p.add_argument(
        "--mode",
        type=str,
        help="run mode",
        choices=["test", "file", "all"],
        default="all",
        dest="mode",
    )
    a = p.parse_args()
    d = importlib.import_module(f"Day_{a.day:02d}").AdventDay()
    if a.mode in ("test", "all"):
        print("TEST:")
        d.run_from_test_strings()
    if a.mode in ("file", "all"):
        print("FILE:")
        d.run_from_file()


if __name__ == "__main__":
    main()
