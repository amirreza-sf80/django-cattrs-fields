from django.core import validators
from django.core.exceptions import ValidationError


def forbid_falsy_values_validator(val):
    if not val:
        raise ValueError("falsy values are not allowed")


def forbid_falsy_numbers(val):
    """since 0 is a valid value for numeric fields to have, a simple `not` check doesn't work."""
    if not val and (val != 0 or val is False):
        raise ValueError("value is required")


def null_char_validator(val):
    forbid_falsy_values_validator(val)
    try:
        validators.ProhibitNullCharactersValidator()(val)
    except ValidationError as e:
        raise ValueError(e.message)


def char_field_validation(val):
    null_char_validator(val)
    if not isinstance(val, str):
        raise ValueError("value should be a string object")


def slug_field_validation(val):
    char_field_validation(val)
    try:
        validators.validate_unicode_slug(val)
    except ValidationError as e:
        raise ValueError(e.message)
