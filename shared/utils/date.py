from datetime import datetime, timezone, timedelta


def get_current_utc_time() -> datetime:
    """Get the current time in UTC timezone."""
    return datetime.now(timezone.utc)


def get_current_local_time() -> datetime:
    """Get the current local time."""
    return datetime.now()


def format_date(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object to string."""
    return dt.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse a datetime string to a datetime object."""
    return datetime.strptime(date_str, format_str)


def add_days(dt: datetime, days: int) -> datetime:
    """Add a specified number of days to a datetime object."""
    return dt + timedelta(days=days)


def to_iso8601(dt: datetime) -> str:
    """Convert a datetime object to ISO 8601 string."""
    return dt.isoformat()
