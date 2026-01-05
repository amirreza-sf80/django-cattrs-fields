import math

from django.utils.regex_helper import _lazy_re_compile

from django_cattrs_fields.fields import (
    FloatField,
    IntegerField,
)
from django_cattrs_fields.validators import forbid_falsy_values_validator


# Integer hooks


def integer_structure(val, _) -> IntegerField:
    forbid_falsy_values_validator(val)
    return val


def integer_structure_nullable(val, _) -> IntegerField | None:
    if val is None:
        return None
    return integer_structure(val, _)


# django.forms.fields.IntegerField.re_decimal
re_decimal = _lazy_re_compile(r"\.0*\s*$")


def integer_unstructure(val: IntegerField | None) -> int | None:
    if val is None:
        return None

    try:
        v = int(re_decimal.sub("", str(val)))
    except (ValueError, TypeError) as e:
        raise ValueError from e

    return v


# Float hooks


def float_structure(val, _) -> FloatField:
    forbid_falsy_values_validator(val)
    try:
        val = float(val)
    except (ValueError, TypeError) as e:
        raise ValueError from e

    if not math.isfinite(val):
        raise ValueError("infinite values are not supported.")

    return val


def float_structure_nullable(val, _) -> FloatField | None:
    if val is None:
        return None
    return float_structure(val, _)


def float_unstructure(val: FloatField | None) -> float | None:
    if val is None:
        return None
    try:
        val = float(val)  # pyright: ignore[reportAssignmentType]
    except (ValueError, TypeError) as e:
        raise ValueError from e
    return val
