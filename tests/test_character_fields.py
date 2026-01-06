import json
import uuid

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
from django_cattrs_fields.fields import (
    CharField,
    EmailField,
    SlugField,
    URLField,
    UUIDField,
)


@define
class Worker:
    name: CharField
    email: EmailField
    slug: SlugField
    website: URLField
    unique_id: UUIDField


@define
class WorkerNullable:
    name: CharField | None
    email: EmailField | None
    slug: SlugField | None
    website: URLField | None
    unique_id: UUIDField | None


def test_structure():
    w = {
        "name": "bob",
        "email": "bob@email.com",
        "slug": "bo-b",
        "website": "https://bob.com",
        "unique_id": uuid.uuid4(),
    }

    structure = converter.structure(w, Worker)

    obj = Worker(**w)

    assert structure == obj
    assert isinstance(structure.name, str)
    assert isinstance(structure.email, str)
    assert isinstance(structure.slug, str)
    assert isinstance(structure.website, str)
    assert isinstance(structure.unique_id, uuid.UUID)


def test_structure_invalid_name():
    w = {
        "name": 1,
        "email": "bob@email.com",
        "slug": "bo-b",
        "website": "https://bob.com",
        "unique_id": uuid.uuid4(),
    }

    with pytest.RaisesGroup(ValueError) as exp:
        converter.structure(w, Worker)
    assert str(exp.value.exceptions[0]) == "value should be a string object"


def test_structure_invalid_email():
    w = {
        "name": "bob",
        "email": "bob@email",
        "slug": "bo-b",
        "website": "https://bob.com",
        "unique_id": uuid.uuid4(),
    }

    with pytest.RaisesGroup(ValueError) as exp:
        converter.structure(w, Worker)
    assert str(exp.value.exceptions[0]) == "Enter a valid email address."


def test_structure_invalid_slug():
    w = {
        "name": "bob",
        "email": "bob@email.com",
        "slug": "bo b",
        "website": "https://bob.com",
        "unique_id": uuid.uuid4(),
    }

    with pytest.RaisesGroup(ValueError) as exp:
        converter.structure(w, Worker)
    assert (
        str(exp.value.exceptions[0])
        == "Enter a valid “slug” consisting of Unicode letters, numbers, underscores, or hyphens."  # noqa: E501
    )


def test_structure_invalid_website():
    w = {
        "name": "bob",
        "email": "bob@email.com",
        "slug": "bo-b",
        "website": "://bob.com",
        "unique_id": uuid.uuid4(),
    }

    with pytest.RaisesGroup(ValueError) as exp:
        converter.structure(w, Worker)
    assert str(exp.value.exceptions[0]) == "Enter a valid URL."


def test_structure_invalid_uuid():
    w = {
        "name": "bob",
        "email": "bob@email.com",
        "slug": "bo-b",
        "website": "https://bob.com",
        "unique_id": "sfa",
    }

    with pytest.RaisesGroup(ValueError) as exp:
        converter.structure(w, Worker)
    assert str(exp.value.exceptions[0]) == "badly formed hexadecimal UUID string"


def test_structure_invalid_null():
    w = {
        "name": None,
        "email": None,
        "slug": None,
        "website": None,
        "unique_id": None,
    }
    with pytest.RaisesGroup(ValueError, ValueError, ValueError, ValueError, ValueError) as exp:
        converter.structure(w, Worker)
    assert len(exp.value.exceptions) == 5
    for e in exp.value.exceptions:
        assert str(e) == "falsy values are not allowed"


@pytest.mark.parametrize("name", ["bob", None])
@pytest.mark.parametrize("email", ["bob@email.com", None])
@pytest.mark.parametrize("slug", ["bo-b", None])
@pytest.mark.parametrize("website", ["https://bob.com", None])
@pytest.mark.parametrize("unique_id", [uuid.uuid4(), None])
def test_structure_nullable(name, email, slug, website, unique_id):
    w = {
        "name": name,
        "email": email,
        "slug": slug,
        "website": website,
        "unique_id": unique_id,
    }

    structure = converter.structure(w, WorkerNullable)
    obj = WorkerNullable(**w)

    assert structure == obj

    assert structure.name is None or isinstance(structure.name, str)
    assert structure.email is None or isinstance(structure.email, str)
    assert structure.slug is None or isinstance(structure.slug, str)
    assert structure.website is None or isinstance(structure.website, str)
    assert structure.unique_id is None or isinstance(structure.unique_id, uuid.UUID)


def test_unstructure():
    w = {
        "name": "bob",
        "email": "bob@email.com",
        "slug": "bo-b",
        "website": "https://bob.com",
        "unique_id": uuid.uuid4(),
    }

    structure = converter.structure(w, Worker)

    unstructure = converter.unstructure(structure)

    assert unstructure == w


@pytest.mark.parametrize("name", ["bob", None])
@pytest.mark.parametrize("email", ["bob@email.com", None])
@pytest.mark.parametrize("slug", ["bo-b", None])
@pytest.mark.parametrize("website", ["https://bob.com", None])
@pytest.mark.parametrize("unique_id", [uuid.uuid4(), None])
def test_unstructure_nullable(name, email, slug, website, unique_id):
    w = {
        "name": name,
        "email": email,
        "slug": slug,
        "website": website,
        "unique_id": unique_id,
    }

    structure = converter.structure(w, WorkerNullable)

    unstructure = converter.unstructure(structure)

    assert unstructure == w

    assert unstructure["name"] is None or isinstance(structure.name, str)
    assert unstructure["email"] is None or isinstance(structure.email, str)
    assert unstructure["slug"] is None or isinstance(structure.slug, str)
    assert unstructure["website"] is None or isinstance(structure.website, str)
    assert unstructure["unique_id"] is None or isinstance(structure.unique_id, uuid.UUID)


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
    w = {
        "name": "bob",
        "email": "bob@email.com",
        "slug": "bo-b",
        "website": "https://bob.com",
        "unique_id": str(uuid.uuid4()),
    }
    if converter is cbor2_converter or converter is bson_converter:
        w["unique_id"] = uuid.uuid4()  # pyright: ignore[reportArgumentType]

    structure = converter.structure(w, Worker)

    dump = converter.dumps(structure)

    if converter is bson_converter:
        w["unique_id"] = bson.Binary.from_uuid(w["unique_id"])

    assert dump == dumps(w)


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
def test_loads(converter, dumps):
    w = {
        "name": "bob",
        "email": "bob@email.com",
        "slug": "bo-b",
        "website": "https://bob.com",
        "unique_id": str(uuid.uuid4()),
    }
    if converter is cbor2_converter or converter is bson_converter:
        w["unique_id"] = uuid.uuid4()  # pyright: ignore[reportArgumentType]
        if converter is bson_converter:
            w["unique_id"] = bson.Binary.from_uuid(w["unique_id"])  # pyright: ignore[reportArgumentType]

    dump = dumps(w)

    x = converter.loads(dump, Worker)

    assert x == converter.structure(w, Worker)
    assert isinstance(x.unique_id, uuid.UUID)


@pytest.mark.parametrize("name", ["bob", None])
@pytest.mark.parametrize("email", ["bob@email.com", None])
@pytest.mark.parametrize("slug", ["bo-b", None])
@pytest.mark.parametrize("website", ["https://bob.com", None])
@pytest.mark.parametrize("unique_id", [uuid.uuid4(), None])
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
def test_loads_null(converter, dumps, name, email, slug, website, unique_id):
    w = {
        "name": name,
        "email": email,
        "slug": slug,
        "website": website,
        "unique_id": str(unique_id) if unique_id else None,
    }
    if converter is cbor2_converter:
        w["unique_id"] = unique_id  # pyright: ignore[reportArgumentType]
    if converter is bson_converter and unique_id:
        w["unique_id"] = bson.Binary.from_uuid(unique_id)

    dump = dumps(w)

    x = converter.loads(dump, WorkerNullable)

    assert x == converter.structure(w, WorkerNullable)


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
    w = {
        "name": "bob",
        "email": "bob@email.com",
        "slug": "bo-b",
        "website": "https://bob.com",
        "unique_id": str(uuid.uuid4()),
    }
    if converter is cbor2_converter or converter is bson_converter:
        w["unique_id"] = uuid.uuid4()  # pyright: ignore[reportArgumentType]
        if converter is bson_converter:
            w["unique_id"] = bson.Binary.from_uuid(w["unique_id"])  # pyright: ignore[reportArgumentType]

    structure = converter.structure(w, Worker)

    dump = converter.dumps(structure)
    load = converter.loads(dump, dict)

    assert load == w


@pytest.mark.parametrize("name", ["bob", None])
@pytest.mark.parametrize("email", ["bob@email.com", None])
@pytest.mark.parametrize("slug", ["bo-b", None])
@pytest.mark.parametrize("website", ["https://bob.com", None])
@pytest.mark.parametrize("unique_id", [uuid.uuid4(), None])
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
def test_dump_then_load_null(converter, name, email, slug, website, unique_id):
    w = {
        "name": name,
        "email": email,
        "slug": slug,
        "website": website,
        "unique_id": str(unique_id) if unique_id else None,
    }
    if converter is cbor2_converter or converter is bson_converter:
        w["unique_id"] = uuid.uuid4()  # pyright: ignore[reportArgumentType]
        if converter is bson_converter:
            w["unique_id"] = bson.Binary.from_uuid(w["unique_id"])  # pyright: ignore[reportArgumentType]

    structure = converter.structure(w, WorkerNullable)

    dump = converter.dumps(structure)
    x = converter.loads(dump, WorkerNullable)

    assert x == converter.structure(w, WorkerNullable)
