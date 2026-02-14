import pytest

from attrs import define

from django_cattrs_fields.converters import converter
from django_cattrs_fields.fields import CharField, IntegerField

from tests.books.models import Human


@define
class HumanData:
    name: CharField
    age: IntegerField


@pytest.fixture
def seed(db):
    for i in range(5):
        Human.objects.create(name=f"a{i}", age=i)


def test_structure(seed):
    data = Human.objects.get(id=1)

    struct = converter.structure(data, HumanData)

    man = converter.structure({"name": data.name, "age": data.age}, HumanData)

    assert struct == man
    assert isinstance(struct.name, str)
    assert struct.name == data.name


def test_unstructure(seed):
    data = Human.objects.get(id=1)

    struct = converter.structure(data, HumanData)

    assert converter.unstructure(struct) == {"name": data.name, "age": data.age}
