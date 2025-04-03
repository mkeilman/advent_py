from utils.debug import debug_print
import pytest

@pytest.fixture(scope="class")
def day(request):
    import re
    import Day
    yd = [int(x) for x in re.match(r"Test_Day_(\d+)_(\d+)", request.cls.__name__).groups()]
    return Day.Base.get_day(*yd, {})


class Test_Day_2024_01:

    TEST = [
        "3   4",
        "4   3",
        "2   5",
        "1   3",
        "3   9",
        "3   3",
    ]

    def test_distance_test(self, day):
        assert day.run_from_test_input(input=self.__class__.TEST) == 11

    def test_distance_file(self, day):
        assert day.run_from_file() == 2031679


class Test_Day_2024_02:

    TEST = [
        "7 6 4 2 1",
        "1 2 7 8 9",
        "9 7 6 2 1",
        "1 3 2 4 5",
        "8 6 4 4 1",
        "1 3 6 7 9",
    ]

    def test_safety_test(self, day):
        day.dampen = False
        assert day.run_from_test_input(input=self.__class__.TEST) == 2

    def test_safety_file(self, day):
        day.dampen = False
        assert day.run_from_file() == 282

    def test_safety_test_damped(self, day):
        day.dampen = True
        assert day.run_from_test_input(input=self.__class__.TEST) == 4

    def test_safety_file_damped(self, day):
        day.dampen = True
        assert day.run_from_file() == 349


class Test_Day_2024_03:

    TEST = [
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
    ]


    def test_mult_test(self, day):
        day.respect_enables = False
        assert day.run_from_test_input(input=self.__class__.TEST) == 161

    def test_mult_file(self, day):
        day.respect_enables = False
        assert day.run_from_file() == 174561379

    def test_mult_test_enable(self, day):
        day.respect_enables = True
        assert day.run_from_test_input(input=self.__class__.TEST) == 48

    def test_mult_file_enable(self, day):
        day.respect_enables = True
        assert day.run_from_file() == 106921067


class Test_Day_2024_04:

    TEST = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX",
    ]


    def test_xmas_test(self, day):
        day.x_mas = False
        assert day.run_from_test_input(input=self.__class__.TEST) == 18

    def test_xmas_file(self, day):
        day.x_mas = False
        assert day.run_from_file() == 2434


    def test_xmas_test(self, day):
        day.x_mas = True
        assert day.run_from_test_input(input=self.__class__.TEST) == 9

    def test_xmas_file(self, day):
        day.x_mas = True
        assert day.run_from_file() == 1835



class Test_Day_2024_11:
    
    SIMPLE = ["0 1 10 99 999"]
    LONG = ["125 17"]

    def test_simple(self, day):
        day.set_num_blinks(1)
        assert day.run_from_test_input(input=self.__class__.SIMPLE) == 7

    def test_long_06(self, day):
        day.set_num_blinks(6)
        assert day.run_from_test_input(input=self.__class__.LONG) == 22

    def test_long_25(self, day):
        day.set_num_blinks(25)
        assert day.run_from_test_input(input=self.__class__.LONG) == 55312

    def test_file_25(self, day):
        day.set_num_blinks(25)
        assert day.run_from_file() == 203457

    def test_file_75(self, day):
        day.set_num_blinks(75)
        assert day.run_from_file() == 241394363462435


