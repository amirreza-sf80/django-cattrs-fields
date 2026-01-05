from cattrs.preconf.orjson import make_converter

from .register_hooks import (
    register_structure_hooks,
    register_unstructure_hooks,
)

converter = make_converter()

register_structure_hooks(converter)
register_unstructure_hooks(converter)

__all__ = ("converter",)
