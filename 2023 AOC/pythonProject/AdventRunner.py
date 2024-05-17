import importlib
import Day


def main():
    day = 3
    d = importlib.import_module(f"Day_{day:02d}").AdventDay()
    print("TEST:")
    d.run_from_test_strings()
    print("FILE:")
    d.run_from_file()


if __name__ == "__main__":
    main()
