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
    g = {"graduated": True}
    structure = converter.structure(g, Graduation)

    dump = converter.dumps(structure)

    assert dump == dumps(g)


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
def test_dumps_null(converter, dumps):
    g = {"graduated": None}
    structure = converter.structure(g, GraduationNullable)

    dump = converter.dumps(structure)

    assert dump == dumps(g)


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
def test_loads(converter, dumps):
    g = {"graduated": True}
    dump = dumps(g)

    x = converter.loads(dump, Graduation)

    assert x == converter.structure(g, Graduation)


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
def test_loads_null(converter, dumps):
    g = {"graduated": None}
    dump = dumps(g)

    x = converter.loads(dump, GraduationNullable)

    assert x == converter.structure(g, GraduationNullable)


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
    g = {"graduated": True}
    structure = converter.structure(g, Graduation)

    dump = converter.dumps(structure)
    load = converter.loads(dump, dict)

    assert load == g


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
def test_dump_then_load_null(converter):
    g = {"graduated": None}
    structure = converter.structure(g, GraduationNullable)

    dump = converter.dumps(structure)
    load = converter.loads(dump, dict)

    assert load == g
