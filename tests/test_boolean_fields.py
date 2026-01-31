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
from django_cattrs_fields.converters.bson import serializer as bson_serializer
from django_cattrs_fields.converters.cbor2 import serializer as cbor2_serializer
from django_cattrs_fields.converters.json import serializer as json_serializer
from django_cattrs_fields.converters.msgpack import serializer as msgpack_serializer
from django_cattrs_fields.converters.msgspec import serializer as msgspec_serializer
from django_cattrs_fields.converters.orjson import serializer as orjson_serializer
from django_cattrs_fields.converters.pyyaml import serializer as pyyaml_serializer
from django_cattrs_fields.converters.tomlkit import serializer as tomlkit_serializer
from django_cattrs_fields.converters.ujson import serializer as ujson_serializer
from django_cattrs_fields.fields import BooleanField


@define
class Graduation:
    graduated: BooleanField


@define
class GraduationNullable:
    graduated: BooleanField | None


@pytest.mark.parametrize("b", [True, False])
def test_structure(b):
    g = {"graduated": b}

    structure = converter.structure(g, Graduation)
    obj = Graduation(graduated=b)

    assert structure == obj
    assert isinstance(structure.graduated, bool)


def test_structure_nullable():
    g = {"graduated": None}

    structure = converter.structure(g, GraduationNullable)
    obj = GraduationNullable(graduated=None)

    assert structure == obj
    assert structure.graduated is None

    g2 = {"graduated": True}
    structure = converter.structure(g2, GraduationNullable)
    obj = GraduationNullable(graduated=True)

    assert structure == obj


def test_structure_null_with_not_nullable_raises():
    g = {"graduated": None}

    with pytest.RaisesGroup(ValueError):
        converter.structure(g, Graduation)


@pytest.mark.parametrize("b", [True, False])
def test_unstructure(b):
    g = {"graduated": b}
    structure = converter.structure(g, Graduation)

    unstructure = converter.unstructure(structure)

    assert unstructure == g

    assert isinstance(unstructure["graduated"], bool)


def test_unstructure_nullable():
    g = {"graduated": None}
    structure = converter.structure(g, GraduationNullable)

    unstructure = converter.unstructure(structure)

    assert unstructure == g

    assert unstructure["graduated"] is None


@pytest.mark.parametrize(
    "converter, dumps",
    [
        (bson_serializer, bson.encode),
        (cbor2_serializer, cbor2.dumps),
        (json_serializer, json.dumps),
        (msgpack_serializer, msgpack.dumps),
        (msgspec_serializer, msgspec_json.encode),
        (orjson_serializer, orjson.dumps),
        (pyyaml_serializer, yaml.safe_dump),
        (tomlkit_serializer, tomlkit.dumps),
        (ujson_serializer, ujson.dumps),
    ],
)
def test_dumps(converter, dumps):
    g = {"graduated": True}
    structure = converter.structure(g, Graduation)

    dump = converter.dumps(structure)

    assert dump == dumps(g)


@pytest.mark.parametrize(
    "converter, dumps",
    [
        (bson_serializer, bson.encode),
        (cbor2_serializer, cbor2.dumps),
        (json_serializer, json.dumps),
        (msgpack_serializer, msgpack.dumps),
        (msgspec_serializer, msgspec_json.encode),
        (orjson_serializer, orjson.dumps),
        (pyyaml_serializer, yaml.safe_dump),
        (ujson_serializer, ujson.dumps),
    ],
)
def test_dumps_null(converter, dumps):
    g = {"graduated": None}
    structure = converter.structure(g, GraduationNullable)

    dump = converter.dumps(structure)

    assert dump == dumps(g)


@pytest.mark.parametrize(
    "converter, dumps",
    [
        (bson_serializer, bson.encode),
        (cbor2_serializer, cbor2.dumps),
        (json_serializer, json.dumps),
        (msgpack_serializer, msgpack.dumps),
        (msgspec_serializer, msgspec_json.encode),
        (orjson_serializer, orjson.dumps),
        (pyyaml_serializer, yaml.safe_dump),
        (tomlkit_serializer, tomlkit.dumps),
        (ujson_serializer, ujson.dumps),
    ],
)
def test_loads(converter, dumps):
    g = {"graduated": True}
    dump = dumps(g)

    x = converter.loads(dump, Graduation)

    assert x == converter.structure(g, Graduation)


@pytest.mark.parametrize(
    "converter, dumps",
    [
        (bson_serializer, bson.encode),
        (cbor2_serializer, cbor2.dumps),
        (json_serializer, json.dumps),
        (msgpack_serializer, msgpack.dumps),
        (msgspec_serializer, msgspec_json.encode),
        (orjson_serializer, orjson.dumps),
        (pyyaml_serializer, yaml.safe_dump),
        (ujson_serializer, ujson.dumps),
    ],
)
def test_loads_null(converter, dumps):
    g = {"graduated": None}
    dump = dumps(g)

    x = converter.loads(dump, GraduationNullable)

    assert x == converter.structure(g, GraduationNullable)


@pytest.mark.parametrize(
    "converter",
    [
        (bson_serializer),
        (cbor2_serializer),
        (json_serializer),
        (msgpack_serializer),
        (msgspec_serializer),
        (orjson_serializer),
        (pyyaml_serializer),
        (tomlkit_serializer),
        (ujson_serializer),
    ],
)
def test_dump_then_load(converter):
    g = {"graduated": True}
    structure = converter.structure(g, Graduation)

    dump = converter.dumps(structure)
    load = converter.loads(dump, dict)

    assert load == g


@pytest.mark.parametrize(
    "converter",
    [
        (bson_serializer),
        (cbor2_serializer),
        (json_serializer),
        (msgpack_serializer),
        (msgspec_serializer),
        (orjson_serializer),
        (pyyaml_serializer),
        (ujson_serializer),
    ],
)
def test_dump_then_load_null(converter):
    g = {"graduated": None}
    structure = converter.structure(g, GraduationNullable)

    dump = converter.dumps(structure)
    load = converter.loads(dump, dict)

    assert load == g
