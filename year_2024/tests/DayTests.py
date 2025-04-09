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


class Test_Day_2024_09:

    def test_part_1_test(self, day):
        day.whole_files = False
        assert day.run_from_test_input() == 1928

    def test_part_1_file(self, day):
        day.whole_files = False
        assert day.run_from_file() == 6399153661894

    def test_part_2_test(self, day):
        day.whole_files = True
        assert day.run_from_test_input() == 2858

    def test_part_2_file(self, day):
        day.whole_files = True
        assert day.run_from_file() == 6421724645083


class Test_Day_2024_11:

    def test_part_1_test(self, day):
        day.num_blinks = 1
        assert day.run_from_test_input() == 7

    def test_part_1_test_1(self, day):
        day.num_blinks = 6
        assert day.run_from_test_input(input=day.__class__.SMALL) == 22

    def test_part_1_test_2(self, day):
        day.num_blinks = 25
        assert day.run_from_test_input(input=day.__class__.SMALL) == 55312

    def test_part_1_file(self, day):
        day.num_blinks = 25
        assert day.run_from_file() == 203457

    def test_part_2_file(self, day):
        day.num_blinks = 75
        assert day.run_from_file() == 241394363462435


class Test_Day_2024_13:

    def test_part_1_test(self, day):
        assert day.run_from_test_input() == 480

    def test_part_1_file(self, day):
        assert day.run_from_file() == 31589

    def test_part_2_file(self, day):
        day.prize_offset = 10000000000000
        assert day.run_from_file() == 98080815200063


class Test_Day_2024_14:

    def test_part_1_test(self, day):
        day.tree_tries = 0
        assert day.run_from_test_input() == 12

    def test_part_1_file(self, day):
        day.tree_tries = 0
        day.width = 101
        day.height = 103
        assert day.run_from_file() == 228421332

    def test_part_2_file(self, day):
        day.tree_tries = 10000
        day.tree_start = 7500
        day.width = 101
        day.height = 103
        assert day.run_from_file() == 7790
