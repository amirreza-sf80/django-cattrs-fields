import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from django_cattrs_fields.converters.json import serializer as json_serializer

from tests.books.models import Book


@pytest.fixture
def simple_file():
    return SimpleUploadedFile(name="test_image.jpeg", content=b"wheeee", content_type="image/jpeg")


@pytest.fixture
def create_book(db):
    Book.objects.create(
        pdf=SimpleUploadedFile(name="test_image.jpeg", content=b"wheeee", content_type="image/jpeg")
    )


def test_upload_file_get_200(client, simple_file):
    result = client.post("", {"pdf": simple_file})
    assert result.status_code == 200


def test_post_empty(client):
    result = client.post("")
    assert result.status_code == 400
    assert result.text == "no file"


def test_get_file(client, create_book):
    result = client.get("")
    data = json_serializer.loads(result.text, dict)
    assert "pdf" in data
    assert isinstance(data["pdf"], str)
