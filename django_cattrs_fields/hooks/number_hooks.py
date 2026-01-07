import math
from decimal import Decimal, DecimalException
from typing import get_args

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.regex_helper import _lazy_re_compile

from django_cattrs_fields.fields import (
    DecimalField,
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


# Decimal hooks


def decimal_structure(val: str | Decimal, _, max_digits=None, decimal_places=None) -> DecimalField:
    forbid_falsy_values_validator(val)
    try:
        value = Decimal(val)
    except DecimalException:
        raise ValueError("Enter a number.")

    try:
        validators.DecimalValidator(max_digits=max_digits, decimal_places=decimal_places)(value)
    except ValidationError as e:
        raise ValueError(e.message)

    return value


def decimal_structure_annotated(val: str | Decimal, type) -> DecimalField:
    annotation = get_args(type)
    if len(annotation) > 1:
        max_digits: int | None = getattr(annotation[1], "decimal_max_digits", None)
        decimal_places: int | None = getattr(annotation[1], "decimal_places", None)
    else:
        max_digits = decimal_places = None

    return decimal_structure(val, type, max_digits=max_digits, decimal_places=decimal_places)


def decimal_structure_nullable(val, type) -> DecimalField | None:
    if val is None:
        return None
    return decimal_structure(val, type)


def decimal_unstructure(val: DecimalField | None) -> Decimal | None:
    if not val:
        return None
    return Decimal(val)


def decimal_unstructure_str(val: DecimalField | None) -> str | None:
    """some serializers can't handle decimals, convert to string in those cases"""
    if not val:
        return None
    return str(val.normalize())


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
