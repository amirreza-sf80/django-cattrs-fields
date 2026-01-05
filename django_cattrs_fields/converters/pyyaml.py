from typing import Union

from django.conf import settings

from cattrs.preconf.pyyaml import make_converter

from django_cattrs_fields.fields import UUIDField

from .register_hooks import (
    register_structure_hooks,
    register_unstructure_hooks,
)

converter = make_converter()

register_structure_hooks(converter)
register_unstructure_hooks(converter)

if getattr(settings, "DCF_SERIALIZER_HOOKS", True):
    converter.register_unstructure_hook(UUIDField, lambda x: str(x))
    converter.register_unstructure_hook(
        Union[UUIDField, None], lambda x: str(x) if x else None
    )

__all__ = ("converter",)
