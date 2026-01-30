from collections.abc import Callable
from typing import Any

from cattrs.converters import Converter
from cattrs.gen import make_dict_unstructure_fn

from django_cattrs_fields.fields import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    Empty,
    EmptyField,
    FloatField,
    IntegerField,
    SlugField,
    TimeField,
    URLField,
    UUIDField,
)
from django_cattrs_fields.fields.files import FileField
from django_cattrs_fields.hooks.bool_hooks import (
    boolean_structure,
    boolean_structure_nullable,
    boolean_unstructure,
)
from django_cattrs_fields.hooks.char_hooks import (
    char_structure,
    char_structure_nullable,
    char_unstructure,
    email_structure,
    email_structure_nullable,
    email_unstructure,
    slug_structure,
    slug_structure_nullable,
    slug_unstructure,
    url_structure,
    url_structure_nullable,
    url_unstructure,
    uuid_structure,
    uuid_structure_nullable,
    uuid_unstructure,
)
from django_cattrs_fields.hooks.date_hooks import (
    date_structure,
    date_structure_nullable,
    date_unstructure,
    datetime_structure,
    datetime_structure_nullable,
    datetime_unstructure,
    time_structure,
    time_structure_nullable,
    time_unstructure,
)
from django_cattrs_fields.hooks.file_hooks import (
    file_structure,
    file_structure_nullable,
    file_unstructure,
)
from django_cattrs_fields.hooks.number_hooks import (
    decimal_structure,
    decimal_structure_nullable,
    decimal_unstructure,
    float_structure,
    float_structure_nullable,
    float_unstructure,
    integer_structure,
    integer_structure_nullable,
    integer_unstructure,
)


def skip_empty(cls: Any, converter: Converter) -> Callable[[Any], dict[str, Any]]:
    fn = make_dict_unstructure_fn(cls, converter)

    def unstructure(obj: Any) -> dict[str, Any]:
        data = fn(obj)
        return {k: v for k, v in data.items() if v is not Empty}

    return unstructure


## Structure


def empty_structure(val, _) -> EmptyField | Any:
    return val


# bool


def empty_bool_structure(val, _) -> EmptyField | BooleanField:
    if val is Empty:
        return Empty
    return boolean_structure(val, _)


def empty_bool_structure_nullable(val, _) -> EmptyField | BooleanField | None:
    if val is Empty:
        return Empty
    return boolean_structure_nullable(val, _)


# char


def empty_char_structure(val, _) -> EmptyField | CharField:
    if val is Empty:
        return Empty
    return char_structure(val, _)


def empty_char_structure_nullable(val, _) -> EmptyField | CharField | None:
    if val is Empty:
        return Empty
    return char_structure_nullable(val, _)


# email


def empty_email_structure(val, _) -> EmptyField | CharField:
    if val is Empty:
        return Empty
    return email_structure(val, _)


def empty_email_structure_nullable(val, _) -> EmptyField | CharField | None:
    if val is Empty:
        return Empty
    return email_structure_nullable(val, _)


# slug


def empty_slug_structure(val, _) -> EmptyField | SlugField:
    if val is Empty:
        return Empty
    return slug_structure(val, _)


def empty_slug_structure_nullable(val, _) -> EmptyField | SlugField | None:
    if val is Empty:
        return Empty
    return slug_structure_nullable(val, _)


# url


def empty_url_structure(val, _) -> EmptyField | URLField:
    if val is Empty:
        return Empty
    return url_structure(val, _)


def empty_url_structure_nullable(val, _) -> EmptyField | URLField | None:
    if val is Empty:
        return Empty
    return url_structure_nullable(val, _)


# uuid


def empty_uuid_structure(val, _) -> EmptyField | UUIDField:
    if val is Empty:
        return Empty
    return uuid_structure(val, _)


def empty_uuid_structure_nullable(val, _) -> EmptyField | UUIDField | None:
    if val is Empty:
        return Empty
    return uuid_structure_nullable(val, _)


# int


def empty_integer_structure(val, _) -> EmptyField | IntegerField:
    if val is Empty:
        return Empty
    return integer_structure(val, _)


def empty_integer_structure_nullable(val, _) -> EmptyField | IntegerField | None:
    if val is Empty:
        return Empty
    return integer_structure_nullable(val, _)


# decimal


def empty_decimal_structure(val, _) -> EmptyField | DecimalField:
    if val is Empty:
        return Empty
    return decimal_structure(val, _)


def empty_decimal_structure_nullable(val, _) -> EmptyField | DecimalField | None:
    if val is Empty:
        return Empty
    return decimal_structure_nullable(val, _)


# float


def empty_float_structure(val, _) -> EmptyField | FloatField:
    if val is Empty:
        return Empty
    return float_structure(val, _)


def empty_float_structure_nullable(val, _) -> EmptyField | FloatField | None:
    if val is Empty:
        return Empty
    return float_structure_nullable(val, _)


# date


def empty_date_structure(val, _) -> EmptyField | DateField:
    if val is Empty:
        return Empty
    return date_structure(val, _)


def empty_date_structure_nullable(val, _) -> EmptyField | DateField | None:
    if val is Empty:
        return Empty
    return date_structure_nullable(val, _)


# datetime


def empty_datetime_structure(val, _) -> EmptyField | DateTimeField:
    if val is Empty:
        return Empty
    return datetime_structure(val, _)


def empty_datetime_structure_nullable(val, _) -> EmptyField | DateTimeField | None:
    if val is Empty:
        return Empty
    return datetime_structure_nullable(val, _)


# time


def empty_time_structure(val, _) -> EmptyField | TimeField:
    if val is Empty:
        return Empty
    return time_structure(val, _)


def empty_time_structure_nullable(val, _) -> EmptyField | TimeField | None:
    if val is Empty:
        return Empty
    return time_structure_nullable(val, _)


# file


def empty_file_structure(val, _) -> EmptyField | FileField:
    if val is Empty:
        return Empty
    return file_structure(val, _)


def empty_file_structure_nullable(val, _) -> EmptyField | FileField | None:
    if val is Empty:
        return Empty
    return file_structure_nullable(val, _)


## Unstructure


def empty_unstructure(val: EmptyField | Any) -> EmptyField | Any:
    return val


# bool


def empty_bool_unstructure(val) -> EmptyField | BooleanField | None:
    if val is Empty:
        return Empty
    return boolean_unstructure(val)


# char


def empty_char_unstructure(val) -> EmptyField | CharField | None:
    if val is Empty:
        return Empty
    return char_unstructure(val)


# email


def empty_email_unstructure(val) -> EmptyField | CharField | None:
    if val is Empty:
        return Empty
    return email_unstructure(val)


# slug


def empty_slug_unstructure(val) -> EmptyField | SlugField | None:
    if val is Empty:
        return Empty
    return slug_unstructure(val)


# url


def empty_url_unstructure(val) -> EmptyField | URLField | None:
    if val is Empty:
        return Empty
    return url_unstructure(val)


# uuid


def empty_uuid_unstructure(val) -> EmptyField | UUIDField | None:
    if val is Empty:
        return Empty
    return uuid_unstructure(val)


# int


def empty_integer_unstructure(val) -> EmptyField | IntegerField | None:
    if val is Empty:
        return Empty
    return integer_unstructure(val)


# decimal


def empty_decimal_unstructure(val) -> EmptyField | DecimalField | None:
    if val is Empty:
        return Empty
    return decimal_unstructure(val)


# float


def empty_float_unstructure(val) -> EmptyField | FloatField | None:
    if val is Empty:
        return Empty
    return float_unstructure(val)


# date


def empty_date_unstructure(val) -> EmptyField | DateField | None:
    if val is Empty:
        return Empty
    return date_unstructure(val)


# datetime


def empty_datetime_unstructure(val) -> EmptyField | DateTimeField | None:
    if val is Empty:
        return Empty
    return datetime_unstructure(val)


# time


def empty_time_unstructure(val) -> EmptyField | TimeField | None:
    if val is Empty:
        return Empty
    return time_unstructure(val)


# file


def empty_file_unstructure(val) -> EmptyField | FileField | None:
    if val is Empty:
        return Empty
    return file_unstructure(val)
