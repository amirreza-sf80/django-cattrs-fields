from django.forms import model_to_dict
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from decimal import Decimal

import pytest

from attrs import define

import bson
import cbor2
import msgpack
import orjson
import ujson
import yaml
import tomlkit

from msgspec import json as msgspec_json

from django_cattrs_fields.converters import converter
from django_cattrs_fields.converters.bson import serializer as bson_serializer
from django_cattrs_fields.converters.cbor2 import serializer as cbor2_serializer
from django_cattrs_fields.converters.json import serializer as json_serializer
from django_cattrs_fields.converters.msgpack import serializer as msgpack_serializer
from django_cattrs_fields.converters.msgspec import serializer as msgspec_serializer
from django_cattrs_fields.converters.orjson import serializer as orjson_serializer
from django_cattrs_fields.converters.pyyaml import serializer as pyyaml_serializer
from django_cattrs_fields.converters.tomlkit import serializer as tomlkit_serializer
from django_cattrs_fields.converters.ujson import serializer as ujson_serializer
from django_cattrs_fields.fields import CharField, DecimalField, IntegerField
from django_cattrs_fields.fields.files import FileField

from tests.books.models import Book


@define
class Food:
    name: CharField
    price: DecimalField
    rate: IntegerField


@define
class BookData:
    pdf: FileField


@pytest.fixture
def create_books(db):
    for i in range(10):
        Book.objects.create(
            pdf=SimpleUploadedFile(
                name=f"test_image{i}.jpeg", content=b"wheeeee", content_type="image/jpeg"
            )
        )


def test_structure():
    data = [
        {"name": "pizza", "price": "13.25", "rate": 4},
        {"name": "burger", "price": "10.33", "rate": 5},
        {"name": "fried chicken", "price": "15.11", "rate": 5},
    ]

    structure = converter.structure(data, list[Food])
    man = [converter.structure(i, Food) for i in data]

    assert structure == man
    assert isinstance(structure[0], Food)


def test_structure_model(create_books):
    data = Book.objects.all()

    structure = converter.structure(data, list[BookData])
    man = [converter.structure(model_to_dict(d), BookData) for d in data]

    assert structure == man


def test_unstructure():
    data = [
        {"name": "pizza", "price": Decimal("13.25"), "rate": 4},
        {"name": "burger", "price": Decimal("10.33"), "rate": 5},
        {"name": "fried chicken", "price": Decimal("15.11"), "rate": 5},
    ]

    structure = converter.structure(data, list[Food])

    assert converter.unstructure(structure, list) == data


def test_unstructure_model(create_books):
    data = Book.objects.all()

    structure = converter.structure(data, list[BookData])
    man = [converter.unstructure(s) for s in structure]

    assert converter.unstructure(structure, list) == man


@pytest.mark.parametrize(
    "converter, dumps",
    [
        pytest.param(bson_serializer, bson.encode, marks=pytest.mark.xfail),
        (cbor2_serializer, cbor2.dumps),
        (json_serializer, json.dumps),
        (msgpack_serializer, msgpack.dumps),
        (msgspec_serializer, msgspec_json.encode),
        (orjson_serializer, orjson.dumps),
        (pyyaml_serializer, yaml.safe_dump),
        pytest.param(tomlkit_serializer, tomlkit.dumps, marks=pytest.mark.xfail),
        (ujson_serializer, ujson.dumps),
    ],
)
def test_dumps(converter, dumps):
    data = [
        {"name": "pizza", "price": "13.25", "rate": 4},
        {"name": "burger", "price": "10.33", "rate": 5},
        {"name": "fried chicken", "price": "15.11", "rate": 5},
    ]

    structure = converter.structure(data, list[Food])

    if converter in {cbor2_serializer}:
        for i in data:
            i["price"] = Decimal(i["price"])

    dump = converter.dumps(structure)

    assert dump == dumps(data)


@pytest.mark.parametrize(
    "converter, dumps",
    [
        pytest.param(bson_serializer, bson.encode, marks=pytest.mark.xfail),
        (cbor2_serializer, cbor2.dumps),
        (json_serializer, json.dumps),
        (msgpack_serializer, msgpack.dumps),
        (msgspec_serializer, msgspec_json.encode),
        (orjson_serializer, orjson.dumps),
        (pyyaml_serializer, yaml.safe_dump),
        pytest.param(tomlkit_serializer, tomlkit.dumps, marks=pytest.mark.xfail),
        (ujson_serializer, ujson.dumps),
    ],
)
def test_loads(converter, dumps):
    data = [
        {"name": "pizza", "price": "13.25", "rate": 4},
        {"name": "burger", "price": "10.33", "rate": 5},
        {"name": "fried chicken", "price": "15.11", "rate": 5},
    ]
    dump = dumps(data)

    x = converter.loads(dump, list[Food])
    man = [converter.structure(i, Food) for i in data]

    assert x == man
