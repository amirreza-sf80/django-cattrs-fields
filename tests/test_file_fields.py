import io
import json

import pytest

from django.core.files.uploadedfile import (
    SimpleUploadedFile,
    TemporaryUploadedFile,
    UploadedFile,
    InMemoryUploadedFile,
)

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
from django_cattrs_fields.fields.files import FileField

from tests.books.models import Book


@define
class PDF:
    pdf: FileField


@define
class PDFNullable:
    pdf: FileField | None


@pytest.fixture
def memory_file():
    content = b"Hello, this is an in-memory uploaded file."
    file_buffer = io.BytesIO(content)
    file = InMemoryUploadedFile(
        file=file_buffer,
        field_name="file",
        name="example.txt",
        content_type="text/plain",
        size=len(content),
        charset=None,
    )
    file.seek(0)
    return file


@pytest.fixture
def temp_file():
    file = TemporaryUploadedFile(
        name="example_temp.txt",
        content_type="text/plain",
        size=0,
        charset=None,
    )
    file.write(b"Hello, this is a temporary uploaded file.")
    file.seek(0)
    return file


@pytest.fixture
def simple_file():
    return SimpleUploadedFile(name="test_image.jpeg", content=b"wheeee", content_type="image/jpeg")


def test_structure_uploaded(memory_file, temp_file, simple_file):
    pdf = {"pdf": memory_file}

    structure = converter.structure(pdf, PDF)
    obj = PDF(**pdf)

    assert structure == obj
    assert isinstance(structure.pdf, UploadedFile)
    assert isinstance(structure.pdf, InMemoryUploadedFile)

    pdf = {"pdf": temp_file}

    structure = converter.structure(pdf, PDF)
    obj = PDF(**pdf)

    assert structure == obj
    assert isinstance(structure.pdf, UploadedFile)
    assert isinstance(structure.pdf, TemporaryUploadedFile)

    pdf = {"pdf": simple_file}
    structure = converter.structure(pdf, PDF)
    obj = PDF(**pdf)

    assert structure == obj
    assert isinstance(structure.pdf, UploadedFile)
    assert isinstance(structure.pdf, SimpleUploadedFile)


@pytest.mark.parametrize(
    "memory, temp, simple", [(True, False, False), (False, True, False), (False, False, True)]
)
def test_structure_uploaded_nullable(memory_file, temp_file, simple_file, memory, temp, simple):
    pdf = {"pdf": memory_file if memory else None}

    structure = converter.structure(pdf, PDF)
    obj = PDF(**pdf)

    assert structure == obj
    if memory:
        assert isinstance(structure.pdf, UploadedFile)
        assert isinstance(structure.pdf, InMemoryUploadedFile)
    else:
        assert structure.pdf is None

    pdf = {"pdf": temp_file if temp else None}

    structure = converter.structure(pdf, PDF)
    obj = PDF(**pdf)

    assert structure == obj
    if temp:
        assert isinstance(structure.pdf, UploadedFile)
        assert isinstance(structure.pdf, TemporaryUploadedFile)
    else:
        assert structure.pdf is None

    pdf = {"pdf": simple_file if simple else None}
    structure = converter.structure(pdf, PDF)
    obj = PDF(**pdf)

    assert structure == obj
    if simple:
        assert isinstance(structure.pdf, UploadedFile)
        assert isinstance(structure.pdf, SimpleUploadedFile)
    else:
        assert structure.pdf is None


def test_unstructure_uploaded(memory_file, temp_file, simple_file):
    pdf = {"pdf": memory_file}
    structure = converter.structure(pdf, PDF)

    unstructure = converter.unstructure(structure)
    assert unstructure == pdf
    assert isinstance(structure.pdf, InMemoryUploadedFile)

    pdf = {"pdf": temp_file}
    structure = converter.structure(pdf, PDF)

    unstructure = converter.unstructure(structure)
    assert unstructure == pdf
    assert isinstance(structure.pdf, TemporaryUploadedFile)

    pdf = {"pdf": simple_file}
    structure = converter.structure(pdf, PDF)

    unstructure = converter.unstructure(structure)
    assert unstructure == pdf
    assert isinstance(structure.pdf, SimpleUploadedFile)


@pytest.mark.parametrize(
    "memory, temp, simple", [(True, False, False), (False, True, False), (False, False, True)]
)
def test_unstructure_uploaded_nullable(memory_file, temp_file, simple_file, memory, temp, simple):
    pdf = {"pdf": memory_file if memory else None}

    structure = converter.structure(pdf, PDF)
    unstructure = converter.unstructure(structure)

    assert unstructure == pdf
    if memory:
        assert isinstance(unstructure["pdf"], UploadedFile)
        assert isinstance(unstructure["pdf"], InMemoryUploadedFile)
    else:
        assert unstructure["pdf"] is None

    pdf = {"pdf": temp_file if temp else None}

    structure = converter.structure(pdf, PDF)
    unstructure = converter.unstructure(structure)

    assert unstructure == pdf
    if temp:
        assert isinstance(unstructure["pdf"], UploadedFile)
        assert isinstance(unstructure["pdf"], TemporaryUploadedFile)
    else:
        assert unstructure["pdf"] is None

    pdf = {"pdf": simple_file if simple else None}
    structure = converter.structure(pdf, PDF)
    unstructure = converter.unstructure(structure)

    assert unstructure == pdf
    if simple:
        assert isinstance(unstructure["pdf"], UploadedFile)
        assert isinstance(unstructure["pdf"], SimpleUploadedFile)
    else:
        assert unstructure["pdf"] is None


def test_structure_field_file(simple_file, db):
    b = Book.objects.create(pdf=simple_file)
    s = {"pdf": b.pdf}

    structure = converter.structure(s, PDF)
    assert isinstance(structure.pdf, str)
    assert structure.pdf == b.pdf.url


@pytest.mark.parametrize("simple", [True, False])
def test_structure_field_file_nullable(simple_file, db, simple):
    b = Book.objects.create(pdf=simple_file if simple else None)
    s = {"pdf": b.pdf}

    structure = converter.structure(s, PDFNullable)
    if simple:
        assert isinstance(structure.pdf, str)
        assert structure.pdf == b.pdf.url
    else:
        assert structure.pdf is None


def test_unstructure_field_file(simple_file, db):
    b = Book.objects.create(pdf=simple_file)
    s = {"pdf": b.pdf}
    structure = converter.structure(s, PDF)

    unstructure = converter.unstructure(structure)

    assert isinstance(unstructure["pdf"], str)
    assert unstructure["pdf"] == b.pdf.url


@pytest.mark.parametrize("simple", [True, False])
def test_unstructure_field_file_nullable(simple_file, db, simple):
    b = Book.objects.create(pdf=simple_file if simple else None)
    s = {"pdf": b.pdf}
    structure = converter.structure(s, PDFNullable)

    unstructure = converter.unstructure(structure)

    if simple:
        assert isinstance(unstructure["pdf"], str)
        assert unstructure["pdf"] == b.pdf.url
    else:
        assert unstructure["pdf"] is None


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
def test_dumps(db, converter, dumps, simple_file, memory_file, temp_file):
    b = Book.objects.create(pdf=simple_file)

    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDF)
    dump = converter.dumps(structure)
    pdf["pdf"] = pdf["pdf"].url
    assert dump == dumps(pdf)

    b = Book.objects.create(pdf=memory_file)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDF)
    dump = converter.dumps(structure)
    pdf["pdf"] = pdf["pdf"].url
    assert dump == dumps(pdf)

    b = Book.objects.create(pdf=temp_file)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDF)
    dump = converter.dumps(structure)
    pdf["pdf"] = pdf["pdf"].url
    assert dump == dumps(pdf)


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
@pytest.mark.parametrize(
    "memory, temp, simple", [(True, False, False), (False, True, False), (False, False, True)]
)
def test_dumps_nullable(
    memory_file, temp_file, simple_file, memory, temp, simple, converter, dumps, db
):
    b = Book.objects.create(pdf=simple_file if simple else None)

    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDFNullable)
    dump = converter.dumps(structure)
    pdf["pdf"] = pdf["pdf"].url if simple else None

    assert dump == dumps(pdf)

    b = Book.objects.create(pdf=memory_file if memory else None)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDFNullable)
    dump = converter.dumps(structure)
    pdf["pdf"] = pdf["pdf"].url if memory else None

    assert dump == dumps(pdf)

    b = Book.objects.create(pdf=temp_file if temp else None)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDFNullable)
    dump = converter.dumps(structure)
    pdf["pdf"] = pdf["pdf"].url if temp else None

    assert dump == dumps(pdf)


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
def test_loads(db, converter, dumps, simple_file, memory_file, temp_file):
    b = Book.objects.create(pdf=simple_file)
    pdf = {"pdf": b.pdf.url}

    dump = dumps(pdf)

    assert converter.loads(dump, PDF) == PDF(**pdf)

    b = Book.objects.create(pdf=memory_file)
    pdf = {"pdf": b.pdf.url}

    dump = dumps(pdf)
    assert converter.loads(dump, PDF) == PDF(**pdf)

    b = Book.objects.create(pdf=temp_file)
    pdf = {"pdf": b.pdf.url}

    dump = dumps(pdf)

    assert converter.loads(dump, PDF) == PDF(**pdf)


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
@pytest.mark.parametrize(
    "memory, temp, simple", [(True, False, False), (False, True, False), (False, False, True)]
)
def test_loads_nullable(
    db, converter, dumps, simple_file, memory_file, temp_file, memory, temp, simple
):
    b = Book.objects.create(pdf=simple_file if simple else None)
    pdf = {"pdf": b.pdf.url if simple else None}

    dump = dumps(pdf)

    assert converter.loads(dump, PDFNullable) == PDFNullable(**pdf)

    b = Book.objects.create(pdf=memory_file if memory else None)
    pdf = {"pdf": b.pdf.url if memory else None}

    dump = dumps(pdf)
    assert converter.loads(dump, PDFNullable) == PDFNullable(**pdf)

    b = Book.objects.create(pdf=temp_file if temp else None)
    pdf = {"pdf": b.pdf.url if temp else None}

    dump = dumps(pdf)

    assert converter.loads(dump, PDFNullable) == PDFNullable(**pdf)


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
def test_dumps_then_loads(db, converter, simple_file, memory_file, temp_file):
    b = Book.objects.create(pdf=simple_file)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDF)
    dump = converter.dumps(structure)
    pdf["pdf"] = pdf["pdf"].url
    obj = PDF(**pdf)

    assert converter.loads(dump, PDF) == obj

    b = Book.objects.create(pdf=memory_file)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDF)
    dump = converter.dumps(structure)
    pdf["pdf"] = pdf["pdf"].url
    obj = PDF(**pdf)

    assert converter.loads(dump, PDF) == obj

    b = Book.objects.create(pdf=temp_file)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDF)
    dump = converter.dumps(structure)
    pdf["pdf"] = pdf["pdf"].url
    obj = PDF(**pdf)

    assert converter.loads(dump, PDF) == obj


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
@pytest.mark.parametrize(
    "memory, temp, simple", [(True, False, False), (False, True, False), (False, False, True)]
)
def test_dumps_then_loads_nullable(
    db, converter, simple_file, memory_file, temp_file, memory, temp, simple
):
    b = Book.objects.create(pdf=simple_file if simple else None)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDFNullable)
    dump = converter.dumps(structure)
    if simple:
        pdf["pdf"] = pdf["pdf"].url
    obj = PDFNullable(**pdf)

    assert converter.loads(dump, PDFNullable) == obj

    b = Book.objects.create(pdf=memory_file if memory else None)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDFNullable)
    dump = converter.dumps(structure)
    if memory:
        pdf["pdf"] = pdf["pdf"].url
    obj = PDFNullable(**pdf)

    assert converter.loads(dump, PDFNullable) == obj

    b = Book.objects.create(pdf=temp_file if temp else None)
    pdf = {"pdf": b.pdf}

    structure = converter.structure(pdf, PDFNullable)
    dump = converter.dumps(structure)
    if temp:
        pdf["pdf"] = pdf["pdf"].url
    obj = PDFNullable(**pdf)

    assert converter.loads(dump, PDFNullable) == obj
