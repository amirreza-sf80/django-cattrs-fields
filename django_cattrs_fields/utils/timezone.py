import datetime
from datetime import timezone, tzinfo

from django.conf import settings
from django.utils import timezone as dj_timezone

# these codes were copied from drf
# TODO: check the quality


def datetime_exists(dt: datetime.datetime):
    """Check if a datetime exists. Taken from: https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html"""
    # There are no non-existent times in UTC, and comparisons between
    # aware time zones always compare absolute times; if a datetime is
    # not equal to the same datetime represented in UTC, it is imaginary.
    return dt.astimezone(timezone.utc) == dt


def datetime_ambiguous(dt: datetime.datetime):
    """Check whether a datetime is ambiguous. Taken from: https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html"""
    # If a datetime exists and its UTC offset changes in response to
    # changing `fold`, it is ambiguous in the zone specified.
    return datetime_exists(dt) and (dt.replace(fold=not dt.fold).utcoffset() != dt.utcoffset())


def valid_datetime(dt: datetime.datetime):
    """Returns True if the datetime is not ambiguous or imaginary, False otherwise."""
    if isinstance(dt.tzinfo, tzinfo) and not datetime_ambiguous(dt):
        return True
    return False


def enforce_timezone(value: datetime.datetime) -> datetime.datetime:
    """
    When `self.default_timezone` is `None`, always return naive datetimes.
    When `self.default_timezone` is not `None`, always return aware datetimes.
    """
    field_timezone = dj_timezone.get_current_timezone() if settings.USE_TZ else None
    if field_timezone is not None:
        if dj_timezone.is_aware(value):
            try:
                return value.astimezone(field_timezone)
            except OverflowError:
                raise ValueError("Datetime value out of range")
        try:
            dt = dj_timezone.make_aware(value, field_timezone)
            # When the resulting datetime is a ZoneInfo instance, it won't necessarily
            # throw given an invalid datetime, so we need to specifically check.
            if not valid_datetime(dt):
                raise ValueError(f"Invalid datetime for the timezone {field_timezone}")
            return dt
        except Exception as e:
            raise ValueError from e
    elif (field_timezone is None) and dj_timezone.is_aware(value):
        return dj_timezone.make_naive(value, datetime.timezone.utc)
    return value
