from typing import Union, get_args

from attrs import has
from cattrs._compat import is_annotated
from cattrs.converters import Converter

from django.conf import settings

from django_cattrs_fields.fields import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    EmptyField,
    FloatField,
    IntegerField,
    SlugField,
    TimeField,
    URLField,
    UUIDField,
)
from django_cattrs_fields.fields.files import FileField
from django_cattrs_fields.hooks import (
    structure_model_factory,
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
    time_structure,
    time_structure_nullable,
    time_unstructure,
    url_structure,
    url_structure_nullable,
    url_unstructure,
    uuid_structure,
    uuid_structure_nullable,
    uuid_unstructure,
)
from django_cattrs_fields.hooks.empty_hooks import (
    empty_bool_structure,
    empty_bool_structure_nullable,
    empty_bool_unstructure,
    empty_char_structure,
    empty_char_structure_nullable,
    empty_char_unstructure,
    empty_date_structure,
    empty_date_structure_nullable,
    empty_date_unstructure,
    empty_datetime_structure,
    empty_datetime_structure_nullable,
    empty_datetime_unstructure,
    empty_decimal_structure,
    empty_decimal_structure_nullable,
    empty_decimal_unstructure,
    empty_email_structure,
    empty_email_structure_nullable,
    empty_email_unstructure,
    empty_file_structure,
    empty_file_structure_nullable,
    empty_file_unstructure,
    empty_float_structure,
    empty_float_structure_nullable,
    empty_float_unstructure,
    empty_integer_structure,
    empty_integer_structure_nullable,
    empty_integer_unstructure,
    empty_slug_structure,
    empty_slug_structure_nullable,
    empty_slug_unstructure,
    empty_structure,
    empty_time_structure,
    empty_time_structure_nullable,
    empty_time_unstructure,
    empty_unstructure,
    empty_url_structure,
    empty_url_structure_nullable,
    empty_url_unstructure,
    empty_uuid_structure,
    empty_uuid_structure_nullable,
    empty_uuid_unstructure,
    skip_empty,
)
from django_cattrs_fields.hooks.list_hooks import list_structure_hook_factory, is_list_of_attrs


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
    converter.register_structure_hook(EmptyField, empty_structure)
    converter.register_structure_hook(FloatField, float_structure)
    converter.register_structure_hook(IntegerField, integer_structure)
    converter.register_structure_hook(SlugField, slug_structure)
    converter.register_structure_hook(TimeField, time_structure)
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
    converter.register_structure_hook(Union[TimeField, None], time_structure_nullable)
    converter.register_structure_hook(Union[URLField, None], url_structure_nullable)
    converter.register_structure_hook(Union[UUIDField, None], uuid_structure_nullable)

    # Empty Unions
    converter.register_structure_hook(Union[BooleanField, EmptyField], empty_bool_structure)
    converter.register_structure_hook(Union[CharField, EmptyField], empty_char_structure)
    converter.register_structure_hook(Union[EmptyField, EmptyField], empty_email_structure)
    converter.register_structure_hook(Union[SlugField, EmptyField], empty_slug_structure)
    converter.register_structure_hook(Union[URLField, EmptyField], empty_url_structure)
    converter.register_structure_hook(Union[UUIDField, EmptyField], empty_uuid_structure)
    converter.register_structure_hook(Union[IntegerField, EmptyField], empty_integer_structure)
    converter.register_structure_hook(Union[DecimalField, EmptyField], empty_decimal_structure)
    converter.register_structure_hook(Union[FloatField, EmptyField], empty_float_structure)
    converter.register_structure_hook(Union[DateField, EmptyField], empty_date_structure)
    converter.register_structure_hook(Union[DateTimeField, EmptyField], empty_datetime_structure)
    converter.register_structure_hook(Union[TimeField, EmptyField], empty_time_structure)

    converter.register_structure_hook(
        Union[BooleanField, EmptyField], empty_bool_structure_nullable
    )
    converter.register_structure_hook(
        Union[CharField, EmptyField, None], empty_char_structure_nullable
    )
    converter.register_structure_hook(
        Union[EmptyField, EmptyField, None], empty_email_structure_nullable
    )
    converter.register_structure_hook(
        Union[SlugField, EmptyField, None], empty_slug_structure_nullable
    )
    converter.register_structure_hook(
        Union[URLField, EmptyField, None], empty_url_structure_nullable
    )
    converter.register_structure_hook(
        Union[UUIDField, EmptyField, None], empty_uuid_structure_nullable
    )
    converter.register_structure_hook(
        Union[IntegerField, EmptyField, None], empty_integer_structure_nullable
    )
    converter.register_structure_hook(
        Union[DecimalField, EmptyField, None], empty_decimal_structure_nullable
    )
    converter.register_structure_hook(
        Union[FloatField, EmptyField, None], empty_float_structure_nullable
    )
    converter.register_structure_hook(
        Union[DateField, EmptyField, None], empty_date_structure_nullable
    )
    converter.register_structure_hook(
        Union[DateTimeField, EmptyField, None], empty_datetime_structure_nullable
    )
    converter.register_structure_hook(
        Union[TimeField, EmptyField, None], empty_time_structure_nullable
    )

    # File

    if getattr(settings, "DCF_FILE_HOOKS", True):
        converter.register_structure_hook(FileField, file_structure)
        converter.register_structure_hook(Union[FileField, None], file_structure_nullable)
        converter.register_structure_hook(Union[FileField, EmptyField], empty_file_structure)
        converter.register_structure_hook(
            Union[FileField, EmptyField, None], empty_file_structure_nullable
        )


def register_model_structure_hook(converter: Converter):
    """these hooks only make sense on a normal converter, not serializers"""
    converter.register_structure_hook_factory(has, structure_model_factory)
    converter.register_structure_hook_factory(is_list_of_attrs, list_structure_hook_factory)


def register_unstructure_hooks(converter: Converter):
    converter.register_unstructure_hook(BooleanField, boolean_unstructure)
    converter.register_unstructure_hook(CharField, char_unstructure)
    converter.register_unstructure_hook(EmailField, email_unstructure)
    converter.register_unstructure_hook(EmptyField, empty_unstructure)
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


# some serializers have special versions of the following hooks,
# we register them in separate functions so we don't register these for those serializers


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


def register_time_unstructure_hooks(converter: Converter):
    converter.register_unstructure_hook(TimeField, time_unstructure)
    converter.register_unstructure_hook(Union[TimeField, None], time_unstructure)


def register_all_unstructure_hooks(converter: Converter):
    register_unstructure_hooks(converter)
    register_uuid_unstructure_hooks(converter)
    register_date_unstructure_hooks(converter)
    register_datetime_unstructure_hooks(converter)
    register_decimal_unstructure_hooks(converter)
    register_time_unstructure_hooks(converter)


# empty hooks are meant to be used by dedicated converters,
# not the default converter or any of the serializers
# tho it's possible to use this with the default converter, it's not recommended


def register_empty_unstructure_hook_factory(converter: Converter):
    converter.register_unstructure_hook_factory(has, skip_empty)


# TODO: see if there is a better way to do this
def register_empty_unstructure_hooks(converter: Converter):
    # Empty Unions
    converter.register_unstructure_hook(Union[BooleanField, EmptyField], empty_bool_unstructure)
    converter.register_unstructure_hook(Union[CharField, EmptyField], empty_char_unstructure)
    converter.register_unstructure_hook(Union[EmailField, EmptyField], empty_email_unstructure)
    converter.register_unstructure_hook(Union[SlugField, EmptyField], empty_slug_unstructure)
    converter.register_unstructure_hook(Union[URLField, EmptyField], empty_url_unstructure)
    converter.register_unstructure_hook(Union[UUIDField, EmptyField], empty_uuid_unstructure)
    converter.register_unstructure_hook(Union[IntegerField, EmptyField], empty_integer_unstructure)
    converter.register_unstructure_hook(Union[DecimalField, EmptyField], empty_decimal_unstructure)
    converter.register_unstructure_hook(Union[FloatField, EmptyField], empty_float_unstructure)
    converter.register_unstructure_hook(Union[DateField, EmptyField], empty_date_unstructure)
    converter.register_unstructure_hook(
        Union[DateTimeField, EmptyField], empty_datetime_unstructure
    )
    converter.register_unstructure_hook(Union[TimeField, EmptyField], empty_time_unstructure)

    converter.register_unstructure_hook(
        Union[BooleanField, EmptyField, None], empty_bool_unstructure
    )
    converter.register_unstructure_hook(Union[CharField, EmptyField, None], empty_char_unstructure)
    converter.register_unstructure_hook(
        Union[EmailField, EmptyField, None], empty_email_unstructure
    )
    converter.register_unstructure_hook(Union[SlugField, EmptyField, None], empty_slug_unstructure)
    converter.register_unstructure_hook(Union[URLField, EmptyField, None], empty_url_unstructure)
    converter.register_unstructure_hook(Union[UUIDField, EmptyField, None], empty_uuid_unstructure)
    converter.register_unstructure_hook(
        Union[IntegerField, EmptyField, None], empty_integer_unstructure
    )
    converter.register_unstructure_hook(
        Union[DecimalField, EmptyField, None], empty_decimal_unstructure
    )
    converter.register_unstructure_hook(
        Union[FloatField, EmptyField, None], empty_float_unstructure
    )
    converter.register_unstructure_hook(Union[DateField, EmptyField, None], empty_date_unstructure)
    converter.register_unstructure_hook(
        Union[DateTimeField, EmptyField], empty_datetime_unstructure
    )
    converter.register_unstructure_hook(Union[TimeField, EmptyField], empty_time_unstructure)

    if getattr(settings, "DCF_FILE_HOOKS", True):
        converter.register_unstructure_hook(Union[FileField, EmptyField], empty_file_unstructure)
        converter.register_unstructure_hook(
            Union[FileField, EmptyField, None], empty_file_unstructure
        )


def register_all_empty_unstructure_hooks(converter: Converter):
    register_empty_unstructure_hook_factory(converter)
    register_empty_unstructure_hooks(converter)
