from datetime import datetime


class RateLimitException(Exception):
    """Rate Limit Exceeded"""
    reset_datetime: datetime

    def __init__(self, reset_datetime: datetime, message: str = None):
        super(RateLimitException, self).__init__(message)
        self.reset_datetime = reset_datetime
