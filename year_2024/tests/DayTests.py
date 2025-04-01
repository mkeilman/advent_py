from utils.debug import debug
import pytest


def _day():
    import re
    import sys
    import Day
    yd = [int(x) for x in re.match(r"test_day_(\d+)_(\d+)", sys._getframe(1).f_code.co_name).groups()]
    return Day.Base.get_day(*yd, {})


def test_day_2024_11():
    d = _day()

    d.set_num_blinks(1)
    n = d.run_from_test_strings(substitute_strings=["0 1 10 99 999"])
    assert n == 7

    d.set_num_blinks(6)
    n = d.run_from_test_strings(substitute_strings=["125 17"])
    assert n == 22

    d.set_num_blinks(25)
    n = d.run_from_test_strings(substitute_strings=["125 17"])
    assert n == 55312

    n = d.run_from_file()
    assert n == 203457

    d.set_num_blinks(75)
    n = d.run_from_file()
    assert n == 241394363462435


