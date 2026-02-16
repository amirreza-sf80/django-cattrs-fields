from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
    UploadedFile,
)
from django.db.models.fields.files import FieldFile
from django.utils.translation import gettext_lazy as _

from django_cattrs_fields.fields.files import FileField

__all__ = (
    "file_structure",
    "file_structure_nullable",
    "file_unstructure",
)


def file_structure(val: FileField | FieldFile, _t) -> FileField | str:
    # handling file uploaded by client
    if isinstance(val, UploadedFile):
        if not hasattr(val, "name") and not hasattr(val, "size"):
            raise ValueError(_("No file was submitted. Check the encoding type on the form."))
        if not val.name:
            raise ValueError(_("No filename could be determined."))

        # this is either a `InMemoryUploadedFile` or `TemporaryUploadedFile` or a custom object
        return val

    # GET request, return the file url to client
    elif isinstance(val, FieldFile):
        return val.url

    # if using this field as a client, and we call some API, we get the url back as a string
    return val


def file_structure_nullable(
    val: FileField | FieldFile | None,
    _t,
) -> FileField | str | None:
    if not val:
        return None
    return file_structure(val, _t)


def file_unstructure(
    val: FileField | FieldFile | str | None,
) -> InMemoryUploadedFile | TemporaryUploadedFile | str | None:
    if not val:
        return None
    # handling file uploaded by client
    if isinstance(val, UploadedFile):
        return val

    # normally a structured data doesn't have FieldFile,
    # but just in case user wants to do something manual
    elif isinstance(val, FieldFile):
        return val.url

    # url
    return val
