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
        assert day.run_from_test_input(input=Test_Day_2024_11.SIMPLE) == 7

    def test_long_06(self, day):
        day.set_num_blinks(6)
        assert day.run_from_test_input(input=Test_Day_2024_11.LONG) == 22

    def test_long_25(self, day):
        day.set_num_blinks(25)
        assert day.run_from_test_input(input=Test_Day_2024_11.LONG) == 55312

    def test_file_25(self, day):
        day.set_num_blinks(25)
        assert day.run_from_file() == 203457

    def test_file_75(self, day):
        day.set_num_blinks(75)
        assert day.run_from_file() == 241394363462435


