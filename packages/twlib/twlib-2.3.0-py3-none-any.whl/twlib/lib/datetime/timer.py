import datetime
import time
import timeit

import pytest


class Timer:
    """Measure time used."""

    def __init__(self, round_ndigits: int = 0):
        self._round_ndigits = round_ndigits
        self._start_time = timeit.default_timer()

    def __call__(self) -> float:
        return round(timeit.default_timer() - self._start_time, self._round_ndigits)

    def __str__(self) -> str:
        return str(datetime.timedelta(seconds=self()))

    def __repr__(self) -> str:
        return f"Timer(seconds={self()})"


def test_timer_interactive():
    timer = Timer(round_ndigits=2)

    # Access as a string
    print(f"Time elapsed is {timer=}.")

    time.sleep(0.1)
    print(f"Time elapsed is {timer=}.")

    # Access as a float
    print(f"Time elapsed as float is {timer()}.")
    time.sleep(0.1)
    print(f"Time elapsed as float is {timer()}.")


def test_timer():
    # Instantiate Timer with no rounding
    timer_no_rounding = Timer(0)
    time.sleep(1)  # sleep for 1 second
    assert timer_no_rounding() >= 1
    assert (
        int(str(timer_no_rounding).split(":")[-1]) == 1
    )  # the seconds part should be 1

    # Instantiate Timer with 2 digits rounding
    timer_with_rounding = Timer(2)
    time.sleep(1.23456)  # sleep for 1.23456 seconds
    assert 1.23 <= timer_with_rounding() <= 1.24
    assert float(str(timer_with_rounding).split(":")[-1]) == pytest.approx(1.23, 0.01)
