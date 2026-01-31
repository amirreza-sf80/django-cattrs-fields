import json
from decimal import Decimal
from typing import Annotated

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
from django_cattrs_fields.fields import DecimalField, IntegerField, FloatField, Params


@define
class PeopleNumbers:
    age: IntegerField
    salary: FloatField
    accurate_salary: DecimalField


@define
class PeopleNumbersAnnotated:
    age: IntegerField
    salary: FloatField
    accurate_salary: Annotated[DecimalField, Params(decimal_max_digits=5, decimal_places=3)]


@define
class PeopleNumbersNullable:
    age: IntegerField | None
    salary: FloatField | None
    accurate_salary: DecimalField | None


@define
class PeopleNumbersNullableAnnotated:
    age: IntegerField | None
    salary: FloatField | None
    accurate_salary: Annotated[DecimalField, Params(decimal_max_digits=5, decimal_places=3)] | None


def test_structure():
    pn = {"age": 25, "salary": 100.5, "accurate_salary": "10.5"}

    structure = converter.structure(pn, PeopleNumbers)
    pn["accurate_salary"] = Decimal(pn["accurate_salary"])
    obj = PeopleNumbers(**pn)

    assert structure == obj
    assert isinstance(structure.age, int)
    assert isinstance(structure.salary, float)
    assert isinstance(structure.accurate_salary, Decimal)


def test_structure_annotated():
    pn = {"age": 25, "salary": 100.5, "accurate_salary": "10.5"}

    structure = converter.structure(pn, PeopleNumbersAnnotated)
    pn["accurate_salary"] = Decimal(pn["accurate_salary"])
    obj = PeopleNumbersAnnotated(**pn)

    assert structure == obj
    assert isinstance(structure.age, int)
    assert isinstance(structure.salary, float)
    assert isinstance(structure.accurate_salary, Decimal)

    pn["accurate_salary"] = "100.12"
    with pytest.RaisesGroup(ValueError):
        converter.structure(pn, PeopleNumbersAnnotated)

    pn["accurate_salary"] = "10.1234"
    with pytest.RaisesGroup(ValueError):
        converter.structure(pn, PeopleNumbersAnnotated)


@pytest.mark.parametrize(
    "age, salary, accurate_salary", [(None, 43.1, None), (11, None, None), (None, None, "11.4")]
)
def test_structure_nullable(age, salary, accurate_salary):
    pn = {"age": age, "salary": salary, "accurate_salary": accurate_salary}

    structure = converter.structure(pn, PeopleNumbersNullable)
    if accurate_salary:
        pn["accurate_salary"] = Decimal(accurate_salary)
    obj = PeopleNumbersNullable(**pn)

    assert structure == obj

    assert isinstance(structure.age, int) or structure.age is None
    assert structure.salary is salary or isinstance(structure.salary, float)
    assert isinstance(structure.accurate_salary, Decimal) or structure.accurate_salary is None


@pytest.mark.parametrize(
    "age, salary, accurate_salary", [(None, 43.1, None), (11, None, None), (None, None, "11.4")]
)
def test_structure_nullable_annotated(age, salary, accurate_salary):
    pn = {"age": age, "salary": salary, "accurate_salary": accurate_salary}

    structure = converter.structure(pn, PeopleNumbersNullableAnnotated)
    if accurate_salary:
        pn["accurate_salary"] = Decimal(accurate_salary)
    obj = PeopleNumbersNullableAnnotated(**pn)

    assert structure == obj

    assert isinstance(structure.age, int) or structure.age is None
    assert structure.salary is salary or isinstance(structure.salary, float)
    assert isinstance(structure.accurate_salary, Decimal) or structure.accurate_salary is None

    pn["accurate_salary"] = "100.12"
    with pytest.RaisesGroup(ValueError):
        converter.structure(pn, PeopleNumbersNullableAnnotated)

    pn["accurate_salary"] = "10.1234"
    with pytest.RaisesGroup(ValueError):
        converter.structure(pn, PeopleNumbersNullableAnnotated)


@pytest.mark.parametrize(
    "age, salary, accurate_salary", [(None, 43.1, "11.4"), (11, 12.1, None), (11.3, None, "11.4")]
)
def test_structure_null_with_not_nullable_raises(age, salary, accurate_salary):
    pn = {"age": age, "salary": salary, "accurate_salary": accurate_salary}
    with pytest.RaisesGroup(ValueError):
        converter.structure(pn, PeopleNumbers)


def test_unstructure():
    pn = {"age": 25, "salary": 100.5, "accurate_salary": "11.4"}
    structure = converter.structure(pn, PeopleNumbers)

    unstructure = converter.unstructure(structure)

    pn["accurate_salary"] = Decimal(pn["accurate_salary"])
    assert unstructure == pn

    assert isinstance(unstructure["age"], int)
    assert isinstance(unstructure["salary"], float)
    assert isinstance(unstructure["accurate_salary"], Decimal)


def test_unstructure_annotated():
    pn = {"age": 25, "salary": 100.5, "accurate_salary": "11.4"}
    structure = converter.structure(pn, PeopleNumbersAnnotated)

    unstructure = converter.unstructure(structure)

    pn["accurate_salary"] = Decimal(pn["accurate_salary"])
    assert unstructure == pn

    assert isinstance(unstructure["age"], int)
    assert isinstance(unstructure["salary"], float)
    assert isinstance(unstructure["accurate_salary"], Decimal)


@pytest.mark.parametrize(
    "age, salary, accurate_salary", [(None, 43.1, None), (11, None, None), (None, None, "43.1")]
)
def test_unstructure_nullable(age, salary, accurate_salary):
    pn = {"age": age, "salary": salary, "accurate_salary": accurate_salary}
    structure = converter.structure(pn, PeopleNumbersNullable)
    unstructure = converter.unstructure(structure)

    if accurate_salary:
        accurate_salary = Decimal(accurate_salary)
        pn["accurate_salary"] = accurate_salary
    assert unstructure == pn

    assert isinstance(unstructure["age"], int) or unstructure["age"] is None
    assert unstructure["salary"] is salary or unstructure["salary"] == salary
    assert (
        unstructure["accurate_salary"] is accurate_salary
        or unstructure["accurate_salary"] == accurate_salary
    )


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
    pn = {"age": 25, "salary": 100.5, "accurate_salary": "11.1"}
    structure = converter.structure(pn, PeopleNumbers)
    if converter in {cbor2_converter}:
        pn["accurate_salary"] = Decimal(pn["accurate_salary"])

    dump = converter.dumps(structure)

    assert dump == dumps(pn)


@pytest.mark.parametrize(
    "age, salary, accurate_salary", [(None, 43.1, None), (11, None, None), (None, None, "43.13")]
)
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
def test_dumps_nullable(converter, dumps, age, salary, accurate_salary):
    pn = {"age": age, "salary": salary, "accurate_salary": accurate_salary}
    structure = converter.structure(pn, PeopleNumbersNullable)

    dump = converter.dumps(structure)

    if accurate_salary:
        if converter in {cbor2_converter}:
            pn["accurate_salary"] = Decimal(accurate_salary)
    assert dump == dumps(pn)


@pytest.mark.parametrize("age, salary, accurate_salary", [(43, 43.1, "12.32"), (11, 11, 21)])
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
def test_loads(converter, dumps, age, salary, accurate_salary):
    pn = {"age": age, "salary": salary, "accurate_salary": accurate_salary}
    dump = dumps(pn)

    x = converter.loads(dump, PeopleNumbers)
    pn["accurate_salary"] = pn["accurate_salary"]

    pn["accurate_salary"] = Decimal(pn["accurate_salary"])
    assert x == PeopleNumbers(**pn)


@pytest.mark.parametrize(
    "age, salary, accurate_salary", [(None, 43.1, None), (11, None, None), (None, None, "13.11")]
)
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
def test_loads_nullable(converter, dumps, age, salary, accurate_salary):
    pn = {"age": age, "salary": salary, "accurate_salary": accurate_salary}
    dump = dumps(pn)

    x = converter.loads(dump, PeopleNumbersNullable)

    if accurate_salary:
        pn["accurate_salary"] = Decimal(accurate_salary)
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
    pn = {"age": 25, "salary": 100.5, "accurate_salary": "12.43"}
    structure = converter.structure(pn, PeopleNumbers)

    dump = converter.dumps(structure)
    load = converter.loads(dump, PeopleNumbers)

    if converter in {msgspec_converter, cbor2_converter}:
        pn["accurate_salary"] = Decimal(pn["accurate_salary"])
    assert converter.unstructure(load) == pn


@pytest.mark.parametrize(
    "age, salary, accurate_salary", [(None, 43.1, None), (11, None, None), (None, None, "12.11")]
)
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
def test_dump_then_load_nullable(converter, age, salary, accurate_salary):
    pn = {"age": age, "salary": salary, "accurate_salary": accurate_salary}
    structure = converter.structure(pn, PeopleNumbersNullable)

    dump = converter.dumps(structure)
    load = converter.loads(dump, PeopleNumbersNullable)

    if converter in {msgspec_converter, cbor2_converter}:
        if accurate_salary:
            pn["accurate_salary"] = Decimal(accurate_salary)
    assert converter.unstructure(load) == pn
