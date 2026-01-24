from typing import Union

from bson.binary import Binary

from cattrs.preconf.bson import make_converter

from django.conf import settings

from django_cattrs_fields.fields import DateField, DecimalField, UUIDField
from django_cattrs_fields.hooks.number_hooks import decimal_unstructure_str

from .register_hooks import (
    register_structure_hooks,
    register_unstructure_hooks,
    register_datetime_unstructure_hooks,
)

converter = make_converter()

register_structure_hooks(converter)

register_unstructure_hooks(converter)
register_datetime_unstructure_hooks(converter)

if getattr(settings, "DCF_SERIALIZER_HOOKS", True):
    converter.register_unstructure_hook(UUIDField, lambda x: Binary.from_uuid(x))
    converter.register_unstructure_hook(
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

    converter.register_unstructure_hook(DateField, lambda x: x.isoformat())
    converter.register_unstructure_hook(
        Union[DateField, None], lambda x: x.isoformat() if x else None
    )
    converter.register_structure_hook(UUIDField, bson_uuid_structure)
    converter.register_structure_hook(Union[UUIDField, None], bson_uuid_structure_nullable)

    converter.register_unstructure_hook(DecimalField, decimal_unstructure_str)
    converter.register_unstructure_hook(Union[DecimalField, None], decimal_unstructure_str)

__all__ = ("converter",)
