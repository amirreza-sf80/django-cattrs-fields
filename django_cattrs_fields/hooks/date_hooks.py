import datetime

from django.utils import formats
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.translation import gettext_lazy as _

from django_cattrs_fields.fields import DateField, DateTimeField, TimeField
from django_cattrs_fields.utils.timezone import enforce_timezone
from django_cattrs_fields.validators import forbid_falsy_values_validator


__all__ = (
    "date_structure",
    "date_structure_nullable",
    "date_unstructure",
    "datetime_structure",
    "datetime_structure_nullable",
    "datetime_unstructure",
    "time_structure",
    "time_structure_nullable",
    "time_unstructure",
    "time_unstructure_str",
)

# Date hooks


def date_structure(val, _) -> DateField:
    forbid_falsy_values_validator(val)

    if isinstance(val, datetime.date):
        return val
    elif isinstance(val, datetime.datetime):
        return val.date()
    else:
        try:
            parsed = parse_date(val)
            if parsed is not None:
                return parsed

        except ValueError:
            raise ValueError(
                f"“{val}” value has the correct format (YYYY-MM-DD) but it is an invalid date."
            )
        raise ValueError(
            f"“{val}” value has an invalid date format. It must be in YYYY-MM-DD format."
        )


def date_structure_nullable(val, _) -> DateField | None:
    if val is None:
        return None
    return date_structure(val, _)


def date_unstructure(val: DateField | None) -> datetime.date | None:
    if val is None:
        return None
    return datetime.date(val.year, val.month, val.day)


# DateTime hooks


def datetime_structure(val, _) -> DateTimeField:
    forbid_falsy_values_validator(val)

    if isinstance(val, datetime.datetime):
        return enforce_timezone(val)
    elif isinstance(val, datetime.date):
        return enforce_timezone(datetime.datetime(val.year, val.month, val.day))

    try:
        parsed = parse_datetime(val)
        if parsed is not None:
            return enforce_timezone(parsed)
    except ValueError:
        raise ValueError(
            f"“{val}s” value has the correct format "
            "(YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]) "
            "but it is an invalid date/time."
        )

    raise ValueError(
        f"“{val}s” value has an invalid format. It must be in "
        "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format."
    )


def datetime_structure_nullable(val, _) -> DateTimeField | None:
    if val is None:
        return None
    return datetime_structure(val, _)


def datetime_unstructure(val: DateTimeField | None) -> datetime.datetime | None:
    if val is None:
        return None

    return val


# Time hooks


def time_structure(val, _t) -> TimeField:
    forbid_falsy_values_validator(val)

    if isinstance(val, datetime.time):
        return val
    for format in formats.get_format_lazy("TIME_INPUT_FORMATS"):
        try:
            return datetime.datetime.strptime(val, format).time()
        except (ValueError, TypeError):
            continue
    raise ValueError(_("Enter a valid time."))


def time_structure_nullable(val, _) -> TimeField | None:
    if val is None:
        return None
    return time_structure(val, _)


def time_unstructure(val: TimeField | None) -> datetime.time | None:
    if val is None:
        return None

    return val


def time_unstructure_str(val: TimeField | None) -> str | None:
    if val is None:
        return None
    return val.isoformat()
