from utils.debug import debug
import pytest


def _day():
    import re
    import sys
    import Day
    from Day import Base
    yd = [int(x) for x in re.match(r"test_day_(\d+)_(\d+)", sys._getframe(1).f_code.co_name).groups()]
    return Day.Base.get_day(*yd, {})


def test_day_2024_11():
    d = _day()
    d.run_from_test_strings()
    pass

