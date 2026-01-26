from typing import Union

from cattrs.preconf.cbor2 import make_converter
from django.conf import settings

from django_cattrs_fields.fields import TimeField
from django_cattrs_fields.hooks.date_hooks import time_unstructure_str

from .register_hooks import (
    register_date_unstructure_hooks,
    register_datetime_unstructure_hooks,
    register_decimal_unstructure_hooks,
    register_structure_hooks,
    register_unstructure_hooks,
    register_uuid_unstructure_hooks,
)

converter = make_converter()

register_structure_hooks(converter)
register_unstructure_hooks(converter)
register_datetime_unstructure_hooks(converter)
register_date_unstructure_hooks(converter)
register_decimal_unstructure_hooks(converter)
register_uuid_unstructure_hooks(converter)

if getattr(settings, "DCF_SERIALIZER_HOOKS", True):
    converter.register_unstructure_hook(TimeField, time_unstructure_str)
    converter.register_unstructure_hook(Union[TimeField, None], time_unstructure_str)

__all__ = ("converter",)
