import uuid

from django.core import validators
from django.core.exceptions import ValidationError

from django_cattrs_fields.fields import (
    CharField,
    EmailField,
    SlugField,
    UUIDField,
    URLField,
)
from django_cattrs_fields.validators import (
    null_char_validator,
    char_field_validation,
    slug_field_validation,
)


__all__ = (
    "char_structure",
    "char_structure_nullable",
    "char_unstructure",
    "email_structure",
    "email_structure_nullable",
    "email_unstructure",
    "slug_structure",
    "slug_structure_nullable",
    "slug_unstructure",
    "uuid_structure",
    "uuid_structure_nullable",
    "uuid_unstructure",
    "url_structure",
    "url_structure_nullable",
    "url_unstructure",
)

# Char hooks


def char_structure(val, _) -> CharField:
    char_field_validation(val)
    return val


def char_structure_nullable(val, _) -> CharField | None:
    if val is None:
        return None
    return char_structure(val, _)


def char_unstructure(val: CharField | None) -> str | None:
    return val


# Email hooks


def email_structure(val, _) -> EmailField:
    char_field_validation(val)
    try:
        validators.validate_email(val)
    except ValidationError as e:
        raise ValueError(e.message)
    return val


def email_structure_nullable(val, _) -> EmailField | None:
    if val is None:
        return None

    return email_structure(val, _)


def email_unstructure(val: EmailField | None) -> str | None:
    return val


# Slug hooks


def slug_structure(val, _) -> SlugField:
    slug_field_validation(val)
    return val


def slug_structure_nullable(val, _) -> SlugField | None:
    if val is None:
        return None
    return val


def slug_unstructure(val: SlugField | None) -> str | None:
    return val


# UUID hooks


def uuid_structure(val, _) -> UUIDField:
    null_char_validator(val)

    if isinstance(val, uuid.UUID):
        return val
    return uuid.UUID(val)


def uuid_structure_nullable(val, _) -> UUIDField | None:
    if val is None:
        return None
    return uuid_structure(val, _)


def uuid_unstructure(val: UUIDField | None) -> uuid.UUID | None:
    return val


# URL hooks


def url_structure(val, _) -> URLField:
    char_field_validation(val)
    try:
        validators.URLValidator()(val)
    except ValidationError as e:
        raise ValueError(e.message)

    return val


def url_structure_nullable(val, _) -> URLField | None:
    if val is None:
        return None

    return url_structure(val, _)


def url_unstructure(val: URLField | None) -> str | None:
    return val
