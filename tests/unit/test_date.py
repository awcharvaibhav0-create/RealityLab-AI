from datetime import datetime
from shared.utils.date import get_current_utc_time, format_date, parse_date, add_days


def test_get_current_utc_time():
    dt = get_current_utc_time()
    assert isinstance(dt, datetime)
    assert dt.tzinfo is not None


def test_format_and_parse_date():
    dt = datetime(2023, 1, 1, 12, 0, 0)
    formatted = format_date(dt)
    assert formatted == "2023-01-01 12:00:00"

    parsed = parse_date(formatted)
    assert parsed == dt


def test_add_days():
    dt = datetime(2023, 1, 1)
    future = add_days(dt, 5)
    assert future.day == 6
