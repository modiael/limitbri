import pytest

from time import sleep
from datetime import timedelta
from limitbri.decorators import rate_limit
from limitbri.exceptions import RateLimitException


@rate_limit(max_calls=1, interval=timedelta(seconds=1))
def count(n: int = 0, seconds=0):
    sleep(seconds)
    return n + 1


def test_raises_one_exception():
    with pytest.raises(RateLimitException):
        times = 2
        for _ in range(times):
            count()
