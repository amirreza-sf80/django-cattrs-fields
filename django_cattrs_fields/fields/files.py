from typing import Union

from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    SimpleUploadedFile,
    TemporaryUploadedFile,
)

type FileField = Union[InMemoryUploadedFile, TemporaryUploadedFile, SimpleUploadedFile, str]
