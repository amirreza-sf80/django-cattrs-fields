from django.core import validators
from django.core.exceptions import ValidationError


def forbid_falsy_values_validator(val):
    if not val:
        raise ValueError("falsy values are not allowed")


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
