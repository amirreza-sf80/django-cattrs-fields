from typing import (
    Dict,
    List,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    TypedDict,
)

from attrs import Factory, define, field
from pytest import fixture, raises

from cattrs import Converter
from cattrs._compat import Mapping
from cattrs.errors import IterableValidationError
from cattrs.gen import make_dict_structure_fn
from cattrs.v import format_exception

from django_cattrs_fields import transform_error


@fixture
def c() -> Converter:
    """We need only converters with detailed_validation=True."""
    return Converter(detailed_validation=True)


def test_attribute_errors(c: Converter) -> None:
    @define
    class C:
        a: int
        b: int = 0

    try:
        c.structure({}, C)
    except Exception as exc:
        assert transform_error(exc) == {"a": "required field missing"}

    try:
        c.structure({"a": 1, "b": "str"}, C)
    except Exception as exc:
        assert transform_error(exc) == {"b": "invalid value for type, expected int"}

    @define
    class D:
        c: C

    try:
        c.structure({}, D)
    except Exception as exc:
        assert transform_error(exc) == {"c": "required field missing"}

    try:
        c.structure({"c": {}}, D)
    except Exception as exc:
        assert transform_error(exc) == {"c.a": "required field missing"}

    try:
        c.structure({"c": 1}, D)
    except Exception as exc:
        assert transform_error(exc) == {"c": "invalid value for type, expected C"}

    try:
        c.structure({"c": {"a": "str"}}, D)
    except Exception as exc:
        assert transform_error(exc) == {"c.a": "invalid value for type, expected int"}

    @define
    class E:
        a: Optional[int]

    with raises(Exception) as exc:
        c.structure({"a": "str"}, E)

    # Complicated due to various Python versions.
    tn = Optional[int].__name__ if hasattr(Optional[int], "__name__") else repr(Optional[int])
    assert transform_error(exc.value) == {"a": f"invalid value for type, expected {tn}"}


def test_class_errors(c: Converter) -> None:
    """Errors not directly related to attributes are parsed correctly."""

    @define
    class C:
        a: int
        b: int = 0

    c.register_structure_hook(C, make_dict_structure_fn(C, c, _cattrs_forbid_extra_keys=True))

    try:
        c.structure({"d": 1}, C)
    except Exception as exc:
        assert transform_error(exc, path="") == {
            "a": "required field missing",
            "$#0": "extra fields found (d)",
        }


def test_untyped_class_errors(c: Converter) -> None:
    """Errors on untyped attrs classes transform correctly."""

    @define
    class C:
        a = field()

    def struct_hook(v, __):
        if v == 0:
            raise ValueError()
        raise TypeError("wrong type")

    c.register_structure_hook_func(lambda t: t is None, struct_hook)

    with raises(Exception) as exc_info:
        c.structure({"a": 0}, C)

    assert transform_error(exc_info.value) == {"a": "invalid value"}

    with raises(Exception) as exc_info:
        c.structure({"a": 1}, C)

    assert transform_error(exc_info.value) == {"a": "invalid type (wrong type)"}


def test_sequence_errors(c: Converter) -> None:
    try:
        c.structure(["str", 1, "str"], List[int])
    except Exception as exc:
        assert transform_error(exc) == {
            "[0]": "invalid value for type, expected int",
            "[2]": "invalid value for type, expected int",
        }

    try:
        c.structure(1, List[int])
    except Exception as exc:
        assert transform_error(exc) == {"$": "invalid value for type, expected an iterable"}

    try:
        c.structure(["str", 1, "str"], Tuple[int, ...])
    except Exception as exc:
        assert transform_error(exc) == {
            "[0]": "invalid value for type, expected int",
            "[2]": "invalid value for type, expected int",
        }

    try:
        c.structure(["str", 1, "str"], Sequence[int])
    except Exception as exc:
        assert transform_error(exc) == {
            "[0]": "invalid value for type, expected int",
            "[2]": "invalid value for type, expected int",
        }

    try:
        c.structure(["str", 1, "str"], MutableSequence[int])
    except Exception as exc:
        assert transform_error(exc) == {
            "[0]": "invalid value for type, expected int",
            "[2]": "invalid value for type, expected int",
        }

    @define
    class C:
        a: List[int]
        b: List[List[int]] = Factory(list)

    try:
        c.structure({"a": ["str", 1, "str"]}, C)
    except Exception as exc:
        assert transform_error(exc) == {
            "a[0]": "invalid value for type, expected int",
            "a[2]": "invalid value for type, expected int",
        }

    try:
        c.structure({"a": [], "b": [[], ["str", 1, "str"]]}, C)
    except Exception as exc:
        assert transform_error(exc) == {
            "b[1][0]": "invalid value for type, expected int",
            "b[1][2]": "invalid value for type, expected int",
        }

    # IterableValidationErrors with subexceptions without notes
    exc = IterableValidationError("Test", [TypeError("Test")], list[str])

    assert transform_error(exc) == {"$#0": "invalid type (Test)"}


def test_mapping_errors(c: Converter) -> None:
    try:
        c.structure({"a": 1, "b": "str"}, Dict[str, int])
    except Exception as exc:
        assert transform_error(exc) == {"['b']": "invalid value for type, expected int"}

    @define
    class C:
        a: Dict[str, int]

    try:
        c.structure({"a": {"a": "str", "b": 1, "c": "str"}}, C)
    except Exception as exc:
        assert transform_error(exc) == {
            "a['a']": "invalid value for type, expected int",
            "a['c']": "invalid value for type, expected int",
        }

    try:
        c.structure({"a": 1}, C)
    except Exception as exc:
        assert transform_error(exc) == {"a": "expected a mapping"}

    try:
        c.structure({"a": 1, "b": "str"}, Mapping[str, int])
    except Exception as exc:
        assert transform_error(exc) == {"['b']": "invalid value for type, expected int"}

    try:
        c.structure({"a": 1, "b": "str"}, MutableMapping[str, int])
    except Exception as exc:
        assert transform_error(exc) == {"['b']": "invalid value for type, expected int"}

    try:
        c.structure({"a": 1, 2: "str"}, MutableMapping[int, int])
    except Exception as exc:
        assert transform_error(exc) == {
            "['a']": "invalid value for type, expected int",
            "[2]": "invalid value for type, expected int",
        }


def test_custom_error_fn(c: Converter) -> None:
    def my_format(exc, type):
        if isinstance(exc, KeyError):
            return "no key"
        return format_exception(exc, type)

    @define
    class C:
        a: int
        b: int = 1

    try:
        c.structure({"b": "str"}, C)
    except Exception as exc:
        assert transform_error(exc, format_exception=my_format) == {
            "a": "no key",
            "b": "invalid value for type, expected int",
        }


def test_custom_error_fn_nested(c: Converter) -> None:
    def my_format(exc, type):
        if isinstance(exc, TypeError):
            return "Must be correct type"
        return format_exception(exc, type)

    @define
    class C:
        a: Dict[str, int]

    try:
        c.structure({"a": {"a": "str", "b": 1, "c": None}}, C)
    except Exception as exc:
        assert transform_error(exc, format_exception=my_format) == {
            "a['a']": "invalid value for type, expected int",
            "a['c']": "Must be correct type",
        }


def test_typeddict_attribute_errors(c: Converter) -> None:
    """TypedDict errors are correctly generated."""

    class C(TypedDict):
        a: int
        b: int

    try:
        c.structure({}, C)
    except Exception as exc:
        assert transform_error(exc) == {
            "a": "required field missing",
            "b": "required field missing",
        }

    try:
        c.structure({"b": 1}, C)
    except Exception as exc:
        assert transform_error(exc) == {"a": "required field missing"}

    try:
        c.structure({"a": 1, "b": "str"}, C)
    except Exception as exc:
        assert transform_error(exc) == {"b": "invalid value for type, expected int"}

    class D(TypedDict):
        c: C

    try:
        c.structure({}, D)
    except Exception as exc:
        assert transform_error(exc) == {"c": "required field missing"}

    try:
        c.structure({"c": {}}, D)
    except Exception as exc:
        assert transform_error(exc) == {
            "c.a": "required field missing",
            "c.b": "required field missing",
        }

    try:
        c.structure({"c": 1}, D)
    except Exception as exc:
        assert transform_error(exc) == {"c#0": "invalid type (expected a mapping, not int)"}
    try:
        c.structure({"c": {"a": "str"}}, D)
    except Exception as exc:
        assert transform_error(exc) == {
            "c.a": "invalid value for type, expected int",
            "c.b": "required field missing",
        }

    class E(TypedDict):
        a: Optional[int]

    with raises(Exception) as exc:
        c.structure({"a": "str"}, E)

    # Complicated due to various Python versions.
    tn = Optional[int].__name__ if hasattr(Optional[int], "__name__") else repr(Optional[int])
    assert transform_error(exc.value) == {"a": f"invalid value for type, expected {tn}"}


def test_other_errors():
    """Errors without explicit support transform predictably."""
    assert format_exception(IndexError("Test"), List[int]) == "unknown error (Test)"
