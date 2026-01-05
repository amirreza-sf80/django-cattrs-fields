from typing import Any


from django_cattrs_fields.fields import (
    BooleanField,
)

BOOLEAN_VALUES: dict[Any, bool] = {
    "t": True,
    "y": True,
    "yes": True,
    "true": True,
    "on": True,
    "1": True,
    1: True,
    "f": False,
    "n": False,
    "no": False,
    "false": False,
    "off": False,
    "0": False,
    0: False,
}

__all__ = (
    "boolean_structure",
    "boolean_structure_nullable",
    "boolean_unstructure",
    "BOOLEAN_VALUES",
)


def boolean_structure(val, _) -> BooleanField:
    try:
        val = BOOLEAN_VALUES[val]
    except KeyError as e:
        raise ValueError from e

    return val


def boolean_structure_nullable(val, _) -> BooleanField | None:
    if val is None:
        return None
    return boolean_structure(val, _)


def boolean_unstructure(val: BooleanField | None) -> bool | None:
    return val
