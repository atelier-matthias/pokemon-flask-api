from typing import NamedTuple

from flask_pymongo import DESCENDING


class Sort(NamedTuple):
    field: str
    direction: str

    def get_tuple(self):
        return [(self.field, -1 if self.direction == DESCENDING else 1)]


class Pagination(NamedTuple):
    limit: int
    offset: int

    def need_count(self, count):
        return count == self.limit or (self.limit < self.offset and count == 0)

