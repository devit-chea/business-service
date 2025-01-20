from datetime import datetime
from decimal import Decimal


def get_date_format(date_time: datetime = None, str_format: str = None):
    if not date_time:
        date_time = datetime.now()
    if str_format:
        return date_time.strftime(str_format)
    return date_time.strftime("%Y-%m-%d")


def get_relationship_field(model):
    result = []
    fields = model._meta.get_fields()
    for field in fields:
        if field.is_relation and hasattr(field, "null") and not field.null:
            result.append(field)
    return result


def to_decimal(value):
    if isinstance(value, Decimal):
        return value

    value = value if value is not None else 0
    return Decimal(value)


def to_int(value):
    if isinstance(value, int):
        return value
    return int(value) if value is not None else 0
