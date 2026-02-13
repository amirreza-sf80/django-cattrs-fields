import importlib

import pytest

from attrs import define

from django_cattrs_fields import converters
from django_cattrs_fields.fields import (
    CharField,
    Empty,
    EmptyField,
    IntegerField,
)


@define
class WorkerPatch:
    age: IntegerField
    name: CharField | EmptyField = Empty


@pytest.fixture
def converter(settings):
    settings.DCF_EMPTY_HOOKS = True
    # need to reload to apply the new settings
    importlib.reload(converters)
    yield converters.converter


def test_structure(converter):
    w = {"name": "bob", "age": 32}

    struct = converter.structure(w, WorkerPatch)

    obj = WorkerPatch(**w)

    assert struct == obj

    assert isinstance(struct.name, str)
    assert isinstance(struct.age, int)

    w = {"age": 32}

    struct = converter.structure(w, WorkerPatch)

    obj = WorkerPatch(**w)

    assert struct == obj

    assert isinstance(struct.name, EmptyField)
    assert isinstance(struct.age, int)


def test_unstructure(converter):
    w = {"name": "bob", "age": 32}

    struct = converter.structure(w, WorkerPatch)

    unstruct = converter.unstructure(struct)

    assert unstruct == w

    w = {"age": 32}

    struct = converter.structure(w, WorkerPatch)

    unstruct = converter.unstructure(struct)

    assert unstruct == w
