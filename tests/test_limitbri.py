import pytest
from time import sleep, time
from datetime import timedelta
from limitbri.decorators import rate_limit


@rate_limit(max_calls=1, interval=timedelta(seconds=1))
def count_with_limit(n: int = 0, seg: int = 0):
    sleep(seg)
    return n + 1


@rate_limit(interval=timedelta(seconds=0))
def count_no_limit(n: int = 0, seg: int = 0):
    sleep(seg)
    return n + 1


def setup_function():
    count_with_limit.resetInterval = None


def test_execute_once():
    counter = count_with_limit()
    assert counter == 1


def test_execute_multiple():
    times = 2
    counter = 0
    initial_time = time()
    for _ in range(times):
        counter = count_with_limit(n=counter, seg=1)
    assert counter == times
    assert (time() - initial_time) >= times


def test_execute_multiple_no_limit():
    times = 10
    counter = 0
    for i in range(times):
        counter = count_no_limit(n=counter)
    assert counter == times
