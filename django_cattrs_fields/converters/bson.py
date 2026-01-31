from typing import Union

from bson.binary import Binary

from cattrs.preconf.bson import make_converter

from django.conf import settings

from django_cattrs_fields.fields import DateField, DecimalField, TimeField, UUIDField
from django_cattrs_fields.hooks.date_hooks import time_unstructure_str
from django_cattrs_fields.hooks.number_hooks import decimal_unstructure_str

from .register_hooks import (
    register_structure_hooks,
    register_unstructure_hooks,
    register_datetime_unstructure_hooks,
)

serializer = make_converter()

register_structure_hooks(serializer)

register_unstructure_hooks(serializer)
register_datetime_unstructure_hooks(serializer)

if getattr(settings, "DCF_SERIALIZER_HOOKS", True):
    serializer.register_unstructure_hook(UUIDField, lambda x: Binary.from_uuid(x))
    serializer.register_unstructure_hook(
        Union[UUIDField, None], lambda x: Binary.from_uuid(x) if x else None
    )

    def bson_uuid_structure(val, _) -> UUIDField:
        if isinstance(val, Binary):
            return val.as_uuid()
        return val

    def bson_uuid_structure_nullable(val, _) -> UUIDField | None:
        if val is None:
            return None
        return bson_uuid_structure(val, _)

    serializer.register_unstructure_hook(DateField, lambda x: x.isoformat())
    serializer.register_unstructure_hook(
        Union[DateField, None], lambda x: x.isoformat() if x else None
    )
    serializer.register_structure_hook(UUIDField, bson_uuid_structure)
    serializer.register_structure_hook(Union[UUIDField, None], bson_uuid_structure_nullable)

    serializer.register_unstructure_hook(DecimalField, decimal_unstructure_str)
    serializer.register_unstructure_hook(Union[DecimalField, None], decimal_unstructure_str)
    serializer.register_unstructure_hook(TimeField, time_unstructure_str)
    serializer.register_unstructure_hook(Union[TimeField, None], time_unstructure_str)

__all__ = ("serializer",)
