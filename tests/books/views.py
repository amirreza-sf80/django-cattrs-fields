from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponseBadRequest, HttpResponseBase
from django.http.request import HttpRequest
from django.http.response import HttpResponse

import attrs

from django_cattrs_fields.converters import converter
from django_cattrs_fields.converters.json import converter as json_converter
from django_cattrs_fields.fields.files import FileField

from .models import Book


@attrs.define
class BookData:
    pdf: FileField


def view(request: HttpRequest) -> HttpResponseBase:
    if request.method == "POST":
        exp = None
        try:
            structured_data = converter.structure(
                {**request.POST.dict(), **request.FILES.dict()}, BookData
            )
        except* (ValueError, KeyError) as e:
            exp = e

        if exp:
            return HttpResponseBadRequest("no file")

        if not isinstance(structured_data.pdf, UploadedFile):
            return HttpResponseBadRequest("not instance of UploadedFile")

        data = converter.unstructure(structured_data)

        if not isinstance(data["pdf"], UploadedFile):
            return HttpResponseBadRequest("not instance of UploadedFile after unstructure")

        return HttpResponse("done")

    b = Book.objects.last()
    data = json_converter.dumps(converter.structure({"pdf": b.pdf}, BookData))
    return HttpResponse(data)
