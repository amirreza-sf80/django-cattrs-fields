from typing import Union, get_args

from cattrs.converters import Converter
from cattrs._compat import is_annotated

from django.conf import settings

from django_cattrs_fields.fields import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    EmailField,
    DecimalField,
    FloatField,
    IntegerField,
    SlugField,
    URLField,
    UUIDField,
)
from django_cattrs_fields.fields.files import FileField
from django_cattrs_fields.hooks import (
    boolean_structure,
    boolean_structure_nullable,
    boolean_unstructure,
    char_structure,
    char_structure_nullable,
    char_unstructure,
    date_structure,
    date_structure_nullable,
    date_unstructure,
    datetime_structure,
    datetime_structure_nullable,
    datetime_unstructure,
    decimal_structure,
    decimal_structure_annotated,
    decimal_structure_nullable,
    decimal_unstructure,
    email_structure,
    email_structure_nullable,
    email_unstructure,
    file_structure,
    file_structure_nullable,
    file_unstructure,
    float_structure,
    float_structure_nullable,
    float_unstructure,
    integer_structure,
    integer_structure_nullable,
    integer_unstructure,
    slug_structure,
    slug_structure_nullable,
    slug_unstructure,
    url_structure,
    url_structure_nullable,
    url_unstructure,
    uuid_structure,
    uuid_structure_nullable,
    uuid_unstructure,
)


def register_structure_hooks(converter: Converter):
    converter.register_structure_hook(BooleanField, boolean_structure)
    converter.register_structure_hook(CharField, char_structure)
    converter.register_structure_hook(DateField, date_structure)
    converter.register_structure_hook(DateTimeField, datetime_structure)
    converter.register_structure_hook_func(
        lambda t: is_annotated(t) and get_args(t)[0] is DecimalField, decimal_structure_annotated
    )
    converter.register_structure_hook(DecimalField, decimal_structure)
    converter.register_structure_hook(EmailField, email_structure)
    converter.register_structure_hook(FloatField, float_structure)
    converter.register_structure_hook(IntegerField, integer_structure)
    converter.register_structure_hook(SlugField, slug_structure)
    converter.register_structure_hook(URLField, url_structure)
    converter.register_structure_hook(UUIDField, uuid_structure)

    # Union types
    converter.register_structure_hook(Union[BooleanField, None], boolean_structure_nullable)
    converter.register_structure_hook(Union[CharField, None], char_structure_nullable)
    converter.register_structure_hook(Union[DateField, None], date_structure_nullable)
    converter.register_structure_hook(Union[DecimalField, None], decimal_structure_nullable)
    converter.register_structure_hook(Union[DateTimeField, None], datetime_structure_nullable)
    converter.register_structure_hook(Union[EmailField, None], email_structure_nullable)
    converter.register_structure_hook(Union[FloatField, None], float_structure_nullable)
    converter.register_structure_hook(Union[IntegerField, None], integer_structure_nullable)
    converter.register_structure_hook(Union[SlugField, None], slug_structure_nullable)
    converter.register_structure_hook(Union[URLField, None], url_structure_nullable)
    converter.register_structure_hook(Union[UUIDField, None], uuid_structure_nullable)

    # File

    if getattr(settings, "DCF_FILE_HOOKS", True):
        converter.register_structure_hook(FileField, file_structure)
        converter.register_structure_hook(Union[FileField, None], file_structure_nullable)


def register_unstructure_hooks(converter: Converter):
    converter.register_unstructure_hook(BooleanField, boolean_unstructure)
    converter.register_unstructure_hook(CharField, char_unstructure)
    converter.register_unstructure_hook(EmailField, email_unstructure)
    converter.register_unstructure_hook(FloatField, float_unstructure)
    converter.register_unstructure_hook(IntegerField, integer_unstructure)
    converter.register_unstructure_hook(SlugField, slug_unstructure)
    converter.register_unstructure_hook(URLField, url_unstructure)

    # Union types
    converter.register_unstructure_hook(Union[BooleanField, None], boolean_unstructure)
    converter.register_unstructure_hook(Union[CharField, None], char_unstructure)
    converter.register_unstructure_hook(Union[EmailField, None], email_unstructure)
    converter.register_unstructure_hook(Union[FloatField, None], float_unstructure)
    converter.register_unstructure_hook(Union[IntegerField, None], integer_unstructure)
    converter.register_unstructure_hook(Union[SlugField, None], slug_unstructure)
    converter.register_unstructure_hook(Union[URLField, None], url_unstructure)

    # File

    if getattr(settings, "DCF_FILE_HOOKS", True):
        converter.register_unstructure_hook(FileField, file_unstructure)
        converter.register_unstructure_hook(Union[FileField, None], file_unstructure)


def register_uuid_unstructure_hooks(converter: Converter):
    converter.register_unstructure_hook(UUIDField, uuid_unstructure)
    converter.register_unstructure_hook(Union[UUIDField, None], uuid_unstructure)


def register_date_unstructure_hooks(converter: Converter):
    converter.register_unstructure_hook(DateField, date_unstructure)
    converter.register_unstructure_hook(Union[DateField, None], date_unstructure)


def register_datetime_unstructure_hooks(converter: Converter):
    converter.register_unstructure_hook(DateTimeField, datetime_unstructure)
    converter.register_unstructure_hook(Union[DateTimeField, None], datetime_unstructure)


def register_decimal_unstructure_hooks(converter: Converter):
    converter.register_unstructure_hook(DecimalField, decimal_unstructure)
    converter.register_unstructure_hook(Union[DecimalField, None], decimal_unstructure)


def register_all_unstructure_hooks(converter: Converter):
    register_unstructure_hooks(converter)
    register_uuid_unstructure_hooks(converter)
    register_date_unstructure_hooks(converter)
    register_datetime_unstructure_hooks(converter)
    register_decimal_unstructure_hooks(converter)
