from typing import Optional
from uuid import UUID

from commons.errors import (
    error_missing,
    invalid_string,
    too_small,
    invalid_uuid,
    too_big,
    invalid_number,
)
from commons.parsers import (
    parse_uuid,
    parse_int,
)


def map_str(data: dict, field_name: str, errors: dict, required: bool = True, minimal: int = None) -> Optional[str]:
    field_value = data.get(field_name)

    if not field_value:
        if required:
            errors[field_name] = error_missing
    elif not isinstance(field_value, str):
        errors[field_name] = invalid_string
    elif minimal and len(field_value) < minimal:
        errors[field_name] = too_small(minimal)

    return field_value


def map_int(data: dict, field_name: str, errors: dict, default: Optional[int] = None, required: bool = True, min: int = None, max: int = None) -> Optional[int]:
    field_value = data.get(field_name)

    if field_value is None:
        if required:
            errors[field_name] = error_missing
        else:
            field_value = default
    else:
        field_value = parse_int(field_value, default=None)

        if field_value is None:
            errors[field_name] = invalid_number
        else:
            if min and field_value < min:
                errors[field_name] = too_small(min)
            elif max and field_value > max:
                errors[field_name] = too_big(max)

    return field_value


def map_uuid(data: dict, field_name: str, errors: dict, required: bool = True, error_field: str = None) -> Optional[UUID]:
    field_value = data.get(field_name)

    error_field = error_field if error_field else field_name

    if not field_value:
        if required:
            errors[error_field] = error_missing
    else:
        field_value = parse_uuid(field_value)

        if field_value is None:
            errors[error_field] = invalid_uuid

    return field_value
