import json

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
from django_cattrs_fields.converters.bson import converter as bson_converter
from django_cattrs_fields.converters.cbor2 import converter as cbor2_converter
from django_cattrs_fields.converters.json import converter as json_converter
from django_cattrs_fields.converters.msgpack import converter as msgpack_converter
from django_cattrs_fields.converters.msgspec import converter as msgspec_converter
from django_cattrs_fields.converters.orjson import converter as orjson_converter
from django_cattrs_fields.converters.pyyaml import converter as pyyaml_converter
from django_cattrs_fields.converters.tomlkit import converter as tomlkit_converter
from django_cattrs_fields.converters.ujson import converter as ujson_converter
from django_cattrs_fields.fields import IntegerField, FloatField


@define
class PeopleNumbers:
    age: IntegerField
    salary: FloatField


@define
class PeopleNumbersNullable:
    age: IntegerField | None
    salary: FloatField | None


def test_structure():
    pn = {"age": 25, "salary": 100.5}

    structure = converter.structure(pn, PeopleNumbers)
    PeopleNumbers(age=4, salary=4.3)
    obj = PeopleNumbers(**pn)

    assert structure == obj
    assert isinstance(structure.age, int)

    assert isinstance(structure.salary, float)


@pytest.mark.parametrize("age, salary", [(None, 43.1), (11, None)])
def test_structure_nullable(age, salary):
    pn = {"age": age, "salary": salary}

    structure = converter.structure(pn, PeopleNumbersNullable)
    obj = PeopleNumbersNullable(**pn)

    assert structure == obj

    assert isinstance(structure.age, int) or structure.age is None

    assert structure.salary is salary or isinstance(structure.salary, float)


def test_structure_null_with_not_nullable_raises():
    pn = {"age": None, "salary": 123}
    with pytest.RaisesGroup(ValueError):
        converter.structure(pn, PeopleNumbers)


def test_unstructure():
    pn = {"age": 25, "salary": 100.5}
    structure = converter.structure(pn, PeopleNumbers)

    unstructure = converter.unstructure(structure)

    assert unstructure == pn

    assert isinstance(unstructure["age"], int)

    assert isinstance(unstructure["salary"], float)


@pytest.mark.parametrize("age, salary", [(None, 43.1), (11, None)])
def test_unstructure_nullable(age, salary):
    pn = {"age": age, "salary": salary}
    structure = converter.structure(pn, PeopleNumbersNullable)
    unstructure = converter.unstructure(structure)

    assert unstructure == pn

    assert isinstance(unstructure["age"], int) or unstructure["age"] is None

    assert unstructure["salary"] is salary or unstructure["salary"] == salary


@pytest.mark.parametrize(
    "converter, dumps",
    [
        (bson_converter, bson.encode),
        (cbor2_converter, cbor2.dumps),
        (json_converter, json.dumps),
        (msgpack_converter, msgpack.dumps),
        (msgspec_converter, msgspec_json.encode),
        (orjson_converter, orjson.dumps),
        (pyyaml_converter, yaml.safe_dump),
        (tomlkit_converter, tomlkit.dumps),
        (ujson_converter, ujson.dumps),
    ],
)
def test_dumps(converter, dumps):
    pn = {"age": 25, "salary": 100.5}
    structure = converter.structure(pn, PeopleNumbers)

    dump = converter.dumps(structure)

    assert dump == dumps(pn)


@pytest.mark.parametrize("age, salary", [(None, 43.1), (11, None)])
@pytest.mark.parametrize(
    "converter, dumps",
    [
        (bson_converter, bson.encode),
        (cbor2_converter, cbor2.dumps),
        (json_converter, json.dumps),
        (msgpack_converter, msgpack.dumps),
        (msgspec_converter, msgspec_json.encode),
        (orjson_converter, orjson.dumps),
        (pyyaml_converter, yaml.safe_dump),
        (ujson_converter, ujson.dumps),
    ],
)
def test_dumps_nullable(converter, dumps, age, salary):
    pn = {"age": age, "salary": salary}
    structure = converter.structure(pn, PeopleNumbersNullable)

    dump = converter.dumps(structure)

    assert dump == dumps(pn)


@pytest.mark.parametrize("age, salary", [(43, 43.1), (11, 11)])
@pytest.mark.parametrize(
    "converter, dumps",
    [
        (bson_converter, bson.encode),
        (cbor2_converter, cbor2.dumps),
        (json_converter, json.dumps),
        (msgpack_converter, msgpack.dumps),
        (msgspec_converter, msgspec_json.encode),
        (orjson_converter, orjson.dumps),
        (pyyaml_converter, yaml.safe_dump),
        (tomlkit_converter, tomlkit.dumps),
        (ujson_converter, ujson.dumps),
    ],
)
def test_loads(converter, dumps, age, salary):
    pn = {"age": age, "salary": salary}
    dump = dumps(pn)

    x = converter.loads(dump, PeopleNumbers)

    assert x == PeopleNumbers(**pn)


@pytest.mark.parametrize("age, salary", [(None, 43.1), (11, None)])
@pytest.mark.parametrize(
    "converter, dumps",
    [
        (bson_converter, bson.encode),
        (cbor2_converter, cbor2.dumps),
        (json_converter, json.dumps),
        (msgpack_converter, msgpack.dumps),
        (msgspec_converter, msgspec_json.encode),
        (orjson_converter, orjson.dumps),
        (pyyaml_converter, yaml.safe_dump),
        (ujson_converter, ujson.dumps),
    ],
)
def test_loads_nullable(converter, dumps, age, salary):
    pn = {"age": age, "salary": salary}
    dump = dumps(pn)

    x = converter.loads(dump, PeopleNumbersNullable)

    assert x == PeopleNumbersNullable(**pn)
    assert x.salary is salary or x.salary == salary


@pytest.mark.parametrize(
    "converter",
    [
        (bson_converter),
        (cbor2_converter),
        (json_converter),
        (msgpack_converter),
        (msgspec_converter),
        (orjson_converter),
        (pyyaml_converter),
        (tomlkit_converter),
        (ujson_converter),
    ],
)
def test_dump_then_load(converter):
    pn = {"age": 25, "salary": 100.5}
    structure = converter.structure(pn, PeopleNumbers)

    dump = converter.dumps(structure)
    load = converter.loads(dump, dict)

    assert load == pn


@pytest.mark.parametrize("age, salary", [(None, 43.1), (11, None)])
@pytest.mark.parametrize(
    "converter",
    [
        (bson_converter),
        (cbor2_converter),
        (json_converter),
        (msgpack_converter),
        (msgspec_converter),
        (orjson_converter),
        (pyyaml_converter),
        (ujson_converter),
    ],
)
def test_dump_then_load_nullable(converter, age, salary):
    pn = {"age": age, "salary": salary}
    structure = converter.structure(pn, PeopleNumbersNullable)

    dump = converter.dumps(structure)
    load = converter.loads(dump, dict)

    assert load == pn
