from typing import Union

from django.conf import settings

from cattrs.preconf.msgpack import make_converter

from django_cattrs_fields.fields import DateField, DateTimeField, DecimalField, TimeField, UUIDField
from django_cattrs_fields.hooks.date_hooks import time_unstructure_str
from django_cattrs_fields.hooks.number_hooks import decimal_unstructure_str

from .register_hooks import (
    register_structure_hooks,
    register_unstructure_hooks,
)

converter = make_converter()

register_structure_hooks(converter)
register_unstructure_hooks(converter)

if getattr(settings, "DCF_SERIALIZER_HOOKS", True):
    converter.register_unstructure_hook(UUIDField, lambda x: str(x))
    converter.register_unstructure_hook(Union[UUIDField, None], lambda x: str(x) if x else None)

    converter.register_unstructure_hook(DateField, lambda x: x.isoformat())
    converter.register_unstructure_hook(
        Union[DateField, None], lambda x: x.isoformat() if x else None
    )
    converter.register_unstructure_hook(DateTimeField, lambda x: x.isoformat())
    converter.register_unstructure_hook(
        Union[DateTimeField, None], lambda x: x.isoformat() if x else None
    )
    converter.register_unstructure_hook(DecimalField, decimal_unstructure_str)
    converter.register_unstructure_hook(Union[DecimalField, None], decimal_unstructure_str)
    converter.register_unstructure_hook(TimeField, time_unstructure_str)
    converter.register_unstructure_hook(Union[TimeField, None], time_unstructure_str)


__all__ = ("converter",)
