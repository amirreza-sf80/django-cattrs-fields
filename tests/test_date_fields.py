from datetime import date, datetime, time
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
from django_cattrs_fields.fields import DateField, DateTimeField, TimeField
from django_cattrs_fields.utils.timezone import enforce_timezone


@define
class Human:
    birth: DateField
    death: DateTimeField
    work_start: TimeField


@define
class HumanNullable:
    birth: DateField | None
    death: DateTimeField | None
    work_start: TimeField | None


def test_structure():
    d = datetime(year=2080, month=1, day=21)
    h = {
        "birth": date(year=2000, month=5, day=11),
        "death": d,
        "work_start": time(hour=9, minute=0, second=0),
    }

    structure = converter.structure(h, Human)

    h["death"] = enforce_timezone(d)
    obj = Human(**h)

    assert structure == obj
    assert isinstance(structure.birth, date)
    assert isinstance(structure.death, datetime)
    assert isinstance(structure.work_start, time)


@pytest.mark.parametrize("b", [date.today(), None])
@pytest.mark.parametrize("d", [datetime.now(), None])
@pytest.mark.parametrize("t", [time(hour=8), None])
def test_structure_nullable(b, d, t):
    h = {"birth": b, "death": d, "work_start": t}

    structure = converter.structure(h, HumanNullable)

    if h["death"]:
        h["death"] = enforce_timezone(d)
    obj = HumanNullable(**h)

    assert structure == obj


def test_structure_datetime_as_date_date_as_datetime_time_as_str():
    h = {
        "birth": datetime(year=2080, month=1, day=21),
        "death": date(year=2000, month=5, day=11),
        "work_start": time(8).strftime("%H:%M:%S"),
    }

    structure = converter.structure(h, Human)

    assert isinstance(structure.birth, date)
    assert isinstance(structure.death, datetime)
    assert isinstance(structure.work_start, time)


def test_structure_iso_format():
    b = date(year=2000, month=5, day=11)
    d = datetime(year=2080, month=1, day=21)
    t = time(9)
    h = {"birth": b.isoformat(), "death": d.isoformat(), "work_start": t.isoformat()}

    structure = converter.structure(h, Human)

    assert isinstance(structure.birth, date)
    assert isinstance(structure.death, datetime)
    assert isinstance(structure.work_start, time)
    assert structure.birth == b
    assert structure.death == enforce_timezone(d)
    assert structure.work_start == t


def test_unstructure():
    d = datetime(year=2080, month=1, day=21)
    h = {"birth": date(year=2000, month=5, day=11), "death": d, "work_start": time(8)}

    structure = converter.structure(h, Human)

    unstructure = converter.unstructure(structure)
    h["death"] = enforce_timezone(d)

    assert unstructure == h


@pytest.mark.parametrize(
    "b, d, t", [(date.today(), None, None), (None, datetime.now(), None), (None, None, time(7))]
)
def test_unstructure_nullable(b, d, t):
    h = {"birth": b, "death": d, "work_start": t}

    structure = converter.structure(h, HumanNullable)

    unstructure = converter.unstructure(structure)
    if h["death"]:
        h["death"] = enforce_timezone(d)

    assert unstructure == h


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
    b = date(year=2000, month=5, day=11)
    d = datetime(year=2080, month=1, day=21)
    t = time(5)
    h = {"birth": b, "death": d, "work_start": t}

    structure = converter.structure(h, Human)

    dump = converter.dumps(structure)

    if converter in {
        json_converter,
        msgpack_converter,
        ujson_converter,
        bson_converter,
    }:
        h["birth"] = b.isoformat()

    h["death"] = enforce_timezone(d)
    if converter in {
        json_converter,
        msgpack_converter,
        ujson_converter,
    }:
        h["death"] = h["death"].isoformat()

    if converter in {
        cbor2_converter,
        ujson_converter,
        msgpack_converter,
        bson_converter,
        json_converter,
        pyyaml_converter,
    }:
        h["work_start"] = h["work_start"].isoformat()

    assert dump == dumps(h)


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
@pytest.mark.parametrize(
    "b, d, t",
    [
        (date(year=2000, month=5, day=11), None, None),
        (None, datetime(year=2080, month=1, day=21), None),
        (None, None, time(5, 23)),
    ],
)
def test_dumps_nullable(converter, dumps, b, d, t):
    h = {"birth": b, "death": d, "work_start": t}

    structure = converter.structure(h, HumanNullable)

    dump = converter.dumps(structure)

    if converter in {
        json_converter,
        msgpack_converter,
        ujson_converter,
        bson_converter,
    }:
        if b:
            h["birth"] = b.isoformat()

    if d:
        h["death"] = enforce_timezone(d)
    if (
        converter
        in {
            json_converter,
            msgpack_converter,
            ujson_converter,
        }
        and d
    ):
        h["death"] = h["death"].isoformat()

    if (
        converter
        in {
            msgpack_converter,
            ujson_converter,
            bson_converter,
            json_converter,
            pyyaml_converter,
            cbor2_converter,
        }
        and t
    ):
        h["work_start"] = h["work_start"].isoformat()

    assert dump == dumps(h)


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
    b = date(year=2000, month=5, day=11)
    d = datetime(year=2080, month=1, day=21)
    t = time(13, 21)
    h = {"birth": b.isoformat(), "death": d.isoformat(), "work_start": t.isoformat()}

    dump = dumps(h)

    load = converter.loads(dump, Human)
    assert load == converter.structure(h, Human)


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
@pytest.mark.parametrize(
    "b, d, t",
    [
        (date(year=2000, month=5, day=11), None, None),
        (None, datetime(year=2080, month=1, day=21), None),
        (None, None, time(10, 44)),
    ],
)
def test_loads_nullable(converter, dumps, b, d, t):
    h = {
        "birth": b.isoformat() if b else None,
        "death": d.isoformat() if d else None,
        "work_start": t.isoformat() if t else None,
    }
    hc = {"birth": b if b else None, "death": d if d else None, "work_start": t if t else None}

    dump = dumps(h)

    load = converter.loads(dump, HumanNullable)
    assert load == converter.structure(h, HumanNullable)
    assert load == converter.structure(hc, HumanNullable)


@pytest.mark.parametrize(
    "converter",
    [
        pytest.param(
            bson_converter, marks=pytest.mark.xfail
        ),  # it seems bson fails to serializer datetime safely
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
    b = date(year=2000, month=5, day=11)
    d = datetime(year=2080, month=1, day=21, hour=2, minute=5)
    t = time(5, 11, 11)
    h = {"birth": b, "death": d, "work_start": t}

    structure = converter.structure(h, Human)

    dump = converter.dumps(structure)
    load = converter.loads(dump, Human)

    h["death"] = enforce_timezone(h["death"])

    assert load.birth == h["birth"]
    assert load.death == h["death"]
    assert load.work_start == h["work_start"]


@pytest.mark.parametrize(
    "converter",
    [
        pytest.param(
            bson_converter, marks=pytest.mark.xfail
        ),  # it seems bson fails to work datetime safely
        (cbor2_converter),
        (json_converter),
        (msgpack_converter),
        (msgspec_converter),
        (orjson_converter),
        (pyyaml_converter),
        (ujson_converter),
    ],
)
@pytest.mark.parametrize(
    "b, d, t",
    [
        (date(year=2000, month=5, day=11), None, None),
        (None, datetime(year=2080, month=1, day=21, hour=2, minute=5), None),
        (None, None, time(0, 1, 4)),
    ],
)
def test_dump_then_load_nullable(converter, b, d, t):
    h = {"birth": b, "death": d, "work_start": t}

    structure = converter.structure(h, HumanNullable)

    dump = converter.dumps(structure)
    load = converter.loads(dump, HumanNullable)

    if d:
        h["death"] = enforce_timezone(h["death"])

    assert load.birth == h["birth"]
    assert load.death == h["death"]
    assert load.work_start == h["work_start"]
