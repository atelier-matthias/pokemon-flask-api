from datetime import datetime
from typing import (
    Optional,
    Union,
)
from uuid import UUID

from commons import iso8601


def parse_uuid(str_uuid: str, default=None) -> Optional[UUID]:
    try:
        if isinstance(str_uuid, bytes):
            str_uuid = str_uuid.decode()
        if not isinstance(str_uuid, UUID):
            return UUID(str_uuid)
        else:
            return str_uuid
    except (ValueError, TypeError, AttributeError):
        return default


def parse_date(date_stamp, default=None) -> datetime:
    try:
        return iso8601.parse_date(date_stamp)
    except (ValueError, iso8601.ParseError, TypeError):
        return default


def parse_int(value: Union[float, int, str], default: Optional[int] = 0):
    try:
        out = int(value)
    except (ValueError, TypeError):
        out = default
    return out
