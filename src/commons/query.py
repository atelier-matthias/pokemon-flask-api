from dataclasses import dataclass
from datetime import datetime
from typing import (
    Union,
    List,
    Tuple,
    Set,
    Optional,
)
from uuid import UUID

from bson import ObjectId
from flask import Request

from commons.commands import (
    Sort,
    Pagination,
)
from commons.handlers import DateTimeRange
from commons.parsers import (
    parse_uuid,
    parse_date,
)


@dataclass(frozen=True)
class ListParamsVO:
    __slots__ = 'sorting', 'direction', 'per_page', 'page'
    sorting: str
    direction: str
    per_page: int
    page: int

    @property
    def page_start(self):
        return 0 if not self.page or self.page < 0 else self.page

    def get_limit(self, max_limit: int = 50, default_limit: int = 25):
        if self.per_page:
            return self.per_page if 0 < self.per_page < max_limit else default_limit
        else:
            return default_limit


class QueryParams:
    __slots__ = ('_handler', '_sort_field', '_sort_order', '_limit', '_page')

    class Fields:
        SORT = 'sort'
        ORDER = 'order'
        PAGE = 'page'
        LIMIT = 'limit'

    class Direction:
        ASC = 'asc'
        DESC = 'desc'

    def __init__(self, request: Request) -> None:
        super().__init__()
        self._handler: Request = request
        self._sort_field: str = None
        self._sort_order: str = None
        self._limit: int = 0
        self._page: int = 0

    @classmethod
    def search(cls, request: Request, available_sort: Union[List[str], Tuple, Set[str]],
               default_sort_field: str,
               default_sort_order: str,
               max_limit: int = 50, default_limit: int = 25):

        query_params = cls(request)

        query_params._sort_field = request.args.get(cls.Fields.SORT, None)
        if query_params._sort_field is None or query_params._sort_field not in available_sort:
            query_params._sort_field = default_sort_field

        query_params._sort_order: str = request.args.get(cls.Fields.ORDER, None)
        if query_params._sort_order is None or query_params._sort_order not in {cls.Direction.ASC, cls.Direction.DESC}:
            query_params._sort_order = default_sort_order

        try:
            query_params._limit = int(request.args.get(cls.Fields.LIMIT, default_limit))
            if 0 > query_params._limit or query_params._limit > max_limit:
                query_params._limit = default_limit
        except (ValueError, TypeError):
            query_params._limit = default_limit

        try:
            query_params._page = int(request.args.get(cls.Fields.PAGE, 0))
            if 0 > query_params._page:
                query_params._page = 0
        except (ValueError, TypeError):
            query_params._page = 0
        return query_params

    def get_sort_field(self) -> str:
        return self._sort_field

    def get_sort_order(self) -> str:
        return self._sort_order

    def get_sort(self) -> Sort:
        return Sort(self.get_sort_field(), self.get_sort_order())

    def get_page(self) -> int:
        return self._page

    def get_limit(self) -> int:
        return self._limit

    def get_pagination(self) -> Pagination:
        limit = self.get_limit()

        return Pagination(limit, self.get_page() * limit)

    def fetch_list_params(self) -> ListParamsVO:
        return ListParamsVO(
                sorting=self.get_sort_field(),
                direction=self.get_sort_order(),
                per_page=self.get_limit(),
                page=self.get_page()
        )

    def get_uuid_arg(self, field_name: str) -> Optional[UUID]:
        return parse_uuid(self._handler.get_argument(field_name, None))

    def get_datetime_range_arg(self, field_name: str, default: Optional[str] = None) -> Optional[DateTimeRange]:
        date_from = parse_date(self._handler.get_argument(f"{field_name}From", default))
        date_to = parse_date(self._handler.get_argument(f"{field_name}To", default))
        if date_to:
            date_to = datetime(date_to.year, date_to.month, date_to.day, 23, 59, 59)

        return DateTimeRange(date_from, date_to)

    def get_arg(self, field_name: str, default: Optional[str] = None, min_len: Optional[int] = None, max_len: Optional[int] = None) -> Optional[str]:
        value = self._handler.args.get(field_name, None)

        if value is None:
            return default

        if min_len and len(value) < min_len:
            return default

        if max_len and len(value) > max_len:
            return default

        return value

    def get_all_params(self):
        return {key: self._handler.get_argument(key) for key in self._handler.request.arguments}
