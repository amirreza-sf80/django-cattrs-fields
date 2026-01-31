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

serializer = make_converter()

register_structure_hooks(serializer)
register_unstructure_hooks(serializer)
register_datetime_unstructure_hooks(serializer)
register_date_unstructure_hooks(serializer)
register_decimal_unstructure_hooks(serializer)
register_uuid_unstructure_hooks(serializer)

if getattr(settings, "DCF_SERIALIZER_HOOKS", True):
    serializer.register_unstructure_hook(TimeField, time_unstructure_str)
    serializer.register_unstructure_hook(Union[TimeField, None], time_unstructure_str)

__all__ = ("serializer",)
