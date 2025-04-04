from utils.debug import debug_print
import pytest

@pytest.fixture(scope="class")
def day(request):
    import re
    import Day
    yd = [int(x) for x in re.match(r"Test_Day_(\d+)_(\d+)", request.cls.__name__).groups()]
    return Day.Base.get_day(*yd, {})


class Test_Day_2024_01:

    def test_part_1_test(self, day):
        day.calc = "col-diffs"
        assert day.run_from_test_input() == 11

    def test_part_1_file(self, day):
        day.calc = "col-diffs"
        assert day.run_from_file() == 2031679

    def test_part_2_test(self, day):
        day.calc = "similarity"
        assert day.run_from_test_input() == 31

    def test_part_2_file(self, day):
        day.calc = "similarity"
        assert day.run_from_file() == 19678534


class Test_Day_2024_02:

    def test_part_1_test(self, day):
        day.dampen = False
        assert day.run_from_test_input() == 2

    def test_part_1_file(self, day):
        day.dampen = False
        assert day.run_from_file() == 282

    def test_part_2_test(self, day):
        day.dampen = True
        assert day.run_from_test_input() == 4

    def test_part_2_file(self, day):
        day.dampen = True
        assert day.run_from_file() == 349


class Test_Day_2024_03:

    def test_part_1_test(self, day):
        day.respect_enables = False
        assert day.run_from_test_input() == 161

    def test_part_1_file(self, day):
        day.respect_enables = False
        assert day.run_from_file() == 174561379

    def test_part_2_test(self, day):
        day.respect_enables = True
        assert day.run_from_test_input() == 48

    def test_part_2_file(self, day):
        day.respect_enables = True
        assert day.run_from_file() == 106921067


class Test_Day_2024_04:

    def test_part_1_test(self, day):
        day.x_mas = False
        assert day.run_from_test_input() == 18

    def test_part_1_file(self, day):
        day.x_mas = False
        assert day.run_from_file() == 2434

    def test_part_2_test(self, day):
        day.x_mas = True
        assert day.run_from_test_input() == 9

    def test_part_2_file(self, day):
        day.x_mas = True
        assert day.run_from_file() == 1835


class Test_Day_2024_05:

    def test_part_1_test(self, day):
        day.ordered = True
        assert day.run_from_test_input() == 143

    def test_part_1_file(self, day):
        day.ordered = True
        assert day.run_from_file() == 4957

    def test_part_2_test(self, day):
        day.ordered = False
        assert day.run_from_test_input() == 123

    def test_part_2_file(self, day):
        day.ordered = False
        assert day.run_from_file() == 6938


class Test_Day_2024_06:

    def test_part_1_test(self, day):
        pass

    def test_part_1_file(self, day):
        pass

    def test_part_2_test(self, day):
        pass

    def test_part_2_file(self, day):
        pass


class Test_Day_2024_07:

    def test_part_1_test(self, day):
        day.use_concat = False
        assert day.run_from_test_input() == 3749

    def test_part_1_file(self, day):
        day.use_concat = False
        assert day.run_from_file() == 4364915411363

    def test_part_2_test(self, day):
        day.use_concat = True
        assert day.run_from_test_input() == 11387

    def test_part_2_file(self, day):
        day.use_concat = True
        assert day.run_from_file() == 38322057216320


class Test_Day_2024_08:

    def test_part_1_test(self, day):
        day.t_nodes = False
        assert day.run_from_test_input() == 14

    def test_part_1_file(self, day):
        day.t_nodes = False
        assert day.run_from_file() == 423

    def test_part_2_test(self, day):
        day.t_nodes = True
        assert day.run_from_test_input() == 34

    def test_part_2_file(self, day):
        day.t_nodes = True
        assert day.run_from_file() == 1287


class Test_Day_2024_11:
    
    SIMPLE = ["0 1 10 99 999"]
    LONG = ["125 17"]

    def test_part_1_test(self, day):
        day.set_num_blinks(1)
        assert day.run_from_test_input() == 7

    def test_part_1_test_1(self, day):
        day.set_num_blinks(6)
        assert day.run_from_test_input(input=day.__class__.SMALL) == 22

    def test_part_1_test_2(self, day):
        day.set_num_blinks(25)
        assert day.run_from_test_input(input=day.__class__.SMALL) == 55312

    def test_part_1_file(self, day):
        day.set_num_blinks(25)
        assert day.run_from_file() == 203457

    def test_part_2_file(self, day):
        day.set_num_blinks(75)
        assert day.run_from_file() == 241394363462435


