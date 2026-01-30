from attrs import define

from django_cattrs_fields.converters import converter
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


def test_structure():
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


def test_unstructure():
    w = {"name": "bob", "age": 32}

    struct = converter.structure(w, WorkerPatch)

    unstruct = converter.unstructure(struct)

    assert unstruct == w

    w = {"age": 32}

    struct = converter.structure(w, WorkerPatch)

    unstruct = converter.unstructure(struct)

    assert unstruct == w
