import threading
from functools import wraps
from datetime import datetime, timedelta
from typing import Callable

from limitbri.exceptions import RateLimitException


def rate_limit(max_calls: int = 15, interval: timedelta = timedelta(seconds=900)) -> Callable:
    """
    A marvelous decorator that prevents a function from executing more times
    than allowed in the selected time window.

    It will raises a RateLimitException with the property reset_datetime that
    indicates when is possible to execute the desired function.

    :param max_calls: maximum number of possible executions of the decorated function
    :type max_calls: int

    :param interval: interval of time until counter will reset
    :type interval: timedelta

    :raises RateLimitException

    :returns: decorated function
    """

    def decorator_rate_limit(func):
        def __reset():
            wrapper_rate_limit.calls_done = 0
            wrapper_rate_limit.resetInterval = datetime.now() + interval

        def __is_possible_execute_function() -> bool:
            return wrapper_rate_limit.calls_done < max_calls

        def __is_reset_required() -> bool:
            return wrapper_rate_limit.resetInterval is None or datetime.now() >= wrapper_rate_limit.resetInterval

        @wraps(func)
        def wrapper_rate_limit(*args, **kwargs):
            with wrapper_rate_limit.lock:
                if __is_reset_required():
                    __reset()

                if __is_possible_execute_function():
                    value = func(*args, **kwargs)
                    wrapper_rate_limit.calls_done += 1
                    return value
                else:
                    raise RateLimitException(wrapper_rate_limit.resetInterval)

        wrapper_rate_limit.lock = threading.RLock()
        wrapper_rate_limit.calls_done = 0
        wrapper_rate_limit.resetInterval = None
        return wrapper_rate_limit

    return decorator_rate_limit
