from calendar import timegm
from datetime import datetime


def get_unixtimestamp(date: datetime = None) -> int:
    """
    Converts date and time to unix timestamp
    If date is not provided then it takes current time and convert it to unix timestamp
    :param date: datetime
    :return: int
    """
    if not date or not isinstance(date, datetime):
        date = datetime.utcnow()
    return timegm(date.utctimetuple())
