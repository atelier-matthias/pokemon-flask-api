from datetime import datetime
from typing import Optional


class DateTimeRange:
    __slots__ = ('date_time_from', 'date_time_to')

    date_time_from: Optional[datetime]
    date_time_to: Optional[datetime]

    def __init__(self, date_time_from: Optional[datetime] = None, date_time_to: Optional[datetime] = None):
        self.date_time_from = date_time_from
        self.date_time_to = date_time_to

    def is_empty(self):
        return not self.date_time_from and not self.date_time_to
