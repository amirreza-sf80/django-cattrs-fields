from cattrs.preconf.msgspec import make_converter

from .register_hooks import (
    register_structure_hooks,
    register_all_unstructure_hooks,
)

serializer = make_converter()

register_structure_hooks(serializer)
register_all_unstructure_hooks(serializer)

__all__ = ("serializer",)
