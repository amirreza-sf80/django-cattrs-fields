from django.conf import settings

from cattrs.preconf.tomlkit import make_converter

from django_cattrs_fields.fields import DecimalField, UUIDField
from django_cattrs_fields.hooks.number_hooks import decimal_unstructure_str

from .register_hooks import (
    register_structure_hooks,
    register_unstructure_hooks,
    register_datetime_unstructure_hooks,
    register_date_unstructure_hooks,
    register_time_unstructure_hooks,
)

serializer = make_converter()

register_structure_hooks(serializer)

register_unstructure_hooks(serializer)
register_date_unstructure_hooks(serializer)
register_datetime_unstructure_hooks(serializer)
register_time_unstructure_hooks(serializer)


if getattr(settings, "DCF_SERIALIZER_HOOKS", True):
    serializer.register_unstructure_hook(UUIDField, lambda x: str(x))
    serializer.register_unstructure_hook(DecimalField, decimal_unstructure_str)

__all__ = ("serializer",)
