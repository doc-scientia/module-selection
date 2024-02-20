from datetime import datetime


def to_datetime(formatted: str, naive=False) -> datetime:
    format = f"%Y-%m-%dT%H:%M:%S{'.%f' if '.' in formatted else ''}%z"
    parsed = datetime.strptime(formatted, format)
    return parsed.replace(tzinfo=None) if naive else parsed


def to_datetime_string(date: datetime) -> str:
    return datetime.strftime(date, "%Y-%m-%dT%H:%M:%S%z")
