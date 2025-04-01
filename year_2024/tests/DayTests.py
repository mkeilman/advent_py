from utils.debug import debug_print
import pytest

@pytest.fixture(scope="class")
def day(request):
    import re
    import Day
    yd = [int(x) for x in re.match(r"Test_Day_(\d+)_(\d+)", request.cls.__name__).groups()]
    return Day.Base.get_day(*yd, {})


class Test_Day_2024_11:
    
    SIMPLE = ["0 1 10 99 999"]
    LONG = ["125 17"]

    def test_simple(self, day):
        day.set_num_blinks(1)
        n = day.run_from_test_strings(substitute_strings=Test_Day_2024_11.SIMPLE)
        assert n == 7

    def test_long_06(self, day):
        day.set_num_blinks(6)
        n = day.run_from_test_strings(substitute_strings=Test_Day_2024_11.LONG)
        assert n == 22

    def test_long_25(self, day):
        day.set_num_blinks(25)
        n = day.run_from_test_strings(substitute_strings=Test_Day_2024_11.LONG)
        assert n == 55312

    def test_file_25(self, day):
        day.set_num_blinks(25)
        n = day.run_from_file()
        assert n == 203457

    def test_file_75(self, day):
        day.set_num_blinks(75)
        n = day.run_from_file()
        assert n == 241394363462435


